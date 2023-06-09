from flask import Flask, request, jsonify
import pandas as pd
from geopy.distance import geodesic

app = Flask(__name__)

@app.route('/products', methods=['GET'])
def search():
    product = request.args.get('product')
    chain = request.args.get('chain')
    bioequivalent = request.args.get('bioequivalent')
    sort_by = request.args.get('sort_by')
    order = request.args.get('order')

    df = pd.read_csv('../data/products.csv')

    if chain:
        # Filtramos las filas donde la columna 'chain' es igual a la cadena
        df = df[df['chain'] == chain]

    if bioequivalent:
        # Filtramos las filas donde la columna 'bioequivalent' es igual al bioequivalente
        df = df[df['bioequivalent'] == bioequivalent]

    if product:
        # Filtramos las filas donde la columna 'description' contiene el producto
        df = df[df['description'].str.contains(product, case=False, na=False)]

    if sort_by in ['price', 'chain', 'description', 'bioequivalent']:
        ascending = True if order == 'asc' else False
        # Ordenamos el DataFrame de acuerdo al parámetro 'sort_by'
        df = df.sort_values(by=sort_by, ascending=ascending)

    # Convertimos el dataframe filtrado a un diccionario y lo retornamos como respuesta JSON
    return jsonify(df.to_dict(orient='records'))


@app.route('/drugstores', methods=['GET'])
def get_drugstores():
    chain = request.args.get('chain')
    lat = request.args.get('latitude')
    lon = request.args.get('longitude')
    phone = request.args.get('phone')
    df = pd.read_csv('../data/drugstores.csv')
    if chain:
        df = df[df['chain'].str.contains(chain, case=False, na=False)]
    if lat and lon:
        df['distance'] = df.apply(lambda row: geodesic((lat, lon), (row['latitude'], row['longitude'])).km, axis=1)
        df = df.sort_values('distance')
    if phone:
        df = df[df['phone'].str.contains(phone, case=False, na=False)]
    return jsonify(df.to_dict(orient='records'))

if __name__ == "__main__":
    # source venv/bin/activate 
    app.run(debug=True, port=5001)
