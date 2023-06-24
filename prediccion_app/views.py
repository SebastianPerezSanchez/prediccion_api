from rest_framework import viewsets
from rest_framework.response import Response
import requests

from prediccion_app.models import Movimientos, Almacen, Productos
from prediccion_app.serializers import MovimientosSerializer, AlmacenSerializer, ProductosSerializer
from prediccion_app.prediction import predecir_ventas

def serialize_predictions(predictions):
    serialized_predictions = []
    for _, prediction in predictions.iterrows():
        serialized_prediction = {
            'fecha': prediction['ds'].strftime('%d/%m/%Y'),
            'producto': prediction['producto'],
            'cantidad': prediction['yhat']
        }
        serialized_predictions.append(serialized_prediction)
    return serialized_predictions

class ProductosViewSet(viewsets.ModelViewSet):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializer


class MovimientosViewSet(viewsets.ModelViewSet):
    queryset = Movimientos.objects.all()
    serializer_class = MovimientosSerializer
    
class AlmacenViewSet(viewsets.ModelViewSet):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer
    
class PredictionViewSet(viewsets.ViewSet):
    def list(self, request):
        
        # Obtener los valores dinámicos desde la aplicación externa
        start_date = request.GET.get('start_date')
        num_periods = int(request.GET.get('num_periods'))
        frequency = request.GET.get('frequency')
        almacen = request.GET.get('almacen')
        
        # Realizar la solicitud a la API para obtener los datos
        url = 'http://127.0.0.1:8000/api/movimientos/'
        response = requests.get(url)
        data = response.json()

        # Pasar los datos a la función predecir_ventas
        predictions = predecir_ventas(data, start_date, num_periods, frequency, almacen)
        serialized_predictions = serialize_predictions(predictions)  # Función para serializar los resultados según tus necesidades
        return Response(serialized_predictions)