from flask import Flask, request, jsonify, make_response
import pandas as pd
import io
from geopy.distance import geodesic
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/products', methods=['GET'])
def search():
    product = request.args.get('product')
    chain = request.args.get('chain')
    phone = request.args.get('phone')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
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


    if phone:
        drugstores = get_drugstores()
        drugstores = pd.read_json(io.BytesIO(drugstores.data))
        if drugstores.empty: return jsonify([])
        drugstores = drugstores[drugstores['phone'].str.contains(phone, case=False, na=False)]
        chains = drugstores['chain'].unique()
        df = df[df['chain'].isin(chains)]
        if df.empty: return jsonify([])

    if latitude and longitude:
        drugstores = get_drugstores()
        drugstores = pd.read_json(io.BytesIO(drugstores.data))
        drugstores['distance'] = drugstores.apply(lambda row: geodesic((latitude, longitude), (row['latitude'], row['longitude'])).km, axis=1)

        drugstores = drugstores[drugstores['distance'] <= 20]
        chains = drugstores['chain'].unique()
        df = df[df['chain'].isin(chains)]
        df['distance'] = df.apply(lambda row: drugstores[drugstores['chain'] == row['chain']]['distance'].min(), axis=1)

    if sort_by in ['price', 'chain', 'description', 'bioequivalent']:
        ascending = True if order == 'asc' else False
        # Ordenamos el DataFrame de acuerdo al parámetro 'sort_by'
        df = df.sort_values(by=sort_by, ascending=ascending)

    # Convertimos el dataframe filtrado a un diccionario y lo retornamos como respuesta JSON
    if df.empty: return jsonify([])
    return make_response(df.to_json(orient='records'), 200)


@app.route('/drugstores', methods=['GET'])
def get_drugstores():
    chain = request.args.get('chain')
    lat = request.args.get('latitude')
    lon = request.args.get('longitude')
    phone = request.args.get('phone')
    product = request.args.get('product')

    df = pd.read_csv('../data/drugstores.csv')

    if product:
        products = pd.read_csv('../data/products.csv')
        products = products[products['description'].str.contains(product, case=False, na=False)]
        chains = products['chain'].unique()
        df = df[df['chain'].isin(chains)]

    if chain and chain != '':
        df = df[df['chain'].str.contains(chain, case=False, na=False)]
    if not (lat and lon):
        lat = -33.44204
        lon = -70.60463
        
    df['distance'] = df.apply(lambda row: geodesic((lat, lon), (row['latitude'], row['longitude'])).km, axis=1)
    df = df.sort_values('distance')
    if phone and phone != '':
        df = df[df['phone'].str.contains(phone, case=False, na=False)]
    
    if df.empty: return jsonify([])
    # df_final = df.head(10)
    df_final = df[df['distance'] <= 5]
    if df_final.shape[0] < 5:
        df_final = df.head(10)

    return make_response(df_final.to_json(orient='records'), 200)

if __name__ == "__main__":
    # source venv/bin/activate 
    app.run(debug=True, port=5000)
