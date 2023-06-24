from djongo import models
from bson import ObjectId


# Create your models here.

class Productos(models.Model):
    _id = models.ObjectIdField()
    nombre = models.CharField(max_length=500)
    precio = models.IntegerField()
    codigo = models.CharField(max_length=500)
    
    class Meta:
        db_table = 'productos'

class Movimientos(models.Model):
    fecha = models.DateTimeField()
    producto = models.CharField(max_length = 500)
    cantidad = models.IntegerField()
    tipo_movimiento = models.CharField(max_length = 500)
    codigo_recibido = models.CharField(max_length = 500)
    almacen = models.CharField(max_length = 500)
    
    class Meta:
        db_table = 'movimientos'
        
class Almacen(models.Model):
    nombre = models.CharField(max_length=500)

    class Meta:
        db_table = 'almacens'
