from .Ancestry import Container
from ..util.urls import urls
from ..util import zhihu
from .. import config


class People(Container):
    """知乎的用户对象"""

    def __init__(self, id):
        super().__init__(id, '用户', 'people')

        if 2 == 1:  # 单纯为了编辑器能智能提示
            self.is_followed = ""
            self.following_count = ""
            self.is_hanged = ""
            self.shared_count = ""
            self.user_type = ""
            self.is_unicom_free = ""
            self.pins_count = ""
            self.is_following = ""
            self.marked_answers_text = ""
            self.is_activity_blocked = ""
            self.infinity = ""
            self.is_force_renamed = ""
            self.favorite_count = ""
            self.live_count = ""
            self.is_blocking = ""
            self.lite_favorite_content_count = ""
            self.is_baned = ""
            self.headline = ""
            self.is_enable_signalment = ""
            self.is_enable_watermark = ""
            self.reactions_count = ""
            self.following_favlists_count = ""
            self.is_bind_sina = ""
            self.favorited_count = ""
            self.open_ebook_feature = ""
            self.badge = ""
            self.following_topic_count = ""
            self.description = ""
            self.business = ""
            self.columns_count = ""
            self.following_columns_count = ""
            self.answer_count = ""
            self.cover_url = ""
            self.url_token = ""
            self.question_count = ""
            self.articles_count = ""
            self.name = ""
            self.gender = ""
            self.is_subscribing = ""
            self.is_locked = ""
            self.avatar_url = ""
            self.following_question_count = ""
            self.thanked_count = ""
            self.hosted_live_count = ""
            self.participated_live_count = ""
            self.independent_articles_count = ""
            self.voteup_count = ""

    def init(self, id='', token=''):
        id = id or token
        self.following = {'people_count': 0,
                          'topic_count': 0,
                          'favlist_count': 0,
                          'column_count': 0,
                          'question_count': 0}
        zhihu.info(f'People 对象 {id} ({self})初始化')
        responseJSON = zhihu.json(f'https://api.zhihu.com/people/{id or token}')
        self.load(responseJSON)

    def is_waterman(self):
        '''没有收藏夹(正常人至少会有一个),没有联通免流,没有想法,没有答案(一个也没有?),不关注任何一个专栏那就是三无小号了'''
        if self.favorite_count == 0 and self.is_unicom_free == False and self.pins_count == 0 and self.answer_count == 0 and self.following['column_count'] == 0:
            return True
        else:
            return False

    def load(self, JSON):
        super().load(JSON)
        for v in ['is_followed', 'voteup_count', 'is_hanged', 'shared_count', 'user_type', 'is_unicom_free', 'pins_count', 'is_following', 'marked_answers_text', 'is_activity_blocked', 'infinity', 'is_force_renamed', 'favorite_count', 'live_count', 'is_blocking', 'lite_favorite_content_count', 'is_baned', 'headline', 'is_enable_signalment', 'is_enable_watermark', 'reactions_count', 'is_bind_sina', 'favorited_count', 'open_ebook_feature', 'badge', 'description', 'business', 'columns_count', 'answer_count', 'cover_url', 'url_token', 'question_count', 'articles_count', 'name', 'gender', 'is_subscribing', 'is_locked', 'avatar_url', 'thanked_count', 'hosted_live_count', 'participated_live_count', 'independent_articles_count']:
            if JSON.get(v) != None:
                setattr(self, v, JSON.get(v))

        if 'gender' in JSON:
            self.sex = {-1: "他", 0: "她", 1: "他"}[(JSON.get('gender'))]

        dataObj = {
            'people_count': JSON.get('following_count'),
            'topic_count': JSON.get('following_topic_count',),
            'favlist_count': JSON.get('following_favlists_count',),
            'column_count': JSON.get('following_columns_count',),
            'question_count': JSON.get('following_question_count',),

        }
        for k, v in dataObj.items():
            if v != None:
                self.following[k] = v

    @zhihu.iter_factory('activities')
    def activities(x):
        """返回{name}的动态 """
        return x

    @zhihu.iter_factory('msgs')
    def msgs(x):
        """返回与{name}的私信 """
        return x

    @zhihu.iter_factory('marked_answers')
    def marked_answers(x):
        """返回{name}的被推荐的答案 """
        from .Answer import Answer
        return Answer(x)

    @zhihu.iter_factory('answers')
    def answers(x):
        """返回{name}的答案 """
        from .Answer import Answer
        return Answer(x)

    @zhihu.iter_factory('articles')
    def articles(x):
        """返回{name}的文章 """
        from .Article import Article
        return Article(x)

    # @zhihu.iter_factory('lives')
    # def lives(x):
    #     """返回{name}的Live """
    #     from .Live import Live
    #     return Live(x)

    @zhihu.iter_factory('pins')
    def pins(x):
        """返回{name}的想法 """
        from .Pin import Pin
        return Pin(x)

    @zhihu.iter_factory('collections')
    def collections(x):
        """返回{name}的收藏夹 """
        from .Collection import Collection
        return Collection(x)

    @zhihu.iter_factory('columns')
    def columns(x):
        """返回{name}的专栏 """
        from .Column import Column
        return Column(x)

    # @zhihu.iter_factory('publications')
    # def publications(x):
    #     """返回{name}的著作 """
    #     from .Publication import Publication
    #     return Publication(x)

    @zhihu.iter_factory('following_columns')
    def following_columns(x):
        """返回{name}关注的专栏 """
        from .Column import Column
        return Column(x)

    @zhihu.iter_factory('following_collections')
    def following_collections(x):
        """返回{name}关注的收藏夹 """
        from .Collection import Collection
        return Collection(x)

    @zhihu.iter_factory('following_topics')
    def following_topics(x):
        """返回{name}关注的话题 """
        from .Topic import Topic
        topic = Topic(x['topic'])
        topic.contributions_count = x['contributions_count']
        return topic

    @zhihu.log_attr
    def common_edits(self):
        """返回{name}的公共编辑 """
        # if 'X-Xsrftoken' not in config.headers:
        #     return None
        responseText = zhihu.jsonp(f'https://www.zhihu.com/people/{self.url_token}/logs', {'offset': '0'}).get('msg')[1]
        r = re.findall(r'''<div class="zm-item" id="([\w-]+)"\>\s*
<h2 class="zm-item-title">\s*
<a target="_blank" href="[\w\/]+">([^<]+)</a>\s*
</h2>
<div>
<a target="_blank" data-hovercard="[^"]+" href="/people/([^"]+)">([^<]+)</a>
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
    def send(self, content):
        """给{name}发送私信 """
        url = urls(self, 'send')('content')
        responseJSON = zhihu.jsonp(url[0], url[1])
        return self

    @zhihu.log_attr
    def sendImage(self, image_url, height=250, width=250):
        """给{name}发送私信图片 """
        url = urls(self, 'sendImage')(image_url, height, width)
        responseJSON = zhihu.jsonp(url[0], url[1])
        return self

    @zhihu.log_attr
    def block(self):
        """屏蔽{name} """
        url = urls(self, 'block')()
        responseJSON = zhihu.jsonp(url[0], url[1])
        return self

    @zhihu.log_attr
    def unblock(self):
        """取消屏蔽{name} """
        url = urls(self, 'unblock')()
        responseJSON = zhihu.jsond(url)
        return self

    @zhihu.log_attr
    def activity_block(self):
        """屏蔽{name}的动态"""
        url = urls(self, 'activity_block')()
        responseJSON = zhihu.jsonp(url[0], url[1])
        return self

    @zhihu.log_attr
    def activity_unblock(self):
        """取消屏蔽{name}的动态"""
        url = urls(self, 'activity_unblock')()
        responseJSON = zhihu.jsond(url)
        return self
