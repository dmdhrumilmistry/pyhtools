from ppadb.client import Client
from ppadb.device import Device
from os.path import isfile, basename
from textwrap import dedent

import frida
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')


class PinCertificateExceptions:
    '''
    Pin Certificate Exception Class
    '''
    class ServerNotRunning(Exception):
        pass

    class NoDevicesFound(Exception):
        pass


class PinCertificate:
    def __init__(self, apk_path: str,  package_name: str, cert_path: str, frida_binary_path: str, frida_script_path: str, device_name: str, host: str = '127.0.0.1', port: int = 5037, apk_installed: bool = False,):
        # check data types
        assert type(apk_path) == str
        assert type(package_name) == str
        assert type(cert_path) == str
        assert type(device_name) == str
        assert type(frida_binary_path) == str
        assert type(host) == str
        assert type(port) == int
        assert type(apk_installed) == bool

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
        self.__apk_installed = apk_installed
        self.__package_name = package_name
        self.__cert_path = cert_path
        self.__frida_path = frida_binary_path

        # set initial values
        self.device = None

        # connect to adb server
        self._adb = Client(
            host=host,
            port=port
        )

    def get_device(self):
        self.devices()
        device: Device = self._adb.device(self.__device_name)
        return device

    def devices(self):
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
        devices = frida.enumerate_devices()
        if len(devices) == 0:
            raise PinCertificateExceptions.NoDevicesFound(
                "No Frida Devices Found")

        return devices

    def pin_certificate(self):
        logging.info("Starting Certificate Pinning Procedure..")

        # get device
        self.device: Device = self.get_device()
        logging.info(f'Connected to {self.__device_name} device')

        # install certificate
        if not self.__apk_installed:
            self.device.install(path=self.__apk_path, reinstall=True)
            logging.info(
                f'{basename(self.__apk_path)} APK installation completed')

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

        # start frida server
        logging.info("Starting Frida server")
        self.device.shell('/data/local/tmp/frida-server &')



if __name__ == '__main__':
    pinner = PinCertificate(
        apk_path=r'apk-path',
        package_name=r'com.app.package',
        cert_path=r'burp_pro_cert.der',
        frida_binary_path=r'frida-server-15.1.28-android-x86',
        frida_script_path=r'bypass-ssl-pinning.js',
        device_name='emulator-5554',
        host='127.0.0.1',
        port=5037,
    )

    pinner.pin_certificate()
