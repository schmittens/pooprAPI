#!flask/bin/python
from flask import Flask, jsonify, make_response, request
from helper import gps, db2, dbinfo, jsonMaker
from flaskext.mysql import MySQL
import datetime
from time import strftime

# from log import logger


app = Flask(__name__)


mysql = MySQL()


# instantiate dbinfo
db = dbinfo.info()


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = db.user
app.config['MYSQL_DATABASE_PASSWORD'] = db.pw
app.config['MYSQL_DATABASE_DB'] = db.db
app.config['MYSQL_DATABASE_HOST'] = db.host
mysql.init_app(app)


fieldNames = ['id', 'title', 'lat', 'lon', 'description',
              'imagepath', 'free', 'sex', 'unisex', 'services',
              'rating', 'confirmation', 'contested',
              'creator', 'created']



@app.before_first_request
def initialize():
    # app.logger.setLevel(logging.Info)
    print("initialize")


@app.before_request
def test_before():
    print("before_request")


#@app.after_request
#def test_after(response):
#    print("after_request")


@app.errorhandler(404)
def not_found(error):
    # logger.requestMetadata(request, "404 request")
    result = [{'error': str(error)}]
    # logger.logInfo(result)
    return make_response(jsonify(result), 404)


@app.errorhandler(405)
def not_allowed(error):
    # logger.requestMetadata(request, "405 request")
    result = [{'error': str(error)}]
    # logger.logInfo(result)
    return make_response(jsonify(result), 405)


@app.route('/api/')
@app.route('/')
def index():
    # logger.requestMetadata(request, "INDEX request")
    returnString = """

        <html>
        <p>You are at the index. There are no actions you can take here. The API structure is as follows:</p>

        <p>Get list of facilities near a given position, with radius in meters: /api/v1.0/facilities/lon=X&lat=Y&rad=Z</p>

        <p>Show a specific facility: /api/v1.0/facilities/show/123</p>

        <p>Confirm a user created facility: /api/v1.0/facilities/confirm/123</p>

        <p>Rate an existing facility: /api/v1.0/facilities/rate/123</p>

        <p>Dispute a user created facility: /api/v1.0/facilities/dispute/123</p>

        <p><strike>#Create a new facility: /api/v1.0/facilities/create</strike></p>
        </html>

    """

    return returnString


@app.route('/api/v1.0/facilities/show/<int:fid>', methods=['GET'])
def get_facility(fid):

    # logger.requestMetadata(request, "Show request")

    connection = mysql.connect()
    cursor = connection.cursor()

    try:
        cursor.callproc('facilities_get_by_id',[fid])
        data = cursor.fetchall()

        if len(data) == 1:
            return jsonMaker.make(data, fieldNames)

        else:
            return jsonify([{'error': 'facility {0} does not exist'.format(fid)}])

    except:
        return jsonify([{'error': 'could not get facility {0}'.format(fid)}])

    finally:
        cursor.close()
        connection.close()


@app.route('/api/v1.0/facilities/confirm/fid=<int:fid>&user=<string:user>', methods=['GET'])
def confirm_facility(fid, user):

    # logger.requestMetadata(request, "Confirm request")

    try:
        connection = mysql.connect()
        cursor = connection.cursor()

    except:
        return jsonify([{'error': 'database connection failed'}])

    try:
        cursor.callproc('facilities_verify_existence_by_id', [fid])
        fExists = cursor.fetchone()
        print(fExists)

        if fExists == None:
            return jsonify([{'error': 'facility {0} does not exist'.format(fid)}])

        cursor.callproc('confirms_get_by_id_user', [fid,user])
        uExists = cursor.fetchone()
        # prepare date one week ago
        minusOneWeek = datetime.datetime.today() - datetime.timedelta(days=7)
        # figure out time format, this returns datetime.datetime function!
        #print(uExists[0])
        #uExists = strftime('%Y-%m-%d %H:%M:%S',str(uExists[0]))
        #print(uExists)
        #print(minusOneWeek)

        if uExists:
            return jsonify([{'error': 'user {0} already confirmed facility {1}'.format(user,fid)}])

        cursor.callproc('facilities_confirm_by_id',[fid])
        data1 = cursor.fetchall()
        cursor.callproc('confirms_confirm_by_id_user',[fid,user])
        data2 = cursor.fetchall()
        if len(data1) == 0 & len(data2) == 0:
            connection.commit()
            return jsonify([{'success': 'facility {0} confirmed'.format(fid)}])
        else:
            return jsonify([{'error': 'confirmation of facility {0} failed'.format(fid)}])

    except:
        return jsonify([{'error': 'could not confirm facility {0} for user {1}'.format(fid,user)}])

    finally:
        cursor.close()
        connection.close()


@app.route('/api/v1.0/facilities/rate/fid=<int:fid>&rating=<int:rating>&user=<string:user>', methods=['GET'])
def rate_facility(fid, rating, user):

    # logger.requestMetadata(request, "Rate request")

    connection = mysql.connect()
    cursor = connection.cursor()

    try:
        cursor.callproc('facilities_verify_existence_by_id', [fid])
        exists = cursor.fetchone()

        if exists == None:
            return jsonify([{'error': 'facility {0} does not exist'.format(fid)}])

        cursor.callproc('ratings_get_by_id_user',[fid,user])
        uExists = cursor.fetchone()

        if uExists:
            return jsonify([{'error': 'user {0} already rated facility{1}'.format(user, fid)}])

        cursor.callproc('ratings_rate_by_id_rating_user', [fid, rating, user])
        data = cursor.fetchall()
        if len(data) == 0:
            connection.commit()
            return jsonify([{'success': 'facility {0} rated {1} by user {2}'.format(fid, rating, user)}])
        else:
            return jsonify([{'error': 'rating of facility {0} failed'.format(fid)}])

    except:
        return jsonify([{'error': 'could not rate ({0}) facility {1} for user {2}'.format(rating,fid,user)}])

    finally:
        cursor.close()
        connection.close()


@app.route('/api/v1.0/facilities/dispute/fid=<int:fid>&user=<string:user>', methods=['GET'])
def dispute_facility(fid, user):

    # logger.requestMetadata(request, "Dispute request")

    connection = mysql.connect()
    cursor = connection.cursor()

    try:
        cursor.callproc('facilities_verify_existence_by_id', [fid])
        exists = cursor.fetchone()

        if exists == None:
            return jsonify([{'error': 'facility {0} does not exist'.format(fid)}])

        cursor.callproc('disputes_dispute_by_id_user',(fid,user))
        uExists = cursor.fetchone()

        if uExists:
            return jsonify([{'error': 'user {0} already disputed facility {1}'.format(user,fid)}])

        cursor.callproc('facilities_dispute_by_id', [fid])
        data = cursor.fetchall()
        if len(data) == 0:
            connection.commit()
            return jsonify([{'success': 'facility {0} disputed'.format(fid)}])
        else:
            return jsonify([{'error': 'dispute of facility {0} by user {1} failed'.format(fid,user)}])

    except:
        return jsonify([{'error': 'could not dispute facility {0} for user {1}'.format(fid,user)}])

    finally:
        cursor.close()
        connection.close()


@app.route('/api/v1.0/facilities/remove_dispute/<int:fid>', methods=['GET'])
def remove_dispute_facility(fid):

    # logger.requestMetadata(request, "Remove dispute request")

    connection = mysql.connect()
    cursor = connection.cursor()

    try:
        cursor.callproc('facilities_verify_existence_by_id', [fid])
        exists = cursor.fetchone()

        if exists == None:
            return jsonify([{'error': 'facility {0} does not exist'.format(fid)}])

        cursor.callproc('disputes_clear_disputes_by_id',[fid])
        dCleared = cursor.fetchall()
        cursor.callproc('facilities_remove_dispute_by_id',[fid])
        fCleared = cursor.fetchall()

        if len(dCleared) == 0 & len(fCleared) == 0:
            connection.commit()
            return jsonify([{'success': 'dispute removed from facility {0}'.format(fid)}])
        else:
            return jsonify([{'error': 'failed to remove dispute form facility {0}'.format(fid)}])

    except:
        return jsonify([{'error': 'could not remove dispute from facility {0}'.format(fid)}])

    finally:
        cursor.close()
        connection.close()


@app.route('/api/v1.0/facilities/position/lat=<string:lat>&lon=<string:lon>&rad=<int:rad>', methods=['GET'])
@app.route('/api/v1.0/facilities/position/lon=<string:lon>&lat=<string:lat>&rad=<int:rad>', methods=['GET'])
def get_facilities(lon, lat, rad):
    lon = float(lon)
    lat = float(lat)

    # print("lon: {}; lat: {}; rad: {}".format(lon, lat, rad))

    # logger.requestMetadata(request, "Position request")

    # print(bounded)

    # logger.logInfo(query, False)

    bounded = gps.calculateBounds(lon, lat, rad)

    connection = mysql.connect()
    cursor = connection.cursor()

    try:
        cursor.callproc('facilities_get_by_coordinate',(bounded["lowerLon"], bounded["upperLon"], bounded["lowerLat"], bounded["upperLat"]))
        data = cursor.fetchall()

        return jsonMaker.make(data, fieldNames)

    except:
        return jsonify([{'error':'could not get facilities for lat={0} lon={1} rad={2}'.format(lat, lon, rad)}])

    finally:
        cursor.close()
        connection.close()


@app.route('/api/v1.0/facilities/create', methods=['POST'])
def create_facility():

    # logger.requestMetadata(request, "Create request")

    # will have to get payload from request.get_json(), using dummy values for now
    values = ["'test title 3'", '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']

    query = """
       INSERT INTO `poopr_facilities`
       (%s)
       VALUES
       (%s)
    """ % (', '.join(fieldNames[1:-1]), ', '.join(values))

    print(query)

    # logger.logInfo(query, False)

    dbase = db2.SQL(query, fieldNames)
    return jsonify(dbase.run())


@app.route('/api/v1.0/request', methods=['POST'])
def test_request():
    # will not work with browser, use cURL instead:
    # curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d "{'json':{'data':'here'}}" http://theurl.com/to/post/to
    # values = ['test title', '1.0101', '2.0202', 'description', '/img', '1', 'male, female', '1', '1', '1', '1', '1', '1']
    print(request.data)
    print(request.get_json(force=True))
    print(request.headers, request.method, request.json)
    return jsonify([{"success":"data received"}])


if __name__ == '__main__':
    app.run(debug=True)