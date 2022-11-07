from config import conf
import re
import requests
from time import sleep
from ping3 import ping


def reboot():
    session = requests.session()
    login = session.post(url=conf.ONU_LOGIN_URL, data=conf.ONU_LOGIN_POST_DATA)
    if login.status_code == 200:
        resetrouter = session.get(url="http://192.168.125.1/resetrouter.html")
        if resetrouter.status_code == 200:
            find_session_key = re.findall(
                'sessionKey=(.*[0-9])', resetrouter.text)[0][1:]
            if find_session_key == '':
                print('Cannot Get Session Key.')
            else:
                print('sessionKey: ' + find_session_key)
        else:
            print("Get Session Key Failed.")
    else:
        print("Login Failed.")
    reboot = session.get(url=conf.ONU_REBOOT_URL.format(
        key=find_session_key), headers=conf.HEADERS)
    print('Reboot Status:' + str(reboot.status_code))


def probe(Locations):
    ErrorCount = 0
    for Location in Locations:
        sleep(10)
        Result = ping(Location)
        if Result is False:
            ErrorCount += 1
        print("{}: {}.".format(Location, Result))
    if ErrorCount > 1:
        return False
    else:
        return True


if __name__ == '__main__':
    while True:
        if not probe(Locations=conf.PING):
            reboot()
