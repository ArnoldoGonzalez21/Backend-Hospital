from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os
import csv
from Paciente import Paciente
from Enfermera import Enfermera
from Doctor import Doctor
from Medicamento import Medicamento

app = Flask(__name__)
CORS(app)

administrador = {
    "nombre":"Ingrid",
    "apellido":"Perez",
    "nombre_usuario":"admin",
    "contrasena":"1234"   
} 

pacientes = []
enfermeras = []
doctores = []
medicamentos = []

@app.route('/', methods=['GET'])
def principal():
    return 'Por fin'

#---------------------------Paciente----------------------------------
@app.route('/registro_paciente', methods=['POST'])
def registro_paciente():
    contenido = request.get_json()
    nombre = contenido['nombre']
    apellido = contenido['apellido']
    fecha_nacimiento = contenido['fecha_nacimiento']
    sexo = contenido['sexo']
    nombre_usuario = contenido['nombre_usuario']
    if (existe_usuario(nombre_usuario)):
        return jsonify({'agregado':0,'mensaje':'El Usuario que desea Agregar Ya Existe'})
    contrasena = contenido['contrasena']
    telefono = contenido['telefono']
    paciente_nuevo = Paciente(nombre,apellido,fecha_nacimiento,sexo,nombre_usuario,contrasena,telefono)
    global pacientes
    pacientes.append(paciente_nuevo)
    return jsonify({'agregado':1,'mensaje':'Registro Exitoso'})

@app.route('/obtener_paciente', methods=['GET'])
def obtener_paciente():
    json_pacientes = []
    global pacientes
    for paciente in pacientes:
        json_pacientes.append(paciente.get_json())
    return jsonify(json_pacientes)

def existe_usuario(nombre_usuario):
    if nombre_usuario == administrador['nombre_usuario']:
        return True
    global pacientes
    global enfermeras
    global doctores
    for paciente in pacientes:
        if paciente.nombre_usuario == nombre_usuario:
            return True
    for enfermera in enfermeras:
        if enfermera.nombre_usuario == nombre_usuario:
            return True
    for doctor in doctores:
        if doctor.nombre_usuario == nombre_usuario:
            return True

def verificar_contrasena(nombre_usuario, contrasena):
    if nombre_usuario == administrador['nombre_usuario'] and contrasena == administrador['contrasena']:
        return True
    global pacientes
    for paciente in pacientes:
        if paciente.nombre_usuario == nombre_usuario and paciente.contrasena == contrasena:
            return True
    return False

@app.route('/editar_paciente', methods=['POST'])
def editar_paciente():
    contenido = request.get_json()
    indice = contenido['indice']
    nombre = contenido['nombre']
    apellido = contenido['apellido']
    fecha_nacimiento = contenido['fecha_nacimiento']
    sexo = contenido['sexo']
    nombre_usuario = contenido['nombre_usuario']
    if (existe_usuario(nombre_usuario)):
        return jsonify({'agregado':0,'mensaje':'El Nombre de Usuario que desea Agregar Ya Existe'})
    contrasena = contenido['contrasena']
    telefono = contenido['telefono']
    i = int(indice)
    global pacientes
    pacientes[i].modificar_perfil(nombre, apellido, fecha_nacimiento, sexo, nombre_usuario, contrasena, telefono)
    return jsonify(pacientes[i].get_json())


#---------------------------Enfermera----------------------------------
@app.route('/obtener_enfermera', methods=['GET'])
def obtener_enfermera():
    json_enfermera = []
    global enfermeras
    for enfermera in enfermeras:
        json_enfermera.append(enfermera.get_json())
    return jsonify(json_enfermera)

@app.route('/registro_enfermera', methods=['POST'])
def registro_enfermera():
    contenido = request.get_json()
    nombre = contenido['nombre']
    apellido = contenido['apellido']
    fecha_nacimiento = contenido['fecha_nacimiento']
    sexo = contenido['sexo']
    nombre_usuario = contenido['nombre_usuario']
    if (existe_usuario_enfermera(nombre_usuario)):
        return jsonify({'agregado':0,'mensaje':'El Usuario que DESEA Agregar Ya Existe'})
    contrasena = contenido['contrasena']
    telefono = contenido['telefono']
    enfermera_nueva = Enfermera(nombre,apellido,fecha_nacimiento,sexo,nombre_usuario,contrasena,telefono)
    global enfermeras
    enfermeras.append(enfermera_nueva)
    return jsonify({'agregado':2,'mensaje':'Registro Exitoso'})

def existe_usuario_enfermera(nombre_usuario):
    if nombre_usuario == administrador['nombre_usuario']:
        return True
    global enfermeras
    global doctores
    global pacientes
    for enfermera in enfermeras:
        if enfermera.nombre_usuario == nombre_usuario:
            return True
    for doctor in doctores:
        if doctor.nombre_usuario == nombre_usuario:
            return True
    for paciente in pacientes:
        if paciente.nombre_usuario == nombre_usuario:
            return True 
    return False

def verificar_contrasena_enfermera(nombre_usuario, contrasena):
    if nombre_usuario == administrador['nombre_usuario'] and contrasena == administrador['contrasena']:
        return True
    global enfermeras
    for enfermera in enfermeras:
        if enfermera.nombre_usuario == nombre_usuario and enfermera.contrasena == contrasena:
            return True
    return False

