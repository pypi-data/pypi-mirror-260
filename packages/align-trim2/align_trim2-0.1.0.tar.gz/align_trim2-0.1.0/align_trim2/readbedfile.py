import sys
import pandas as pd


def merge_sites(canonical, alt):
    """Merges a canonical primer site with an alt site, producing an interval that encompasses both

    Parameters
    ----------
    canonical : dict
        The canonical primer site, provided as a dictionary of the bed file row
    alt : dict
        The alt primer site, provided as a dictionary of the bed file row

    Returns
    -------
    dict
        A dictionary of the merged site, where the dict represents a bed file row
    """
    # base the merged site on the canonical
    mergedSite = canonical

    # check the both the canonical and alt are the same direction
    if canonical["direction"] != alt["direction"]:
        print(
            "could not merge alt with different orientation to canonical",
            file=sys.stderr,
        )
        raise SystemExit(1)

    # merge the start/ends of the alt with the canonical to get the largest window possible
    if alt["start"] < canonical["start"]:
        mergedSite["start"] = alt["start"]
    if alt["end"] > canonical["end"]:
        mergedSite["end"] = alt["end"]
    return mergedSite


def getPrimerNumber(primerID) -> int | str:
    """Infer the primer number based on it's ID containing _alt

    Parameters
    ----------
    primerID : string
        The primer ID from the 4th field of the primer scheme

    Returns
    -------
    int | str
        The primer number, or _alt if the primer is an alt primer. Will return primerNumber 0 if the primer is not an alt

    """
    primerID_list = primerID.split("_")

    if len(primerID_list) == 0:
        raise ValueError(f"Invalid primerID: {primerID}")

    # Catch alts
    if "alt" in primerID_list[-1].lower():
        return "alt"
    # if PrimerNumber is give in the primerID, return it
    if primerID_list[-1].isdigit():
        return int(primerID_list[-1])
    # if the primer is not an alt, return 0
    else:
        return 0


def getPrimerBaseName(primerID) -> str:
    """Infer the primer base name based on it's ID containing

    Parameters
    ----------
    primerID : string
        The primer ID from the 4th field of the primer scheme

    Returns
    -------
    str
        The primer base name, with the PrimerNumber | _alt removed
    """
    primerID_list = primerID.split("_")
    if len(primerID_list) == 0:
        raise ValueError(f"Invalid primerID: {primerID}")

    # if PrimerNumber is give in the primerID, return it
    if primerID_list[-1].isdigit() or "alt" in primerID_list[-1].lower():
        return "_".join(primerID_list[:-1])
    # if the primer is not an alt, return primerID
    else:
        return primerID


def getPrimerDirection(primerID):
    """Infer the primer direction based on it's ID containing LEFT/RIGHT

    Parameters
    ----------
    primerID : string
        The primer ID from the 4th field of the primer scheme
    """
    if "LEFT" in primerID:
        return "+"
    elif "RIGHT" in primerID:
        return "-"
    else:
        print("LEFT/RIGHT must be specified in Primer ID", file=sys.stderr)
        raise SystemExit(1)


def read_bed_file(fn) -> dict[str, list]:
    """Parses a bed file and collapses alts into canonical primer sites

    Parameters
    ----------
    fn : str
        The bedfile to parse

    Returns
    -------
    list
        A list of dictionaries, where each dictionary contains a row of the parsed bedfile.
        The available dictionary keys are - Primer_ID, direction, start, end
    """

    # read the primer scheme into a pandas dataframe and run type, length and null checks
    primers = pd.read_csv(
        fn,
        sep="\t",
        header=None,
        comment="#",
        names=["chrom", "start", "end", "Primer_ID", "PoolName", "direction"],
        dtype={
            "chrom": str,
            "start": int,
            "end": int,
            "Primer_ID": str,
            "PoolName": str,
            "direction": str,
        },
        usecols=(0, 1, 2, 3, 4, 5),
    )  # type: ignore

    if len(primers.index) < 1:
        print("primer scheme file is empty", file=sys.stderr)
        raise SystemExit(1)
    if primers.isnull().sum().sum():
        print("malformed primer scheme file", file=sys.stderr)
        raise SystemExit(1)

    # Parsed from bedfile, so we don't need to infer the direction
    # compute the direction
    # primers["direction"] = primers.apply(
    #    lambda row: getPrimerDirection(row.Primer_ID), axis=1
    # )

    # Parse PrimerNumber from Primer_ID
    # Can either be int or _alt depending on the primer version
    primers["PrimerNumber"] = primers["Primer_ID"].apply(lambda x: getPrimerNumber(x))
    # Parse the Primer_ID to get the PrimerBaseName
    primers["PrimerBaseName"] = primers["Primer_ID"].apply(
        lambda x: getPrimerBaseName(x)
    )

    ## Handle the alts and primerClouds
    # separate alt primers into a new dataframe
    altFilter = primers["PrimerBaseName"].duplicated("first")
    alts = pd.DataFrame(
        columns=(
            "chrom",
            "start",
            "end",
            "Primer_ID",
            "PoolName",
            "direction",
            "PrimerNumber",
            "PrimerBaseName",
        )
    )
    alts = pd.concat([alts, primers[altFilter]])  # type: ignore
    primers = primers.drop(primers[altFilter].index.values)  # type: ignore

    # convert the primers dataframe to dictionary, indexed by Primer_ID
    #  - verify_integrity is used to prevent duplicate Primer_IDs being processed
    bedFile = primers.set_index(
        "PrimerBaseName", drop=False, verify_integrity=True
    ).T.to_dict()

    # merge alts
    for _, row in alts.iterrows():
        PrimerBaseName = row["PrimerBaseName"]

        # check the bedFile if another version of this primer exists
        if PrimerBaseName not in bedFile:

            # add to the bed file and continue
            bedFile[PrimerBaseName] = row.to_dict()
            continue

        # otherwise, we've got a primer ID we've already seen so merge the alt
        mergedSite = merge_sites(bedFile[PrimerBaseName], row)

        # update the bedFile
        bedFile[PrimerBaseName] = mergedSite

    # group the bedFile dict by chromname
    chromBedFile = {}
    for primer in bedFile.values():
        chrom = primer["chrom"]
        if chrom not in chromBedFile:
            chromBedFile[chrom] = []
        chromBedFile[chrom].append(primer)

    # return the bedFile as a list
    return chromBedFile
