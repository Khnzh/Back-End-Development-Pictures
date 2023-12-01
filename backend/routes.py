from . import app

import os

import json

from flask import jsonify, request, make_response, abort, url_for  # noqa; F401





SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

json_url = os.path.join(SITE_ROOT, "data", "pictures.json")

data: list = json.load(open(json_url))

songs={}





######################################################################

# RETURN HEALTH OF THE APP

######################################################################







@app.route("/health")

def health():

    return jsonify(dict(status="OK")), 200





######################################################################

# COUNT THE NUMBER OF PICTURES

######################################################################







@app.route("/count")

def count():

    """return length of data"""

    if data:

        return jsonify(length=len(data)), 200





    return {"message": "Internal server error"}, 500







######################################################################

# GET ALL PICTURES

######################################################################

@app.route("/picture", methods=["GET"])

def get_pictures():

    if data:

        for i, x in enumerate(data):

            songs[f'song{i}']=x

        return songs, 200

   

    return {"message": "Internal server error"}, 500





######################################################################

# GET A PICTURE

######################################################################







@app.route("/picture/<int:id>", methods=["GET"])

def get_picture_by_id(id):

    if data:

       for picture in data:

        if picture["id"] == id:

            return picture, 200

    return {"message": "picture not found"}, 404







######################################################################

# CREATE A PICTURE

######################################################################

@app.route("/picture", methods=["POST"])

def create_picture():

    picture = request.json

    for x in data:

        if int(x['id']) == int(picture['id']):

            return {'Message': f"picture with id {picture['id']} already present"}, 302

       

    try:

        data.append(picture)

    except KeyError:

        return {"message": "data not defined"}, 403

   

    return picture, 201







######################################################################

# UPDATE A PICTURE

######################################################################







@app.route("/picture/<int:id>", methods=["PUT"])

def update_picture(id):

    picture=request.json

    for x in data:

        if x['id']==id:

            # for key in x.keys():

                # x[key]=picture[key]

            x.update(picture)

            return x, 200

       

    return {"message": "picture not found"}, 404





######################################################################

# DELETE A PICTURE

######################################################################

@app.route("/picture/<int:id>", methods=["DELETE"])

def delete_picture(id):

    for x in data:

        if x['id']==id:

            data.remove(x)

            return '',204

       

    return {"message": "picture not found"}, 404