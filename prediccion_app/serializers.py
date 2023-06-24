from rest_framework import serializers
from prediccion_app.models import Movimientos, Almacen, Productos
from django.shortcuts import get_object_or_404
from bson import ObjectId

class AlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Almacen
        fields = ('nombre',)
        
class MovimientosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movimientos
        fields = ('fecha', 'producto', 'cantidad', 'almacen')

class PredictionSerializer(serializers.Serializer):
    producto = serializers.CharField()
    ds = serializers.DateField()
    yhat = serializers.FloatField()
    yhat_lower = serializers.FloatField()
    yhat_upper = serializers.FloatField()
    
def serialize_predictions(predictions):
    serializer = PredictionSerializer(predictions, many = True)
    return serializer.data

class ProductosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Productos
        fields = ('_id','nombre', 'precio', 'codigo')
