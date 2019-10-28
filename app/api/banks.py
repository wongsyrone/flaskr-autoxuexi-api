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
       abort(404, message=f'<Question id={id}> not EXIST!') 

class Question(Resource):
    def get(self, question_id):
        return exist_or_abort(question_id).to_json()

    def put(self, question_id):
        item = exist_or_abort(question_id)
        pass
        return item, 201



    def delete(self, question_id):
        item = exist_or_abort(question_id)
        db.session.delete(item)
        de.session.commit()
        return '', 204


parser = reqparse.RequestParser()
parser.add_argument('category', type=str)
parser.add_argument('content', type=str)

class QuestionList(Resource):
    def get(self):
        args = parser.parse_args()
        category = args['category']
        content = args['content']
        # category, content = request.json['category'], request.json['content']
        # print(f'category {category}\tcontent {content}')
        if category:
            category_list = category.split(' ')
            if content:
                content_like = re.sub(r'\s+|(%20)', '%', content)
                # print(content_like)
                res = Bank.query.filter(Bank.category.in_(category_list)).filter(Bank.content.like(content_like)).all()
            else:
                res = Bank.query.filter(Bank.category.in_(category_list)).all()
        else:
            res =  Bank.query.all()
        if 1 == len(res):
            return res[0].to_json()
        else:
            return [item.to_json() for item in res]

    def post(self):
        # print(request.json)
        question = Bank.from_json(request.json)
        content_like = re.sub(r'\s+|(%20)', '%', question.content)
        # print(str(question))
        if Bank.query.filter_by(category=question.category).filter(Bank.content.like(content_like)).first():
            print(f'该题已存在，无需添加')
            abort(400, message=f'已拒绝 <Bank {question.content}> 重复添加！')
        else:
            print(question)
            db.session.add(question)
            db.session.commit()
            return question.to_json(), 201

api.add_resource(QuestionList, '/questions')
api.add_resource(Question, '/questions/<int:question_id>')
        