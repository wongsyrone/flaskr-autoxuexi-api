from flask import render_template
from flask import Blueprint
from .. import db
from ..model import Bank


main_bp = Blueprint('main', __name__, url_prefix='/')

@main_bp.route('/')
def index():
    import re

    data = [x for x in Bank.query.all()] # if "挑战题" == x.category]
    for item in data:
        item.content = re.sub(r'(\s\s+)|((\(|（)\s*(\)|）))|(【\s*】)', "____", item.content)
        item.options = item.options.split('|')
        # print(item.options)

    return render_template('index.html', banks=data)