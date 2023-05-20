from ppadb.client import Client
from ppadb.device import Device
from os.path import isfile, basename
from os import system
from . import utils

import asyncio
import frida
import logging
import threading
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')


class PinCertificateExceptions:
    '''Pin Certificate Exception Class'''
    class ServerNotRunning(Exception):
        '''Server Not Running Exception Class'''
    class NoDevicesFound(Exception):
        '''No Devices Found Exception Class'''


class PinCertificate:
    def __init__(self, apk_path: str,  package_name: str, cert_path: str, frida_binary_path: str, frida_script_path: str, device_name: str, host: str = '127.0.0.1', port: int = 5037,):
        '''Pin Certificate class
        
        Args:
            apk_path (str): apk file path
            package_name (str): package name of apk file
            cert_path (str): file path of certificate to be installed
            frida_binary_path (str): file path of frida binary file
            frida_script_file (str): file path of cert installer script to be executed in frida after frida installation
            device_name (str): name of device for adb connection
            host (str): adb host ip
            port (int): adb host port

        Returns:
            None (None): None
        '''
        # check data types
        assert type(apk_path) == str
        assert type(package_name) == str
        assert type(cert_path) == str
        assert type(device_name) == str
        assert type(frida_binary_path) == str
        assert type(frida_script_path) == str
        assert type(host) == str
        assert type(port) == int

        # check if files are available at their paths
        if not isfile(apk_path):
            raise FileNotFoundError(f'{apk_path} APK file not found')

        if not isfile(cert_path):
            raise FileNotFoundError(f'{cert_path} Certificate file not found')

        if not isfile(frida_binary_path):
            raise FileNotFoundError(
                f'{frida_binary_path} Frida binary file not found')

        if not isfile(frida_script_path):
            raise FileNotFoundError(
                f'{frida_binary_path} Frida binary file not found')

        # assign values
        self.__device_name = device_name
        self.__apk_path = apk_path
        self.__package_name = package_name
        self.__cert_path = cert_path
        self.__frida_path = frida_binary_path
        self.__frida_script_path = frida_script_path

        # connect to adb server
        self._adb = Client(
            host=host,
            port=port
        )

        # set initial values
        self.device = self.get_device()

    def get_device(self):
        '''Get adb device
        
        Args:
            None

        Returns:
            ppadb.device.Device: returns specified adb device
        '''
        _ = self.get_adb_devices()
        device: Device = self._adb.device(self.__device_name)
        return device

    def get_adb_devices(self):
        '''returns lis of all adb devices
        
        Args:
            None

        Returns:
            list: list of connected adb devices
        '''
        try:
            devices: list[Device] = self._adb.devices()
            if len(devices) == 0:
                raise PinCertificateExceptions.NoDevicesFound(
                    "No ADB Devices Attached")

            return devices
        except RuntimeError:
            raise PinCertificateExceptions.ServerNotRunning(
                "ADB Server is not running, start using `adb start-server`")

    def get_frida_devices(self):
        '''Get list of devices running frida

        Args:
            None:

        Returns:
            list: list of adb connected devices running frida server
        '''
        devices = frida.enumerate_devices()
        if len(devices) == 0:
            raise PinCertificateExceptions.NoDevicesFound(
                "No Frida Devices Found")

        return devices

    def install_apk(self, force_install: bool = True):
        '''Installs apk on device
        
        Args:
            force_install (bool): if True then uninstalls apk if already installed then installs apk again

        Returns:
            bool: True if installed successfully else False
        '''
        if self.device.is_installed(self.__package_name) and force_install:
            self.device.uninstall(self.__package_name)

        self.device.install(self.__apk_path)

        if self.device.is_installed(self.__package_name):
            return True
        
        return False

    def start_frida(self):
        '''Starts Frida server on target device
        
        Args:
            None
        
        Returns:
            None
        '''
        asyncio.run(utils.run('adb shell /data/local/tmp/frida-server &'))

    def pin_certificate(self):
        '''Starts certificate pinning procedure to the apk

        Args:
            None

        Returns:
            None
        '''
        logging.info("Starting Certificate Pinning Procedure..")

        # get device
        self.device: Device = self.get_device()
        logging.info(f'Connected to {self.__device_name} device')

        # install apk
        logging.info('Installing package')
        if self.install_apk():
            logging.info(
                f'{basename(self.__apk_path)} APK installation completed successfully')
        else:
            logging.error(
                f'{basename(self.__apk_path)} APK installation failed!')

        # push certificate to the device
        self.device.push(
            src=self.__cert_path,
            dest=r'/data/local/tmp/cert-der.crt',
            mode=644
        )
        logging.info(
            f'{self.__cert_path} certificate pushed to /data/local/tmp/cert-der.crt')

        # push frida binary to the device
        self.device.push(
            src=self.__frida_path,
            dest=r'/data/local/tmp/frida-server',
            mode=555
        )
        logging.info(
            f'{self.__frida_path} frida binary pushed to /data/local/tmp/frida-server')

        # start frida server in different thread
        logging.info("Starting Frida server")
        frida_thread = threading.Thread(target=self.start_frida)
        frida_thread.start()
        # self.device.shell('su /data/local/tmp/frida-server &')

        # Start SSL pinning
        system(
            f'frida -U -l {self.__frida_script_path} --no-paus -f {self.__package_name}')
