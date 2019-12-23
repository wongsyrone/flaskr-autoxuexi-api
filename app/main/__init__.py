from flask import render_template
from flask import Blueprint
from .. import db
from ..model import Bank


main_bp = Blueprint('main', __name__, url_prefix='/')

@main_bp.route('/')
def index():
    import re

    data = [x for x in Bank.query.all()] # if "单选题" == x.category]
    length_of_bank = len(data)
    for item in data:
        item.content = re.sub(r'(\s\s+)|((\(|（)\s*(\)|）))|(【\s*】)', "____", item.content)
        item.options = item.options.split('|')
        # print(item.options)

    return render_template('index.html', banks=data, length=length_of_bank)

@main_bp.route('/downloads')
def downloads():
    return "云主机本就花钱买的低配版，何况压力增大，干这种吃力不讨好的事真的很蠢，后期将考虑接受捐赠"

