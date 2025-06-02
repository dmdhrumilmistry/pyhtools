# PyHTools

![PyHTools Logo](https://i.ibb.co/CtwVV5T/Py-HTools-without-bg-cropped.png)

* Python Hacking Tools (PyHTools) (pht) is a collection of python written hacking tools consisting of network scanner, arp spoofer and detector, dns spoofer, code injector, packet sniffer, network jammer, email sender, downloader, wireless password harvester credential harvester, keylogger, download&execute, and reverse_backdoor along with website login bruteforce, scraper, web spider etc. PHT also includes malwares which are undetectable by the antiviruses.

* These tools are written in python3, refer installation to install/download tools and its dependencies.

* PyHTools comes with UI, but you can also use command line to use tools individually.

**`NOTE` : The UI hasn't been updated yet with new tools, Refer examples for more information**

## PyPi Downloads

|Period|Count|
|:----:|:---:|
|Weekly|[![Downloads](https://static.pepy.tech/personalized-badge/pyhtools?period=week&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/pyhtools)|
|Monthy|[![Downloads](https://static.pepy.tech/personalized-badge/pyhtools?period=month&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/pyhtools)|
|Total|[![Downloads](https://static.pepy.tech/personalized-badge/pyhtools?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/pyhtools)|

## Disclaimer

The disclaimer advises users to use the open source project for ethical and legitimate purposes only and refrain from using it for any malicious activities. The creators and contributors of the project are not responsible for any illegal activities or damages that may arise from the misuse of the project. Users are solely responsible for their use of the project and should exercise caution and diligence when using it. Any unauthorized or malicious use of the project may result in legal action and other consequences.

[Read More](./DISCLAIMER.md)

### Notice

To comply with PyPi's [Acceptable Use Policy](https://pypi.org/policy/acceptable-use-policy/)

All Evil files are moved to another repository: [pyhtools-evil-files](https://github.com/dmdhrumilmistry/pyhtools-evil-files)

Install Evil packages using below command:

```bash
python3 -m pip install git+https://github.com/dmdhrumilmistry/pyhtools-evil-files.git
```

Never use provided resources for malicious purpose.

## Join Our Discord Community

[![Join our Discord server!](https://invidget.switchblade.xyz/DJrnAg4nv2)](http://discord.gg/DJrnAg4nv2)

## How To Videos

* Gain access to remote shell over the Internet using HTTP Backdoor

  [![YT Thumbnail](https://img.youtube.com/vi/Wg-PiywAqyw/maxresdefault.jpg)](https://youtu.be/Wg-PiywAqyw)

## Installation

### Virtual Env Setup

It is advised to use virtual environment for any installation.

* Create virtual environment

  ```bash
  python -m venv .venv
  ```

* Activate venv

  ```bash
  source .venv/bin/activate
  ```

### Using pip

* Install main branch using pip

  ```bash
  # platform independent (but it doesn't support few features)
  python -m pip install git+https://github.com/dmdhrumilmistry/pyhtools.git@main#egg=pyhtools

  ## OS Specific Installations
  # for windows
  python -m pip install git+https://github.com/dmdhrumilmistry/pyhtools.git@main#egg=pyhtools[windows]

  # for linux
  python -m pip install git+https://github.com/dmdhrumilmistry/pyhtools.git@main#egg=pyhtools[linux]
  ```

### Manual Method

* Open terminal

* Install [git](https://git-scm.com/) and [python3](https://python.org) (>=3.10) package

* Install [Poetry](https://python-poetry.org/docs/#installation)

  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```

* clone the repository to your machine

  ```bash
  git clone https://github.com/dmdhrumilmistry/pyhtools.git
  ```

* Change directory

  ```bash
  cd pyhtools
  ```

* Install with poetry 

  ```bash
  # without options
  poetry install --sync

  # for windows
  poetry install --sync -E windows

  # for linux
  poetry install --sync -E linux
  ```

  > Run above commands in virtual env

## Start PyHTools

* run pyhtools.py

  ```bash
  python -m pyhtools
  ```

* to get all the commands use `help`

  ```bash
  pyhtools >> help
  ```

> If you're using Termux or windows, then use `pip` instead of `pip3`.  
> Few features are only for linux os, hence they might not work on windows and require admin priviliges.

### Open In Google Cloud Shell

* Temporary Session  
  [![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fdmdhrumilmistry%2Fpyhtools&ephemeral=true&show=terminal&cloudshell_print=./DISCLAIMER.md)
* Perisitent Session  
  [![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fdmdhrumilmistry%2Fpyhtools&ephemeral=false&show=terminal&cloudshell_print=./DISCLAIMER.md)

## Package Tools and Features

### Attackers

* `For Networks`

  * Network Scanner
  * Mac changer
  * ARP Spoofing
  * DNS spoofing
  * Downloads Replacer
  * Network Jammer
  * Pkt Sniffer
  * Code Injector

* `For Websites`

  * Login Guesser (Login Bruteforcer)
  * Web Spider
  * Web crawler (detects dirs | subdomains)
  * Web Vulnerablity Scanner

* `For Android`
  * mitm
    * Custom Certificate Pinner

### Detectors

* ARP Spoof Detector

### Malwares/Trojans/Payloads/Ransomwares/Worms

* Email Sender (reporter)
* Downloader
* Wireless Password Harvester
* Credential Harvester
* Keylogger (dlogs)
* Reverse Backdoors
  * TCP
  * HTTP
* Download and Execute
* Telegram Data Harvester
* DMSecRansomware
* Telegram Remote Code Executor
* DirCloner

> **NOTE:** Do not upload/send/report malwares to anti virus services such as `VirusTotal`. This will make program detectable

## Project Updates

* [View](https://github.com/users/dmdhrumilmistry/projects/2/views/1)

## How to Package a Evil Files

* [Example Script](./examples/EvilFiles)
* [View How to create a Trojan](./HowTo/Malwares/CreateTrojanPackage.md)
* [Generator Script](./examples/EvilFiles/generatorScript.py)

`Note`: On linux host machines, user needs to install `patchelf` package. Install using below command.

```bash
apt/dnf/yum install patchelf
```

> Above command needs root privileges.

## Have any Ideas 💡 or issue

* Create an issue
* Fork the repo, update script and create a Pull Request

## Contributing

Refer [CONTRIBUTIONS.md](/.github/CONTRIBUTING.md) for contributing to the project.

## LICENSE

PyHTools is distributed under `MIT` License. Refer [License](/LICENSE) for more information.

## Connect With Me

|                                                                                                                       |                                                       Platforms                                                       |                                                                                                                                        |
| :-------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------: |
|       [![GitHub](https://img.shields.io/badge/Github-dmdhrumilmistry-333)](https://github.com/dmdhrumilmistry)        | [![LinkedIn](https://img.shields.io/badge/LinkedIn-Dhrumil%20Mistry-4078c0)](https://linkedin.com/in/dmdhrumilmistry) |             [![Twitter](https://img.shields.io/badge/Twitter-dmdhrumilmistry-4078c0)](https://twitter.com/dmdhrumilmistry)             |
| [![Instagram](https://img.shields.io/badge/Instagram-dmdhrumilmistry-833ab4)](https://instagram.com/dmdhrumilmistry/) |     [![Blog](https://img.shields.io/badge/Blog-Dhrumil%20Mistry-bd2c00)](https://dmdhrumilmistry.github.io/blog)      | [![Youtube](https://img.shields.io/badge/YouTube-Dhrumil%20Mistry-critical)](https://www.youtube.com/channel/UChbjrRvbzgY3BIomUI55XDQ) |

<!-- GitAds-Verify: IHA3SE338WE6JLH9VFCBK1Q8VPJYI3IR -->
