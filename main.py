import re
import yaml
import requests
from time import sleep
from ping3 import ping

import logging
import sys

log_fmt = '%(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_fmt, datefmt='%H:%M:%S', filemode='a')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
log_fmt = logging.Formatter(log_fmt)
ch.setFormatter(log_fmt)
logging.getLogger("logtest").addHandler(ch)

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
            logging.info('Session Key: {}.'.format(SessionKey))
        else:
            logging.info("Get Session Key Failed.")
    else:
        logging.info("Login Failed.")
    reboot = session.get(
        url="{}/rebootinfo.cgi?sessionKey={}".format(
            conf['gateway']['url'], SessionKey),
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        }
    )
    log = 'Reboot Status: {}.'.format(reboot.status_code)
    logging.info(log)


def probe(conf):
    ErrorCount = 0
    for Location in conf['probe']['locations']:
        sleep(conf['probe']['time'])
        Result = ping(Location)
        if Result is False:
            ErrorCount += 1
        log = "{}: {}.".format(Location, Result)
        logging.info(log)
    if ErrorCount > 1:
        return False
    else:
        return True


def GetConf(ConfigFilePath):
    with open(ConfigFilePath, 'r', encoding='utf-8') as f:
        return yaml.load(f.read(), Loader=yaml.Loader)


if __name__ == '__main__':
    conf = GetConf("config/config.yaml")
    logging.info("Start.")
    if not probe(conf):
        logging.info("Probe error.")
        reboot(conf)
    else:
        logging.info("Probe Success.")
