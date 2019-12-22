#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: flaskr
@file: banks.py
@author: kessil
@contact: https://github.com/kessil/flaskr/
@time: 2019-09-09(星期一) 16:54
@Copyright © 2019. All rights reserved.
'''
import re
from flask import request
from flask_restful import Resource, abort, reqparse
from . import api
from .. import db
from ..model import Bank

def exist_or_abort(id):
    item = Bank.query.filter_by(id=id).first()
    if item:
        return item
    else:
       abort(404, message='<Question id=%d> not EXIST!'%id) 

class Question(Resource):
    def get(self, question_id):
        return exist_or_abort(question_id).to_json()

    def put(self, question_id):
        # args = parser.parse_args()
        item = exist_or_abort(question_id)
        # item.answer = args['answer']
        # item.excludes = args['excludes']
        # db.session.add(item)
        # db.session.commit()
        return item, 201



    def delete(self, question_id):
        item = exist_or_abort(question_id)
        db.session.delete(item)
        de.session.commit()
        return '', 204

class QuestionList(Resource):
    def get(self):
        question = Bank.from_json(request.json)
        if question and question.category:
            category_list = question.category.split(' ')
            if question and question.content:
                content_like = re.sub(r'(\s+)|(%20)|(（出题单位：.*）)', '%', question.content)
                content_like += "" if content_like[-1] == '%' else "%"
                # print(content_like)
                
                res = Bank.query.filter(Bank.category.in_(category_list)) \
                                .filter(Bank.content.like(content_like)) \
                                .filter(Bank.options==question.options).all()
            else:
                res = Bank.query.filter(Bank.category.in_(category_list)).all()
        else:
            res =  Bank.query.all()

        if 0 == len(res):
            abort(404, message='<Question %s> not EXIST!'%question.content)
        elif 1 == len(res):
            return res[0].to_json(), 200
        else:
            return [item.to_json() for item in res], 200

    def post(self):
        # print(request.json)
        question = Bank.from_json(request.json)
        content_like = re.sub(r'\s+|(%20)|(（出题单位：.*）)', '%', question.content)
        content_like += "" if content_like[-1] == '%' else "%"
        # print(str(question))
        bank =  Bank.query.filter_by(category=question.category) \
                    .filter(Bank.content.like(content_like)) \
                    .filter_by(options=question.options).first()

        if not question.answer:
            # 查询需求
            if bank and bank.answer:
                return bank.to_json(), 200
            else:
                return None, 404
        else:
            # 修改需求
            if bank and bank.answer:
                return None, 404
            elif not bank:
                db.session.add(question)
                db.sessino.commit()
                return None, 201
            else:
                bank.answer = question.answer
                bank.exclude += question.excludes
                db.session.commit()
                return None, 201

    def put(self):
        # print(request.json)
        question = Bank.from_json(request.json)
        content_like = re.sub(r'\s+|(%20)|(（出题单位：.*）)', '%', question.content)
        content_like += "" if content_like[-1] == '%' else "%"
        # print(str(question))
        bank = Bank.query.filter_by(category=question.category) \
                    .filter(Bank.content.like(content_like)) \
                    .filter_by(options=question.options).first()
        if bank:
            if bank.answer and bank.answer == question.answer:
                print('本题已保存正确答案, 跳过更新')
                return bank.to_json(), 404
            print('更新题库 [answer = %s] [excludes: %s += %s]' \
                %(question.answer, bank.excludes, question.excludes))
            # print("answer: %s = %s"%(bank.answer, question.answer))
            # print("excludes: %s += %s"%(bank.excludes, question.excludes))
            # print(f'{bank.excludes} += {question["excludes"]}')
            # prrnt(f'{bank.answer} = {question["answer"]}')
            # abort(400, message=f'已拒绝 <Bank {question.content}> 重复添加！')
            bank.answer = question.answer
            bank.excludes += question.excludes
            # db.session.add(bank)
            db.session.commit()
            return bank.to_json(), 200
        else:
            print('新增题库 %s [answer: %s]\t[excludes: %s]' \
                %(question.content, question.answer, question.excludes))
            db.session.add(question)
            db.session.commit()
            return question.to_json(), 201


api.add_resource(QuestionList, '/questions')
api.add_resource(Question, '/questions/<int:question_id>')
        
