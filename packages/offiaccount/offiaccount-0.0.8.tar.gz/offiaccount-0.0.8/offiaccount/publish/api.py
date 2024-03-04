from offiaccount.base import Tokenizer

class Publish(Tokenizer):
    def __init__(self, app):
        super().__init__(app)
        self.base_url = 'https://api.weixin.qq.com/cgi-bin/freepublish'

    def publish(self, media_id):
        # https://developers.weixin.qq.com/doc/offiaccount/Publish/Publish.html
        publish_url = self.base_url + '/submit?access_token=' + self.access_token
        data = {'media_id': media_id}
        return self._post(url=publish_url, data=data)

    def batchget(self, offset=0, count=20, no_content=0):
        # https://developers.weixin.qq.com/doc/offiaccount/Publish/Get_publication_records.html
        batchget_url = self.base_url + '/batchget?access_token=' + self.access_token
        data = {
            'offset': offset,
            'count': count,
            'no_content': no_content,
        }
        return self._post(url=batchget_url, data=data)