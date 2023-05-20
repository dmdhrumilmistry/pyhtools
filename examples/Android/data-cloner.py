from pyhtools.attackers.Android.forensics.data_harvester import DataHarvester

cloner = DataHarvester(
        dest_path=r'path', # path where cloned data will be stored on host machine
        device_name='emulator-5554', # device name using `adb devices`
        host='127.0.0.1', # adb server ip
        port=5037, # adb server port
    )

# start cloning
cloner.start()