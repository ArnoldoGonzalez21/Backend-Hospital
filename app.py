from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os
import csv
from Paciente import Paciente
from Enfermera import Enfermera
from Doctor import Doctor
from Medicamento import Medicamento
from Cita import Cita
from Factura import Factura
from Receta import Receta

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
citas = []
facturas = []
recetas = []

@app.route('/', methods=['GET'])
def principal():
    return 'Arnoldo Luis Antonio González Camey   201701548'

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
    paciente_nuevo = Paciente(nombre,apellido,fecha_nacimiento,sexo,nombre_usuario,contrasena,telefono,False)
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
    return False    

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
    i = int(indice)
    global pacientes
    nombre_usuario = contenido['nombre_usuario']
    if (existe_usuario(nombre_usuario) and pacientes[i].nombre_usuario != nombre_usuario):
        return jsonify({'agregado':0,'mensaje':'El Nombre de Usuario que desea Agregar Ya Existe'})
    contrasena = contenido['contrasena']
    telefono = contenido['telefono']
    pacientes[i].modificar_perfil(nombre, apellido, fecha_nacimiento, sexo, nombre_usuario, contrasena, telefono)
    return jsonify({'agregado':1,'mensaje':'Datos Modificados Exitosamente'})

@app.route('/eliminar_paciente', methods=['POST'])
def eliminar_paciente():
    cuerpo = request.get_json()
    indice = cuerpo['indice']
    i = int(indice)
    global pacientes
    pacientes.pop(i)
    return jsonify({"mensaje":"Paciente Eliminado Exitosamente"})

#---------------------------Cita----------------------------------

@app.route('/obtener_cita', methods=['GET'])
def obtener_cita():
    json_citas = []
    global citas
    for cita in citas:
        json_citas.append(cita.get_json())
    return jsonify(json_citas)

@app.route('/solicitar_cita', methods=['POST'])
def solicitar_cita():
    contenido = request.get_json()
    indice = contenido['indice']
    i = int(indice)
    if (existe_cita(i)):
        return jsonify({'agregado':6,'mensaje':'El Paciente tiene una Cita Pendiente'})
    fecha = contenido['fecha']
    hora = contenido['hora']
    motivo = contenido['motivo']
    estado = contenido['estado']
    cita_nueva = Cita(i, fecha, hora, motivo, estado,-1)
    global citas
    global pacientes
    citas.append(cita_nueva)
    pacientes[i].estado = True
    return jsonify({'agregado':5,'mensaje':'Cita Agregada Exitosamente'})

@app.route('/responder_cita', methods=['POST'])
def responder_cita():
    contenido = request.get_json()
    posicion = contenido['posicion'] #posicion
    i = int(posicion)
    indice = contenido['indice']
    estado = contenido['estado']
    global citas
    global pacientes
    j = int(indice)
    if estado == 2 or estado == 3:
        pacientes[j].estado = False
    citas[i].cambiar_estado_cita(indice, estado)
    return jsonify({'agregado':7,'mensaje':'Estado de la Cita Cambiado Exitosamente'})

@app.route('/asignar_doctor', methods=['POST'])
def asignar_doctor():
    contenido = request.get_json()
    posicion = contenido['posicion'] #posicion
    i = int(posicion)
    indice = contenido['indice']
    doctor = contenido['doctor'] #posicion del doctor
    j = int(doctor)
    global citas
    global doctores
    agregar_cita = int(doctores[j].citas) + 1
    doctores[j].citas = agregar_cita
    citas[i].asignar_doctor(indice, doctor)
    return jsonify({'agregado':8,'mensaje':'Médico Asignado Exitosamente'})

def existe_cita(indice):
    global pacientes
    if pacientes[indice].estado:
        return True;
    return False

#---------------------------Factura----------------------------------

@app.route('/obtener_factura', methods=['GET'])
def obtener_factura():
    json_facturas = []
    global facturas
    for factura in facturas:
        json_facturas.append(factura.get_json())
    return jsonify(json_facturas)

