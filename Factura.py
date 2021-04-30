class Factura():
    def __init__(self,fecha,paciente,doctor,total):
        self.fecha = fecha
        self.paciente = paciente
        self.doctor = doctor
        self.total = total
    
    def get_json(self):
        return{
            "fecha":self.fecha,
            "paciente":self.paciente,
            "doctor":self.doctor,
            "total":self.total
        }