
# msa-geohash

Base32 Geoashing as a service. From wikipedia:

> Geohash is a geocoding system invented by Gustavo Niemeyer and placed into the public domain. It is a hierarchical spatial data structure which subdivides space into buckets of grid shape.

> Geohashes offer properties like arbitrary precision and the possibility of gradually removing characters from the end of the code to reduce its size (and gradually lose precision).

Built with [pygeohash](https://pypi.python.org/pypi/pygeohash) and [geojson](https://pypi.python.org/pypi/geojson).

## Quick start

Execute the microservice container with the following command :

    docker run -ti -p 9907:80 msagency/msa-geohash

## Example(s)

To get a geohash from a pair of coordinates, you can use the /encode url :

    $ curl 'http://localhost:9907/geohash/encode?lat=45.53617&lon=-73.62075'
    {
      "geohash": "f25eh9x52jq4"
    }

The same url also handles geojson points, via a http POST :

    $ curl -XPOST 'http://localhost:9907/geohash/encode' -H 'Content-Type: application/json' -d '{
      "coordinates": [
        -73.62075,
        45.53617
      ],
      "type": "Point"
    }'

    {
      "geohash": "f25eh9x52jq4"
    }

Decoding the geohash will return the coordinates, in geojson :

    $ curl 'http://localhost:9907/geohash/decode/f25eh9x52jq4'
    {
      "coordinates": [
        -73.62075,
        45.53617
      ],
      "type": "Point"
    }

Geohashes can be shortened to modify the area they cover, this can be evaluated with the /precision url :

    $ curl 'http://localhost:9907/geohash/precision/f25eh9x52jq4'
    {
      "precision": {
        "number": 0.6,
        "unit": "meters"
      }
    }

    $ curl 'http://localhost:9907/geohash/precision/f25eh9'
    {
      "precision": {
        "number": 610,
        "unit": "meters"
      }
    }

By default the /decode function will return the center of the geohash area, however it's possible to get a more accurate decoding with the `exact=true` parameter. With this parameter a geojson polygon will be returned instead of a point, taking into account the margin of error of the geohash :

    $ curl 'http://localhost:9907/geohash/decode/f25eh9?exact=true'
    {
      "coordinates": [
        [
          [
            -73.63037109375,
            45.538330078125
          ],
          [
            -73.63037109375,
            45.5328369140625
          ],
          [
            -73.619384765625,
            45.5328369140625
          ],
          [
            -73.619384765625,
            45.538330078125
          ],
          [
            -73.63037109375,
            45.538330078125
          ]
        ]
      ],
      "type": "Polygon"
    }


## Endpoints

- [/geohash/encode/?lat=XX.XX&lon=XX.XX ](/geohash/encode?lat=45.53617&lon=-73.62075) Compute a geohash from the given lat,lon
- [/geohash/decode/:geohash](/geohash/decode/f25eh9x52jq4) Decode a geohash, returns a geojson point
- [/geohash/decode/:geohash?exact=true](/geohash/decode/f25eh9x52jq4) Decodes a geohash, return a geojson polygon
- [/geohash/precision/:geohash](/geohash/precision/f25eh9x52jq4) Estimate the precision of a geohash

## Standard endpoints

- [/ms/version](/ms/version) : returns the version number
- [/ms/name](/ms/name) : returns the name
- [/ms/readme.md](/ms/readme.md) : returns the readme (this file)
- [/ms/readme.html](/ms/readme.html) : returns the readme as html
- [/swagger/swagger.json](/swagger/swagger.json) : returns the swagger api documentation
- [/swagger/#/](/swagger/#/) : returns swagger-ui displaying the api documentation
- [/nginx/stats.json](/nginx/stats.json) : returns stats about Nginx
- [/nginx/stats.html](/nginx/stats.html) : returns a dashboard displaying the stats from Nginx

## About

A project by the [Microservices Agency](http://microservices.agency).
