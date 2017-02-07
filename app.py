#
# References
# https://en.wikipedia.org/wiki/Geohash
# http://geojson.org/geojson-spec.html
# http://www.macwright.org/2015/03/23/geojson-second-bite.html
#
from flask import Flask, jsonify, redirect, request
import pygeohash as pygeohash
import geojson
import json

app = Flask(__name__)


@app.route('/geohash/encode', methods=['GET'])
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


@app.route('/geohash/encode', methods=['POST'])
def encode_from_geojson():

    try:
        data = request.json

        if data['type'] == 'Point':

            # remember that geohash uses lat,lon
            # but geojson uses lon,lat
            lon = data['coordinates'][0]
            lat = data['coordinates'][1]

            result = pygeohash.encode(lat, lon)

            data = {'geohash': result}
            response = jsonify(data)
            return response

        else:
            msg = {'ERROR': 'Geojson type is not a Point'}
            return jsonify(msg), 400

    except Exception as e:
        print(e)
        msg = {'ERROR': 'Could not parse geojson.'}
        return jsonify(msg), 400


    return ""



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

            # 1 ---- 4
            # |      |
            # 2 ---- 3
            #
            box1 = (lon - lon_err, lat + lat_err)
            box2 = (lon - lon_err, lat - lat_err)
            box3 = (lon + lon_err, lat - lat_err)
            box4 = (lon + lon_err, lat + lat_err)

            response = jsonify(geojson.Polygon([[box1, box2, box3, box4, box1]]))
            return response

        except Exception as e:
            print(e)
            msg = {'ERROR': 'Could not decode the geohash'}
            return jsonify(msg), 400

    else:

        try:
            # Returning two float with latitude and longitude
            # containing only relevant digits and with trailing zeroes removed
            lat, lon = pygeohash.decode(geohash)

            #lat = result[0]
            #lon = result[1]

            # lat, lon to geojson point
            response = jsonify(geojson.Point([lon, lat]))
            return response

        except Exception as e:
            print(e)
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
