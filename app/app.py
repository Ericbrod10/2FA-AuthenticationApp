from typing import List, Dict

import pytz
import simplejson as json
from flask import Flask, request, Response, redirect, abort, send_from_directory
from flask import render_template
from flask import url_for, flash, make_response
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import secrets
import datetime
import pyqrcode
from pyqrcode import QRCode
import random
import png
from flask import send_file
import os
from PIL import Image
from io import StringIO
from flask import request

# import ssl
# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# context.load_cert_chain("server.crt", "server.key")
'''
@app.route('/get_image')

def get_image():
    if request.args.get('type') == '1':
       filename = 'ok.gif'
    else:
       filename = 'error.gif'
    return send_file(filename, mimetype='image/gif')
'''
app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'PCN_Data'
mysql.init_app(app)
eastern = pytz.timezone("US/Eastern")
startingURL = 'https://100.8.177.164/ath/'


@app.route('/<int:player_id>', methods=['GET'])
def form_get(player_id):
    cursor = mysql.get_db().cursor()

    inputData = (player_id)
    searchQuery = """SELECT player_id
                    FROM PlayerLogTable 
                    WHERE player_id = %s AND MobileIP != 'NULL' """
    cursor.execute(searchQuery, inputData)
    CheckedResult = cursor.fetchall()
    if CheckedResult != ():
        result = "Checked"
        return render_template('index.html', title='Home', player_id=player_id, result=result)

    inputData = (player_id)
    searchQuery = """SELECT player_id
                    FROM PlayerLogTable 
                    WHERE player_id = %s AND MobileIP = 'NULL' """
    cursor.execute(searchQuery, inputData)
    result = cursor.fetchall()
    # return render_template('index.html', title='Home', player_id=player_id, result=result)
    if result != ():
        inputData = (player_id)

        linkGen = secrets.token_urlsafe(16)
        linkGenDb = linkGen
        linkGen = startingURL + linkGen
        ImgID = str(random.randint(1, 9999999))
        filename = 'QR_Code' + ImgID + '.png'
        path = '/app/' + filename
        try:
            os.remove(path)
        except:
            print('No File Deleted')

        url = pyqrcode.create(linkGen)
        url.png(path, scale=10)

        images = []
        im = Image.open(path)
        w, h = im.size
        aspect = 1.0 * w / h

        images.append({
            'width': int(w),
            'height': int(h),
            'src': filename
        })

        AthCode = str(random.randint(1, 99999))
            # redirectLink = '/'+str(player_id)
            # full_filename = os.path('QR_Code.png')
            # full_filename = {'image': open('QR_Code.png', 'rb')}

        res = make_response(render_template('index.html', title='Authenticator', athCode=AthCode,
                                                GenLink=linkGen, result=result, **{'images': images}))

        if not request.cookies.get('PCNCookie'):
            cookie = secrets.token_urlsafe(32)
            res.set_cookie('PCNCookie', cookie, max_age=60 * 60 * 24 * 365 * 5)
        else:
            cookie = request.cookies.get('PCNCookie')

        inputData = (int(AthCode), linkGenDb, int(player_id))

        sql_insert_query = """UPDATE PlayerLogTable SET AthCode = %s, linkGen = %s WHERE Player_ID = %s"""
        cursor.execute(sql_insert_query, inputData)
        mysql.get_db().commit()

            #  return send_file("QR_Code.png", mimetype='image/png')
        return res
    else:
        return render_template('index.html', title='Home', player_id=player_id, result=result)


