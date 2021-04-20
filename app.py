from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os

app = Flask(__name__)
CORS(app)

administrador = {
    "nombre":"Arnoldo",
    "apellido":"González",
    "nombre_usuario":"admin",
    "contrasena":"1234"   
} 

pacientes = []

@app.route('/', methods=['GET'])
def principal():
    return 'Por fin'

@app.route('/registro_paciente', methods=['POST'])
def registro_paciente():
    contenido = requets.get_json()
    nombre = contenido['nombre']
    apellido = contenido['apellido']
    fecha_nacimiento = contenido['fecha_nacimiento']
    sexo = contenido['sexo']
    nombre_usuario = contenido['nombre_usuario']
    if (existe_usuario(nombre_usuario)):
        return jsonify({'agregado':0,'mensaje':'Existe el usuario'})
    contrasena = contenido['contrasena']
    telefono = contenido['telefono']
    paciente_nuevo = Paciente(nombre,apellido,fecha_nacimiento,sexo,nombre_usuario,contrasena,telefono)
    global pacientes
    pacientes.append(paciente_nuevo)
    return jsonify({'agregado':1,'mensaje':'Registro exitoso'})


@app.route('/obtener_paciente', methods=['GET'])
def obtener_paciente():
    json_pacientes = []
    global pacientes
    for paciente in pacientes:
        json_pacientes.append(paciente.get_json())
    return jsonify(json_pacientes)

@app.route('/login', methods=['GET'])
def login():
    nombre_usuario = request.args.get("nombre_usuario")
    contrasena = request.args.get("contrasena")
    if not existe_usuario(nombre_usuario):
        return jsonify({'estado':0,'mensaje':'no existe el usuario'})
    if verificar_contrasena(nombre_usuario, contrasena):
        return jsonify({'estado':1,'mensaje':'login existoso'})
    return jsonify({'estado':0,'mensaje':'La contraseña es incorrecta'})

def existe_usuario(nombre_usuario):
    if nombre_usuario == administrador['nombre_usuario']:
        return True
    global pacientes
    for paciente in pacientes:
        if paciente.nombre_usuario == nombre_usuario:
            return True
    return False

def verificar_contrasena(nombre_usuario, contrasena):
    if nombre_usuario == administrador['nombre_usuario'] and contrasena == administrador['contrasena']:
        return True
    global pacientes
    for paciente in pacientes:
        if paciente.nombre_usuario == nombre_usuario and paciente.contrasena == contrasena:
            return True
    return False 
    
if __name__ == '__main__':
    puerto = int(os.environ.get('PORT',3000))
    app.run(host= '0.0.0.0',port=puerto)
    
