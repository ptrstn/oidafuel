import argparse

from oidafuel import __version__
from oidafuel.econtrol import (
    get_regions,
)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Check gas prices for a given location"
    )

    parser.add_argument(
        "--version", action="version", version="%(prog)s {}".format(__version__)
    )

    parser.add_argument("--list-regions", action="store_true", help="List Regions")

    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.list_regions:
        regions = get_regions()
        for state in regions:
            print(f"{state.region_code:4} {state.name:30} [{state.region_type}]")
            for sub_region in state.sub_regions:
                print(
                    f"{sub_region.region_code:4} "
                    f"{sub_region.name:30} "
                    f"[{sub_region.region_type}]"
                )


if __name__ == "__main__":
    main()
