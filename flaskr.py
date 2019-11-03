#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: flaskr
@file: flaskr.py
@author: kessil
@contact: https://github.com/kessil/flaskr/
@time: 2019-09-09(星期一) 16:54
@Copyright © 2019. All rights reserved.
'''
import os
from app import create_app, db
from app.model import Bank
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Bank=Bank)


if __name__ == "__main__":
    app.run()