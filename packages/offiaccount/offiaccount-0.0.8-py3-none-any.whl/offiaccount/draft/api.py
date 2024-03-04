from offiaccount.base import Tokenizer

class Draft(Tokenizer):
    def __init__(self, app):
        super().__init__(app)
        self.base_url = 'https://api.weixin.qq.com/cgi-bin/draft'

    def add(self, data):
        # https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html
        add_url = self.base_url + '/add?access_token=' + self.access_token
        r = self.client.post(url=add_url, json=data).json()
        return r

    def get(self, media_id):
        get_url = self.base_url + '/get?access_token=' + self.access_token
        pass

    def batchget(self, offset=0, count=20, no_content=0):
        # https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Get_draft_list.html
        batchget_url = self.base_url + '/batchget?access_token=' + self.access_token
        data = {
            'offset': offset,
            'count': count,
            'no_content': no_content,
        }
        return self.client.post(url=batchget_url, json=data).json()

    def count(self):
        count_url = self.base_url + '/count?access_token=' + self.access_token
        return self.client.get(count_url).json()
