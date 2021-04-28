class Cita():
    def __init__(self,indice,fecha,hora,motivo):
        self.indice = indice
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo 
    
    def get_json(self):
        return{
            "indice":self.indice,
            "fecha":self.fecha,
            "hora":self.hora,
            "motivo":self.motivo
        }    

    def solicitar_cita(self,indice,fecha,hora,motivo):
        self.indice = indice
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo 