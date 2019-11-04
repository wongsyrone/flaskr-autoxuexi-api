from flask import render_template
from flask import Blueprint
from .. import db
from ..model import Bank


main_bp = Blueprint('main', __name__, url_prefix='/')

@main_bp.route('/')
def index():
    data = [x for x in Bank.query.all() if x.answer]
    return render_template('index.html', banks=data)