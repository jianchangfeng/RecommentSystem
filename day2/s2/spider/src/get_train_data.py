#!/usr/bin/env python
# coding=utf-8
import sys
import json
import time
import sql_appbk


def publish_data():
    sql_com = 'SELECT video_info_iqiyi_category.category_id ,video_info_iqiyi.title ' \
              ' FROM video_info_iqiyi LEFT JOIN video_info_iqiyi_category ' \
              'ON video_info_iqiyi.category = video_info_iqiyi_category.category_name'
    # print sql_com
    results = sql_appbk.mysql_com(sql_com)
    # try:
    # 执行SQL语句
    # cursor.execute(sqlcom)
    # 获取所有记录列表
    # results = cursor.fetchall()
    # except:
    # print "Error: unable to select data"
    # 关闭数据库连接
    # db.close()
    return results


if __name__ == "__main__":

    category_info_list = [
        {"category_name": "欢乐精选", "category_id": "1"},
        {"category_name": "娱乐八卦", "category_id": "2"},
        {"category_name": "搞笑短片", "category_id": "3"},
        {"category_name": "影视剧吐槽", "category_id": "4"},
        {"category_name": "雷人囧事", "category_id": "5"},
        {"category_name": "爆笑节目", "category_id": "6"},
        {"category_name": "萌宠", "category_id": "7"},
        {"category_name": "童趣", "category_id": "8"},
        {"category_name": "奇闻趣事", "category_id": "9"},
        {"category_name": "恶搞配音", "category_id": "10"},
        {"category_name": "相声", "category_id": "11"},
        {"category_name": "小品", "category_id": "12"},
        {"category_name": "猎奇", "category_id": "13"},
        {"category_name": "啪啪奇", "category_id": "14"}
    ]

    re = publish_data()
    for item in re:
        print(str(item["category_id"]) + " " + item["title"].replace(" ", ""))  # 空格隔开,注意去掉tilte的空格
