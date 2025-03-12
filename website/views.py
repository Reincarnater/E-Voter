from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Candidate
from . import db
import os

views = Blueprint('views', __name__)

def group_candidates_by_position(candidates):
    grouped_candidates = {}
    for candidate in candidates:
        position = candidate.position
        if position not in grouped_candidates:
            grouped_candidates[position] = []
        grouped_candidates[position].append(candidate)
    return grouped_candidates

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    
    return render_template("home.html", user=current_user)


@views.route('/vote', methods=['GET', 'POST'])
@login_required
def Candidate_List():
    candidates = Candidate.query.all()
    grouped_candidates = group_candidates_by_position(candidates)
    return render_template('Candidate_List.html', grouped_candidates=grouped_candidates, user=current_user)

@views.route('/vote/<int:id>', methods=['POST'])
@login_required
def vote(id):
    candidate = Candidate.query.get_or_404(id)
    candidate.votes += 1
    db.session.commit()
    flash('Your vote has been counted!', category='success')
    return redirect(url_for('views.candidate_list'))

@views.route('/Teachers', methods=['GET', 'POST'])
@login_required
def Teacher_home():
    
    return render_template("Teacher_home.html", user=current_user)

@views.route('/add_candidate', methods=['GET', 'POST'])
@login_required
def add_candidate():
    if request.method == "POST":
        candidate_name = request.form['name']
        candidate_description = request.form['description']
        candidate_image = request.files['image']
        ##candidate_position = request.form['Position']
  
        filename = secure_filename(candidate_image.filename)
        candidate_image.save(os.path.join('website/static/images', filename))
        new_candidate = Candidate(name=candidate_name, description=candidate_description, image=filename) ##Position=candidate_position#
        db.session.add(new_candidate)
        db.session.commit()
    candidates = Candidate.query.all()
    return render_template("add_candidate.html", candidates=candidates, user=current_user)

@views.route('/update_candidates/<int:id>', methods=['GET', 'POST'])
@login_required
def update_candidates(id):
    candidates_to_update = Candidate.query.get_or_404(id)
    if request.method == "POST":
        Updated_name = request.form['name']
        Updated_description = request.form['description']
        Updated_image = request.files['image']

        Updated_filename = secure_filename(Updated_image.filename)
        candidates_to_update.image.save(os.path.join('website/static/images', Updated_filename))
        candidates_to_update = Candidate(name=Updated_name, description=Updated_description, image=Updated_filename)
        db.session.commit()
        return redirect('/add_candidate', candidates_to_update=candidates_to_update, user=current_user)
    
    return render_template("update_candidates.html", user=current_user)

@views.route('/display_candidate/<int:id>', methods=['GET', 'POST'])
@login_required
def display_candidate(id):
    candidate_to_display = Candidate.query.get_or_404(id)

    return render_template("display_candidate.html", candidate_to_display=candidate_to_display, user=current_user)

@views.route('/delete_candidates/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_candidates(id):
    candidate_to_delete = Candidate.query.get_or_404(id)
    try:
        db.session.delete(candidate_to_delete)
        db.session.commit()
        return redirect('/add_candidate')
    except:
        return 'There was a problem deleting the candidate'

