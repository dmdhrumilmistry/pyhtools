from pyhtools.attackers.Android.mitm.cert_pin import PinCertificate

pinner = PinCertificate(
    apk_path=r'/home/hacker/apks/com.application.name.apk', # application package path
    package_name=r'com.application.name', # package name of target application
    cert_path=r'burp_cert.der', # burpsuite/custom CA certificate
    frida_binary_path=r'frida-server-15.1.28-android-x86', # download and update path, (https://github.com/frida/frida/releases)
    frida_script_path=r'script.js', # download from frida examples (https://codeshare.frida.re/@pcipolloni/universal-android-ssl-pinning-bypass-with-frida/)
    device_name='emulator-5554', # device name from adb
    host='127.0.0.1', # adb host
    port=5037, # adb port
)

pinner.pin_certificate()

# once certificate is pinned you can exit python script using ctrl+c then return key