@app.route('/generar_factura', methods=['POST'])
def generar_factura():
    contenido = request.get_json()
    fecha = contenido['fecha']
    paciente = contenido['paciente']
    doctor = contenido['doctor']
    total = contenido['total']
    factura_nueva = Factura(fecha, paciente, doctor, total)
    global facturas
    facturas.append(factura_nueva)
    return jsonify({'agregado':9,'mensaje':'Factura Agregada Exitosamente'})

#---------------------------Receta----------------------------------

@app.route('/obtener_receta', methods=['GET'])
def obtener_receta():
    json_recetas = []
    global recetas
    for receta in recetas:
        json_recetas.append(receta.get_json())
    return jsonify(json_recetas)

@app.route('/crear_receta', methods=['POST'])
def crear_receta():
    global recetas
    contenido = request.get_json()
    fecha = contenido['fecha']
    paciente = contenido['paciente']
    padecimiento = contenido['padecimiento']
    descripcion = contenido['descripcion']
    receta_nueva = Receta(fecha, paciente, padecimiento, descripcion, 1)
    recetas.append(receta_nueva)
    return jsonify({'agregado':10,'mensaje':'Receta Agregada Exitosamente'})

def existe_padecimiento(padecimiento):
    global recetas
    contador = 0
    for receta in recetas:
        contador = contador + 1
        if receta.padecimiento == padecimiento:
            return contador
    return -1    

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
    if (existe_usuario(nombre_usuario)):
        return jsonify({'agregado':0,'mensaje':'El Usuario que DESEA Agregar Ya Existe'})
    contrasena = contenido['contrasena']
    telefono = contenido['telefono']
    enfermera_nueva = Enfermera(nombre,apellido,fecha_nacimiento,sexo,nombre_usuario,contrasena,telefono)
    global enfermeras
    enfermeras.append(enfermera_nueva)
    return jsonify({'agregado':2,'mensaje':'Registro Exitoso'})

def verificar_contrasena_enfermera(nombre_usuario, contrasena):
    if nombre_usuario == administrador['nombre_usuario'] and contrasena == administrador['contrasena']:
        return True
    global enfermeras
    for enfermera in enfermeras:
        if enfermera.nombre_usuario == nombre_usuario and enfermera.contrasena == contrasena:
            return True
    return False

@app.route('/editar_enfermera', methods=['POST'])
def editar_enfermera():
    contenido = request.get_json()
    indice = contenido['indice']
    nombre = contenido['nombre']
    apellido = contenido['apellido']
    fecha_nacimiento = contenido['fecha_nacimiento']
    sexo = contenido['sexo']    
    i = int(indice)
    global enfermeras
    nombre_usuario = contenido['nombre_usuario']
    if (existe_usuario(nombre_usuario) and enfermeras[i].nombre_usuario != nombre_usuario):
        return jsonify({'agregado':0,'mensaje':'El Nombre de Usuario que desea Agregar Ya Existe'})
    contrasena = contenido['contrasena']
    telefono = contenido['telefono']
    enfermeras[i].modificar_perfil(nombre, apellido, fecha_nacimiento, sexo, nombre_usuario, contrasena, telefono)
    return jsonify({'agregado':1,'mensaje':'Datos Modificados Exitosamente'})

@app.route('/eliminar_enfermera', methods=['POST'])
def eliminar_enfermera():
    cuerpo = request.get_json()
    indice = cuerpo['indice']
    i = int(indice)
    global enfermeras
    enfermeras.pop(i)
    return jsonify({"mensaje":"Enfermera Eliminada exitosamente"})

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
    if (existe_usuario(nombre_usuario)):
        return jsonify({'agregado':0,'mensaje':'El Usuario que desea Agregar Ya Existe'})
    contrasena = contenido['contrasena']
    especialidad = contenido['especialidad']
    telefono = contenido['telefono']
    doctor_nuevo = Doctor(nombre,apellido,fecha_nacimiento,sexo,nombre_usuario,contrasena,especialidad,telefono,0)
    global doctores
    doctores.append(doctor_nuevo)
    return jsonify({'agregado':3,'mensaje':'Registro Exitoso'})

