from flask import Flask, request, jsonify
import pandas as pd
from geopy.distance import geodesic

app = Flask(__name__)

@app.route('/products', methods=['POST'])
def search():
    print("Buscando productos")
    keyword = request.json['keyword']
    df = pd.read_csv('../data/products.csv')
    # Filtramos las filas donde la columna 'name' contiene la palabra clave
    results = df[df['name'].str.contains(keyword, case=False, na=False)]
    # Convertimos el dataframe filtrado a un diccionario y lo retornamos como respuesta JSON
    return jsonify(results.to_dict(orient='records'))


@app.route('/drugstores', methods=['GET'])
def get_drugstores():
    chain = request.args.get('chain')
    lat = request.args.get('latitude')
    lon = request.args.get('longitude')
    df = pd.read_csv('../data/drugstores.csv')
    if chain:
        df = df[df['chain'].str.contains(chain, case=False, na=False)]
    if lat and lon:
        df['distance'] = df.apply(lambda row: geodesic((lat, lon), (row['latitude'], row['longitude'])).km, axis=1)
        df = df.sort_values('distance')
    return jsonify(df.to_dict(orient='records'))

if __name__ == "__main__":
    # source venv/bin/activate 
    app.run(debug=True, port=5001)
