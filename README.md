# PyHTools

<!-- Image Dim: 940x788 -->
![Image](https://github.com/dmdhrumilmistry/pyhtools/blob/main/.images/PyHTools.png?raw=true)

- Python Hacking Tools (PyHTools) (pht) is a collection of python written hacking tools consisting of network scanner, arp spoofer and detector, dns spoofer, code injector, packet sniffer, network jammer, email sender, downloader, wireless password harvester credential harvester, keylogger, download&execute, and reverse_backdoor along with website login bruteforce, scraper, web spider etc. PHT also includes malwares which are undetectable by the antiviruses.

![PHT Image](https://github.com/dmdhrumilmistry/pyhtools/blob/main/.images/Windows_CLI-main.png)

- The tools provided are for educational purposes only. The developers are no way responsible for misuse of information and tools provided. All the information and tools are meant to help newbies to learn new concepts. 

- These tools are written in python3, refer installation to install/download tools and its dependencies.

- PyHTools comes with UI, but you can also use command line to use tools individually.

**`NOTE` : The UI hasn't been updated yet with new tools, and evil files so using cli is preferred.**

### Installation

1. Open terminal

2. Install git package
   ```
   sudo apt install git python3 -y
   ```
   
3. clone the repository to your machine
   ```
   git clone https://github.com/dmdhrumilmistry/pyhtools.git
   ```
4. Change directory
   ```
   cd pyhtools
   ```
  
5. install requirements
   ```
   python3 -m pip install -r requirements.txt
   ```

### Start PHTools

1. change to pyhtools directory 
   ```
   cd pyhtools
   ```
2. run pyhtools.py
   ```
   python3 pyhtools.py
   ```
3. to get all the commands use `help`
   ```
   pyhtools >> help
   ```

> There may be chances that pyfiglet or kamene will not be installed through requirements.txt, you can install manually using `pip3 install pyfiglet kamene`.
> If you're using Termux or windows, then use `pip` instead of `pip3`. 

### Tools and Features 
   #### Attackers
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
      -  Login Guesser (Login Bruteforcer)
      -  Web Spider
      -  Web crawler (detects dirs | subdomains)
      -  Web Vulnerablity Scanner

   #### Detectors
   - ARP Spoof Detector
   
   #### Malwares/Trojans/Payloads/Ransomwares/Worms
   - Email Sender (reporter)
   - Downloader
   - Wireless Password Harvester
   - Credential Harvester
   - Keylogger (dlogs)
   - Reverse Backdoors
      - [TCP](https://github.com/dmdhrumilmistry/pyhtools/tree/main/malwares/reverse_backdoor/TCP)
      - [HTTP](https://github.com/dmdhrumilmistry/pyhtools/tree/main/malwares/reverse_backdoor/HTTP)
   - Download and Execute
   - [Telegram Data Harvester](https://github.com/dmdhrumilmistry/pyhtools/blob/main/malwares/telegram_data_harvester/HowToUse.md)
   - [DMSecRansomware](https://github.com/dmdhrumilmistry/pyhtools/blob/main/ransomwares/dmsec/HowToUse.md)
   - [Telegram Remote Code Executor](https://github.com/dmdhrumilmistry/pyhtools/tree/main/malwares/TelegramRemoteCodeExecutor)
   - DirCloner
  > Do not upload/send/report malwares to anti virus services such as `VirusTotal`. This will make program detectable
     

### Dependencies

   **`PHT`** requires following programs/scripts to run properly -
   - `Python`
      - `subprocess`
      - `scapy`
      - `kamene`
      - `pyfiglet`
      - `argparse`
      - `re`
      - `sys`
      - `os`
      - `shutil`
      - `pyinstaller`
   
   > **NOTE:** most of the modules are pre-installed, still to ensure the proper working of scripts, user should install the required modules using pip
      

### How to Package a Trojan
- [View How to create a Trojan](https://github.com/dmdhrumilmistry/hacking_tools/blob/master/malwares/Trojans/HowToCreateTrojanPackage.md)


### Have any Ideas 💡 or issue
- Create an issue
- Fork the repo, update script and create a Pull Request
       
       
 ### Connect with me on:
  
  <p align ="left">
    <a href = "https://github.com/dmdhrumilmistry" target="_blank"><img src = "https://img.shields.io/badge/Github-dmdhrumilmistry-333"></a>
    <a href = "https://www.instagram.com/dmdhrumilmistry/" target="_blank"><img src = "https://img.shields.io/badge/Instagram-dmdhrumilmistry-833ab4"></a>
    <a href = "https://twitter.com/dmdhrumilmistry" target="_blank"><img src = "https://img.shields.io/badge/Twitter-dmdhrumilmistry-4078c0"></a><br>
    <a href = "https://www.youtube.com/channel/UChbjrRvbzgY3BIomUI55XDQ" target="_blank"><img src = "https://img.shields.io/badge/YouTube-Dhrumil%20Mistry-critical"></a>
    <a href = "https://dhrumilmistrywrites.blogspot.com/ " target="_blank"><img src = "https://img.shields.io/badge/Blog-Dhrumil%20Mistry-bd2c00"></a>
    <a href = "https://www.linkedin.com/in/dhrumil-mistry-312966192/" target="_blank"><img src = "https://img.shields.io/badge/LinkedIn-Dhrumil%20Mistry-4078c0"></a><br>
   </p>
  
