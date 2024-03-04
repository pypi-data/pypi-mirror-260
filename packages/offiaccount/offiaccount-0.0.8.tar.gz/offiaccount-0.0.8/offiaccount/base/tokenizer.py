import time
from offiaccount.base import BaseAPI

class Tokenizer(BaseAPI):
    def __init__(self, app):
        super().__init__()

        self.app_path = app
        self.app = self.json_load(app)

        if 'appid' not in self.app or 'secret' not in self.app:
            raise RuntimeError('<appid> and <secret> must be set!')
        # https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Get_access_token.html
        self.__token_url = \
            'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'\
            .format(self.app['appid'], self.app['secret'])

        ip_url = 'http://httpbin.org/ip'
        ip_info = self.client.get(ip_url).json()
        self.app['ip'] = ip_info['origin']
        self.ts_key = 'timestamp'
        self.exp_key = 'expires_in'

        self.__update_access_token()

    @property
    def access_token(self):
        self.__update_access_token()
        return self.app['access_token']

    def __update_access_token(self):
        expired = False
        if self.ts_key not in self.app or self.exp_key not in self.app:
            expired = True
        elif self.app[self.ts_key] + self.app[self.exp_key] - 300 < time.time():
            expired = True

        if not expired:
            return
        self.app[self.ts_key] = time.time()

        r = self.client.get(self.__token_url).json()

        if 'access_token' not in r or 'expires_in' not in r:
            errmsg = f'Get access token failed! {r}'
            raise RuntimeError(errmsg)

        self.app.update(r)
        self.json_dump(self.app, self.app_path)
