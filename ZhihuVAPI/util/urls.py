from . import zhihu
import re


def get_id_from_url(url, type_name):
    if type_name == '用户':
        search = re.search(r'[\da-zA-Z]{32}', url)
        if search:
            return ['id', search.group()]
        search = re.match(r'https:\/\/www\.zhihu\.com\/people\/([\da-zA-Z-_]+)', url)
        if search:
            return ['token', search.group(1)]
    elif type_name == '问题':
        search = re.match(r'https:\/\/www.zhihu.com\/question\/(\d{8,12})', url)
        if search:
            return search.group(1)
    elif type_name == '话题':
        search = re.match(r'https:\/\/www.zhihu.com\/topic\/(\d{8,12})', url)
        if search:
            return search.group(1)
    elif type_name == '答案':
        search = re.match(r'https:\/\/www\.zhihu\.com\/question\/\d{8,12}\/answer\/(\d{8,12})', url)
        if search:
            return search.group(1)
    elif type_name == '文章':
        search = re.match(r'https:\/\/(?:www|zhuanlan).zhihu.com\/p\/(\d{8,12})', url)
        if search:
            return search.group(1)
    elif type_name == '想法':
        search = re.match(r'https:\/\/(?:api|www).zhihu.com\/pin(?:s)?\/(\d{1,})', url)
        if search:
            return search.group(1)
    elif type_name == '专栏':
        search = re.match(r'https:\/\/zhuanlan.zhihu.com\/(.{1,})', url)
        if search:
            return search.group(1)
    elif type_name == '收藏夹':
        search = re.match(r'https:\/\/www.zhihu.com\/collection\/(\d{1,})', url)
        if search:
            return search.group(1)


