import psycopg2
from flask import Flask, jsonify, request
import re
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
CORS(app)


@app.route("/select", methods=['POST'])
def query_data():

    # create connection
    conn = psycopg2.connect("dbname=postgres user=jgmayc")
    conn.autocommit = True
    cur = conn.cursor()

    # get POST data
    content = request.get_json()

    statement = content['SQL']

    column_list = re.match('SELECT(.*)FROM', statement)
    column_list = ''.join(column_list.groups())
    column_list = list(column_list.split(','))




    # send SQL to database and catch results
    cur.execute(statement)
    result_list = cur.fetchall()
    cur.close()

    data = {}
    row_list = []

    for row in result_list:
        results = {}
        for property, value in zip(column_list, row):
            property = property.replace(' ', '')
            results[property] = str(value)
        row_list.append(results)
    data['data'] = row_list


    # return json results
    return jsonify(data)

@app.route("/dml", methods=['POST'])
def update_data():

    # create connection
    conn = psycopg2.connect("dbname=postgres user=jgmayc")
    conn.autocommit = True
    cur = conn.cursor()

    # get POST data
    content = request.get_json()

    statement = content['SQL']

    # send SQL to database
    cur.execute(statement)
    cur.close()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

if __name__ == "__main__":
    app.run()