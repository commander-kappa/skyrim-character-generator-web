from flask.helpers import abort
from flask import render_template, request
import json

import model
import exceptions as exc

#TODO: VALIDATE SHEET

def get_model(name:str):
    if name in model.TABLES:
        return getattr(model, name)
    else:
        raise exc.TableNotExists(f"Table {name} does not exist in model.py")

def get_query_json(table_name:str)-> dict:
    query = get_model(table_name).query.all()
    out = []
    for item in query:
        json_obj = {}
        for column in getattr(model, table_name).__table__.columns:
            json_obj[column.name] = getattr(item, column.name)
        out.append(json_obj)
    return out


def register_routes(app, db):
    @app.template_filter('add_quotes')
    def add_quotes(inStr:str) -> str:
        return f"\"{inStr}\""

    @app.template_filter('idify')
    def idify(inStr:str) -> str:
        return inStr.replace(' ', '_').lower()

    @app.template_filter('get_table_json')
    def get_table_json(table_name:str) -> list:
        return f"{get_query_json(table_name)}"

    @app.route('/get/<path:table>')
    def get_table(table):
        try:
            return get_query_json(table)
        except exc.TableNotExists as e:
            print(e.message)
            abort(404)


    @app.route("/")
    def index():
        tables = {}
        
        for table_name in model.TABLES:
            tables[table_name] = get_query_json(table_name)

        return render_template('index.html', tables=tables)