#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: flaskr
@file: __init__.py
@author: kessil
@contact: https://github.com/kessil/flaskr/
@time: 2019-09-09(星期一) 17:06
@Copyright © 2019. All rights reserved.
'''

from flask import Flask
from werkzeug.utils import import_string
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name):

    # 构造Flask实例
    app = Flask(__name__)

    # 载入配置文件
    app.config.from_object(config[config_name])
    

    # 支持跨域
    CORS(app, supports_credentials=True)

    # 手动初始化
    config[config_name].init_app(app)
    db.init_app(app)

    # 注册蓝图
    blueprints = ['app.api:api_bp', 'app.main:main_bp']
    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)

    # 返回实例
    return app

