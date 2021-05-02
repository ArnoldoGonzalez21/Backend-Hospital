class Receta():
    def __init__(self,fecha,paciente,padecimiento,descripcion,cantidad):
        self.fecha = fecha
        self.paciente = paciente
        self.padecimiento = padecimiento
        self.descripcion = descripcion
        self.cantidad = cantidad #numero de padecimientos iguales
    
    def get_json(self):
        return{
            "fecha":self.fecha,
            "paciente":self.paciente,
            "padecimiento":self.padecimiento,
            "descripcion":self.descripcion
        }