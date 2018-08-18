from .Ancestry import Container
from ..util.urls import urls
from ..util import zhihu
from .. import config


class Question(Container):
    """知乎的问题对象"""

    def __init__(self, id):
        super().__init__(id, '问题', 'question')
        if 2 == 1:  # 单纯为了编辑器能智能提示
            self.question_type = ''
            self.created = ''
            self.updated_time = ''
            self.is_editable = ''
            self.is_reportable = ''
            self.allow_delete = ''
            self.admin_closed_comment = ''
            self.has_publishing_draft = ''
            self.answer_count = ''
            self.comment_count = ''
            self.follower_count = ''
            self.collapsed_answer_count = ''
            self.comment_permission = ''
            self.detail = ''
            self.editable_detail = ''
            self.status = ''
            self.relationship = ''
            self.topics = ''
            self.author = ''
            self.can_comment = ''
            self.suggest_edit = ''
            self.thumbnail_info = ''
            self.review_info = ''
            self.mute_info = ''

    def init(self, id=''):
        zhihu.info(f'Question 对象 {id} ({self})初始化')
        responseJSON = zhihu.json(f'https://api.zhihu.com/questions/{id}')
        self.load(responseJSON)

    def load(self, JSON):
        super().load(JSON)
        from .Topic import Topic
        dataObj = {
            'content': JSON.get('detail'),
            'is_anonymous': JSON.get('relationship', {}).get('is_anonymous'),
            'is_author': JSON.get('relationship', {}).get('is_author'),
            'is_following': JSON.get('relationship', {}).get('is_following'),
            'is_close': JSON.get('status', {}).get('is_close'),
            'is_locked': JSON.get('status', {}).get('is_locked'),
            'is_suggest': JSON.get('status', {}).get('is_suggest'),
            'is_suggest_edit': JSON.get('suggest_edit', {}).get('status'),
            'is_evaluate': JSON.get('status', {}).get('is_evaluate'),
            'topics': list(map(lambda x: Topic(x), JSON.get('topics'))) if JSON.get('topics') else None
        }
        for k, v in dataObj.items():
            if v != None:
                setattr(self, k, v)
        for v in ['title', 'question_type', 'is_editable', 'is_reportable', 'allow_delete', 'admin_closed_comment', 'has_publishing_draft', 'answer_count', 'comment_count', 'follower_count', 'collapsed_answer_count', 'editable_detail', 'status', 'relationship', 'thumbnail_info', 'review_info', 'mute_info']:
            if JSON.get(v) != None:
                setattr(self, v, JSON.get(v))

    @zhihu.iter_factory('answers')
    def answers(x):
        """返回{name}的答案 """
        from .Answer import Answer
        return Answer(x)

    def common_edits(self):
        """返回{name}的公共编辑 """
        # if 'X-Xsrftoken' not in config.headers:
        #     return None
        responseText = zhihu.jsonp(f'https://www.zhihu.com/Question/{self.url_token}/logs', {'offset': '0'}).get('msg')[1]
        r = re.findall(r'''<div class="zm-item" id="([\w-]+)"\>\s*
<h2 class="zm-item-title">\s*
<a target="_blank" href="[\w\/]+">([^<]+)</a>\s*
</h2>
<div>
<a target="_blank" data-hovercard="[^"]+" href="/Question/([^"]+)">([^<]+)</a>
<span class="zg-gray-normal">([^<]+)</span>
</div>\s*''', responseText)
        r2 = re.findall(r'''<time datetime="[^"]+">([^<])+</time>''', responseText)
        while True:
            i = 0
            for v in r:
                yield {
                    'id': v[0],
                    'title': v[1],
                    'user_id': v[2],
                    'user_name': v[3],
                    'action': v[4],
                    'date': r2[i][0]
                }
                i += 1

    @zhihu.log_attr
    def anonymous(self):
        '''在问题 {name} 下匿名'''
        url = urls(self, 'anonymous')('true')
        responseJSON = zhihu.jsonp(url[0], url[1])
        return self

    @zhihu.log_attr
    def unanonymous(self):
        '''在问题 {name} 下取消匿名'''
        url = urls(self, 'anonymous')('false')
        responseJSON = zhihu.jsonp(url[0], url[1])
        return self

    @zhihu.log_attr
    def answer(self, content, is_copyable='true', comment_permission='all'):
        '''答案了问题 {name}'''
        responseJSON = zhihu.jsonp(urls(self, 'answer')(), {
            'question_id': self.id,
            'is_copyable': is_copyable,
            'can_reward': 'false',
            'comment_permission': comment_permission,
            'tagline': '',
            'content': content
        })
        return self

    @zhihu.log_attr
    def del_answer(self):
        '''删除了问题 {name} 下的答案'''
        responseJSON = zhihu.jsond(urls(self, 'answer')())
        return self
