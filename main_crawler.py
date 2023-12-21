# -*- coding: utf-8 -*-
# @Time    : 2023/11/29 20:46
# @Author  : 逝不等琴生
# @File    : main_crawler.py
# @PROJECT_NAME: DeveloperRelationCrawler
# @Software: PyCharm
import datetime
from itertools import islice

import requests
import time
from database_utils import Database, User
from concurrent.futures import ThreadPoolExecutor, as_completed

db_utils = Database()


# def run(user_id, tokens, log_file_path):
#     for token in tokens:
#         url = f'https://api.github.com/user/{user_id}'
#         headers = {
#             'Authorization': f'token {token}',
#             'Content-Type': 'application/json'
#         }
#         response = requests.get(url, headers=headers)
#         remain_cnt = response.headers.get('X-RateLimit-Remaining')
#         if response.status_code == 200:
#             user = response.json()
#             uid = user['id']
#             login = user['login']
#             name = user['name']
#             company = user['company']
#             blog = user['blog']
#             location = user['location']
#             email = user['email']
#             bio = user['bio']
#             public_repos = user['public_repos']
#             followers = user['followers']
#             following = user['following']
#             created_at = user['created_at']
#             updated_at = user['updated_at']
#             record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             db_utils.add_or_update(
#                 User(id=uid, login=login, name=name, company=company, blog=blog, location=location, email=email,
#                      bio=bio,
#                      public_repos=public_repos, followers=followers, following=following, created_at=created_at,
#                      updated_at=updated_at, record_time=record_time))
#             msg = f'user_id:{user_id} user_login:{login}  成功'
#             print(msg)
#             # log_to_file(log_file_path, msg)
#             return
#         elif response.status_code == 403 or response.status_code == 401:
#             # 如果超过限制，切换到下一个 token
#             # msg = f'Token {token} 已超过限制'
#             # print(msg)
#             # log_to_file(log_file_path, msg)
#             continue
#         else:
#             msg = f'请求失败，状态码: {response.status_code}'
#             print(msg)
#             # log_to_file(log_file_path, msg)
#             return None
#     # 如果所有 token 都超过限制，等待一小时后重试
#     print('所有 token 都已超过限制，等待 1 小时后重试...')
#     time.sleep(3000)  # 等待 1 小时
#     return run(user_id, tokens)  # 递归调用以重试


def run(user_id, tokens, idx, log_file_path):
    token = tokens[idx]
    url = f'https://api.github.com/user/{user_id}'
    headers = {
        'Authorization': f'token {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    remain_cnt = response.headers.get('X-RateLimit-Remaining')
    if response.status_code == 200:
        user = response.json()
        uid = user['id']
        login = user['login']
        name = user['name']
        company = user['company']
        blog = user['blog']
        location = user['location']
        email = user['email']
        bio = user['bio']
        public_repos = user['public_repos']
        followers = user['followers']
        following = user['following']
        created_at = user['created_at']
        updated_at = user['updated_at']
        record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db_utils.add_or_update(
            User(id=uid, login=login, name=name, company=company, blog=blog, location=location, email=email,
                 bio=bio,
                 public_repos=public_repos, followers=followers, following=following, created_at=created_at,
                 updated_at=updated_at, record_time=record_time))
        msg = f'user_id:{user_id} user_login:{login}  成功'
        print(msg)
        # log_to_file(log_file_path, msg)
        return
    elif response.status_code == 403 or response.status_code == 401:
        # 如果超过限制，切换到下一个 token
        # msg = f'Token {token} 已超过限制'
        # print(msg)
        # log_to_file(log_file_path, msg)
        return run(user_id, tokens, (idx + 1) % len(tokens), log_file_path)
    else:
        # msg = f'请求失败，状态码: {response.status_code}'
        # print(msg)
        # log_to_file(log_file_path, msg)
        return None
    # 如果所有 token 都超过限制，等待一小时后重试
    print('所有 token 都已超过限制，等待 1 小时后重试...')
    time.sleep(3000)  # 等待 1 小时
    return run(user_id, tokens)  # 递归调用以重试


def log_to_file(log_file, message):
    with open(log_file, 'a', encoding='utf-8') as file:
        file.write(message + '\n')

def batch(iterable, size):
    """将迭代器分成大小固定的批次"""
    it = iter(iterable)
    while True:
        chunk = tuple(islice(it, size))
        if not chunk:
            return
        yield chunk

if __name__ == '__main__':
    tokens = [
        'your_token'
    ]

    log_file_path = 'github_log.txt'

    thread_count = 20

    batch_size = 1000  # 可以根据需要调整批次大小

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for batch_of_user_ids in batch(range(1082300, 90000000), batch_size):
            futures = [executor.submit(run, user_id, tokens, user_id % len(tokens), log_file_path) for user_id in
                       batch_of_user_ids]
            for future in as_completed(futures):
                result = future.result()
