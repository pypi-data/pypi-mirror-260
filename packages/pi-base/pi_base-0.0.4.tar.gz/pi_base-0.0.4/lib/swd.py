#!/usr/bin/env python3

# We're not going after extreme performance here
# pylint: disable=logging-fstring-interpolation
from __future__ import annotations

from abc import ABC, abstractmethod
import argparse
import logging
import os
import platform
import subprocess
import sys
import time
from typing import Optional

from os_utils import which

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__ if __name__ != "__main__" else None)
logger.setLevel(logging.DEBUG)


class AtDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class SWDInterface(ABC):
    """Abstract interface for SWD implementations."""

    def _install_pip(self, package_or_packages, path=None):  # TODO: (when needed) Move to app_utils
        packages = package_or_packages if isinstance(package_or_packages, list) else [package_or_packages]
        cmd = [sys.executable, "-m", "pip", "install"] + packages
        if path:
            cmd += [f"--target={path}"]
        return subprocess.check_call(cmd)

    def _install_brew(self, package_or_packages, path=None):  # TODO: (when needed) Move to app_utils
        packages = package_or_packages if isinstance(package_or_packages, list) else [package_or_packages]
        try:
            # Run the commands to install packages
            subprocess.run(["brew", "install"] + packages, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing brew packages {packages}: {e}")
            return e.returncode
        except FileNotFoundError as e:
            print("brew command not found. Make sure you are running this script on a system with Homebrew.")
            return e.errno
        return 0

    def _install_win_pacman(self, package_or_packages, path=None):  # TODO: (when needed) Move to app_utils
        packages = package_or_packages if isinstance(package_or_packages, list) else [package_or_packages]
        try:
            pacman = which("pacman")
            if not pacman:
                raise FileNotFoundError
            # Run the commands to install packages
            subprocess.run([pacman, "--noconfirm", "-Syuq"], check=True)
            subprocess.run([pacman, "--noconfirm", "-Syq"] + packages, check=True)
            # See <https://wiki.archlinux.org/title/Pacman/Tips_and_tricks>
        except subprocess.CalledProcessError as e:
            print(f"Error installing pacman packages {packages}: {e}")
            return e.returncode
        except FileNotFoundError as e:
            print('"pacman" command not found. Make sure you are running this script on a Windows system with pacman (MSYS2).')
            return e.errno
        return 0

    def _install_apt_linux(self, package_or_packages, path=None):  # TODO: (when needed) Move to app_utils
        packages = package_or_packages if isinstance(package_or_packages, list) else [package_or_packages]
        try:
            # Run the apt command to install openocd
            sudo = which("sudo")
            if not sudo:
                raise FileNotFoundError('"sudo" command not found')
            apt = which("apt")
            if not apt:
                raise FileNotFoundError('"apt" command not found')
            subprocess.run([sudo, apt, "update"], check=True)
            subprocess.run([sudo, apt, "install"] + packages, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing apt packages {packages}: {e}")
            return e.returncode
        except FileNotFoundError as e:
            print(f"{e}. Make sure you are running this script on a Debian-based Linux system.")
            return e.errno
        return 0

    @abstractmethod
    def install(self) -> int:
        """Install required dependencies on the OS."""
        return -1

    @abstractmethod
    def uninstall(self) -> int:
        """Uninstall all OS components that self.install() installed."""
        return -1

    @abstractmethod
    def program(self, firmware_path: Optional[str] = None, bootloader_path: Optional[str] = None, do_erase=True) -> int:
        """Optionally erase and optionally Program connected device with given image file.

        Args:
            firmware_path (str, optional): Firmware image file path.
            bootloader_path (str, optional): Bootloader image file path.
            do_erase (bool, optional): True will erase the target Flash memory. Defaults to True.

        Returns:
            int: error code
        """
        return -1


class JLink(SWDInterface):
    # J-Link Commander
    # https://www.segger.com/downloads/jlink/JLink_Windows_x86_64.exe
    # https://www.segger.com/downloads/jlink/JLink_Windows.exe
    # https://www.segger.com/downloads/jlink/JLink_Linux_arm64.deb
    # https://www.segger.com/downloads/jlink/JLink_Linux_arm.deb
    # https://www.segger.com/downloads/jlink/JLink_MacOSX_universal.pkg
    #
    # Program FW to device:
    # write one of FW images:
    # loadfile "C:\payrange\Hardware\BLE5-BKPro\Bringup\bks_pro\bks_pro_provision.s37"
    # loadfile "C:\payrange\Hardware\BLE5-BKPro\Bringup\bks_pro\bks_pro_alliance.s37"
    # loadfile "C:\payrange\Hardware\BLE5-BKPro\Bringup\bks_pro\bks_pro_battery.s37"
    # loadfile "C:\payrange\Hardware\BLE5-BKPro\Bringup\bks_pro\bks_pro_pulse.s37"
    # followed by the bootloader (.s37 have absolute addresses)
    # loadfile "C:\payrange\Hardware\BLE5-BKPro\Bringup\bks_pro\bks_bootloader.s37"
    # complete script:
    # device EFR32BG24AXXXF1024
    # SI SWD
    # SPEED AUTO
    # connect
    # erase
    # loadfile bkspro_provision_20230605.s37
    # loadfile bootloader-bks_plus.s37
    # exit
    pass


class ProbeRS(SWDInterface):
    # probe-rs
    # See: <https://github.com/probe-rs/probe-rs/issues/1700>
    pass


class OpenOCD(SWDInterface):
    def __init__(self):
        pass

    def _install_mac(self):
        mac_packages = [
            "libtool",
            "automake",
            "libusb",
            "wget",
            "pkg-config",
            "gcc",
            "texinfo",
        ]
        return self._install_brew(mac_packages)
        # TODO: (when needed) Implement the rest of openocd install for MacOS, see <https://www.raspberrypi.com/documentation/microcontrollers/debug-probe.html#macos>
        # Also see files: <https://sourceforge.net/projects/openocd/files/openocd/>

    def _install_lin(self):
        return self._install_apt_linux("openocd")

    def _build_openocd_win(self):
        branch = "rp2040-v0.12.0"
        git_cmd = ["git", "clone", "https://github.com/raspberrypi/openocd.git"]  # TODO: (when needed) Use official repo (or clone with EFR32xx2 patches)
        if branch:
            git_cmd += ["--branch", branch]
        # ? git_cmd += ['--depth=1']
        build_dir = "~"  # TODO: (when needed) Implement build dir selection (config file?)
        commands = [
            ["cd", build_dir],
            git_cmd,
            ["cd", "openocd"],
            ["./bootstrap"],
            ["./configure", "--disable-werror"],  # TODO: (when needed) Make --disable-werror OS dependent. Unfortunately disable-werror is needed because not everything compiles cleanly on Windows
            ["make", "-j4"],
        ]
        # TODO: (when needed) Implement
        return -1

    def _install_win(self):
        win_packages = [
            "mingw-w64-x86_64-toolchain",
            "git",
            "make",
            "libtool",
            "pkg-config",
            "autoconf",
            "automake",
            "texinfo",
            "mingw-w64-x86_64-libusb",
            "mingw-w64-x86_64-openocd",  # Install pre-build package (instead of compiling from sources)
        ]
        return self._install_win_pacman(win_packages)
        # Also see files: <https://sourceforge.net/projects/openocd/files/openocd/>

    def install(self):
        if os.name == "nt":
            return self._install_win()
        elif platform.system() == "Darwin":  # MacOS
            return -1  # TODO: (when needed) Implement openocd install on MacOS
        elif os.name == "posix":  # Linux
            return self._install_lin()
        return -1

    def uninstall(self):
        # TODO: (when needed) Implement
        return -1

    def program(self, firmware_path: Optional[str] = None, bootloader_path: Optional[str] = None, do_erase=True):
        # TODO: (when fixed upstream) There's un-merged PR for flashing EFR32xx2 <https://review.openocd.org/c/openocd/+/6173> which seems to be required for OpenOCD to work on EFR32BG24.
        # Also see <https://github.com/knieriem/openocd-efm32-series2>

        # Path to the OpenOCD executable (modify as needed)
        OPENOCD_PATH = "openocd"

        # Target processor configuration file for STLINK-V3MINI (modify as needed)
        TARGET_CONFIG = "stlink-v3mini.cfg"

        # Launch OpenOCD to program the firmware
        openocd_cmd = [OPENOCD_PATH, "-f", TARGET_CONFIG, "-c", "init", "-c", "reset halt"]
        if do_erase:
            openocd_cmd += [
                "-c",
                "flash erase",
            ]
        if firmware_path:
            openocd_cmd += [
                # '-c', f'flash write_image {firmware_path} 0x08000000'
                "-c",
                f"flash write_image {firmware_path}",
            ]
        if bootloader_path:
            openocd_cmd += [
                # '-c', f'flash write_image {bootloader_path} 0x08000000'
                "-c",
                f"flash write_image {bootloader_path}",
            ]

        openocd_cmd += ["-c", "reset run", "-c", "exit"]

        try:
            # Run OpenOCD
            subprocess.run(openocd_cmd, check=True)
            print("Firmware programming successful!")
        except subprocess.CalledProcessError as e:
            print(f"Error programming firmware: {e}")
        except FileNotFoundError:
            print("OpenOCD executable not found. Please check the path.")

        return 0


class PyOCD(SWDInterface):
    def __init__(self):
        pass

    def install(self):
        return self._install_pip("pyOCD")
        # TODO: (now) Implement adding packs: `pyocd pack install efr32bg24`

    def uninstall(self):
        # TODO: (when needed) Implement
        return -1

    def erash(self):
        # ? pyocd erase --chip -t efr32bg24a010f1024im40 -O reset_type=hw -O connect_mode='under-reset'
        return -1

    def program(self, firmware_path: Optional[str] = None, bootloader_path: Optional[str] = None, do_erase=True):
        target_id = "STLINK-V3MINI-E"

        # import pyocd  # pylint: disable=import-outside-toplevel
        # from pyocd.board import MbedBoard  # pylint: disable=import-outside-toplevel
        # import pyOCD.board  # pylint: disable=import-outside-toplevel
        import pyocd.core  # pylint: disable=import-outside-toplevel

        # import pyocd.board  # pylint: disable=import-outside-toplevel
        from pyocd.board.mbed_board import MbedBoard  # pylint: disable=import-outside-toplevel

        try:
            board = MbedBoard(board_id=target_id)
            if firmware_path:
                with open(firmware_path, "rb") as binary_file:
                    binary_data = binary_file.read()

                target = board.target
                target.halt()

                # Erase the flash memory
                target.flash.init()
                target.flash.eraseAll()

                # Program the binary firmware image
                target.flash.program(binary_data, 0x0)

                # Verify the programming
                if target.flash.verify(binary_data, 0x0):
                    print("Firmware programmed successfully.")
                else:
                    print("Firmware programming failed.")

            target.reset()
            board.uninit()

        except pyocd.core.exceptions.Error as e:
            print(f'Error {type(e)} "{e}"')
        except Exception as e:
            print(f'Error {type(e)} "{e}"')

        return 0


class BMP(SWDInterface):
    def __init__(self):
        self.bmpy = None

    def install(self):
        # res = self._install_pip('bmpy')
        # return res
        # TODO: (now) Install GDB toolchain files
        return 0

    def uninstall(self):
        # TODO: (when needed) Implement
        return -1

    def probe_fw_upgrade(self, firmware_file):
        # TODO: (when needed) Implement
        # bmputil flash blackmagic-native.elf
        # dfu-util.exe  -d 1d50:6018,:6017 -s 0x08002000:leave -D blackmagic.bin
        # sudo dfu-util -d 1d50:6018,:6017 -s 0x08002000:leave -D blackmagic-native.bin
        pass

    def program(self, firmware_path: Optional[str] = None, bootloader_path: Optional[str] = None, do_erase=True):
        # Used lates FW blackmagic-native-v1_10_0-rc0. Series 2 (BG24) is not supported in current efm32.c.

        # See progress of issue <https://github.com/blackmagic-debug/blackmagic/issues/1296> and PR <https://github.com/blackmagic-debug/blackmagic/pull/1436>

        # To install FW on BMP probe, use dfu-util <https://dfu-util.sourceforge.net/>,
        # On Windows, first run Zadiq <https://zadig.akeo.ie/> to install WinUSB driver on DFU devices (1d50:6018, 1d50:6017)
        # $ /c/dev/pi-base/lib/swd/blackmagic/dfu-utils/dfu-util-0.11-binaries/win64/dfu-util.exe -d 1d50:6018,6017 -s 0x08002000:leave -D blackmagic-native-v1_10_0-rc0.bin
        # port = '/dev/ttyACM0'
        # To detect ports: $(wildcard /dev/serial/by-id/usb-Black_Sphere_Technologies_Black_Magic_Probe_*-if00 /dev/cu.usbmodem*1)
        port = "\\\\.\\COM3"
        toolchain_path = "/c/SiliconLabs/SimplicityStudio/v5/developer/toolchains/gnu_arm/10.3_2021.10/bin"
        cmds = [
            f"{toolchain_path}/arm-none-eabi-gdb.exe",
            "-nx",
            "--batch",
            # f"{toolchain_path}/arm-none-eabi-gdb", "-nx", "--batch",
            "-ex",
            "target extended-remote {port}",
            # "-ex", "monitor tpwr enable", # To power-on target side if it is not powered
            # ?? "-ex", "monitor connect_srst disable", #
            # ?? "-ex", "monitor connect_srst enable", #
            "-ex",
            "monitor reset",  # Pulse nRST, disconnect the target
            "-ex",
            "monitor erase_mass",  # Erase whole device flash
            # "-ex", "monitor jtag_scan", $ For JTAG connection
            "-ex",
            "monitor swdp_scan",
            "-ex",
            "attach 1",
            # file C:\\payrange\\Hardware\\BLE5-BKPro\\Bringup\\bks_pro\\bks_pro_provision.s37
            "-ex",
            f"load {firmware_path}"
            # load C:\\payrange\\Hardware\\BLE5-BKPro\\Bringup\\bks_pro\\bks_pro_provision.s37
            "-ex",
            "compare-sections",
            "firmware.elf"
            # file C:\\payrange\\Hardware\\BLE5-BKPro\\Bringup\\bks_pro\\bks_bootloader.s37
            "-ex",
            f"load {bootloader_path}",
            # load C:\\payrange\\Hardware\\BLE5-BKPro\\Bringup\\bks_pro\\bks_bootloader.s37
            "-ex",
            "compare-sections",
            # "-ex", "run",
            "-ex",
            "kill",  # Reset the target, Disconnect from target
        ]

        error = """(gdb) monitor swdp_scan
Target voltage: 3.3V
Please report unknown device with Designer 0x673 Part ID 0x1f41
Please report unknown device with Designer 0x673 Part ID 0x1f41
Available Targets:
No. Att Driver
*** 1   Unknown ARM Cortex-M Designer 0x673 Part ID 0x1f41 M33
*** 2   Unknown ARM Cortex-M Designer 0x673 Part ID 0x1f41 M0+
"""
        scr = """
        # Print BMPM version
            monitor version
            # To make sure the target is not in a "strange" mode we tell BMPM to reset the
            # target using the reset pin before connecting to it.
            monitor connect_srst enable
            # Enable target power (aka. provide power to the target side of the level shifters)
            monitor tpwr enable
            # Scan for devices using SWD interface
            monitor swdp_scan
            # Alternatively scan for devices using JTAG. (comment out the above line...)
            # monitor jtag_scan
            # Attach to the newly found target if available. (if it fails the script exits)
            attach 1
            # Success! Lets make some sound!
            shell paplay /usr/share/sounds/ubuntu/stereo/message.ogg
            # Load aka. flash the binary
            load
            # Check if the flash matches the binary
            compare-sections
            # Reset the target and disconnect
            kill
"""
        # TODO: (now) execute cmds

    def chatgpt_hallucination_program(self, firmware_path=None, bootloader_path=None, do_erase=True):
        bmpy = self.bmpy

        # Create a Black Magic Probe object
        probe = bmpy.BMP()

        # Connect to the Black Magic Probe hardware
        probe.connect()

        # Check if the probe is connected successfully
        if probe.connected():
            print("Connected to Black Magic Probe")
        else:
            print("Failed to connect to Black Magic Probe")
            sys.exit()

        # Halt the target processor
        probe.halt()

        # Erase the flash memory of the target processor (optional)
        if do_erase:
            probe.erase_flash()

        # Load the firmware binary file
        probe.load_binary(firmware_path)

        # Program the firmware into the flash memory of the target processor
        probe.program_flash()

        # Verify the programmed firmware
        if probe.verify_flash():
            print("Firmware programming successful")
        else:
            print("Firmware programming failed")

        # Reset the target processor
        probe.reset()

        # Disconnect from the Black Magic Probe
        probe.disconnect()

        # Delay to allow the target processor to reset and start running the new firmware
        time.sleep(2)

        print("Programming complete")
        return 0


def SWD(driver_type: str, *args, **kwargs) -> SWDInterface | None:
    inst = None
    if driver_type.lower() == "bmp":
        inst = BMP(*args, **kwargs)
    if driver_type.lower() in ["openocd", "ocd"]:
        inst = OpenOCD(*args, **kwargs)
    if driver_type.lower() == "pyocd":
        inst = PyOCD(*args, **kwargs)
    return inst


def OsSWD(driver_type=None, *args, **kwargs) -> SWDInterface:
    if not driver_type:
        # TODO: (when needed) Implement: driver_type = 'bmp'
        if os.name == "nt" or platform.system() == "Darwin":  # Windows
            driver_type = "ocd"
        elif os.name == "posix":  # Linux, MacOS
            driver_type = "pyocd"
        else:
            raise NotImplementedError(f"Unsupported OS {os.name}")

    swd = SWD(driver_type)
    if not swd:
        raise ValueError(f"Error getting SWD class for {driver_type}")
    return swd


def cmd_install(driver_type, options=None) -> int:
    swd = OsSWD(driver_type)
    return swd.install()


def cmd_uninstall(driver_type, options=None) -> int:
    swd = OsSWD(driver_type)
    return swd.uninstall()


def cmd_program(driver_type, image_file, bootloader_file=None, options=None) -> int:
    swd = OsSWD(driver_type)
    return swd.program(image_file, bootloader_file)


def parse_args():
    parser = argparse.ArgumentParser(description="SWD programmer")

    # Common optional arguments
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")

    # Positional argument for the command
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Parser for 'install' command
    install_parser = subparsers.add_parser("install", help="Add a new printer")
    install_parser.add_argument("driver_type", type=str, help="Driver type")

    # Parser for 'program' command
    program_parser = subparsers.add_parser("program", help="Add a new printer")
    program_parser.add_argument("driver_type", type=str, help="Driver type")
    program_parser.add_argument("image_file", type=str, help="Image file path")
    program_parser.add_argument("bootloader_file", type=str, help="Bootloader file path", default=None)

    # Parse the command line arguments
    args = parser.parse_args()
    return args, parser


def main():
    args, parser = parse_args()
    logger.debug(f"DEBUG {vars(args)}")

    try:
        if args.command == "install":
            options = AtDict()
            return cmd_install(args.driver_type, options)

        # if args.command == 'uninstall':
        #     options = AtDict()
        #     return cmd_uninstall(options)

        if args.command == "program":
            options = AtDict()
            return cmd_program(args.driver_type, args.image_file, args.bootloader_file, options)

        # if args.command == 'devices':
        #     options = AtDict()
        #     return cmd_devices(options)

        # if args.command == 'printers':
        #     options = AtDict()
        #     return cmd_printers(options)

        # if args.command == 'add':
        #     options = AtDict()
        #     if args.location:
        #         options['location'] = args.location
        #     if args.description:
        #         options['description'] = args.description
        #     return cmd_add_printer(args.printer_name, args.printer_uri, args.ppd_file, options)

        # if args.command == 'autoadd':
        #     options = AtDict()
        #     return cmd_autoadd_printers(options)

        # if args.command == 'delete':
        #     options = AtDict()
        #     return cmd_delete_printer(args.printer_name, options)

        # if args.command == 'test':
        #     options = AtDict()
        #     return cmd_print_test(args.printer_name, options)

        # if args.command == 'print':
        #     return cmd_print_file(args.printer_name, args.file_name, options=args.rest)

    except Exception as e:
        logger.error(f'Error {type(e)} "{e}"')
        return -1

    parser.print_help()
    return 1


if __name__ == "__main__":
    rc = main()
    if rc:
        sys.exit(rc)
