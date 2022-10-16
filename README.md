# PyHTools

![PyHTools Logo](https://i.ibb.co/CtwVV5T/Py-HTools-without-bg-cropped.png)

- Python Hacking Tools (PyHTools) (pht) is a collection of python written hacking tools consisting of network scanner, arp spoofer and detector, dns spoofer, code injector, packet sniffer, network jammer, email sender, downloader, wireless password harvester credential harvester, keylogger, download&execute, and reverse_backdoor along with website login bruteforce, scraper, web spider etc. PHT also includes malwares which are undetectable by the antiviruses.

- The tools provided are for educational purposes only. The developers are no way responsible for misuse of information and tools provided. All the information and tools are meant to help users to learn concepts. Use tools wisely!

- These tools are written in python3, refer installation to install/download tools and its dependencies.

- PyHTools comes with UI, but you can also use command line to use tools individually.

**`NOTE` : The UI hasn't been updated yet with new tools, Refer examples for more information**

## How To Videos

- Gain access to remote shell over the Internet using HTTP Backdoor

  [![YT Thumbnail](https://img.youtube.com/vi/Wg-PiywAqyw/maxresdefault.jpg)](https://youtu.be/Wg-PiywAqyw)

## Installation

### Using pip

- Install main branch using pip

  ```bash
  pip install git+https://github.com/dmdhrumilmistry/pyhtools.git
  ```

- Install Release from PyPi

  ```bash
  pip install pyhtools
  ```

### Manual Method

- Open terminal

- Install git package

  ```bash
  sudo apt install git python3 -y
  ```

- clone the repository to your machine

  ```bash
  git clone https://github.com/dmdhrumilmistry/pyhtools.git
  ```

- Change directory

  ```bash
  cd pyhtools
  ```

- install requirements

  ```bash
  python3 -m pip install -e .
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

> There may be chances that pyfiglet or kamene will not be installed through requirements.txt, you can install manually using `pip3 install pyfiglet kamene`.  
> If you're using Termux or windows, then use `pip` instead of `pip3`.  
> Few features are only for linux os, hence they might not work on windows and require admin priviliges.

### Open In Google Cloud Shell

- Temporary Session  
  [![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fdmdhrumilmistry%2Fpyhtools&ephemeral=true&show=terminal&cloudshell_print=./README.md)
  
- Perisitent Session  
  [![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fdmdhrumilmistry%2Fpyhtools&ephemeral=false&show=terminal&cloudshell_print=./README.md)

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
