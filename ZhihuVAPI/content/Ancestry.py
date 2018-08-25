from ..util import zhihu
from ..util import urls
import re


class Ancestry():
    '''
    所有知乎对象的祖宗
    '''

    def __init__(self, id, type_name, eng_type_name):
        self.id = id
        self.is_init = False
        self.type_name = type_name
        self.eng_type_name = eng_type_name

        # 开始构造
        if zhihu.test(self, 'id', id):  # 传入 ID 的情况
            self.init(id=id)
        elif zhihu.test(self, 'token', id):  # 传入 URL-Token 的情况
            self.init(token=id)
        elif id.__class__.__name__ == 'dict':  # 传入字典的情况
            self.load(id)
        # 传入 URL 的情况
        elif id.__class__.__name__ == 'str' and re.match(r'https:\/\/', id):
            id = urls.get_id_from_url(id, self.type_name)
            zhihu.info(f'传入 URL 得到{id}  {self.type_name}')
            if self.type_name == '用户':  # 用户有两种方式:Token 和 ID
                self.init(**{id[0]: id[1]})
            else:
                self.init(id=id)

        elif id.__class__.__name__ == 'str':  # 开始搜索
            pass
            # TODO:开始搜索

    def __getattr__(self, v):

        if self.is_init == False:
            self.is_init = True
            self.init(self.id)
            try:
                return getattr(self, v)
            except Exception as e:
                raise e
        else:
            raise AttributeError(f'{self.type_name}不存在 {v} 属性')

    def load(self, JSON):
        self.id = JSON.get('id')
        self.url = JSON.get('url')

    def urls(self, type_name):
        return urls(self, type_name)


class Container(Ancestry):
    """知乎可关注的对象,问题、话题、收藏夹、专栏和人类"""

    def __init__(self, id, type_name, eng_type_name):
        super().__init__(id, type_name, eng_type_name)
        if 2 == 1:
            self.followers_count = ''
            self.fans_count = ''
            self.description = ''

    def load(self, JSON):
        super().load(JSON)
        if JSON.get('description') != None:
            self.description = JSON.get('description')
        if JSON.get('title'):
            self.title = JSON.get('title')
        if JSON.get('follower_count') != None or JSON.get('followers_count') != None:
            self.followers_count = JSON.get('follower_count') if JSON.get('follower_count') != None else JSON.get('followers_count')
            self.fans_count = JSON.get('follower_count') if JSON.get('follower_count') != None else JSON.get('followers_count')

    @zhihu.iter_factory('followers')
    def followers(x):
        '''获取{type_name} {name}粉丝列表'''
        from .People import People
        return People(x)

    @zhihu.iter_factory('followers')
    def fans(x):
        '''获取{type_name} {name}的粉丝列表'''
        from .People import People
        return People(x)

    @zhihu.log_attr
    def follow(self):
        '''关注了{type_name} {name}'''
        url = urls(self, 'follow')
        zhihu.jsonp(url)
        return self

    @zhihu.log_attr
    def unfollow(self):
        '''关注了{type_name} {name}'''
        url = urls(self, 'follow')
        zhihu.jsond(url[0])
        return self


class Content(Ancestry):
    """知乎可赞同可收藏内容的对象,想法,答案,文章"""
    # if 2 == 1:
    #     from .People import People

    def __init__(self, id, type_name, eng_type_name):
        super().__init__(id, type_name, eng_type_name)
        if 2 == 1:
            self.excerpt = ''
            self.admin_closed_comment = ''
            self.voteup_count = ''
            self.can_comment = ''
            self.comment_permission = ''
            self.comment_count = ''
            self.suggest_edit = ''
            self.updated_time = ''
            self.created_time = ''

    def load(self, JSON):
        super().load(JSON)

        if JSON.get('author'):
            from .People import People
            self.author = People(JSON.get('author'))

        for v in ['excerpt', 'admin_closed_comment', 'voteup_count', 'can_comment', 'comment_permission', 'comment_count', 'suggest_edit', 'updated_time', 'created_time']:
            if JSON.get(v) != None:
                setattr(self, v, JSON.get(v))
        if JSON.get('updated_time') != None:
            self.updated_time = JSON.get('updated')
        if JSON.get('created_time') != None:
            self.created_time = JSON.get('created')

    @zhihu.iter_factory('comments')
    def comments(x):
        '''获取{name}的评论列表'''
        from .Comment import Comment
        return Comment(x)

    @zhihu.iter_factory('collapsed_comments')
    def collapsed_comments(x):
        '''获取{name}被折叠的评论列表'''
        from .Comment import Comment
        return Comment(x)

    @zhihu.iter_factory('voters')
    def voters(x):
        '''获取{name}的点赞列表'''
        from .People import People
        return People(x)

    @zhihu.iter_factory('collections')
    def collections(x):
        '''获取{name}的收藏夹列表'''
        from .Collection import Collection
        return Collection(x)

    @zhihu.log_attr
    def commment(self, content):
        doc_output_content = content[1:6]if len(content) > 6 else content
        '''评论了{name}的{type_name}:doc_output_content'''
        url = urls(self, 'commment')(content)
        responseJSON = zhihu.jsonp(url[0], url[1])
        return self

    @zhihu.log_attr
    def vote(self):
        '''赞同了{name}的{type_name}'''
        url = urls(self, 'vote')('vote')
        responseJSON = zhihu.jsonp(url[0], url[1])

        return self

    @zhihu.log_attr
    def unvote(self):
        '''取消对{name}的{type_name}的赞同'''
        url = urls(self, 'vote')('unvote')
        responseJSON = zhihu.jsonp(url[0], url[1])

        return self

    @zhihu.log_attr
    def collect(self, add=[], remove=[]):
        '''收藏了{name}的{type_name}'''
        url = urls(self, 'collect')(add, remove)
        responseJSON = zhihu.jsonp(url[0], url[1])
        return self

    @zhihu.log_attr
    def uncollect(self, remove=[], add=[]):
        '''取消收藏了{name}的{type_name}'''
        url = urls(self, 'collect')(add, remove)
        responseJSON = zhihu.jsonp(url[0], url[1])
        return self
