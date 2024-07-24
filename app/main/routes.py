from flask import Flask, Blueprint, jsonify, redirect, render_template, request, url_for
import markdown


#####Global variablen
from ..globals import Globals


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template(Globals.html_dir_main+'index.html')

@main_bp.errorhandler(404)
def page_not_found(e):
    return render_template(Globals.html_dir_errors+'404.html'), 404

