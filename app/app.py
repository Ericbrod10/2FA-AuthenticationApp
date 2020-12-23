from typing import List, Dict

import pytz
import simplejson as json
from flask import Flask, request, Response, redirect
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


@app.route('/<int:player_id>', methods=['GET'])
def form_get(player_id):
    cursor = mysql.get_db().cursor()
    return render_template('index.html', title='Home', player_id=player_id)


@app.route('/<int:player_id>', methods=['POST'])
def form_insert_post(player_id):
    cursor = mysql.get_db().cursor()
    linkGen = secrets.token_urlsafe(16)
    ### May need to as full URL here... ###
    linkGen = '/' + linkGen

    url = pyqrcode.create(linkGen)
    url.png('QR_Code.png', scale=10)

    AthCode = str(random.randint(1, 99999))
    # redirectLink = '/'+str(player_id)
    # full_filename = os.path('QR_Code.png')
    # full_filename = {'image': open('QR_Code.png', 'rb')}

    res = make_response(render_template('index.html', title='Authenticator', img=full_filename, athCode=AthCode,
                                        GenLink=linkGen))
    # res = make_response(redirect('/<int:player_id>', code=302), )
    # res.data(title='Authenticator', player_id=player_id, athCode=AthCode)
    if not request.cookies.get('PCNCookie'):
        cookie = secrets.token_urlsafe(32)
        res.set_cookie('PCNCookie', cookie, max_age=60 * 60 * 24 * 365 * 5)
    else:
        cookie = request.cookies.get('PCNCookie')

    LogTime = datetime.datetime.now(tz=eastern).strftime('%Y-%m-%d %H:%M:%S')

    inputData = (
        LogTime, int(player_id), request.form.get('Gamertag'), cookie, 'NULL', 'NULL', 'NULL', int(AthCode), linkGen)

    sql_insert_query = """INSERT INTO PlayerLogTable (LogTime, player_id, Gamertag, cookie, ComputerIP, MobileCookieID, 
    MobileIP, AthCode, linkGen) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()

    #  return send_file("QR_Code.png", mimetype='image/png')
    return res


@app.route('/imgGen')
def GetImage():
    filename = request.form_get('GenLink')
    filename = '/' + filename
    url = pyqrcode.create(filename)
    url.png('QR_Code.png', scale=10)
    return send_file("QR_Code.png", mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
