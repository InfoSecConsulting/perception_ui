from flask import Blueprint
dashboards = Blueprint('dashboards', __name__)
from . import controllers
