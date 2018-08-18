from .Ancestry import Container
from ..util.urls import urls
from ..util import zhihu
from .. import config


class Column(Container):
    """知乎的专栏对象"""

    def __init__(self, id):
        super().__init__(id, '专栏', 'column')
        if 2 == 1:
            self.accept_submission = ""
            self.description = ""
            self.title = ""
            self.topics = ""
            self.intro = ""
            self.image_url = ""
            self.coauthors_count = ""
            self.articles_count = ""

    def init(self, id=''):
        zhihu.info(f'Column 对象 {id} ({self})初始化')
        responseJSON = zhihu.json(
            f'https://api.zhihu.com/columns/{id}?include=%24.intro')
        self.load(responseJSON)

    def load(self, JSON):
        super().load(JSON)

        from .Topic import Topic
        dataObj = {
            'topics': list(map(lambda x: Topic(x), JSON.get('topics'))) if JSON.get('topics') else None,
            'followers_count': JSON.get('followers')
        }
        for k, v in dataObj.items():
            if v != None:
                setattr(self, k, v)
        for v in ['accept_submission', 'description', 'title', 'intro', 'image_url', 'coauthors_count', 'articles_count']:
            if JSON.get(v) != None:
                setattr(self, v, JSON.get(v))

    @zhihu.iter_factory('articles')
    def articles(x):
        from .Article import Article
        return Article(x)

    @zhihu.iter_factory('coauthors')
    def coauthors(x):
        from .People import People
        return People(x)
