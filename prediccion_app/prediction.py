import pandas as pd
from prophet import Prophet
import datetime


def predecir_ventas(data): 
    # Convertir los documentos a un DataFrame de pandas
    data = pd.DataFrame(data)

    # Convertir la columna de fechas a tipo datetime con el formato correcto
    data['fecha'] = data['fecha'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))

    # Crear una lista para almacenar los pronósticos de cada producto
    predictions = []

    # Realizar el modelo por cada producto
    for producto in data['producto'].unique():
        # Filtrar los datos por producto
        product_data = data[data['producto'] == producto]

        # Agrupar los datos por mes y calcular la suma de las ventas diarias para cada mes
        monthly_data = product_data.groupby(pd.Grouper(key='fecha', freq='M')).sum().reset_index()

        # Verificar filas no nulas
        if monthly_data['cantidad'].count() >= 2:
            # Renombrar las columnas a "ds" y "y"
            monthly_data.rename(columns={'fecha': 'ds', 'cantidad': 'y'}, inplace=True)

            # Inicializar y ajustar el modelo Prophet
            model = Prophet()
            model.fit(monthly_data)

            # Generar fechas futuras para predicción
            future_dates = pd.date_range(start='2023-06-01', periods=4, freq='3M')

            # Crear un DataFrame con las fechas futuras
            future_dataframe = pd.DataFrame({'ds': future_dates})

            # Generar pronósticos mensuales
            forecast = model.predict(future_dataframe)

            # Agregar la columna "producto" al pronóstico
            forecast['producto'] = producto

            # Agregar los pronósticos a la lista de pronósticos
            predictions.append(forecast[['producto', 'ds', 'yhat', 'yhat_lower', 'yhat_upper']])

    # Concatenar los pronósticos de todos los productos
    all_predictions = pd.concat(predictions)
    
    # Eliminar filas con valores nulos en la columna "producto"
    all_predictions = all_predictions.dropna(subset=['producto'])
    
    # Filtrar productos
    filtered_predictions = all_predictions[all_predictions['yhat'] >= 100]   
    
    # Retornar los pronósticos
    return filtered_predictions
    