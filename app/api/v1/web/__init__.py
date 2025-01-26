""" Blueprint for API """
from flask import Blueprint
import os
import importlib.util

web = Blueprint('web', __name__, url_prefix='/')
print('loading web routes')
from app.api.v1.web.login import login
from app.api.v1.web.logout import logout
from app.api.v1.web.registerDoctor import registerDoctor
from app.api.v1.web.registerPatient import registerPatient
from app.api.v1.web.register import registeration
from app.api.v1.web.doctorDashboard import doctorD
from app.api.v1.web.patientDashboard import patientD
from app.api.v1.web.index import indexD
from app.api.v1.web.appointments import *
print('web routes loaded')
