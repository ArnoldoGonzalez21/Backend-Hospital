class Cita():
    def __init__(self,indice,fecha,hora,motivo,estado,doctor):
        self.indice = indice
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo 
        self.estado = estado
        self.doctor = doctor
    
    def get_json(self):
        return{
            "indice":self.indice,
            "fecha":self.fecha,
            "hora":self.hora,
            "motivo":self.motivo,
            "estado":self.estado,
            "doctor":self.doctor
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
    
    def asignar_doctor(self,indice,doctor):
        self.indice = indice
        self.doctor = doctor
        


#pendiente = 0
#aceptada = 1
#completada = 2
#rechazada = 3