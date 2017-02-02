from flask import Flask, jsonify, redirect, request
import pygeohash as pygeohash
from geojson import Point, Polygon

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

    result = pygeohash.encode(lat, lon)

    data = {'geohash': result}
    response = jsonify(data)
    return response


@app.route('/geohash/decode/<geohash>')
def decode(geohash):

    if geohash is None:
        msg = {'ERROR': 'Missing geohash ! Try /decode/<geohash>'}
        return jsonify(msg), 400

    exact_mode = request.args.get("exact")
    if exact_mode:

        try:
            # Returns four float values: latitude, longitude, the plus/minus error
            # for latitude (as a positive number) and the plus/minus
            # error for longitude (as a positive number).
            lat, lon, lat_err, lon_err = pygeohash.decode_exactly(geohash)

            print(lat)
            print(lon)
            print(lat_err)
            print(lon_err)

            # 1 ---- 2
            # |      |
            # 4 ---- 3
            #
            box1 = (lat - lat_err, lon + lon_err)
            box2 = (lat + lat_err, lon + lon_err)
            box3 = (lat + lat_err, lon - lon_err)
            box4 = (lat - lat_err, lon - lon_err)

            print(box1)
            print(box2)
            print(box3)
            print(box4)

            response = jsonify(Polygon([[box1, box2, box3, box4, box1]]))
            return response

        except:
            msg = {'ERROR': 'Could not decode the geohash'}
            return jsonify(msg), 400

    else:

        try:
            # Returning two float with latitude and longitude
            # containing only relevant digits and with trailing zeroes removed
            result = pygeohash.decode(geohash)

            # lat, lon to geojson point
            response = jsonify(Point(result))
            return response

        except:
            msg = {'ERROR': 'Could not decode the geohash'}
            return jsonify(msg), 400


@app.route('/geohash/precision/<geohash>')
def precision(geohash):

    if geohash is None:
        msg = {'ERROR': 'Missing geohash ! Try /precision/<geohash>'}
        return jsonify(msg), 400

    geohash_length = len(geohash)
    if geohash_length > 10:
        geohash_length = 10

    # Precision lookup table for geohashes (in meters)
    # from https://github.com/wdm0006/pygeohash/blob/master/pygeohash/distances.py
    PRECISION = {
        0: 20000000,
        1: 5003530,
        2: 625441,
        3: 123264,
        4: 19545,
        5: 3803,
        6: 610,
        7: 118,
        8: 19,
        9: 3.71,
        10: 0.6,
    }

    result = PRECISION[geohash_length]
    data = {'precision' : { 'number': result, 'unit': 'meters'}}
    response = jsonify(data)
    return response

if __name__ == "__main__":

    app.run(port=8080, threaded=True)
