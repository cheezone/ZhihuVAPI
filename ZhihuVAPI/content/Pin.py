from .Ancestry import Content
from ..util.urls import urls
from ..util import zhihu


class Pin(Content):
    """知乎的想法对象"""

    def __init__(self, id):
        super().__init__(id, '想法', 'Pin')

        if 2 == 1:
            self.virtuals = ""
            self.repin_count = ""
            self.likers = ""
            self.tags = ""
            self.like_count = ""
            self.top_reactions = ""
            self.reaction_count = ""
            self.view_permission = ""
            self.is_deleted = ""
            self.source_pin_id = ""
            self.comments = ""
            self.content = ""
            self.state = ""
            self.tag_specials = ""
            self.excerpt_title = ""
            self.is_admin_close_repin = ""

    @property
    def source_pin(self):
        '''获取{name}的想法的源头'''
        if not self.source_pin_id:
            return None
        from .People import People
        return People(self.source_pin_id)

    def init(self, id=''):
        JSON = zhihu.json(f'https://api.zhihu.com/pins/{id or self.id}')
        self.load(JSON)

    def load(self, JSON):
        super().load(JSON)
        # if JSON.get('contributions') and len(JSON.get('contributions')) > 0:
        #     # TODO
        #     from .Column import Column
        #     self.column = Column(JSON.get('contributions')[0])
        for v in['virtuals', 'repin_count', 'likers', 'tags', 'like_count', 'top_reactions' 'state', 'tag_specials', 'excerpt_title', 'is_admin_close_repin', 'reaction_count', 'view_permission', 'is_deleted', 'source_pin_id']:
            if JSON.get(v) != None:
                setattr(self, v, JSON.get(v))
        datas = {
            'is_voting': JSON.get('virtuals', {}).get('is_liked'),
            'is_favoriting': JSON.get('virtuals', {}).get('is_favorited'),
            # 'comments': JSON.get('comments', []) , # 似乎没有卵用
            'voteup_count': JSON.get('top_reactions', {}).get('like')or 0 if self.is_init else JSON.get('top_reactions', {}).get('like'),
            'content': JSON.get('content', [''])[0],
            # 'img_urls': []if len(JSON.get('content', [''])) < 2 else list(map(lambda x: x['url'] if x['type'] != 'video' else, JSON['content'][1:])),
            # 'img_infos': []if len(JSON.get('content', [''])) < 2 else list(map(lambda x: x if x['type'] != 'video', JSON['content'][1:])),

        }
        for k, v in datas.items():
            if v != None:
                setattr(self, k, v)
