from flask import Flask, render_template, request, flash
from flask_mysqldb import MySQL
# from fastapi import FastAPI

app = Flask(__name__, template_folder='template')
# MYSQL CONNECTION
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "ajay98"
app.config["MYSQL_DB"] = "employe"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usrnm = request.form['usrnm']
        mobno = request.form['mobno']
        email = request.form['email']
        psw = request.form['psw']
        psw1 = request.form['psw1']
        if psw == psw1:
            con = mysql.connection.cursor()
            sql = "insert into empreg(EmpName,MobNo,Email_ID,EmpPsw,EmpPsw1) value (%s,%s,%s,%s,%s)"
            con.execute(sql, [usrnm, mobno, email, psw, psw1])
            mysql.connection.commit()
            con.close()
            flash('User Details Added')
            return render_template("login.html")
        else:
            flash("Entered password was not same")
            return render_template("register.html")
    return render_template("register.html")


@app.route('/')
def login():
    return render_template("login.html")


@app.route('/', methods=['POST'])
def checkit():
    usrnm = request.form['usrnm']
    psw = request.form['psw']
    con = mysql.connection.cursor()
    con.execute("select * from empreg where EmpName='" + usrnm + "'and EmpPsw='" + psw + "'")
    res = con.fetchone()
    if res is None:
        return "Username or Password is Wrong"
    else:
        return "Logged in successfully"


if __name__ == '__main__':
    app.secret_key = "abc123"
    app.run(debug=True)
