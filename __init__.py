

from .content import People
from .content import Question
from .content import Answer
from .content import Article
from .content import Pin
from .content import Comment
from .content import Column
from .content import Collection
from .util import *

__version__ = "1.0.4"
__all__ = []

People = People.People
Question = Question.Question
Answer = Answer.Answer
Article = Article.Article
Pin = Pin.Pin
Comment = Comment.Comment
Column = Column.Column
Collection = Collection.Collection

# 初始化自己
JSON = zhihu.json('https://api.zhihu.com/people/self')
config.hash = JSON['id']
self = People(JSON)
self.created_at = JSON['created_at']
self.email = JSON['email']

# if __name__ == '__main__':
#     print('作为主程序运行')
# else:
#     print('知乎V API 初始化')
