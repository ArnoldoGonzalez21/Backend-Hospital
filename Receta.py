class Receta():
    def __init__(self,fecha,paciente,padecimiento,descripcion):
        self.fecha = fecha
        self.paciente = paciente
        self.padecimiento = padecimiento
        self.descripcion = descripcion
    
    def get_json(self):
        return{
            "fecha":self.fecha,
            "paciente":self.paciente,
            "padecimiento":self.padecimiento,
            "descripcion":self.descripcion
        }