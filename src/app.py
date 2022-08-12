"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")  # Jackson es el lastname y el self no se debe indicar

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# -------------------------- MIS ENDPOINTS ------------------------------- #

@app.route('/members', methods=['GET'])
def handle_members():
    members = jackson_family.get_all_members()  #traer a todos los miembros
    response_body = members
    return jsonify(response_body), 200  # responder los miembros

@app.route('/member/<int:member_id>', methods=['GET'])
def handle_member(member_id):

    member1 = jackson_family.get_member(member_id)
    if member1 is None:
        raise APIException('member not found', status_code=400) 
    else:
        response_body = jackson_family.get_member(member_id)  # traer a un miembro
        return jsonify(response_body), 200  # responder el miembro

@app.route('/member/', methods=['POST'])
def add_new_member():

    # tomar los datos del request, propiedad por propiedad con el metodo .get()
    body_id = request.json.get('id')
    body_first_name = request.json.get('first_name')
    body_last_name = request.json.get('last_name')
    body_age = request.json.get('age')
    body_lucky_numbers = request.json.get('lucky_numbers')

    # componer el miembro nuevo con las variables anteriores obtenidas con get():
    member = {
        'id': body_id,
        'first_name': body_first_name,
        'last_name': body_last_name,
        'age': body_age,
        'lucky_numbers': body_lucky_numbers
    }
    # ahora agregar el nuevo miembro a la familia jackson, no a la clase
    jackson_family.add_member(member)  
    return jsonify("añadido"), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def del_member(member_id):

    member1 = jackson_family.get_member(member_id) # traer al miembro solicitado
    if member1 is None:
        raise APIException('member not found', status_code=400)  # consultar si existe, sino arrojar error
    else:
        jackson_family.delete_member(member_id) # si existe agregarlo a _members con la funcion

    return jsonify({'done': True}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
