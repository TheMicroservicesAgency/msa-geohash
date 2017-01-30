from flask import Flask, jsonify, redirect, request
import pygeohash as geohash
from geojson import Point

app = Flask(__name__)

@app.route('/geohash/encode')
def encode():

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if lat is None or lon is None:
        msg = {'ERROR': 'Missing parameter.'}
        return jsonify(msg), 400

    try:
        lat = float(lat)
    except ValueError:
        msg = {'ERROR': 'The specified latitude is not a number.'}
        return jsonify(msg), 400

    try:
        lon = float(lon)
    except ValueError:
        msg = {'ERROR': 'The specified longitude is not a number.'}
        return jsonify(msg), 400

    if lat < -90.0 or lat > 90.0:
        msg = {'ERROR': 'The specified latitude is invalid.'}
        return jsonify(msg), 400

    if lon < -180.0 or lon > 180.0:
        msg = {'ERROR': 'The specified longitude is invalid.'}
        return jsonify(msg), 400

    result = geohash.encode(lat, lon)

    data = {'geohash': result}
    response = jsonify(data)
    return response

@app.route('/geohash/decode')
def decode():
    ghash = request.args.get("h")

    if ghash is None:
        msg = {'ERROR': 'Missing geohash ! Try /decode?h=<geohash>'}
        return jsonify(msg), 400

    try:
        result = geohash.decode(ghash)
        #data = {'latitude': result[0], 'longitude': result[1]}
        #response = jsonify(data)
        response = jsonify(Point(result))
        return response

    except:
        msg = {'ERROR': 'Could not decode the geohash'}
        return jsonify(msg), 400


if __name__ == "__main__":

    app.run(port=8080, threaded=True)
