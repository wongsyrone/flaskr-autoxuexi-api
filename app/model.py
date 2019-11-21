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
import json
import re
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from pathlib import Path

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

def dump():
    path = Path('./data-output.json')
    data = Bank.query.all()
    res = [item.to_json() for item in data]
    with path.open(mode='w', encoding='utf-8') as fp:
        json.dump(res, fp, ensure_ascii=False)

    print('dump success')



def load():
    path = Path('./data-input.json')
    with path.open(mode='r', encoding='utf-8') as fp:
        data = json.load(fp)
    for item in data:
        question = Bank.from_json(item)
        content_like = re.sub(r'\s+|(%20)|(（出题单位：.*）)', '%', question.content)
        if Bank.query.filter_by(category=question.category).filter(Bank.content.like(content_like)).filter_by(options=question.options).first():
            print('该题已存在，无需添加')
        else:
            db.session.add(question)
            db.session.commit()
            print('添加记录：%s\t[%s]\t[%s]'%(question.content, question.options, question.answer))


