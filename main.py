import re
import yaml
import requests
from time import sleep
from ping3 import ping


def reboot(conf):
    session = requests.session()
    login = session.post(url="{}/ctlogin.cmd".format(conf['gateway']['url']), data={
        'username': conf['gateway']['username'],
        'password': conf['gateway']['password'],
    })
    if login.status_code == 200:
        resetrouter = session.get(
            url="{}/resetrouter.html".format(conf['gateway']['url']))
        if resetrouter.status_code == 200:
            SessionKey = re.findall(
                'sessionKey=(.*[0-9])', resetrouter.text)[0][1:]
            print('Session Key: {}.'.format(SessionKey))
        else:
            print("Get Session Key Failed.")
    else:
        print("Login Failed.")
    reboot = session.get(
        url="{}/rebootinfo.cgi?sessionKey={}".format(
            conf['gateway']['url'], SessionKey),
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        }
    )
    print('Reboot Status: {}.'.format(reboot.status_code))


def probe(conf):
    ErrorCount = 0
    for Location in conf['probe']['locations']:
        sleep(conf['probe']['time'])
        Result = ping(Location)
        if Result is False:
            ErrorCount += 1
        print("{}: {}.".format(Location, Result))
    if ErrorCount > 1:
        return False
    else:
        return True


def GetConf(ConfigFilePath):
    with open(ConfigFilePath, 'r', encoding='utf-8') as f:
        return yaml.load(f.read(), Loader=yaml.Loader)


if __name__ == '__main__':
    conf = GetConf("config/config.yaml")
    while True:
        if not probe(conf):
            reboot(conf)
