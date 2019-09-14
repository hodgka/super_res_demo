# -*- coding: utf-8 -*-
from flask import redirect, render_template, request
from flask import g, Blueprint, flash, url_for, session

# from app.services.github import GitHub

blueprint = Blueprint('demos', __name__, url_prefix='/demos')

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
        
    return render_template('demos/requesting.html',
        items=fnames
    )

@blueprint.route('/pokegan')
def pokegan():
   
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
        
    return render_template('demos/requesting.html',
        items=fnames
    )