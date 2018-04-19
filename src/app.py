from flask import Flask, render_template, request, json, jsonify, g
import csv
import sqlite3

DATABASE = "housingdata.db"
app = Flask(__name__)

app.config.from_object(__name__)

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

@app.route("/")
def homepage():
    return render_template('homepage.html')
@app.route("/mainpage")
def mainpage():
    print("i am here")
    return render_template('index3.html')
@app.route("/data")
def print_data():
    cur = get_db().cursor()
    try:
        id = request.args.get("id")
        print(id)
    except ValueError:
        return "error here"
    result = execute_query(
        """SELECT TIME, VALUE
            FROM HOUSE_VALUE_BY_MONTH
            WHERE region_id = ? AND HOUSETYPE_ID= 1""",
            (id,)
    )
    str_rows = [','.join(map(str, row)) for row in result]

    header = 'time, value\n'
    cur.close()
    return header + '\n'.join(str_rows)

@app.route("/getregionname")
def get_region_name():
    cur = get_db().cursor()
    try:
        id = request.args.get("id")
        print(id)
    except ValueError:
        return "error here"
    result = execute_query(
        """SELECT NAME
            FROM REGION
            WHERE ID = ?""",
            (id,)
    )
    str_rows = [','.join(map(str, row)) for row in result]

    header = 'time, value\n'
    cur.close()

    return 'name\n' + result[0][0]





@app.route("/viewdb")
def viewdb():
    conn = sqlite3.connect('housingdata.csv')
    print("I get here")
    rows = execute_query("""SELECT * FROM test""")
    return '<br>'.join(str(row) for row in rows)
if __name__ == "__main__":
    app.run()