@app.route('/<int:player_id>', methods=['POST'])
def form_insert_post(player_id):
    cursor = mysql.get_db().cursor()
    linkGen = secrets.token_urlsafe(16)
    linkGenDb = linkGen
    ### May need to as full URL here... ###
    linkGen = startingURL + linkGen
    ImgID = str(random.randint(1, 9999999))

    filename = 'QR_Code' + ImgID + '.png'
    path = '/app/' + filename

    try:
        os.remove(path)
    except:
        print('No File Deleted')

    url = pyqrcode.create(linkGen)
    url.png(path, scale=10)

    images = []
    im = Image.open(path)
    w, h = im.size
    aspect = 1.0 * w / h

    images.append({
        'width': int(w),
        'height': int(h),
        'src': filename
    })

    AthCode = str(random.randint(1, 99999))
    # redirectLink = '/'+str(player_id)
    # full_filename = os.path('QR_Code.png')
    # full_filename = {'image': open('QR_Code.png', 'rb')}

    res = make_response(render_template('index.html', title='Authenticator', athCode=AthCode,
                                        GenLink=linkGen, **{'images': images}))

    ComputerIp = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    if not request.cookies.get('PCNCookie'):
        cookie = secrets.token_urlsafe(32)
        res.set_cookie('PCNCookie', cookie, max_age=60 * 60 * 24 * 365 * 5)
    else:
        cookie = request.cookies.get('PCNCookie')

    LogTime = datetime.datetime.now(tz=eastern).strftime('%Y-%m-%d %H:%M:%S')

    inputData = (
        LogTime, int(player_id), request.form.get('Gamertag'), cookie, ComputerIp, 'NULL', 'NULL', int(AthCode), linkGenDb)

    sql_insert_query = """INSERT INTO PlayerLogTable (LogTime, player_id, Gamertag, cookie, ComputerIP, MobileCookieID, 
    MobileIP, AthCode, linkGen) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()

    #  return send_file("QR_Code.png", mimetype='image/png')
    return res


@app.route('/<path:filename>')
def image(filename):
    try:
        w = int(request.args['w'])
        h = int(request.args['h'])
    except (KeyError, ValueError):
        return send_from_directory('.', filename)

    try:
        im = Image.open(filename)
        im.thumbnail((w, h), Image.ANTIALIAS)
        io = StringIO.StringIO()
        im.save(io, format='png')
        return Response(io.getvalue(), mimetype='image/png')

    except IOError:
        abort(404)

    return send_from_directory('.', filename)


@app.route('/ath/<string:linkGen>', methods=['GET'])
def mobileForm_get(linkGen):
    cursor = mysql.get_db().cursor()
    inputData = linkGen
    searchQuery = """SELECT *
                    FROM PlayerLogTable 
                    WHERE linkGen = %s AND MobileIP = 'NULL' """
    cursor.execute(searchQuery, inputData)
    result = cursor.fetchall()
    linkGen = linkGen
    if result != ():
        return render_template('mobile.html', title='Home', result=result, linkGen=linkGen)
    else:
        result = 'Invalid Link'
        return render_template('mobile.html', title='Home', result=result, linkGen=linkGen)


@app.route('/ath/<string:linkGen>', methods=['POST'])
def mobileForm_post(linkGen):
    cursor = mysql.get_db().cursor()
    linkGen = linkGen
    inputData = (linkGen, request.form.get('AthCode'))

    searchQuery = """SELECT *
                    FROM PlayerLogTable 
                    WHERE linkGen = %s AND AthCode = %s AND MobileIP = 'NULL' """
    cursor.execute(searchQuery, inputData)
    result = cursor.fetchall()
    if result != ():
        responder = 'Two-Factor Authentication Complete'
        res = make_response(render_template('mobile.html', title='Authenticator', responder=responder, linkGen=linkGen))

        if not request.cookies.get('MobileCookie-16-3-14'):
            cookie = secrets.token_urlsafe(32)
            res.set_cookie('MobileCookie-16-3-14', cookie, max_age=60 * 60 * 24 * 365 * 5)
        else:
            cookie = request.cookies.get('MobileCookie-16-3-14')

        MobileIp = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        UpdateInputData = (cookie, MobileIp, linkGen, request.form.get('AthCode'))
        UpdateQuery = """Update PlayerLogTable SET MobileCookieID = %s, MobileIP = %s
                            WHERE linkGen = %s AND AthCode = %s AND MobileIP = 'NULL' """
        cursor.execute(UpdateQuery, UpdateInputData)
        mysql.get_db().commit()

        return res
    else:
        responder = 'Invalid Code'
        return render_template('mobile.html', title='Home', responder=responder, linkGen=linkGen)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # app.run(host='0.0.0.0', debug=True, ssl_context=context)