#---------------------------Doctor----------------------------------
@app.route('/obtener_doctor', methods=['GET'])
def obtener_doctor():
    json_doctor = []
    global doctores
    for doctor in doctores:
        json_doctor.append(doctor.get_json())
    return jsonify(json_doctor)

@app.route('/registro_doctor', methods=['POST'])
def registro_doctor():
    contenido = request.get_json()
    nombre = contenido['nombre']
    apellido = contenido['apellido']
    fecha_nacimiento = contenido['fecha_nacimiento']
    sexo = contenido['sexo']
    nombre_usuario = contenido['nombre_usuario']
    if (existe_usuario_doctor(nombre_usuario)):
        return jsonify({'agregado':0,'mensaje':'El Usuario que desea Agregar Ya Existe'})
    contrasena = contenido['contrasena']
    telefono = contenido['telefono']
    doctor_nuevo = Doctor(nombre,apellido,fecha_nacimiento,sexo,nombre_usuario,contrasena,telefono)
    global doctores
    doctores.append(doctor_nuevo)
    return jsonify({'agregado':3,'mensaje':'Registro Exitoso'})

def existe_usuario_doctor(nombre_usuario):
    if nombre_usuario == administrador['nombre_usuario']:
        return True
    global doctores
    global enfermeras
    global pacientes
    for doctor in doctores:
        if doctor.nombre_usuario == nombre_usuario:
            return True
    for enfermera in enfermeras:
        if enfermera.nombre_usuario == nombre_usuario:
            return True
    for paciente in pacientes:
        if paciente.nombre_usuario == nombre_usuario:
            return True          
    return False

def verificar_contrasena_doctor(nombre_usuario, contrasena):
    if nombre_usuario == administrador['nombre_usuario'] and contrasena == administrador['contrasena']:
        return True
    global doctores
    for doctor in doctores:
        if doctor.nombre_usuario == nombre_usuario and doctor.contrasena == contrasena:
            return True
    return False

#---------------------------Medicamento----------------------------------
@app.route('/obtener_medicamento', methods=['GET'])
def obtener_medicamento():
    json_medicamento = []
    global medicamentos
    for medicamento in medicamentos:
        json_medicamento.append(medicamento.get_json())
    return jsonify(json_medicamento)

@app.route('/registro_medicamento', methods=['POST'])
def registro_medicamento():
    contenido = request.get_json()
    nombre = contenido['nombre']
    if (existe_medicamento(nombre)):
            return jsonify({'agregado':0,'mensaje':'El Medicamento que desea Agregar Ya Existe'})
    precio = contenido['precio']
    descripcion = contenido['descripcion']
    cantidad = contenido['cantidad']
    medicamento_nuevo = Medicamento(nombre, precio, descripcion, cantidad)
    global medicamentos
    medicamentos.append(medicamento_nuevo)
    return jsonify({'agregado':4,'mensaje':'Registro Exitoso'})

def existe_medicamento(nombre):
    global medicamentos
    for medicamento in medicamentos:
        if medicamento.nombre == nombre:
            return True
    return False

@app.route('/eliminar_medicamento', methods=['POST'])
def eliminar_medicamento():
    cuerpo = request.get_json()
    indice = cuerpo['indice']
    i = int(indice)
    global medicamentos
    medicamentos.pop(i)
    return jsonify({"mensaje":"Medicamento Eliminado exitosamente"})

@app.route('/editar_medicamento', methods=['POST'])
def editar_medicamento():
    cuerpo = request.get_json()
    indice = cuerpo['indice']
    nombre = cuerpo['nombre']
    precio = cuerpo['precio']
    descripcion = cuerpo['descripcion']
    cantidad = cuerpo['cantidad']
    i = int(indice)
    global medicamentos
    medicamentos[i].editar_medicamento(nombre, precio, descripcion, cantidad)
    return jsonify(medicamentos[i].get_json())

#---------------------------Login----------------------------------

@app.route('/login', methods=['GET'])
def login():
    nombre_usuario = request.args.get("nombre_usuario")
    contrasena = request.args.get("contrasena")
    if nombre_usuario == administrador['nombre_usuario'] and contrasena == administrador['contrasena']:
        return jsonify({'estado':4,'mensaje':'Login Exitoso Administrador'})
    if (not existe_usuario(nombre_usuario)) and (not existe_usuario_enfermera(nombre_usuario)) and (not existe_usuario_doctor(nombre_usuario)):
        return jsonify({'estado':0,'mensaje':'El Usuario No Existe'})
    if verificar_contrasena(nombre_usuario, contrasena):
        return jsonify({'estado':1,'mensaje':'Login Existoso Paciente'})
    elif verificar_contrasena_enfermera(nombre_usuario, contrasena):
        return jsonify({'estado':2,'mensaje':'Login Existoso Enfermera'})
    elif verificar_contrasena_doctor(nombre_usuario, contrasena):
        return jsonify({'estado':3,'mensaje':'Login Existoso Doctor'})
    return jsonify({'estado':0,'mensaje':'La Contraseña es Incorrecta'})


if __name__ == '__main__':
    puerto = int(os.environ.get('PORT',3000))
    app.run(host= '0.0.0.0',port=puerto)
    