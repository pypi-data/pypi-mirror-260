from offiaccount.base import Tokenizer

class Material(Tokenizer):
    def __init__(self, app):
        super().__init__(app)
        self.base_url = 'https://api.weixin.qq.com/cgi-bin'

    def uploadimg(self, filename):
        # https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Adding_Permanent_Assets.html
        add_url = self.base_url + '/material/add_material'
        params = {
            'type': 'image',
            'access_token': self.access_token,
        }
        files = {'media': open(filename, 'rb')}
        r = self.client.post(add_url, params=params, files=files).json()
        return r

    def get(self, media_id):
        get_url = self.base_url + '/get?access_token=' + self.access_token
        pass

    def batchget(self, type, offset=0, count=20):
        # https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Get_materials_list.html
        _type_allow_list = ['image', 'video', 'voice', 'news']
        if type not in _type_allow_list:
            raise RuntimeError('Material.batchget type must be set in', _type_allow_list)

        batchget_url = self.base_url + '/material/batchget_material?access_token=' + self.access_token
        data = {
            'type': type,
            'offset': offset,
            'count': count,
        }
        return self.client.post(url=batchget_url, json=data).json()

    def count(self):
        # https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Get_the_total_of_all_materials.html
        count_url = self.base_url + '/material/get_materialcount?access_token=' + self.access_token
        return self.client.get(count_url).json()