def urls(content_obj, type_name: str):
    id = content_obj.id
    class_name = content_obj.type_name
    assert id, '知乎对象的 ID 必须存在'
    # assert zhihu.test(content_obj, 'id',  id),  f'这个 ID 未通过{content_obj.type_name} ID 的测试'
    import json
    urls_contents = {
        '用户': {
            # 'init': lambda:  f'https://api.zhihu.com/people/{id}',

            'followers': lambda offset=0: f'https://api.zhihu.com/people/{id}/followees?offset={offset}&limit=10',
            'follow': lambda: f'https://api.zhihu.com//api/v4/members/{content_obj.url_token}/followers',
            'collections': lambda offset=0: f'https://api.zhihu.com/people/{id}/collections_v2?offset={offset}',
            'articles': lambda offset=0, order_by='': f'https://api.zhihu.com/people/{id}/articles?offset={offset}&limit=2&order_by={order_by}',
            'pins': lambda offset=0, order_by='': f'https://api.zhihu.com/people/{id}/pins?offset={offset}&limit=2&order_by={order_by}',
            'lives': lambda offset=0, order_by='': f'https://api.zhihu.com/lives/people/{id}/statistics?order_by={order_by}&offset={offset}',
            'publications': lambda offset=0: f'https://api.zhihu.com/members/{content_obj.url_token}/publications?offset={offset}&per_page=3',
            'activities': lambda offset=0: f'https://api.zhihu.com/people/{id}/activities?offset={offset}&action_feed=true&limit=10',
            'marked_answers': lambda offset=0: f'https://api.zhihu.com/members/{content_obj.url_token}/marked-answers?offset={offset}&per_page=3',
            'answers': lambda offset=0, order_by='': f'https://api.zhihu.com/people/{id}/answers?order_by={order_by}&offset={offset}&per_page=3',
            'questions': lambda offset=0: f'https://api.zhihu.com/people/{id}/questions?offset={offset}&limit=10',
            'following_columns': lambda offset=0: f'https://api.zhihu.com/people/{id}/following_columns?offset={offset}&limit=10',
            'columns': lambda offset=0: f'https://api.zhihu.com/people/{id}/hscolumns?offset={offset}&limit=10',
            # 'following_topics': lambda offset=0: f'https://api.zhihu.com/people/{id}/following_topic?offset={offset}&limit=10',
            'following_topics': lambda offset=0: f'https://www.zhihu.com/api/v4/members/{content_obj.url_token}/following-topic-contributions?include=data%5B*%5D.topic.introduction&offset=20&limit=20',
            'following_questions': lambda offset=0: f'https://api.zhihu.com/people/{id}/following_questions?offset={offset}&limit=10',
            'send': lambda content: [f'https://api.zhihu.com/messages', {'receiver_id': id,
                                                                         'content': content,
                                                                         'content_type': '0'}],
            'sendImage': lambda image_url, height, width: [f'https://api.zhihu.com/messages', {'receiver_id': id,
                                                                                               'image': {"src": image_url, "data_rawheight": height, "data_rawwidth": width},
                                                                                               'content_type': '1'}],
            'block': lambda: [f'https://api.zhihu.com/settings/blocked_users', {'people_id': id}],
            'unblock': lambda: f'https://api.zhihu.com/settings/blocked_users/{id}',
            'msgs': lambda: [f'https://api.zhihu.com/messages?sender_id={id}', {'people_id': id}],
            'activity_block': lambda: [f'https://api.zhihu.com/people/self/activity_blocked_followees', {'url_token': content_obj.url_token}],
            'activity_unblock': lambda: f'https://api.zhihu.com/people/self/activity_blocked_followees/content_obj.url_token{content_obj.url_token}',


        },
        '答案': {
            'vote': lambda vote='up': [f'https://www.zhihu.com/api/v4/answers/{id}/voters', {"vote": {"type": 'up'}, 'unvote': {"type": 'neutral'},
                                                                                             'down': {"type": 'down'},
                                                                                             'undown': {"type": 'neutral'}}[vote]],
            'nohelp': lambda: f'https://api.zhihu.com/answers/{id}/nothelpers',
            'thank': lambda: f'https://www.zhihu.com/api/v4/answers/{id}/thankers',
            'comment': lambda content='': [f'https://api.zhihu.com/comments', {'content': content, 'resource_id': id, 'type': content_obj.eng_type_name}],
            'collect': lambda: f'https://api.zhihu.com/answers/{id}/collections_v2',
            'collections': lambda offset=0: f'https://api.zhihu.com/answers/{id}/collections_v2?offset={offset}',
            'block': lambda: [f'https://api.zhihu.com/topstory/uninterestv2', {'item_brief': json.dumps({"source": "TS", "type": "answer", "id": id})}],
            # 手机端没有,用的是电脑端的
            'voters': lambda offset=0: f'https://api.zhihu.com/answers/{id}/voters?offset={offset}',
            'comments': lambda offset=0, reverse_order='false': f'https://api.zhihu.com/answers/{id}/root_comments?reverse_order={reverse_order}&offset={offset}',
            'collapsed_comments': lambda offset=0: f' https://api.zhihu.com/answers/{id}/comments/collapsed?offset={offset}'
        },

        '问题': {  # order_by: ['created', '']
            'answers': lambda offset=0, order_by='': f'https://api.zhihu.com/v4/questions/{id}/answers?order_by={order_by}&offset={offset}&per_page=3',
            'answer': lambda: f'https://api.zhihu.com/answers',
            'followers': lambda offset=0: f'https://api.zhihu.com/questions/{id}/followers?offset={offset}&limit=10',
            'follow': lambda: f'https://www.zhihu.com/api/v4/questions/{id}/followers',
            'anonymous': lambda is_anonymous='true': [f'https://api.zhihu.com/questions/{id}/anonymous', {'is_anonymous': 'is_anonymous'}],
            'comments': lambda offset=0, reverse_order='false': f'https://api.zhihu.com/questions/{id}/anonymous?reverse_order={reverse_order}&offset={offset}',
            'comment': lambda content: [f'https://api.zhihu.com/comments', {'content': content,
                                                                            'resource_id': self.id,
                                                                            'type': self.eng_type_name
                                                                            }]
        },

        '话题': {

            'index': lambda: f'https://www.zhihu.com/api/v4/topics/{id}/topic_index',
            'essence_feeds': lambda offset=0: f'https://api.zhihu.com/topics/{id}/essence_feeds?offset={offset}&limit=10',
            'activities': lambda offset=0: f'https://api.zhihu.com/topics/{id}/feeds/top_activity?offset={offset}&limit=10',
            'unanswered_questions': lambda offset=0: f'https://api.zhihu.com/topics/{id}/unanswered_questions?offset={offset}&limit=10',
            'followers': lambda offset=0: f'ttps://www.zhihu.com/api/v4/topics/{id}/followers?offset=&limit=20&include=data%5B*%5D.gender%2Canswer_count%2Carticles_count%2Cfollower_count%2Cis_following%2Cis_followed',
            'follow': lambda: f'https://www.zhihu.com/topic/{id}/followers',


        },

        '文章': {
            'vote': lambda vote='vote': [f'https://www.zhihu.com/api/v4/articles/{id}/voters', {'vote': {'voting': 1}, 'unvote': {'voting': 0}}[vote]],
            'comment': lambda content='': [f'https://api.zhihu.com/comments', {'content': content, 'resource_id': id, 'type': content_obj.eng_type_name}],
            'collect': lambda: f'https://api.zhihu.com/articles/{id}/collections_v2?',
            'collections': lambda offset=0: f'https://api.zhihu.com/articles/{id}/collections_v2?offset={offset}',
            'voters': lambda offset=0: f'https://www.zhihu.com/api/v4/articles/{id}/likers?include=data%5B*%5D.answer_count%2Carticles_count%2Cfollower_count%2Cgender%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={offset}&limit=10',
            'comments': lambda offset=0, reverse_order='false': f'https://api.zhihu.com/articles/{id}/comments?reverse_order={reverse_order}&offset={offset}&status=open',
            'collapsed_comments': lambda offset=0: f' https://api.zhihu.com/articles/{id}/comments/collapsed?offset={offset}'
        },
        '想法': {
            'vote': lambda vote='vote': [f'https://api.zhihu.com/pins/{id}/reactions', {'vote': {"type": 'like'},
                                                                                        'unvote': {"type": 'neutral'}}[vote]],
            'comment': lambda content='': [f'https://api.zhihu.com/comments', {'content': content, 'resource_id': id, 'type': content_obj.eng_type_name}],
            'collect': lambda add=[], remove=[]: [f'https://api.zhihu.com/collections/contents/pin/{id}', {'add_collections': r"&".join(list(map(lambda x: x.name, add))),
                                                                                                           'remove_collections': r"&".join(list(map(lambda x: x.name, remove)))
                                                                                                           }],
            'collections': lambda offset=0: f'https://api.zhihu.com/collections/contents/pin/{id}?offset={offset}',

            'voters': lambda offset=0: f'https://api.zhihu.com/pins/{id}/actions?offset={offset}',
            'comments': lambda offset=0, reverse_order='false': f'https://api.zhihu.com/pins/{id}/root_comments?reverse_order={reverse_order}&offset={offset}',

        },
        '评论': {
            'vote': lambda vote='vote': [f'https://api.zhihu.com/comments/{id}/voters', {
                'vote': {"type": 'up'},
                'unvote': {"type": 'neutral'},
                'down': {"type": 'down'},
                'undown': {"type": 'neutral'}
            }[vote]],
            'delete': lambda: f'https://api.zhihu.com/comments/{id}',
            'recommend': lambda: f'https://api.zhihu.com/comments/{id}/recommend',
            'children': lambda offset=0: f'https://api.zhihu.com/comments/{id}/child_comments?order=ascending&offset={offset}&limit=10',
            'replies': lambda offset=0: f'https://api.zhihu.com/comments/{id}/replies?offset={offset}&limit=10',
            'conversation': lambda offset=0: f'https://api.zhihu.com/comments/{id}/conversation?offset={offset}&limit=10',
        },
        '专栏': {
            'articles': lambda member_hash='', offset=0: f'https://api.zhihu.com/columns/{id}/articles?member_hash={member_hash}&offset={offset}',
            'followers': lambda offset=0: f'https://api.zhihu.com/columns/{id}/followers?offset={offset}',
            'coauthors': lambda offset=0: f'https://api.zhihu.com/columns/{id}/coauthors?offset={offset}',
        },
        '收藏夹': {
            'follower': lambda offset=0: f'https://api.zhihu.com/collections/{id}/followees?offset={offset}&limit=10',
            'follow': lambda: f'https://www.zhihu.com/api/v4/collections/{id}/follower',
            'comments': lambda offset=0, reverse_order='false': f'https://api.zhihu.com/collections/{id}/anonymous?reverse_order={reverse_order}&offset={offset}',
            'comment': lambda content='': [f'https://api.zhihu.com/comments', {'content': content, 'resource_id': id, 'type': content_obj.eng_type_name}],
            'contents': lambda offset=0: f'https://api.zhihu.com/collections/{id}/contents?offset={offset}',
        }
    }

    assert class_name in urls_contents, f'类名 {class_name} 不存在'
    assert type_name in urls_contents[class_name], f'动作 {type_name}不存在'
    return urls_contents[class_name][type_name]


# class ClassName(object):
#     """docstring for ClassName"""

#     def __init__(self):
#         super(ClassName, self).__init__()
#         self.id = 15
#         self.type_name = '用户'


# print(urls(ClassName(), 'people', 'msgs')())
