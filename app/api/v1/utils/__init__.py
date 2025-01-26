#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from app.api.v1.utils.doctor import *
from app.api.v1.utils.patient import *
from app.api.v1.utils.appointment import *
