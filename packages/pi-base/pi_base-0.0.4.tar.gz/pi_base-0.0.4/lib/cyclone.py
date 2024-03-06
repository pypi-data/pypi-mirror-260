#!/usr/bin/env python3

# We're not going after extreme performance here
# pylint: disable=logging-fstring-interpolation

# from abc import ABC, abstractmethod
import argparse
import ctypes
import logging
import importlib
import os

# import platform
import subprocess
import sys

# import time
from time import sleep
from typing import Optional, Union

# "modpath" must be first of our modules
from app_utils import get_os_name, download_and_execute

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__ if __name__ != "__main__" else None)
logger.setLevel(logging.DEBUG)

# For package resolution to work, add script's directory to sys.path:
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# sys.path.append(SCRIPT_DIR)


class AtDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class CycDevice:
    def __init__(self, port=None, name=None, ip=None):
        self.port = port
        self.name = name
        self.ip = ip

    def port_or_ip_or_name(self):
        return self.port or self.ip or self.name


class CycImage:
    def __init__(self, slot=None, storage_type=None, name=None, file=None, crc32=None):
        self.slot = slot
        self.type = storage_type
        self.name = name
        self.file = file
        self.crc32 = crc32


class Cyclone:
    def __init__(self, loggr=logger) -> None:
        self.loggr = loggr
        if not self.loggr:
            raise ValueError("Please provide loggr argument")

        self.cycloneControlSDK = None
        self.cycloneControlSDKObj = None

        self.cycs = []
        self.cyc_id_or_ip = None
        self.cyc_name = None
        self.cyc_handle = 0
        self.cyc_images = None

    def install_driver_win(self) -> int:
        # Windows drivers installer is a program `cyclone/deploy/PEDrivers_install.exe` that requires admin, and runs in a GUI, no headless.
        path = os.path.abspath(os.path.join(SCRIPT_DIR, "cyclone/deploy/PEDrivers_install.exe"))
        self.loggr.error(f'Windows OS drivers installation for PEMicro Cyclone is not implemented. Please install manually by running "{path}".')
        return 1  # NOT IMPLEMENTED

    def install_driver(self) -> int:
        drivers = {
            "Windows": {"func": self.install_driver_win},
            "Linux": {"func": None},  # TODO: (when needed) Implement Cyclone.install_driver_linux()
            "MacOS": {"func": None},  # TODO: (when needed) Implement Cyclone.install_driver_macos()
        }
        os_name = get_os_name()
        driver = drivers.get(os_name)
        if not driver or not driver["func"]:
            raise NotImplementedError(f'No driver install recipe for "{os_name}" OS.')
        return driver["func"]()

    def download_install_package(self, do_install=True) -> int:  # UNUSED
        # Note:
        #   Download is quite involved to implement, as PEMicro server keeps files behind a login wall.
        #   What seems to work is a direct link URL extracted via email using a not-logged in browser.
        #   But further, installation of PEMicro package is GUI-driven and there's no headless install possibility.
        #   So instead, we rely on a hard copy of the libs from PEMicro stashed in this repo.
        downloads = {
            "Windows": {
                "url": "https://www.pemicro.com/downloads/download_file.cfm?download_temp_id=591834&user_id=234017&download_token=484313592311",
                "url_redir": "https://www.pemicro.com/downloads/download_file.cfm?download_id=481",
                "file": "cyclone_install.exe",
                "command": "cyclone_install.exe",
            },
            "Linux": {
                "url": "https://www.pemicro.com/downloads/download_file.cfm?download_temp_id=591910&user_id=234017&download_token=968376209530",
                "url_redir": "https://www.pemicro.com/downloads/download_file.cfm?download_id=577",
                "file": "cyclonecontrolsdk_maclinux.tgz",
                "command": None,
            },
            "MacOS": {
                "url": "https://www.pemicro.com/downloads/download_file.cfm?download_temp_id=591910&user_id=234017&download_token=968376209530",
                "url_redir": "https://www.pemicro.com/downloads/download_file.cfm?download_id=577",
                "file": "cyclonecontrolsdk_maclinux.tgz",
                "command": None,
            },
        }

        os_name = get_os_name()
        download = downloads.get(os_name)
        if not download:
            raise NotImplementedError(f'No download recipe for "{os_name}" OS.')

        command = None
        if do_install:
            # command = download['command'] or [download['file']] # TODO: (when needed) Implement some smarts (should not assume all files are executable, e.g. "*.tgz")
            command = download["command"]
        res = download_and_execute(download["url"], download["file"], command, remove_after=False, loggr=self.loggr)

    def uninstall(self) -> int:
        pass

    def load_lib_maybe(self):
        if self.cycloneControlSDKObj:
            # Already loaded
            return
        # import cycloneControlSDK
        package = os.path.basename(SCRIPT_DIR)
        path = ".cyclone.cycloneControlSDK_python.cycloneControlSDK"
        try:
            self.cycloneControlSDK = importlib.import_module(path, package)
            self.cycloneControlSDKObj = self.cycloneControlSDK.cycloneControlSDK()
            self.loggr.info(f"cycloneControlSDK lib Version {self.cycloneControlSDKObj.version()}")
        except Exception as e:
            self.loggr.error(f'Error {type(e)} "{e}" loading cycloneControlSDK lib, check installation.')
            raise

    def unload_lib_maybe(self):
        if self.cycloneControlSDKObj:
            self.loggr.info("Disconnecting from all connected Cyclones ...")
            self.cycloneControlSDKObj.disconnectFromAllCyclones()
            self.cycloneControlSDKObj.unloadLibrary()
        self.cycloneControlSDKObj = None
        self.cycloneControlSDK = None
        self.cycs = []
        self.cyc_id_or_ip = None
        self.cyc_name = None
        self.cyc_handle = 0
        self.cyc_images = None

    def enumerate_devices(self) -> list[dict[str, str]]:
        self.load_lib_maybe()
        self.cycloneControlSDKObj.enumerateAllPorts()
        cycs_num = self.cycloneControlSDKObj.queryNumberOfAutodetectedCyclones()
        self.cycs = []
        for i in range(cycs_num):
            port = self.cycloneControlSDKObj.queryInformationOfAutodetectedCyclone(i + 1, 3)  # Port/ID 'USB1'
            name = self.cycloneControlSDKObj.queryInformationOfAutodetectedCyclone(i + 1, 2)  # Name 'Universal_PEM46D039'
            ip = self.cycloneControlSDKObj.queryInformationOfAutodetectedCyclone(i + 1, 1)  # IP Address
            self.cycs += [CycDevice(port=port, name=name, ip=ip)]
        return self.cycs

    def cyc_descr(self):
        return f'Cyclone {self.cyc_id_or_ip} "{self.cyc_name}"' if self.cyc_handle != 0 else "(No Cyclone)"

    def cyc_open(self, cyc_id_or_ip) -> int:
        self.load_lib_maybe()
        if not cyc_id_or_ip or cyc_id_or_ip.lower() == "auto":
            cycs = self.enumerate_devices()
            if not cycs:
                raise RuntimeError("No Cyclone devices found to open.")
            cyc_id_or_ip = cycs[0].port_or_ip_or_name()

        if self.cyc_handle != 0 and self.cyc_id_or_ip != cyc_id_or_ip:
            raise RuntimeError(f"Another {self.cyc_descr()} already opened, close it first.")

        self.cyc_handle = self.cycloneControlSDKObj.connectToCyclone(cyc_id_or_ip)
        if self.cyc_handle != 0:
            self.cyc_id_or_ip = cyc_id_or_ip
            self.cyc_name = self.cycloneControlSDKObj.getPropertyValue(self.cyc_handle, 0, self.cycloneControlSDK.CycloneProperties, self.cycloneControlSDK.selectCyclonePropertyName)
            return 0
        return 1

    def cyc_close(self):
        if self.cyc_handle:
            self.loggr.info(f"Disconnecting from {self.cyc_descr()}")
            self.cycloneControlSDKObj.disconnectFromAllCyclones()
        self.cyc_id_or_ip = None
        self.cyc_name = None
        self.cyc_handle = None
        self.cyc_images = None

    def cyc_reset(self) -> int:
        if self.cycloneControlSDKObj.resetCyclone(self.cyc_handle, 7000):
            return 0
        return 1

    def cyc_image_file_info(self, image_file) -> CycImage:
        sap_file = ctypes.c_char_p(image_file.encode("UTF-8"))
        ret_value_crc32 = ctypes.c_ulong()
        ret_value_name = ctypes.c_char_p()
        self.loggr.info(f'Getting CRC32 of file "{image_file}" ... ')
        decoded = False
        if not self.cycloneControlSDKObj.cycloneSpecialFeatures(self.cycloneControlSDK.CYCLONE_GET_IMAGE_CRC32_FROM_FILE, decoded, 0, 0, 0, ctypes.byref(ret_value_crc32), sap_file):
            self.loggr.error("Failed")
            return None  # Fail
        decoded = True
        if not self.cycloneControlSDKObj.cycloneSpecialFeatures(self.cycloneControlSDK.CYCLONE_GET_IMAGE_DESCRIPTION_FROM_FILE, decoded, 0, 0, 0, ctypes.byref(ret_value_name), sap_file):
            self.loggr.error("Failed")
            return None  # Fail
        crc32 = int(ret_value_crc32.value)
        name = ret_value_name.value.decode("UTF-8")
        self.loggr.info("Done")
        self.loggr.info(f"[Image File CRC32] = 0x{crc32:08X}")
        self.loggr.info(f'[Image Description] = "{name}"')
        return CycImage(name=name, file=image_file, crc32=crc32)  # Success

    def cyc_image_get_info(self, slot: int) -> CycImage:
        storage_type = self.cycloneControlSDKObj.getPropertyValue(self.cyc_handle, slot, self.cycloneControlSDK.ImageProperties, self.cycloneControlSDK.selectImagePropertyMediaType)
        name = self.cycloneControlSDKObj.getPropertyValue(self.cyc_handle, slot, self.cycloneControlSDK.ImageProperties, self.cycloneControlSDK.selectImagePropertyName)
        crc32str = self.cycloneControlSDKObj.getPropertyValue(self.cyc_handle, slot, self.cycloneControlSDK.ImageProperties, self.cycloneControlSDK.selectImagePropertyCRC32)
        crc32 = int(crc32str, 16)
        # imageUniqueId = self.cycloneControlSDKObj.getPropertyValue(self.cyc_handle, slot, self.cycloneControlSDK.ImageProperties, self.cycloneControlSDK.selectImagePropertyUniqueId)
        # imageKeyID = self.cycloneControlSDKObj.getPropertyValue(self.cyc_handle, slot, self.cycloneControlSDK.ImageProperties, self.cycloneControlSDK.selectImageKeyID)
        # imageKeyDescription = self.cycloneControlSDKObj.getPropertyValue(self.cyc_handle, slot, self.cycloneControlSDK.ImageProperties, self.cycloneControlSDK.selectImageKeyDescription)
        return CycImage(slot=slot, storage_type=storage_type, name=name, crc32=crc32)

    def cyc_images_get(self, force_fetch=False) -> list[dict[str, Union[int, str]]]:
        if force_fetch or self.cyc_images is None:
            self.cyc_images = []
            numimages = self.cycloneControlSDKObj.countCycloneImages(self.cyc_handle)
            if numimages > 0:
                for i in range(1, numimages + 1):
                    self.cyc_images += [self.cyc_image_get_info(i)]
        return self.cyc_images

    def cyc_image_find(self, name, crc32=None, force_fetch=False):
        images = self.cyc_images_get(force_fetch)
        for image in images:
            if image.name == name and (not crc32 or crc32 == image.crc32):
                return image.slot
        return None

    def cyc_images_add(self, image_files: list[str]) -> int:
        for image_file in image_files:
            if not self.cycloneControlSDKObj.addCycloneImage(self.cyc_handle, self.cycloneControlSDK.MEDIA_INTERNAL, True, image_file):  # noqa: FBT003
                self.loggr.error(f'Failed adding image file "{image_file}" to {self.cyc_descr()}.')
                return 1  # Fail
            slot = len(self.cyc_images) + 1
            self.cyc_images += [self.cyc_image_get_info(slot)]
        return 0  # Success

    def cyc_image_add(self, image_file: str) -> int:
        return self.cyc_images_add([image_file])

    def cyc_image_clear(self, slot: int) -> int:
        if self.cycloneControlSDKObj.eraseCycloneImage(self.cyc_handle, slot):
            # Remove entry from self.cyc_images, as Cyclone removes element and shifts the rest down
            if slot < len(self.cyc_images) + 1:
                del self.cyc_images[slot - 1]
            return 0  # Success
        return 1  # Fail

    def cyc_images_clear_all(self) -> int:
        self.cyc_images = []
        if self.cycloneControlSDKObj.formatCycloneMemorySpace(self.cyc_handle, self.cycloneControlSDK.MEDIA_INTERNAL):
            return 0  # Success
        return 1  # Fail

    def cyc_image_start(self, slot) -> int:
        if not self.cycloneControlSDKObj.startImageExecution(self.cyc_handle, slot):
            return 1  # Fail
        return 0  # Success

    def cyc_image_wait_done(self) -> int:
        while True:
            if self.cycloneControlSDKObj.checkCycloneExecutionStatus(self.cyc_handle) == 0:
                break
            sleep(0.01)
        if self.cycloneControlSDKObj.getNumberOfErrors(self.cyc_handle) == 0:
            return 0  # Success

        error = self.cycloneControlSDKObj.getErrorCode(self.cyc_handle, 1)
        err_descr = self.cycloneControlSDKObj.getDescriptionOfErrorCode(self.cyc_handle, error)
        if self.cycloneControlSDKObj.getLastErrorAddr(self.cyc_handle) != 0:
            self.loggr.error(f'Error {hex(error)} "{err_descr}" during programming, Address={hex(self.cycloneControlSDKObj.getLastErrorAddr(self.cyc_handle))})')
        else:
            self.loggr.error(f'Error {hex(error)} "{err_descr}" during programming.')
        return 1  # Fail

    def cmdOpen(self, cyc_id_or_ip) -> int:
        id1 = cyc_id_or_ip
        if not cyc_id_or_ip or cyc_id_or_ip.lower() == "auto":
            id1 = "auto"
            cyc_id_or_ip = None
        self.loggr.info(f'Opening Cyclone "{id1}":')
        res = self.cyc_open(cyc_id_or_ip)
        if res != 0:
            self.loggr.error(f'Can not connect to Cyclone "{id1}".')
        else:
            self.loggr.info(f"Opened {self.cyc_descr()}. (Handle= {self.cyc_handle!s})")
        return res

    def cmdResetCyclone(self):
        self.loggr.info("Resetting {self.cyc_descr()} ... ")
        res = self.cyc_reset()
        if res != 0:
            self.loggr.error("Error during reset.")
        else:
            self.loggr.info("Done")

    def cmdListImages(self, force=False):
        self.loggr.info(f"List of images on {self.cyc_descr()}:")
        images = self.cyc_images_get(force)
        if images is None or len(images) == 0:
            self.loggr.info("   No Images")
        else:
            for i, image in enumerate(images, 1):
                self.loggr.info(f"   Image {i:02d} ({image.type}) : {image.name:>24s} CRC32=0x{image.crc32:08X}")

    def cmdClearAllImages(self) -> int:
        self.loggr.info("Erasing all internal images on {self.cyc_descr()} ... ")
        res = self.cyc_images_clear_all()
        if res:
            self.loggr.error("Failed.")
            return res
        self.loggr.info("Erased.")
        return 0

    def cmdAddImage(self, image_file_or_files: Union[str, list[str]]) -> int:
        if isinstance(image_file_or_files, str):
            image_file_or_files = [image_file_or_files]
        for image_file in image_file_or_files:
            self.loggr.info(f'Adding internal image "{image_file}" to {self.cyc_descr()} ... ')
            res = self.cyc_image_add(image_file)
            if res:
                self.loggr.error("Failed.")
                return res
            self.loggr.info("Added.")

        return 0

    def cmdReplaceAllImages(self, image_file_or_files: Union[str, list[str]]) -> int:
        res = self.cmdClearAllImages()
        if res:
            return res

        res = self.cmdAddImage(image_file_or_files)
        if res:
            return res

        return 0

    def cmdLaunchImage(self, slot: int) -> int:
        slot = int(slot)
        image_info = self.cyc_image_get_info(slot)
        self.loggr.info(f'Attempting to launch Image #{slot} "{image_info.name}" on {self.cyc_descr()} ...')
        res = self.cyc_image_start(slot)
        if res != 0:
            self.loggr.error("Failed to execute.")
            return res
        self.loggr.info("Started.")

        self.loggr.info(f'Waiting for completion of Image #{slot} "{image_info.name}" on {self.cyc_descr()} ...')
        res = self.cyc_image_wait_done()  # Logs error detail if any.
        if res == 0:  # Success
            self.loggr.info("Programming successful.")
        return res

    def cmdProgramSmart(self, image_file: str, force_upload=False) -> int:
        # Cyclone should be opened (e.g. by self.cmdOpen())
        uploaded = False
        file_info = self.cyc_image_file_info(image_file)
        slot = self.cyc_image_find(file_info.name, file_info.crc32, force_fetch=True)
        if force_upload or not slot:
            if slot:
                self.cyc_image_clear(slot)
            # Upload image onto Cyclone
            self.cyc_image_add(image_file)
            uploaded = True
            # It will get a new slot #
            # We know it will be the last one, but hey, we need to update the images list too.
            slot = self.cyc_image_find(file_info.name, file_info.crc32, force_fetch=True)
        else:
            self.loggr.info(f'Slot {slot} already has image "{file_info.name}" CRC32=0x{file_info.crc32:08X}, not uploading.')
        # Program with the slot
        if not slot:
            raise RuntimeError(f'Fail determining which image on {self.cyc_descr()} to use for programming{" after uploading" if uploaded else ""}')
        return self.cmdLaunchImage(slot)

    def sap_cfg_write(self, output_config_file: str):
        pass  # TODO: (when needed) Implement Cyclone.sap_cfg_write() to write a config file for Cyclone.sap_make()

    def sap_make(
        self,
        config_file: str,
        image_file: str,
        bootloader_file: str,
        output_sap_file: str,
        target="ARM",
        arch_file: Optional[str] = None,
        description: Optional[str] = None,
        logfile: Optional[str] = None,
    ) -> int:
        compilers = {
            "ARM": {
                "exe": "CSAPACMPZ",
            },  # ARM
            "MAC71XX": {
                "exe": "CSAPARMZ",
            },  # MAC71XX, MAC72XX
            "MAC72XX": {
                "exe": "CSAPARMZ",
            },  # MAC71XX, MAC72XX
            "HC_12_": {
                "exe": "CSAPBDM12Z",
            },  # HC(S)12(X)
            "ColdFireV1": {
                "exe": "CSAPBDMCFV1Z",
            },  # ColdFire V1
            "ColdFireV2+": {
                "exe": "CSAPBDMCFZ",
            },  # ColdFire V2, V3, V4
            "MPC5xx": {
                "exe": "CSAPBDMPPCZ",
            },  # MPC5xx/8xx
            "MPC8xx": {
                "exe": "CSAPBDMPPCZ",
            },  # MPC5xx/8xx
            "DSC": {
                "exe": "CSAPDSCZ",
            },  # DSC
            "HCS08": {
                "exe": "CSAPHCS08Z",
            },  # HCS08
            "HC08": {
                "exe": "CSAPMON08Z",
            },  # HC08
            "MPC55XX-57XX": {
                "exe": "CSAPPPCNEXUSZ",
            },  # MPC55XX-57XX
            "RS08": {
                "exe": "CSAPRS08Z",
            },  # RS08
            "S12Z": {
                "exe": "CSAPS12ZZ",
            },  # S12Z
            "STM8": {
                "exe": "CSAPWIZ01",
            },  # STM8
        }
        compiler = compilers.get(target)
        if not compiler:
            raise NotImplementedError(f'No SAP compiler known for "{target}" target.')
        exe = compiler["exe"]
        if get_os_name() == "Windows":
            exe = exe + ".exe"
        # TODO: (now) Implement finding the PEMicro software path (for compiler and arch_file) - use app_utils.
        cyclone_path = "C:\\PEMicro\\cyclone"
        exe_path = os.path.join(cyclone_path, "imageCreation", "ImageCreationSupportFiles")
        exe = os.path.abspath(os.path.join(exe_path, exe))
        # arch_path = os.path.join(cyclone_path, 'supportfiles', 'supportFiles_ARM')
        # TODO: (when needed) Implement finding path and choosing the right file based on target & arch.
        # if not arch_file: arch_file = os.path.join(arch_path, 'SiliconLabs', 'Bluetooth', 'SiliconLabs_EFR32BG24A010F1024_1024KB.arp')

        cmd = [
            exe,
            config_file,
            # "?", # DEBUG (remove it so the program will close after it is done)
            "hideapp",  # TODO: (when needed) Uncomment to hide the GUI.
            "/imagefile",
            output_sap_file,
        ]
        if logfile:
            cmd += ["/logfile", logfile]
        # Use "/PARAMn=s" for passing description, arch, image_file and bootloader_file into .cfg file
        if description:
            # cmd += ['imagecontent', description] # .cfg file ':DESCRIBEIMAGE' will overwrite this.
            # This /imagecontent command is broken, has no effect. Tried /imagecontent, imagecontent, /imagecontent=,
            cmd += [f"/PARAM1={description}"]
        if arch_file:
            cmd += [f"/PARAM2={arch_file}"]
        if image_file:
            cmd += [f"/PARAM3={image_file}"]
        if bootloader_file:
            cmd += [f"/PARAM4={bootloader_file}"]

        str_cmd = " ".join([f'"{c}"' for c in cmd])
        self.loggr.debug(f"SAP make command: {str_cmd}")
        output = subprocess.run(cmd, text=True, capture_output=True, check=False)
        return output.returncode

    def cmdSAPMake(
        self,
        config_file: str,
        image_file: str,
        bootloader_file: str,
        output_sap_file: str,
        target="ARM",
        arch_file: Optional[str] = None,
        description: Optional[str] = None,
        logfile: Optional[str] = None,
    ) -> int:
        self.loggr.info(f'Making SAP file "{output_sap_file}"...')
        res = self.sap_make(config_file, image_file, bootloader_file, output_sap_file, target, arch_file, description, logfile)
        self.loggr.info("Done.")
        return res


