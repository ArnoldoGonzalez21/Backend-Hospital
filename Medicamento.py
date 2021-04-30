class Medicamento():
    def __init__(self,nombre,precio,descripcion,cantidad,venta):
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.venta = venta 
        
    def get_json(self):
        return{
            "nombre":self.nombre,
            "precio":self.precio,
            "descripcion":self.descripcion,
            "cantidad":self.cantidad,
            "venta":self.venta
        }
           
    def editar_medicamento(self, nombre, precio, descripcion, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.cantidad = cantidad
    
    def agregar_venta(self, venta):
        self.venta = venta       