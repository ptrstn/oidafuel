import argparse
import sys

from oidafuel import __version__
from oidafuel.core import get_gas_prices_by_region, get_gas_prices_by_address
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

    parser.add_argument(
        "--fuel-type",
        choices=["SUP", "DIE", "GAS"],
        help="SUP (Super 95), DIE (Diesel) or GAS (Compressed natural gas)",
    )

    location_group = parser.add_mutually_exclusive_group()
    location_group.add_argument("--region", help="Region code")
    location_group.add_argument("--address", help="Address")

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
        return

    region = args.region
    address = args.address
    fuel_type = args.fuel_type

    if not region and not address:
        print("Please specify the region or address")
        sys.exit()

    if not fuel_type:
        print("Please specify the fuel type")
        sys.exit()

    if region:
        gas_prices = get_gas_prices_by_region(int(region), fuel_type)
    else:
        gas_prices = get_gas_prices_by_address(address, fuel_type)

    for gas_price in gas_prices:
        print(
            f"{gas_price.price:1.4} "
            f"{gas_price.name}, "
            f"{gas_price.postal_code} {gas_price.city}, "
            f"{gas_price.address} "
        )


if __name__ == "__main__":
    main()
