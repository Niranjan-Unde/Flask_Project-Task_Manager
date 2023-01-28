from flask import Flask,render_template,redirect,url_for,request
import pymysql

app=Flask(__name__)

db=None
cur=None
def connectDB():
    global db
    global cur
    db=pymysql.connect(host='localhost',user='root',password='root',database='python_test')
    cur=db.cursor()

def disconnectDB():
    cur.close()
    db.close()

def readAllRecords():
    connectDB()
    readQ='select * from todo'
    cur.execute(readQ)
    result=cur.fetchall()
    disconnectDB()
    return result

def insertrecord(task,status):
    connectDB()
    insertQ=f"insert into todo(task,status) values('{task}','{status}')"
    cur.execute(insertQ)
    db.commit()
    disconnectDB()

def deleterecord(tid):
    connectDB()
    deleteQ=f"delete from todo where id={tid}"
    cur.execute(deleteQ)
    db.commit()
    disconnectDB()

# def updaterecord(tid):
#     connectDB()
#     updateQ=f"delete from todo where id={tid}"
#     cur.execute(updateQ)
#     db.commit()
#     disconnectDB()

def readOneRecord(tid):
    connectDB()
    readOneQ=f'select * from todo where id={tid}'
    cur.execute(readOneQ)
    result=cur.fetchone()
    disconnectDB()
    return result

def updaterecord(task,status,tid):
    connectDB()
    updateQ=f"update todo set task='{task}', status='{status}' where id={tid}"
    cur.execute(updateQ)
    db.commit()
    disconnectDB()

@app.route('/')
def index():
    data=readAllRecords()
    return render_template('index.html',data=data)

@app.route('/insert')
def insert():
    return render_template('insert.html')

@app.route('/inserttask')
def inserttask():
    task=request.args.get('task')
    status=request.args.get('status')
    insertrecord(task,status)
    return redirect(url_for('index'))

@app.route('/delete/<tid>')
def delete(tid): 
    deleterecord(tid)
    return redirect(url_for('index'))

@app.route('/update/<tid>')
def update(tid):
    data=readOneRecord(tid)
    return render_template('update.html',data=data)

@app.route('/updatetask/<tid>')
def updatetask(tid):
    task=request.args.get('task')
    status=request.args.get('status')
    updaterecord(task,status,tid)
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)