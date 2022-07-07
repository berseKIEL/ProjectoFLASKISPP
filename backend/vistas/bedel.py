from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user

from ..models.entidad.EntidadUsuario import User

from .. import mysql

vistaBedel = Blueprint("vistaBedel", __name__)

#@bedel.route('/home')