def cmd_install(options=None) -> int:
    cyclone = Cyclone()
    return cyclone.install_driver()


def cmd_uninstall(options=None) -> int:
    cyclone = Cyclone()
    return cyclone.uninstall()


def cmd_list_images(device, options=None) -> int:
    cyclone = Cyclone()
    cyclone.cmdOpen(device)
    return cyclone.cmdListImages()


def cmd_program_from_slot(device, slot, options=None) -> int:
    cyclone = Cyclone()
    cyclone.cmdOpen(device)
    return cyclone.cmdLaunchImage(slot)


def cmd_program(device, image_file, force_upload=False, options=None) -> int:
    cyclone = Cyclone()
    cyclone.cmdOpen(device)
    return cyclone.cmdProgramSmart(image_file, force_upload)


def cmd_sap_make(
    config_file: str,
    image_file: str,
    bootloader_file: str,
    output_sap_file: str,
    target: str = "ARM",
    arch_file: Optional[str] = None,
    description: Optional[str] = None,
    logfile: Optional[str] = None,
):
    cyclone = Cyclone()
    return cyclone.cmdSAPMake(config_file, image_file, bootloader_file, output_sap_file, target, arch_file, description, logfile)


def parse_args():
    parser = argparse.ArgumentParser(description="Cyclone programmer")

    # Common optional arguments
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    parser.add_argument("-d", "--device", type=str, help="Select Cyclone device port or IP or name")

    # Positional argument for the command
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Parser for 'install' command
    install_parser = subparsers.add_parser("install", help="Install drivers")
    # install_parser.add_argument('driver_type', type=str, help='Driver type')

    # Parser for 'images' command
    images_parser = subparsers.add_parser("images", help="List images on the Cyclone device")

    # Parser for 'program_slot' command
    program_slot_parser = subparsers.add_parser("program_slot", help="Program DUT from Cyclone stored image")
    program_slot_parser.add_argument("slot", type=int, help="Slot number")

    # Parser for 'program' command
    program_parser = subparsers.add_parser("program", help="Program DUT")
    program_parser.add_argument("image_file", type=str, help="SAP Image file path")
    program_parser.add_argument("-f", "--force", help="Force upload", action="store_true")

    # Parser for 'sap' command
    sap_parser = subparsers.add_parser("sap", help="Make SAP file")
    sap_parser.add_argument("output_sap_file", type=str, help="SAP output file")
    sap_parser.add_argument("config_file", type=str, help="SAP Config file path")
    sap_parser.add_argument("image_file", type=str, help="Firmware Image file path")
    sap_parser.add_argument("-b", "--bootloader_file", type=str, help="Bootloader Image file path")
    sap_parser.add_argument("-t", "--target", type=str, help="Target architecture")
    sap_parser.add_argument("-d", "--description", type=str, help="Description / name")
    sap_parser.add_argument("-a", "--arch", type=str, help="Architecture file path")
    sap_parser.add_argument("-l", "--log", type=str, help="Log file")

    # Parse the command line arguments
    args = parser.parse_args()
    return args, parser


def main():
    args, parser = parse_args()
    logger.debug(f"DEBUG {vars(args)}")

    try:
        if args.command == "install":
            options = AtDict()
            return cmd_install(options)

        # if args.command == 'uninstall':
        #     options = AtDict()
        #     return cmd_uninstall(options)

        if args.command == "images":
            options = AtDict()
            return cmd_list_images(args.device, options)

        if args.command == "program_slot":
            options = AtDict()
            return cmd_program_from_slot(args.device, args.slot, options)

        if args.command == "program":
            options = AtDict()
            return cmd_program(args.device, args.image_file, args.force, options)

        if args.command == "sap":
            options = AtDict()
            return cmd_sap_make(args.config_file, args.image_file, args.bootloader_file, args.output_sap_file, args.target, args.arch, args.description, args.log)

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
