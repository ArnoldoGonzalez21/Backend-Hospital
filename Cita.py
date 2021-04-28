class Cita():
    def __init__(self,indice,fecha,hora,motivo,estado):
        self.indice = indice
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo 
        self.estado = estado
    
    def get_json(self):
        return{
            "indice":self.indice,
            "fecha":self.fecha,
            "hora":self.hora,
            "motivo":self.motivo,
            "estado":self.estado
        }    

    def solicitar_cita(self,indice,fecha,hora,motivo,estado):
        self.indice = indice
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo 
        self.estado = estado
        
    def cambiar_estado_cita(self,indice,fecha,hora,motivo,estado):
        self.indice = indice
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo 
        self.estado = estado


#pendiente = 0
#aceptada = 1
#completada = 2
#rechazada = 3