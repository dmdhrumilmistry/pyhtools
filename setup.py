from setuptools import setup, find_packages
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='PyHTools',
    version='1.0.1',
    author='Dhrumil Mistry',
    author_email='contact@dmdhrumilmistry.me',
    license='MIT License',
    description='Python Hacking Tools (PyHTools) (pht) is a collection of python written hacking tools consisting of network scanner, arp spoofer and detector, dns spoofer, code injector, packet sniffer, network jammer, email sender, downloader, wireless password harvester credential harvester, keylogger, download&execute, and reverse_backdoor along with website login bruteforce, scraper, web spider etc. PHT also includes malwares which are undetectable by the antiviruses.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'beautifulsoup4>=4.9.3',
        'colorama>=0.4.4',
        'frida-tools>=10.8.0',
        # 'netfilterqueue', #(for linux devices only): sudo pip3 install --upgrade -U git+https://github.com/kti/python-netfilterqueue,
        'kamene>=0.32',
        'nuitka',
        'pure-python-adb',
        'pyfiglet>=0.8.post1',
        'pynput>=1.7.3',
        'pytelegrambotapi>=4.0.1',
        'prettytable>=2.1.0',
        'psutil>=5.8.0',
        'pyinstaller',
        'requests>=2.25.1',
        'scapy>=2.4.5',
        # 'wmi', # for windows process management
        'zstandard',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)
