# -*- coding: utf-8 -*-
from flask import redirect, render_template, request
from flask import g, Blueprint, flash, url_for, session

# from app.services.github import GitHub

blueprint = Blueprint('tutorial', __name__, url_prefix='/tutorial')

@blueprint.route('/super_res')
def super_res():
   
    fnames = ["https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(117).jpg",
    "https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(98).jpg",
    "https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(131).jpg",
    "https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(123).jpg",
    "https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(118).jpg",
    "https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(128).jpg",
    "https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(132).jpg",
    "https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(115).jpg",
    "https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(133).jpg",
    ]
        
    return render_template('tutorial/requesting.html',
        items=fnames
    )

@blueprint.route('/star', methods=['POST'])
def star():
    repo = request.form['full_name']

    if not 'access_token' in session:
        flash('Please sign in with your GitHub account.', 'danger')
        return redirect(url_for('github.fetching'))

    github = GitHub(access_token=session['access_token'])
    github.delete('/user/starred/' + repo)

    return redirect(url_for('tutorial.fetching'))
