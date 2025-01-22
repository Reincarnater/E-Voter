from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    
    return render_template("home.html", user=current_user)

@views.route('/vote', methods=['GET', 'POST'])
@login_required
def voting_system():
    
    return render_template("voting_system.html", user=current_user)

@views.route('/Teachers', methods=['GET', 'POST'])
@login_required
def Teacher_home():
    
    return render_template("Teacher_home.html", user=current_user)

@views.route('/add_candidate', methods=['GET', 'POST'])
@login_required
def Teacher_voting_system():
    
    return render_template("add_candidate.html", user=current_user)

@views.route('/display_candidate', methods=['GET', 'POST'])
@login_required
def displaying_Candidates():
    
    return render_template("display_candidate.html", user=current_user)

@views.route('/Verify')
def Verify():
    return render_template("Authenticator.html", user=current_user)
