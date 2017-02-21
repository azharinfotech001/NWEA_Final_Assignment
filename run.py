from flask import Flask, request, g, jsonify
import json

import sqlite3

DATABASE = 'blog.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory  = g._database.row_factory = sqlite3.Row
    return db

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/post', methods=['POST'])
def create():
    body = request.json.get('body')
    title = request.json.get('title')
    # validations whether required paramaters are provided in the json
    if not body:
        return jsonify (
            error="please provide 'body' parameter"), 400
    if not title:
        return jsonify (
            error="please provide 'title' parameter"), 400

    db = get_db()
    cur = db.cursor()
    countSql = """select count(*) from posts;"""
    cur.execute(countSql);
    _id = cur.fetchone()[0]+1
    sql = """insert into posts (post_id, title, body) values (?, ?, ?)"""
    cur.execute(sql,[_id, body, title])
    db.commit()
    return jsonify(msg= "Success",id=_id), 200


@app.route('/posts', methods=['GET'])
def list():
    db = get_db()
    cur = db.cursor()
    sql = """select * from posts"""
    cur.execute(sql)
    rows = cur.fetchall()
    dictList = [dict(ix) for ix in rows] 
    return jsonify(posts = dictList, count = len(dictList)), 200

if __name__ == '__main__':
    app.run()