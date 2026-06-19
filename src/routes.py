from flask.helpers import abort
from flask import render_template 
from flask import request

from sqlalchemy import exc as sqla_exc

import json

import model
import exceptions as exc 

def get_model(name:str):
    if name in model.TABLES:
        return getattr(model, name)
    else:
        raise exc.TableNotExists(f"Table {name} does not exist in model.py")

def get_query_json(table_name:str)-> list[dict]:
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
    
    @app.route('/submit', methods=['POST'])
    def submit():
        if request.method == 'POST':

            print(request.get_json()) 
            
            attributeValues = request.get_json()['vals']
            name =  request.get_json()['name']
            
            if len(attributeValues) != 9:
                return 'Invalid length', 200
            
            for val in attributeValues[:-1]:
                if val <= 0:
                    return 'Value equals NULL', 200
            
            for i in range(len(attributeValues)):
                query = get_query_json(model.SHEET_TABLES[i])
                if len(query) < attributeValues[i]:
                    print(query)
                    return f"Value out of range at Index {i}, len query: {len(query)}, val: {attributeValues[i]}", 200

            query = db.session.execute(db.select(model.RaceToReligion).filter_by(race=attributeValues[0])).scalars() 
            validReligions = []
            for row in query:
                validReligions.append(row.religion)
            if attributeValues[2] not in validReligions:
                return 'Invalid Religion', 200
            
            query = db.session.execute(db.select(model.SkillToSkill)).scalars() 
            for row in query:
                if row.one in attributeValues[3:6] and row.two in attributeValues[3:6]:
                    return 'Invalid Skill Combo', 200

            

            query = db.session.execute(db.select(model.Start).filter_by(id=attributeValues[-2])).scalar_one()
            
            if query.race is not None:
                if query.race != attributeValues[0]:
                    return 'Start cannot be chosen by Race', 200
            
            if query.specification:
                query = db.session.execute(db.select(model.Specification).filter_by(start=attributeValues[-2])).scalars() 
                validSpecifications = []
                for row in query:
                    validSpecifications.append(row.id)
                if attributeValues[-1] not in validSpecifications:
                    return 'Invalid Specification', 200
            else:
                attributeValues[-1] = None
            
            
            attributeValuesString = '' 
            for i in range(len(attributeValues)): 
                try:
                    query = db.session.execute(db.select(get_model(model.SHEET_TABLES[i])).filter_by(id=attributeValues[i])).scalar_one() 
                    attributeValuesString += f"{model.SHEET_TABLES[i]}: {query.name}\n"
                except sqla_exc.NoResultFound:
                    attributeValuesString += f"{model.SHEET_TABLES[i]}: None\n"

            
            try:
                newSheet = model.Sheet(name=name, attributes=attributeValues)
                db.session.add(newSheet)
                db.session.commit()
            except:
                return 'Server Error, Sheet could not be added to db', 200

            return f"Sheet Submitted\n{attributeValuesString}", 200
    
        else:
            return 'POST Method required', 404
    @app.route('/view/<int:id>')
    def view_sheet(id:int = 0):
        if id < 1:
            return 'Invalid ID'
        
        sheet = db.session.execute(db.select(model.Sheet).filter_by(id=id)).scalar_one() 
        resp = {
                'name': sheet.name,
                'race': db.session.execute(db.select(model.Race).filter_by(id=sheet.race)).scalar_one().name, 
                'sign': db.session.execute(db.select(model.Sign).filter_by(id=sheet.sign)).scalar_one().name, 
                'religion': db.session.execute(db.select(model.Religion).filter_by(id=sheet.religion)).scalar_one().name, 
                'skill_one': db.session.execute(db.select(model.Skill).filter_by(id=sheet.skill_one)).scalar_one().name, 
                'skill_two': db.session.execute(db.select(model.Skill).filter_by(id=sheet.skill_two)).scalar_one().name, 
                'skill_three': db.session.execute(db.select(model.Skill).filter_by(id=sheet.skill_three)).scalar_one().name, 
                'personality': db.session.execute(db.select(model.Personality).filter_by(id=sheet.personality)).scalar_one().name, 
                'start': db.session.execute(db.select(model.Start).filter_by(id=sheet.start)).scalar_one().name 
        }
        if sheet.specification is not None:
            resp['specification'] = db.session.execute(db.select(model.Specification).filter_by(id=sheet.specification)).scalar_one().name 
        else:
            resp['specification'] = 'None'
        
        return resp, 200

    @app.route("/")
    def index():
        tables = {}
        
        for table_name in model.TABLES[:-1]:
            tables[table_name] = get_query_json(table_name)

        return render_template('index.html', tables=tables)
