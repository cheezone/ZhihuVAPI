from .Ancestry import Container
from ..util.urls import urls
from ..util import zhihu
from .. import config


class Collection(Container):
    """知乎的收藏夹对象"""

    def __init__(self, id):
        super().__init__(id, '收藏夹', 'Collection')
        if 2 == 1:
            self.creator = ""
            self.answer_count = ""
            self.comment_count = ""
            self.followers_count = ""
            self.is_public = ""

    def init(self, id=''):
        zhihu.info(f'Collection 对象 {id} ({self})初始化')
        responseJSON = zhihu.json(
            f'https://api.zhihu.com/collections/{id}?include=%24.intro')
        self.load(responseJSON)

    def load(self, JSON):
        super().load(JSON)
        from .People import People

        from .Topic import Topic
        dataObj = {
            'creator': People(JSON.get('creator')) if JSON.get('creator') else None,
            'topics': list(map(lambda x: Topic(x), JSON.get('topics'))) if JSON.get('topics') else None,
            'followers_count': JSON.get('follower_count')
        }
        for k, v in dataObj.items():
            if v != None:
                setattr(self, k, v)
        for v in ['creator', 'answer_count', 'comment_count', 'is_public']:
            if JSON.get(v) != None:
                setattr(self, v, JSON.get(v))

    @zhihu.iter_factory('contents')
    def contents(x):
        class Collection_content():
            """docstring for Collection_content"""

            def __init__(self, obj):
                from . import People
                self.collect_time = obj.get('collect_time')
                self.is_deleted = obj.get('is_deleted')
                if obj['type'] == 'article':
                    from . import Article
                    target = Article.Article(obj)
                elif obj['type'] == 'answer':
                    from . import Answer
                    target = Answer.Answer(obj)
                elif obj['type'] == 'pin':
                    from . import Pin
                    target = Pin.Pin(obj)
                self.content = target
                self.type = obj['type']
        return Collection_content(x)