def verificar_contrasena_doctor(nombre_usuario, contrasena):
    if nombre_usuario == administrador['nombre_usuario'] and contrasena == administrador['contrasena']:
        return True
    global doctores
    for doctor in doctores:
        if doctor.nombre_usuario == nombre_usuario and doctor.contrasena == contrasena:
            return True
    return False

@app.route('/editar_doctor', methods=['POST'])
def editar_doctor():
    contenido = request.get_json()
    indice = contenido['indice']
    nombre = contenido['nombre']
    apellido = contenido['apellido']
    fecha_nacimiento = contenido['fecha_nacimiento']
    sexo = contenido['sexo']
    i = int(indice)
    global doctores
    nombre_usuario = contenido['nombre_usuario']
    if (existe_usuario(nombre_usuario) and doctores[i].nombre_usuario != nombre_usuario):
        return jsonify({'agregado':0,'mensaje':'El Nombre de Usuario que desea Agregar Ya Existe'})
    contrasena = contenido['contrasena']
    especialidad = contenido['especialidad']
    telefono = contenido['telefono']
    doctores[i].modificar_perfil(nombre, apellido, fecha_nacimiento, sexo, nombre_usuario, contrasena, especialidad, telefono)
    return jsonify({'agregado':1,'mensaje':'Datos Modificados Exitosamente'})

@app.route('/eliminar_doctor', methods=['POST'])
def eliminar_doctor():
    cuerpo = request.get_json()
    indice = cuerpo['indice']
    i = int(indice)
    global doctores
    doctores.pop(i)
    return jsonify({"mensaje":"Doctor Eliminado exitosamente"})

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
    medicamento_nuevo = Medicamento(nombre, precio, descripcion, cantidad, 0, -1, 0)
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

@app.route('/agregar_venta_medicamento', methods=['POST'])
def agregar_venta_medicamento():
    cuerpo = request.get_json()
    posicion = cuerpo['posicion']
    venta = cuerpo['venta']
    paciente = cuerpo['paciente']
    compra = cuerpo['compra']
    i = int(posicion)
    global medicamentos
    agregar_venta = int(medicamentos[i].venta) + int(venta)
    medicamentos[i].agregar_venta(agregar_venta, paciente, compra)
    return jsonify(medicamentos[i].get_json())

@app.route('/eliminar_compra', methods=['POST'])
def eliminar_compra():
    cuerpo = request.get_json()
    paciente = cuerpo['paciente']
    global medicamentos
    for medicamento in medicamentos:
        medicamento.compra = 0
    return jsonify({"mensaje":"Compra Eliminada"})


@app.route('/eliminar_medicamento_pedido', methods=['POST'])
def eliminar_medicamento_pedido():
    cuerpo = request.get_json()
    indice = cuerpo['indice']
    venta = cuerpo['venta']
    paciente = cuerpo['paciente']
    i = int(indice)
    global medicamentos
    quitar_venta = int(medicamentos[i].venta) - int(venta)
    medicamentos[i].agregar_venta(quitar_venta, paciente, 0)
    return jsonify({"mensaje":"Medicamento Eliminado Exitosamente"})

#---------------------------Login----------------------------------

@app.route('/login', methods=['GET'])
def login():
    nombre_usuario = request.args.get("nombre_usuario")
    contrasena = request.args.get("contrasena")
    if nombre_usuario == administrador['nombre_usuario'] and contrasena == administrador['contrasena']:
        return jsonify({'estado':4,'mensaje':'Login Exitoso Administrador'})
    if (not existe_usuario(nombre_usuario)):
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
    