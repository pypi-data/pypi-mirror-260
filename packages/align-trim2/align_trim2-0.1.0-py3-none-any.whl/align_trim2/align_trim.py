#!/usr/bin/env python

# Written by Nick Loman

from copy import copy
from collections import defaultdict
import pysam
import sys
import argparse

from align_trim2.readbedfile import read_bed_file

# consumesReference lookup for if a CIGAR operation consumes the reference sequence
consumesReference = [True, False, True, True, False, False, False, True]

# consumesQuery lookup for if a CIGAR operation consumes the query sequence
consumesQuery = [True, True, False, False, True, False, False, True]


def find_primer(bed, pos, direction):
    """Given a reference position and a direction of travel, walk out and find the nearest primer site.

    Parameters
    ----------
    bed : list
        A list of dictionaries, where each dictionary contains a row of bedfile data
    pos : int
        The position in the reference sequence to start from
    direction : string
        The direction to search along the reference sequence

    Returns
    -------
    tuple
        The offset, distance and bed entry for the closest primer to the query position
    """
    from operator import itemgetter

    if direction == "+":
        closest = min(
            [
                (abs(p["start"] - pos), p["start"] - pos, p)
                for p in bed
                if p["direction"] == direction
            ],
            key=itemgetter(0),
        )
    else:
        closest = min(
            [
                (abs(p["end"] - pos), p["end"] - pos, p)
                for p in bed
                if p["direction"] == direction
            ],
            key=itemgetter(0),
        )
    return closest


def trim(segment, primer_pos, end, debug):
    """Soft mask an alignment to fit within primer start/end sites.

    Parameters
    ----------
    segment : pysam.AlignedSegment
        The aligned segment to mask
    primer_pos : int
        The position in the reference to soft mask up to (equates to the start/end position of the primer in the reference)
    end : bool
        If True, the segment is being masked from the end (i.e. for the reverse primer)
    debug : bool
        If True, will print soft masking info during trimming
    """
    # get a copy of the cigar tuples to work with
    cigar = copy(segment.cigartuples)

    # get the segment position in the reference (depends on if start or end of the segment is being processed)
    if not end:
        pos = segment.pos
    else:
        pos = segment.reference_end

    # process the CIGAR to determine how much softmasking is required
    eaten = 0
    while 1:

        # chomp CIGAR operations from the start/end of the CIGAR
        try:
            if end:
                flag, length = cigar.pop()
            else:
                flag, length = cigar.pop(0)
            if debug:
                print("Chomped a %s, %s" % (flag, length), file=sys.stderr)
        except IndexError:
            print(
                "Ran out of cigar during soft masking - completely masked read will be ignored",
                file=sys.stderr,
            )
            break

        # if the CIGAR operation consumes the reference sequence, increment/decrement the position by the CIGAR operation length
        if consumesReference[flag]:
            if not end:
                pos += length
            else:
                pos -= length

        # if the CIGAR operation consumes the query sequence, increment the number of CIGAR operations eaten by the CIGAR operation length
        if consumesQuery[flag]:
            eaten += length

        # stop processing the CIGAR if we've gone far enough to mask the primer
        if not end and pos >= primer_pos and flag == 0:
            break
        if end and pos <= primer_pos and flag == 0:
            break

    # calculate how many extra matches are needed in the CIGAR
    extra = abs(pos - primer_pos)
    if debug:
        print("extra %s" % (extra), file=sys.stderr)
    if extra:
        if debug:
            print("Inserted a %s, %s" % (0, extra), file=sys.stderr)
        if end:
            cigar.append((0, extra))
        else:
            cigar.insert(0, (0, extra))
        eaten -= extra

    # softmask the left primer
    if not end:

        # update the position of the leftmost mappinng base
        segment.pos = pos - extra
        if debug:
            print("New pos: %s" % (segment.pos), file=sys.stderr)

        # if proposed softmask leads straight into a deletion, shuffle leftmost mapping base along and ignore the deletion
        if cigar[0][0] == 2:
            if debug:
                print(
                    "softmask created a leading deletion in the CIGAR, shuffling the alignment",
                    file=sys.stderr,
                )
            while 1:
                if cigar[0][0] != 2:
                    break
                _, length = cigar.pop(0)
                segment.pos += length

        # now add the leading softmask
        cigar.insert(0, (4, eaten))

    # softmask the right primer
    else:
        cigar.append((4, eaten))

    # check the new CIGAR and replace the old one
    if cigar[0][1] <= 0 or cigar[-1][1] <= 0:
        raise Exception(
            "invalid cigar operation created - possibly due to INDEL in primer"
        )
    segment.cigartuples = cigar
    return


