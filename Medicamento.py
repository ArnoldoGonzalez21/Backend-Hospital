class Medicamento():
    def __init__(self,nombre,precio,descripcion,cantidad,venta,paciente,compra):
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.venta = venta
        self.paciente = paciente
        self.compra = compra 
        
    def get_json(self):
        return{
            "nombre":self.nombre,
            "precio":self.precio,
            "descripcion":self.descripcion,
            "cantidad":self.cantidad,
            "venta":self.venta,
            "paciente":self.paciente,
            "compra":self.compra,
        }
           
    def editar_medicamento(self, nombre, precio, descripcion, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.cantidad = cantidad
    
    def agregar_venta(self, venta, paciente, compra):
        self.venta = venta 
        self.paciente = paciente
        self.compra = compra      