# header信息
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
}

ONU_LOGIN_URL = 'http://192.168.125.1/ctlogin.cmd'
ONU_REBOOT_URL = 'http://192.168.125.1/rebootinfo.cgi?sessionKey={key}'

ONU_LOGIN_POST_DATA = {
    'username': 'useradmin',
    'password': '',
}

PING = [
    '223.5.5.5',
    'www.taobao.com',
    'jd.com',
]
