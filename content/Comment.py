from .Ancestry import Content
from ..util.urls import urls
from ..util import zhihu


class Comment(Content):
    """知乎的评论对象"""

    def __init__(self, id):
        super().__init__(id, '评论', 'comment')
        if 2 == 1:  # 单纯为了编辑器能智能提示
            self.content = ""
            self.featured = ""
            self.collapsed = ""
            self.is_author = ""
            self.is_delete = ""
            self.resource_type = ""
            self.reviewing = ""
            self.allow_like = ""
            self.allow_delete = ""
            self.allow_reply = ""
            self.allow_vote = ""
            self.can_recommend = ""
            self.can_collapse = ""
            self.replies_count = ""
            self.vote_count = ""
            self.dislike_count = ""
            self.reply_to_author = ""
            self.voting = ""
            self.disliked = ""
            self.censor_status = ""

    def __str__(self):
        return self.content

    def __repo__(self):
        return f'<{self.name}>:"{self.content}"'

    def init(self, id=''):
        responseJSON = zhihu.json(f'https://api.zhihu.com/comments/{self.id}')
        self.load(responseJSON)

    def load(self, JSON):
        super().load(JSON)
        if JSON.get('question'):
            from .Question import Question
            self.question = Question(JSON.get('question'))
        for v in ['content', 'featured', 'collapsed', 'is_author', 'is_delete', 'resource_type', 'reviewing', 'allow_like', 'allow_delete', 'allow_reply', 'allow_vote', 'can_recommend', 'can_collapse', 'replies_count', 'vote_count', 'dislike_count', 'censor_status']:
            if JSON.get(v) != None:
                setattr(self, v, JSON.get(v))
        from .People import People
        datas = {
            'is_favoriting': JSON.get('relationship', {}).get('is_favorited'),
            'is_nohelping': JSON.get('relationship', {}).get('is_nothelp'),
            'is_thanking': JSON.get('relationship', {}).get('is_thanked'),
            'is_voting': JSON.get('voting'),
            'is_disliked': JSON.get('disliked'),
            'reply_to_author': People(JSON.get('reply_to_author')) if JSON.get('reply_to_author') else None

        }
        for k, v in datas.items():
            if v != None:
                setattr(self, k, v)

    @zhihu.iter_factory('children')
    def children(x):
        """返回{name}的评论的回复 """
        return Comment(x)

    @zhihu.iter_factory('replies')
    def replies(x):
        """返回{name}的评论的回复 """
        return Comment(x)

    @zhihu.iter_factory('conversation')
    def conversation(x):
        """返回{name}的评论的对话 """
        return Comment(x)

    @zhihu.log_attr
    def recommend(self):
        '''推荐{name}的评论'''
        zhihu.jsonp(urls(self, 'recommend'))

    @zhihu.log_attr
    def unrecommend(self):
        '''取消推荐{name}的评论'''
        zhihu.jsond(urls(self, 'unrecommend'))

    @zhihu.log_attr
    def collapse(self):
        '''折叠{name}的评论'''
        zhihu.jsonp(urls(self, 'collapse'))

    @zhihu.log_attr
    def uncollapse(self):
        '''取消折叠{name}的评论'''
        zhihu.jsond(urls(self, 'uncollapse'))

    @zhihu.log_attr
    def delete(self):
        '''删除{name}的评论'''
        zhihu.jsond(urls(self, 'delete'))
