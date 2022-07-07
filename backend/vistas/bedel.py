from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user

from ..models.entidad.EntidadUsuario import User

import os

from .. import mysql

template_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', 'frontend', 'templates','bedel'))

vistaBedel = Blueprint("vistaBedel", __name__,template_folder=template_dir)

#@bedel.route('/home')
