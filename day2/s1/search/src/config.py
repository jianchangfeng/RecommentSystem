# coding=utf-8
import os
import uuid

app_key = "LTAIKNBmekRBd3TX"  # 阿里云的key
app_secret = "JhoeP0Ey8VrrAlCMYZqjnNVlbbhRct"  # 阿里云的secret
base_url = 'http://opensearch-cn-beijing.aliyuncs.com'  # 不同的区域不同,按照区选择即可
index_name = 't_' + str(uuid.uuid4()).replace('-', '')[2:30]  # 默认不变
build_index_name = 'build_test_index_py27'  # 默认不变

try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'
