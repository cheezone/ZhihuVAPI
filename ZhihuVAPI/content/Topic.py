from .Ancestry import Container
from ..util.urls import urls
from ..util import zhihu
from .. import config


class Topic(Container):
    """知乎的话题对象"""

    def __init__(self, id):
        super().__init__(id, '话题', 'topic')
        if 2 == 1:  # 单纯为了编辑器能智能提示
            self.name = ""
            self.introduction = ""
            self.header_card = ""
            self.avatar_url = ""
            self.questions_count = ""
            self.is_following = False

    def init(self, id=''):
        if self.is_init == False:
            zhihu.info(f'Topic 对象 {id} ({self})初始化')
            responseJSON = zhihu.json(f'https://api.zhihu.com/topics/{id}/basic')
            self.load(responseJSON)
            responseJSON = zhihu.json(f'https://api.zhihu.com/topics/{id}/is_following')
            self.load(responseJSON)

    def load(self, JSON):
        super().load(JSON)
        for v in ['name', 'introduction', 'header_card', 'avatar_url', 'questions_count', 'is_following']:
            if JSON.get(v) != None:
                setattr(self, v, JSON.get(v))

    @zhihu.iter_factory('essence_feeds')
    def essence_feeds(x):
        '''返回话题 {name} 的精华'''
        from .Answer import Answer
        return Answer(x)

    @zhihu.iter_factory('unanswered_questions')
    def unanswered_questions(x):
        '''返回话题 {name} 等待答案的问题'''
        from .Question import Question
        return Question(x)

    @zhihu.iter_factory('activities')
    def activities(x):
        '''返回话题 {name} 的动态'''
        target = x['target']
        if x['type'] == 'answer':
            from .Answer import Answer
            return Answer(x)
        elif x['type'] == 'article':
            from .Article import Article
            return Article(x)
        elif x['type'] == 'pin':
            from .Pin import Pin
            return Pin(x)

    @zhihu.log_attr
    def index(self):
        '''返回话题 {name} 的索引'''
        responseJSON = zhihu.json(urls(self, 'index'))
        from .People import People
        editors = list(map(lambda x: People(x), responseJSON['topic_index_editors']))
        from .Topic import Topic
        from .Question import Question
        modules = []
        for v in responseJSON['topic_index_modules']:
            modules.append(
                {
                    'id': v['id'],
                    'items': list(map(lambda x: Question(x), v['items'])),
                    'title': v['title']
                })
        return {
            'editors': editors,
            'modules': modules
        }
