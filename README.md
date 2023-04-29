# PyHTools

![PyHTools Logo](https://i.ibb.co/CtwVV5T/Py-HTools-without-bg-cropped.png)

- Python Hacking Tools (PyHTools) (pht) is a collection of python written hacking tools consisting of network scanner, arp spoofer and detector, dns spoofer, code injector, packet sniffer, network jammer, email sender, downloader, wireless password harvester credential harvester, keylogger, download&execute, and reverse_backdoor along with website login bruteforce, scraper, web spider etc. PHT also includes malwares which are undetectable by the antiviruses.

- These tools are written in python3, refer installation to install/download tools and its dependencies.

- PyHTools comes with UI, but you can also use command line to use tools individually.

**`NOTE` : The UI hasn't been updated yet with new tools, Refer examples for more information**


## Disclaimer

The disclaimer advises users to use the open source project for ethical and legitimate purposes only and refrain from using it for any malicious activities. The creators and contributors of the project are not responsible for any illegal activities or damages that may arise from the misuse of the project. Users are solely responsible for their use of the project and should exercise caution and diligence when using it. Any unauthorized or malicious use of the project may result in legal action and other consequences.

[Read More](./DISCLAIMER.md)


## Join Our Discord Community

[![Join our Discord server!](https://invidget.switchblade.xyz/DJrnAg4nv2)](http://discord.gg/DJrnAg4nv2)

## How To Videos

- Gain access to remote shell over the Internet using HTTP Backdoor

  [![YT Thumbnail](https://img.youtube.com/vi/Wg-PiywAqyw/maxresdefault.jpg)](https://youtu.be/Wg-PiywAqyw)

## Installation

### Using pip

- Install main branch using pip

  ```bash
  python3 -m pip install git+https://github.com/dmdhrumilmistry/pyhtools.git
  ```

- Install Release from PyPi

  ```bash
  # without options
  python3 -m pip install pyhtools

  # for windows
  python3 -m pip install pyhtools[windows]

  # for linux
  python3 -m pip install pyhtools[linux]
  ```

### Manual Method

- Open terminal

- Install git package

  ```bash
  sudo apt install git python3 -y
  ```

- Install [Poetry](https://python-poetry.org/docs/master#installing-with-the-official-installer)

- clone the repository to your machine

  ```bash
  git clone https://github.com/dmdhrumilmistry/pyhtools.git
  ```

- Change directory

  ```bash
  cd pyhtools
  ```

- install with poetry

  ```bash
  # without options
  poetry install

  # for windows
  poetry install -E windows

  # for linux
  poetry install -E linux
  ```

## Start PyHTools

- run pyhtools.py

  ```bash
  python3 -m pyhtools
  ```

- to get all the commands use `help`

  ```bash
  pyhtools >> help
  ```

> If you're using Termux or windows, then use `pip` instead of `pip3`.  
> Few features are only for linux os, hence they might not work on windows and require admin priviliges.

### Open In Google Cloud Shell

- Temporary Session  
  [![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fdmdhrumilmistry%2Fpyhtools&ephemeral=true&show=terminal&cloudshell_print=./DISCLAIMER.md)
- Perisitent Session  
  [![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fdmdhrumilmistry%2Fpyhtools&ephemeral=false&show=terminal&cloudshell_print=./DISCLAIMER.md)

## Package Tools and Features

### Attackers

- `For Networks`

  - Network Scanner
  - Mac changer
  - ARP Spoofing
  - DNS spoofing
  - Downloads Replacer
  - Network Jammer
  - Pkt Sniffer
  - Code Injector

- `For Websites`

  - Login Guesser (Login Bruteforcer)
  - Web Spider
  - Web crawler (detects dirs | subdomains)
  - Web Vulnerablity Scanner

- `For Android`
  - mitm
    - Custom Certificate Pinner

### Detectors

- ARP Spoof Detector

### Malwares/Trojans/Payloads/Ransomwares/Worms

- Email Sender (reporter)
- Downloader
- Wireless Password Harvester
- Credential Harvester
- Keylogger (dlogs)
- Reverse Backdoors
  - TCP
  - HTTP
- Download and Execute
- Telegram Data Harvester
- DMSecRansomware
- Telegram Remote Code Executor
- DirCloner

> **NOTE:** Do not upload/send/report malwares to anti virus services such as `VirusTotal`. This will make program detectable

## Project Updates

- [View](https://github.com/users/dmdhrumilmistry/projects/2/views/1)

## How to Package a Evil Files

- [Example Script](./examples/EvilFiles)
- [View How to create a Trojan](./HowTo/Malwares/CreateTrojanPackage.md)
- [Generator Script](./examples/EvilFiles/generatorScript.py)

`Note`: On linux host machines, user needs to install `patchelf` package. Install using below command.

```bash
apt/dnf/yum install patchelf
```

> Above command needs root privileges.

## Have any Ideas 💡 or issue

- Create an issue
- Fork the repo, update script and create a Pull Request

## Contributing

Refer [CONTRIBUTIONS.md](/.github/CONTRIBUTING.md) for contributing to the project.

## LICENSE

PyHTools is distributed under `MIT` License. Refer [License](/LICENSE) for more information.

## Connect With Me

|                                                                                                                       |                                                       Platforms                                                       |                                                                                                                                        |
| :-------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------: |
|       [![GitHub](https://img.shields.io/badge/Github-dmdhrumilmistry-333)](https://github.com/dmdhrumilmistry)        | [![LinkedIn](https://img.shields.io/badge/LinkedIn-Dhrumil%20Mistry-4078c0)](https://linkedin.com/in/dmdhrumilmistry) |             [![Twitter](https://img.shields.io/badge/Twitter-dmdhrumilmistry-4078c0)](https://twitter.com/dmdhrumilmistry)             |
| [![Instagram](https://img.shields.io/badge/Instagram-dmdhrumilmistry-833ab4)](https://instagram.com/dmdhrumilmistry/) |     [![Blog](https://img.shields.io/badge/Blog-Dhrumil%20Mistry-bd2c00)](https://dmdhrumilmistry.github.io/blog)      | [![Youtube](https://img.shields.io/badge/YouTube-Dhrumil%20Mistry-critical)](https://www.youtube.com/channel/UChbjrRvbzgY3BIomUI55XDQ) |
