from ppadb.client import Client
from ppadb.device import Device
from subprocess import Popen, PIPE, STDOUT

import logging
import shutil
import threading
import os

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')


class DataHarvestorExceptions:
    '''
    Exceptions for DataHarvester class
    '''
    class ServerNotRunning(Exception):
        '''Server Not Running Exception'''
        pass

    class NoDevicesFound(Exception):
        '''No Devices Found Exception'''
        pass


class DataHarvester:
    '''Class to harvest data'''
    def __init__(self, dest_path: str, device_name: str, host: str = '127.0.0.1', port: int = 5037) -> None:
        assert type(dest_path) == str
        assert type(device_name) == str
        assert type(host) == str
        assert type(port) == int

        self.__device_name = device_name
        self.__dest_path = dest_path

        self._adb = Client(
            host=host,
            port=port
        )
        self.device: Device = self.get_device()
        logger.info(f'Using {self.__device_name}')

        # check paths, if present remove all files present
        if os.path.isdir(dest_path):
            logger.warning(
                'Destination Path is already present, complete directory data will be overwritten')
            shutil.rmtree(dest_path)

        # Create Paths
        logger.info('Creating Destination Path')
        os.makedirs(dest_path)

    def get_device(self):
        _ = self.get_adb_devices()
        device: Device = self._adb.device(self.__device_name)
        return device

    def get_adb_devices(self):
        try:
            devices: list[Device] = self._adb.devices()
            if len(devices) == 0:
                raise DataHarvestorExceptions.NoDevicesFound(
                    "No ADB Devices Attached")

            return devices
        except RuntimeError:
            raise DataHarvestorExceptions.ServerNotRunning(
                "ADB Server is not running, start using `adb start-server`")

    def __clone_dir(self, phone_src: str):
        # clone directory to host machine
        Popen(
            ['adb', 'pull', str(phone_src), str(self.__dest_path)],
            shell=True,
            stdout=PIPE,
            stderr=STDOUT,
        )

    def start(self):
        # get package paths
        logger.info('Getting packages list')
        package_paths = [os.path.join('/data/data/', package_path)
                         for package_path in str(self.device.shell('ls -a /data/data')).splitlines()]

        logger.info('Harvesting Data')
        for package_path in package_paths:
            threading.Thread(target=self.__clone_dir,
                             args=(package_path,)).start()

        logger.info('Data Harvesting Completed')