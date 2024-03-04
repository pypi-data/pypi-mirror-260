#!/usr/bin/python3

"""CLI entrypoint utilities"""

from argparse import ArgumentParser, Namespace
from typing import Final, Iterable
from . import __doc__ as description, __version__
from .device import WMIDevice, wmi_bus_devices

__all__ = (
    "ARGUMENT_PARSER",
    "main",
    "main_cli"
)

ARGUMENT_PARSER: Final = ArgumentParser(
    prog="lswmi",
    description=description
)
ARGUMENT_PARSER.add_argument(
    "-v",
    "--version",
    action="version",
    version=f"%(prog)s {__version__}"
)
ARGUMENT_PARSER.add_argument(
    "-V",
    "--verbose",
    action="store_true",
    help="enable verbose output"
)
ARGUMENT_PARSER.add_argument(
    "-g",
    "--guid",
    action="store",
    help="show only devices with the specified GUID"
)


def print_device_summary(device: WMIDevice) -> None:
    """Print a short WMI device summary"""
    print(f'{device.guid}: {device.device_type:<6} (Instances: {device.instances})')


def print_device_verbose(device: WMIDevice) -> None:
    """Print additional WMI device information"""
    try:
        print(f'    Identification: {device.device_id} -> {device.get_acpi_path()}')
    except FileNotFoundError as error:
        print(f'    Unable to get ACPI path: {error}')
        print(f'    Identification: {device.device_id}')

    print(f'    Expensive: {device.expensive}')
    if device.setable is not None:
        print(f'    Setable: {device.setable}')

    if device.driver is not None:
        print(f'    Driver: {device.driver}')


def wmi_devices() -> Iterable[WMIDevice]:
    """Scan for WMI devices"""
    for path in wmi_bus_devices():
        try:
            device = WMIDevice.from_sysfs(path)
        except OSError as error:
            print(f'Unable to read WMI device: {error}')
            continue

        yield device


def main(args: Namespace) -> int:
    """Entrypoint for the ePPID tool"""
    devices = wmi_devices()
    if args.guid is not None:
        devices = filter(lambda d: d.guid == args.guid, devices)

    for device in devices:
        print_device_summary(device)
        if args.verbose:
            print_device_verbose(device)
            print('')

    return 0


def main_cli() -> int:
    """CLI entry point"""
    return main(ARGUMENT_PARSER.parse_args())
