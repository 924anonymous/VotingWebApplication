from flask import Flask,render_template,request,jsonify
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mark1'

mysql = MySQL(app)

def connectdb(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    return "Query Executed Sucessfully"

@app.route('/',methods=['GET','POST'])
def fend():
    # print(data,111111111111111111111111111111)
    query = "SELECT * FROM `votingdata`"
    cur1 = mysql.connection.cursor()
    cur1.execute(query)
    vrecords = cur1.fetchall()
    vrecords = list(vrecords)
    im = vrecords[0][1]
    dp = vrecords[1][1]
    jw = vrecords[2][1]
    # print(vrecords,1111111111)

    query1 = "SELECT * FROM `voters`"
    cur2 = mysql.connection.cursor()
    cur2.execute(query1)
    voters = []
    for i in cur2.fetchall():
        if i[0] != 'None':
            if len(i[0]) != 0:
                voters.append(i[0])
    # print(voters)
    return render_template('fend.html',im=im,dp=dp,jw=jw,voters=voters)



@app.route("/submitdata",methods=['GET','POST'])
def subdata():
    print(request.form.get('insert'))
    data=[]
    data.append(request.form.get('insert'))
    # print(data,11111111111111111111111111111)
    query1 = "SELECT * FROM `voters`"
    cur2 = mysql.connection.cursor()
    cur2.execute(query1)
    voters = []
    for i in cur2.fetchall():
        if len(i[0]) != 0:
            voters.append(i[0])
    print(voters)
    vname = request.form.get('votername')
    # print(vname,444444444444444444)
    if vname not in voters and len(vname)>0:
        if 'deadpool' in data:
            connectdb('''UPDATE `votingdata` SET `votes`= `votes`+1 WHERE `source`= "deadpool"''')
        elif 'ironman' in data:
            connectdb('''UPDATE `votingdata` SET `votes`= `votes`+1 WHERE `source`= "iron man"''')
        elif 'johnwick' in data:
            connectdb('''UPDATE `votingdata` SET `votes`= `votes`+1 WHERE `source`= "john wick"''')

    vname = request.form.get('votername')
    query2 = '''INSERT INTO `voters`(`voter`) VALUES ("{}")'''.format(vname)
    if vname not in voters:
        if len(vname)!=0 and vname != 'None':
            connectdb(query2)
    else:
        print("something is wrong")

    return jsonify({"data":"hi"})



if __name__ == "__main__":
    app.run(debug=True)


