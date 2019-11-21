#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: flaskr
@file: model.py
@author: kessil
@contact: https://github.com/kessil/flaskr/
@time: 2019-09-09(星期一) 17:16
@Copyright © 2019. All rights reserved.
'''
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class Bank(db.Model):
    __tabname__ = 'banks'
    ''' | id | category | content | options | answer | excludes | notes |
        id 序号
        category 类别
        ctontent 题干
        options 选项
        answer 答案
        excludes 排除项
        notes 说明
    '''
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(16), index=True)
    content = db.Column(db.Text, nullable=False)
    options = db.Column(db.Text)
    answer = db.Column(db.String(128))
    excludes = db.Column(db.String(16))
    notes = db.Column(db.Text)

    def __init__(self, **kwargs):
        super(Bank, self).__init__(**kwargs)

    def __repr__(self):
        return '<object Bank %d>'%self.id

    def __str__(self):
        # python 3.0+
        return "%s\n%s\n%s\n"%(self.content, self.options, self.answer)

        # python 3.8+
        # return f'{self.id=}\n{self.category=}\n{self.content=}\n{self.options=}\n{self.answer=}\n{self.excludes=}'

    def to_json(self):
        json_bank = {
            'id': self.id,
            'category': self.category,
            'content': self.content,
            'options': self.options.split('|'),
            'answer': self.answer,
            'excludes': self.excludes,
            'notes': self.notes
        }
        return json_bank

    @staticmethod
    def from_json(json_bank):
        # print(type(json_bank['options']), json_bank['options'])
        if not json_bank:
            return None
        if isinstance(json_bank.get('options'), list) and len(json_bank.get('options')) > 0:
            temp = '|'.join(json_bank.get('options'))
        else:
            temp = ""

        return Bank(            
            category = json_bank.get('category'),
            content = json_bank.get('content'),
            options =  temp,
            answer = json_bank.get('answer') or '',
            excludes = json_bank.get('excludes') or '',
            notes = json_bank.get('notes') or ''
        )
