from flask import Flask, render_template, request, flash, redirect, url_for, session, send_file
from datetime import timedelta
from app import app, db
from app.models import Model, User, Result
import os, random, datetime
import tensorflow as tf
from flask_socketio import emit
from . import socketio
import random
import numpy as np
import json

model = {}

model['weekday_p5_heating'] = tf.keras.models.load_model('app/models/0301_P5_weekday.h5')
model['weekday_p5_holding'] = tf.keras.models.load_model('app/models/0301_P5_weekday_h.h5')
model['weekend_p5_heating'] = tf.keras.models.load_model('app/models/0301_P5_weekend.h5')
model['weekend_p5_holding'] = tf.keras.models.load_model('app/models/0301_P5_weekend_h.h5')

model['weekday_p15_heating'] = tf.keras.models.load_model('app/models/0303_P15_weekday.h5')
model['weekday_p15_holding'] = tf.keras.models.load_model('app/models/0303_P15_weekday_h.h5')
model['weekend_p15_heating'] = tf.keras.models.load_model('app/models/0303_P15_weekend.h5')
model['weekend_p15_holding'] = tf.keras.models.load_model('app/models/0303_P15_weekend_h.h5')

@app.before_request
def make_session_permanent():
    None
    # session.permanent = True
    # app.permanent_session_lifetime = timedelta(minutes=30)

def checkuser(id, pw):
    result = db.session.query(User).filter_by(id = id).first()
    if result is None or result.pw != pw:
        return False
    return True

def insertProduceData(title, date, content, file): 
    try:              
        if file.filename == '':
            db.session.add(Model(title, content, date, None))
            db.session.commit()
            return True
        else:
            s_name, s_ext = os.path.splitext(file.filename)            
            i = 2
            list = os.listdir('app/models/')
            while True:
                if file.filename in list:
                    file.filename = s_name+'({0})'.format(i)+s_ext
                    i += 1
                else:
                    break  
            file.save('app/models/{0}'.format(file.filename)) 
            db.session.add(Model(title, content, date, file.filename))            
            db.session.commit()           
            return True
    except:
        return False
def getPageNum():    
    modelnum = len(db.session.query(Model).all())
    if modelnum % 10 == 0:
        return modelnum/10
    else:
        return modelnum/10 + 1

def getContent(pn):    
    rows = db.session.query(Model).order_by(db.desc(Model.no))[(int(pn)-1) * 10 : (int(pn)-1) * 10 + 10]
    return rows

def getNoContent(no):
    return db.session.query(Model).filter_by(no = no).first()   

@app.route('/loginFail', methods=['GET'])
def loginFail():    
    return render_template('loginFail.html')

@app.route('/realtime/P5', methods = ['GET'])
def realtimeP5():
    return render_template('realtimeP5.html')

@app.route('/realtime/P8', methods = ['GET'])
def realtimeP8():
    return render_template('realtimeP8.html')

@app.route('/realtime/P15', methods = ['GET'])
def realtimeP15():
    return render_template('realtimeP15.html')

@app.route('/home', methods = ['GET'])
def home():
    return render_template('home.html', id = session['id'], time = session['time'])

@app.route('/models/<file>', methods = ['GET'])
def fileDownload(file):    
    file_name = 'app/models/{0}'.format(file)
    return send_file(file_name, as_attachment=True)

@app.route('/produce/content/<no>', methods = ['GET'])
def getProduceContent(no):    
    return render_template('produce/board.html', id = session['id'], row = getNoContent(no), time = session['time'])

@app.route('/getProduceResult', methods = ['POST'])
def getProduceResult():
    file = request.files['file']
    file.filename = file.filename + str(random.randrange(1,4096))
    file.save('app/temp/'+ file.filename)
    new_model = tf.keras.models.load_model('app/temp/'+file.filename)
    stringlist = []
    new_model.summary(print_fn=lambda x:stringlist.append(x))
    short_model_summary = "\n".join(stringlist)
    os.remove('app/temp/'+file.filename)
    return short_model_summary

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('login'))

#index
@app.route('/produce/index/<pn>')
def produce(pn):
    if 'id' not in session:
        return redirect(url_for('login'))
    return render_template('produce/index.html', id = session['id'], rows = getContent(pn), time = session['time'], pn = int(pn), pageNum = int(getPageNum()))

#쓰기
@app.route('/produce/write', methods=['POST', 'GET'])
def produceWrite():
    if request.method == 'POST':
        if insertProduceData(request.form['modelTitle'], request.form['modelDate'], request.form['modelContent'], request.files['modelFile']):
            return redirect(url_for('produce', pn = 1))
        else:
            return 'Error!'
    return render_template('produce/write.html', id = session['id'], time = session['time'])

@app.route('/perform/index')
def perform():
    if 'id' not in session:
        return redirect(url_for('login'))
    return render_template('perform/index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():    
    if request.method == 'POST':
        if checkuser(request.form['id'], request.form['pw']):
            session['id'] = request.form['id']
            session['time'] = datetime.datetime.now()
            return redirect(url_for('home'))
        else:
            return redirect(url_for('loginFail'))
    if 'id' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

# 로그인
@app.route('/', methods=['POST', 'GET'])
def main():    
    return redirect(url_for('login'))


#TEST CODE


@socketio.on('my_broadcast_event')
def test_broadcast_message(model_name, press_code, message):    
    emit(model_name, {'data': message['data']}, broadcast=True , namespace='/'+press_code)

@app.route('/t/<week_type>/<press_code>/<section_type>', methods= ['GET', 'POST'])
def test(week_type, press_code, section_type):    

    data = np.array(request.get_json('data')['data'])
    data1 = data.reshape(1,10,3)
    #min-max scaling
    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler()
    test_data = scaler.fit_transform(data)

    test_data = test_data.reshape(1,10,3)

    #min-max Scaling ##1

    min_val = np.array([np.min(data1[:,0]), np.min(data1[:,1]), 0])
    max_val = np.array([np.max(data1[:,0]), np.max(data1[:,1]), 1])

    for n, m in enumerate(data1):
        data1[n] = (m - min_val) / (max_val - min_val)
   
    model_name = week_type + '_' + press_code + '_' + section_type

    y_pred = model[model_name].predict(test_data)
    print(y_pred)   
    ress = y_pred.astype(int)
    
    test_broadcast_message('0101', press_code,
        {'data' : 
            {
                'data':     data.tolist(),
                'result':   ress.tolist()
            }
        },        
    )
    
    return "{result:" + str(y_pred.reshape(1)) + "}"