import json
from flask import Blueprint
from App.Data.Models.scorecards import Scorecard

jinja_filter = Blueprint('jinja_filter', __name__)


@jinja_filter.app_template_filter("to_console")
def to_console(text):
    print(str(text))
    return ""


@jinja_filter.app_template_filter('json_decode')
def json_decode(o):
    if isinstance(o, Scorecard):
        b = vars(o)
        b['_id'] = str(b['_id'])
        return json.dumps(b)
    else:
        for history in o:
            history[3] = str(history[3])
        return json.dumps(o)
