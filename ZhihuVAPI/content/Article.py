from .Ancestry import Content
from ..util.urls import urls
from ..util import zhihu


class Article(Content):
    """知乎的文章对象"""

    def __init__(self, id):
        if 2 == 1:
            self.status = ""
            self.title = ""
            self.is_normal = ""
            self.reason = ""
            self.can_tip = ""
            self.excerpt_title = ""
            self.contributions = ""
            self.annotation_detail = ""
            self.voting = ""
            self.image_width = ""
            self.annotation_action = ""
            self.has_publishing_draft = ""
            self.linkbox = ""
            self.image_url = ""
            self.tipjarors_count = ""
        super().__init__(id, '文章', 'Article')

    def init(self, id=''):
        responseJSON = zhihu.json(f'https://api.zhihu.com/articles/{id}?include=contributions[*][column][articles_count,is_following]')
        self.load(responseJSON)

    def load(self, JSON):
        super().load(JSON)
        if JSON.get('contributions') and len(JSON.get('contributions')) > 0:
            # TODO
            from .Column import Column
            self.column = Column(JSON.get('contributions')[0]['column'])
        for v in ['status', 'title', 'is_normal', 'reason', 'can_tip', 'excerpt_title', 'contributions', 'annotation_detail', 'voting', 'image_width', 'annotation_action', 'has_publishing_draft', 'linkbox', 'image_url', 'tipjarors_count']:
            if JSON.get(v) != None:
                setattr(self, v, JSON.get(v))

        datas = {
            'is_favoriting': JSON.get('is_favorited'),
            'is_voting': JSON.get('voting')

        }
        for k, v in datas.items():
            if v != None:
                setattr(self, k, v)
