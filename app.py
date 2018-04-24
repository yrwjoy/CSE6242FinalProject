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

@app.route("/linechart")
def print_data():
    cur = get_db().cursor()
    try:
        id = request.args.get("id")
        category = request.args.get("category")
        housetype = request.args.get("housetype")
        from_yr = request.args.get("fromyr")
        to_yr = request.args.get("toyr")
        from_date = sqlite3.datetime.datetime(int(from_yr), 1, 1, 0, 0)
        to_date = sqlite3.datetime.datetime(int(to_yr), 1, 1, 0, 0)
        print(id)
        print(category)
        print(housetype)
        print(from_yr)
        print(to_yr)

    except ValueError:
        return "error here"
    result = execute_query(
        """SELECT TIME, VALUE
            FROM
            (SELECT ID AS SELECTED_HOUSETYPE_ID
            FROM HOUSE_TYPE
            WHERE CATEGORY = ? AND HOUSE_TYPE = ?) LEFT JOIN  HOUSE_VALUE_BY_MONTH
            ON SELECTED_HOUSETYPE_ID = HOUSETYPE_ID
            WHERE region_id = ? AND TIME >= ? AND TIME <= ? AND VALUE IS NOT NULL""",
            (category,housetype,id, from_date, to_date)
    )

    domain = execute_query(
        """SELECT MIN(VALUE), MAX(VALUE)
            FROM
            (SELECT ID AS SELECTED_HOUSETYPE_ID
            FROM HOUSE_TYPE
            WHERE CATEGORY = ?) LEFT JOIN  HOUSE_VALUE_BY_MONTH
            ON SELECTED_HOUSETYPE_ID = HOUSETYPE_ID
            WHERE region_id = ? AND TIME >= ? AND TIME <= ? AND VALUE IS NOT NULL""",
            (category,id, from_date, to_date)
    )

    print domain
    str_rows = [','.join(map(str, row)) for row in result]
    header = 'time,value\n'
    cur.close()
    print header + '\n'.join(str_rows) + '\n' + str(domain[0][0]) + ',' + str(domain[0][1])
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

    cur.close()

    return 'name\n' + result[0][0]


@app.route("/getcurrentprice")
def get_current_price():
    cur = get_db().cursor()
    try:
        id = request.args.get("id")
        print(id)
    except ValueError:
        return "error here"
    result = execute_query(
        """SELECT VALUE 
        from HOUSE_VALUE_BY_MONTH 
        where REGION_ID = ? and TIME = "2018-02-01 00:00:00" and HOUSETYPE_ID =1""",
        (id,)
    )
    print "------------"
    print result[0][0]

    # header = 'time, price\n'

    cur.close()

    return 'price\n' + str(result[0][0])



@app.route("/yscale")
def get_yscale():
    cur = get_db().cursor()
    try:
        id = request.args.get("id")
        category = request.args.get("category")
        housetype = request.args.get("housetype")
        from_yr = request.args.get("fromyr")
        to_yr = request.args.get("toyr")
        from_date = sqlite3.datetime.datetime(int(from_yr), 1, 1, 0, 0)
        to_date = sqlite3.datetime.datetime(int(to_yr), 1, 1, 0, 0)
        print(id)
        print(category)
        print(housetype)
        print(from_yr)
        print(to_yr)

    except ValueError:
        return "error here"

    domain = execute_query(
        """SELECT MIN(VALUE), MAX(VALUE)
            FROM
            (SELECT ID AS SELECTED_HOUSETYPE_ID
            FROM HOUSE_TYPE
            WHERE CATEGORY = ?) LEFT JOIN  HOUSE_VALUE_BY_MONTH
            ON SELECTED_HOUSETYPE_ID = HOUSETYPE_ID
            WHERE region_id = ? AND TIME >= ? AND TIME <= ? AND VALUE IS NOT NULL""",
        (category, id, from_date, to_date)
    )

    print domain

    str_rows = [','.join(map(str, row)) for row in domain]

    header = 'minY,maxY\n'
    cur.close()
    return header + '\n'.join(str_rows)






@app.route("/viewdb")
def viewdb():
    conn = sqlite3.connect('housingdata.csv')
    print("I get here")
    rows = execute_query("""SELECT * FROM test""")
    return '<br>'.join(str(row) for row in rows)
if __name__ == "__main__":
    app.run()