def createPrimerSiteLookup(
    bed: dict[str, list[dict]], ref_lengths: list[tuple[str, int]]
) -> dict[str, list[bool]]:
    """
    Create a primer site lookup dictionary. This does not check primer sites are from a vaild product.

    Args:
        bed (dict[str, list[dict]]): A dictionary containing primer information for each chromosome.
        ref_lengths (list[tuple[str, int]]): A list of tuples containing chromosome names and their lengths.

    Returns:
        dict[str, list[bool]]: A dictionary where the keys are chromosome names and the values are lists of booleans
        indicating the presence of primer sites at each position along the chromosome.
    """
    # Create the empty lookup dictionarys
    primerSiteLookup = {}
    for chrom, length in ref_lengths:
        primerSiteLookup[chrom] = [False for i in range(length)]

        # Fill the lookup array with the primer sites
        for primer in bed.get(chrom, []):
            primerSiteLookup[chrom][primer["start"] : primer["end"]] = [
                True for _ in range(primer["start"], primer["end"])
            ]

    return primerSiteLookup


def go(args):
    """Filter and soft mask an alignment file so that the alignment boundaries match the primer start and end sites.

    Based on the most likely primer position, based on the alignment coordinates.
    """
    # prepare the report outfile
    if args.report:
        reportfh = open(args.report, "w")
        print(
            "QueryName\tReferenceStart\tReferenceEnd\tPrimerPair\tPrimer1\tPrimer1Start\tPrimer2\tPrimer2Start\tIsSecondary\tIsSupplementary\tStart\tEnd\tCorrectlyPaired",
            file=reportfh,
        )

    # set up a counter to track amplicon abundance
    counter = defaultdict(int)

    # open the primer scheme and get the pools
    bed = read_bed_file(args.bedfile)
    ## Change this from the flat list of primers to a dictionary of lists
    pools = {x["PoolName"] for v in bed.values() for x in v}
    pools.add("unmatched")

    # open the input SAM file and process read groups
    infile = pysam.AlignmentFile(args.bamfile, "rb")
    bam_header = infile.header.copy().to_dict()
    if not args.no_read_groups:
        bam_header["RG"] = []
        for pool in pools:
            read_group = {}
            read_group["ID"] = pool
            bam_header["RG"].append(read_group)

    # prepare the alignment outfile
    outfile = pysam.AlignmentFile("-", "wh", header=bam_header)

    # Create the lookup array for the primer scheme
    ref_lengths = list(zip(infile.references, infile.lengths))
    primerSiteLookup = createPrimerSiteLookup(bed, ref_lengths)

    # iterate over the alignment segments in the input SAM file
    for segment in infile:
        # Get primers for this chromname
        segment_bed = bed.get(segment.reference_name, None)  # type: ignore
        if segment_bed is None:
            print(
                "No primers found for chrom %s, skipping" % (segment.reference_name),
                file=sys.stderr,
            )
            continue

        # filter out unmapped and supplementary alignment segments
        if segment.is_unmapped:
            print("%s skipped as unmapped" % (segment.query_name), file=sys.stderr)
            continue
        if segment.is_supplementary:
            print("%s skipped as supplementary" % (segment.query_name), file=sys.stderr)
            continue

        # filter out alignment segments that are not full products
        if args.require_primersites == "none":
            pass
        else:
            fpsite = primerSiteLookup[segment.reference_name][segment.reference_start]
            rpsite = primerSiteLookup[segment.reference_name][segment.reference_end]

            if args.require_primersites == "single":
                if not any([fpsite, rpsite]):
                    print(
                        "%s skipped as not a full product" % (segment.query_name),
                        file=sys.stderr,
                    )
                    continue
            elif args.require_primersites == "both":
                if not all([fpsite, rpsite]):
                    print(
                        "%s skipped as not a full product" % (segment.query_name),
                        file=sys.stderr,
                    )
                    continue

        # locate the nearest primers to this alignment segment
        p1 = find_primer(segment_bed, segment.reference_start, "+")
        p2 = find_primer(segment_bed, segment.reference_end, "-")

        # check if primers are correctly paired and then assign read group
        # NOTE: removed this as a function as only called once
        # TODO: will try improving this / moving it to the primer scheme processing code
        correctly_paired = p1[2]["PrimerBaseName"].replace("_LEFT", "") == p2[2][
            "PrimerBaseName"
        ].replace("_RIGHT", "")
        if not args.no_read_groups:
            if correctly_paired:
                segment.set_tag("RG", p1[2]["PoolName"])
            else:
                segment.set_tag("RG", "unmatched")
        if args.remove_incorrect_pairs and not correctly_paired:
            print(
                "%s skipped as not correctly paired" % (segment.query_name),
                file=sys.stderr,
            )
            continue

        # update the report with this alignment segment + primer details
        report = "%s\t%s\t%s\t%s_%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d" % (
            segment.query_name,
            segment.reference_start,
            segment.reference_end,
            p1[2]["PrimerBaseName"],
            p2[2]["PrimerBaseName"],
            p1[2]["PrimerBaseName"],
            abs(p1[1]),
            p2[2]["PrimerBaseName"],
            abs(p2[1]),
            segment.is_secondary,
            segment.is_supplementary,
            p1[2]["start"],
            p2[2]["end"],
            correctly_paired,
        )
        if args.report:
            print(report, file=reportfh)
        if args.verbose:
            print(report, file=sys.stderr)

        # get the primer positions
        if args.start:
            p1_position = p1[2]["start"]
            p2_position = p2[2]["end"]
        else:
            p1_position = p1[2]["end"]
            p2_position = p2[2]["start"]

        # softmask the alignment if left primer start/end inside alignment
        if segment.reference_start < p1_position:
            try:
                trim(segment, p1_position, False, args.verbose)
                if args.verbose:
                    print(
                        "ref start %s >= primer_position %s"
                        % (segment.reference_start, p1_position),
                        file=sys.stderr,
                    )
            except Exception as e:
                print(
                    "problem soft masking left primer in {} (error: {}), skipping".format(
                        segment.query_name, e
                    ),
                    file=sys.stderr,
                )
                continue

        # softmask the alignment if right primer start/end inside alignment
        if segment.reference_end > p2_position:
            try:
                trim(segment, p2_position, True, args.verbose)
                if args.verbose:
                    print(
                        "ref start %s >= primer_position %s"
                        % (segment.reference_start, p2_position),
                        file=sys.stderr,
                    )
            except Exception as e:
                print(
                    "problem soft masking right primer in {} (error: {}), skipping".format(
                        segment.query_name, e
                    ),
                    file=sys.stderr,
                )
                continue

        # normalise if requested
        if args.normalise:
            pair = "%s-%s-%d" % (
                p1[2]["PrimerBaseName"],
                p2[2]["PrimerBaseName"],
                segment.is_reverse,
            )
            counter[pair] += 1
            if counter[pair] > args.normalise:
                print(
                    "%s dropped as abundance theshold reached" % (segment.query_name),
                    file=sys.stderr,
                )
                continue

        # check the the alignment still contains bases matching the reference
        if segment.cigarstring is not None and "M" not in segment.cigarstring:
            print(
                "%s dropped as does not match reference post masking"
                % (segment.query_name),
                file=sys.stderr,
            )
            continue

        # current alignment segment has passed filters, send it to the outfile
        outfile.write(segment)

    # close up the file handles
    infile.close()
    outfile.close()
    if args.report:
        reportfh.close()


def main():
    parser = argparse.ArgumentParser(
        description="Trim alignments from an amplicon scheme."
    )
    parser.add_argument("bedfile", help="BED file containing the amplicon scheme")
    parser.add_argument("bamfile", help="BAM file")
    parser.add_argument(
        "--normalise", type=int, help="Subsample to n coverage per strand"
    )
    parser.add_argument("--report", type=str, help="Output report to file")
    parser.add_argument(
        "--start", action="store_true", help="Trim to start of primers instead of ends"
    )
    parser.add_argument(
        "--no-read-groups",
        dest="no_read_groups",
        action="store_true",
        help="Do not divide reads into groups in SAM output",
    )
    parser.add_argument("--verbose", action="store_true", help="Debug mode")
    parser.add_argument("--remove-incorrect-pairs", action="store_true")
    parser.add_argument("--require-primersites", choices=["none", "single", "both"])

    args = parser.parse_args()
    go(args)


if __name__ == "__main__":
    main()
