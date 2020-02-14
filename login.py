import pymysql
from flask import Flask, render_template, redirect, url_for, request, make_response, session
from datetime import timedelta
from werkzeug import secure_filename
import os
from flask import send_file

app = Flask(__name__)
app.secret_key = 'pknu'

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

def check(id, pw):
	conn = pymysql.connect(host="localhost", user="root", password="1234",
                       db='login', charset='utf8')
	curs = conn.cursor()
	sql = "select * from login"
	curs.execute(sql)
	row = curs.fetchone()
	while row is not None:			
		if id == row[0] and pw == row[1]:
			conn.close()
			return True		
		row = curs.fetchone()
	conn.close()
	return False

def sign(id, pw):
	conn = pymysql.connect(host="localhost", user="root", password="1234",
                       db='login', charset='utf8')
	curs = conn.cursor()
	try:
		sql = "insert into login values (%s, %s)"
		curs.execute(sql, (id, pw))
		conn.commit()
		conn.close()
		return True
	except:
		conn.close()
		return False

def get():
	conn = pymysql.connect(host="localhost", user="root", password="1234",
                       db='test', charset='utf8')
	curs = conn.cursor()
	sql = "select * from board order by no desc"
	curs.execute(sql)
	rows = curs.fetchall()
	conn.close()
	return rows

def insert(title, writer, content, file):
	conn = pymysql.connect(host="localhost", user="root", password="1234",
                       db='test', charset='utf8')
	curs = conn.cursor()
	if file is None:
		sql = "insert into board (title, writer, contents, date) values (%s, %s, %s, now())"
		curs.execute(sql, (title, writer, content))
	else:
		sql = "insert into board (title, writer, contents, date, file) values (%s, %s, %s, now(), %s)"
		curs.execute(sql, (title, writer, content, file))
	conn.commit()
	conn.close()
	
def getcontent(num):
	conn = pymysql.connect(host="localhost", user="root", password="1234",
                       db='test', charset='utf8')
	curs = conn.cursor()		
	sql = "select * from board where no=%s"
	curs.execute(sql, num)
	row = curs.fetchone()
	conn.close()
	return row	

def getlist(num):
	conn = pymysql.connect(host="localhost", user="root", password="1234",
                       db='test', charset='utf8')
	curs = conn.cursor()
	sql = "select * from board order by no desc limit %s, 10"	
	curs.execute(sql, 10 * (int(num)-1))
	rows = curs.fetchall()
	conn.close()
	return rows

def contentNum():
	conn = pymysql.connect(host="localhost", user="root", password="1234",
                       db='test', charset='utf8')
	curs = conn.cursor()		
	sql = "select count(*) from board"
	curs.execute(sql)
	num = curs.fetchone()
	conn.close()
	return num[0]

@app.route('/write', methods = ['GET', 'POST'])
def write():
	if 'id' not in session:
		return render_template('home.html')
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']
		file = request.files['file']
		if file.filename == '':
			insert(title, session['id'], content, None)
		else:
			dir = session['id']
			if not os.path.isdir(dir):
				os.mkdir(dir)

			s_name, s_ext = os.path.splitext(file.filename)
			i = 2
			list = os.listdir('{0}/'.format(session['id']))
			while True:
				if file.filename in list:
					file.filename = s_name+'({0})'.format(i)+s_ext
					i += 1
				else:
					break		
			file.save('{0}/{1}'.format(session['id'], file.filename))
			insert(title, session['id'], content, file.filename)
		return redirect(url_for('list', num = 1))			
	else:
		return render_template('write.html')
	
@app.route('/home')
def home():	
	if 'id' in session:
		return redirect(url_for('list', num = 1))
	return render_template('home.html')

@app.route('/logout')
def logout():
   session.pop('id', None)
   return redirect(url_for('home'))

@app.route("/")
def main():	
	return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if 'id' in session:
		return redirect(url_for('list', num = 1))
	if request.method == 'POST':
		session['id'] = request.form['id']
		return redirect(url_for('list', num = 1))
	return render_template('login.html')

@app.route("/board/<num>", methods=['GET'])
def list(num):
	if 'id' not in session:
		return render_template('home.html')
	items = getlist(num)
	n = contentNum()//10
	if contentNum()%10 != 0:
		n += 1		
	return render_template('board.html', pn = int(num), rows = items, cnt = n)

@app.route("/board/content/<num>", methods=['GET'])
def content(num):
	if 'id' not in session:
		return render_template('home.html')
	row = getcontent(num)
	if row is None:
		return 'There are no posts.'
	return render_template('content.html', row = row)

@app.route("/download/<writer>/<file>", methods = ['GET'])
def download(writer, file):
	if 'id' not in session:
		return render_template('home.html')
	file_name = '{0}/{1}'.format(writer, file)
	return send_file(file_name, as_attachment=True)
	

if __name__ == "__main__":
	app.run(host='0.0.0.0')






