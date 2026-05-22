from sqlalchemy import ForeignKey
from app import db

TABLES = []

class Race(db.Model):
    TABLES.append(__qualname__)
    __tablename__ = 'race'
    
    id = db.Column(db.SmallInteger, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
 
    def __str__(self): 
        return f"{self.name}"
   
    def __repr__(self): 
        return f"{self.id}, {self.name}"

class Sign(db.Model):
    TABLES.append(__qualname__)
    __tablename__ = 'sign'
    
    id = db.Column(db.SmallInteger, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    class_name = db.Column(db.String(32), nullable=False, name='class_name')

    def __repr__(self): 
        return f"{self.name}"

class Religion(db.Model):
    TABLES.append(__qualname__)
    __tablename__ = 'religion'
    
    id = db.Column(db.SmallInteger, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)

    def __repr__(self): 
        return f"{self.name}"

class Skill(db.Model):
    TABLES.append(__qualname__)
    __tablename__ = 'skill'
    
    id = db.Column(db.SmallInteger, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    class_name = db.Column(db.String(32), nullable=False, name='class_name')

    def __repr__(self): 
        return f"{self.name}"

class Personality(db.Model):
    TABLES.append(__qualname__)
    __tablename__ = 'personality'
    
    id = db.Column(db.SmallInteger, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)

    def __repr__(self): 
        return f"{self.name}"

class Start(db.Model):
    TABLES.append(__qualname__)
    __tablename__ = 'start'
    
    id = db.Column(db.SmallInteger, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    race = db.Column(db.SmallInteger, db.ForeignKey('race.id'), nullable=False)
    specification = db.Column(db.Boolean, nullable=False)

    def __repr__(self): 
        return f"{self.name}"

class Specification(db.Model):
    TABLES.append(__qualname__)
    __tablename__ = 'specification'
    
    id = db.Column(db.SmallInteger, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    start = db.Column(db.SmallInteger, db.ForeignKey('start.id'), nullable=False)

    def __repr__(self): 
        return f"{self.name}"

class RaceToReligion(db.Model):
    TABLES.append(__qualname__)
    __tablename__ = 'race_to_religion'
    
    race = db.Column(db.SmallInteger, db.ForeignKey('race.id'), primary_key=True, nullable=False)
    religion = db.Column(db.SmallInteger, db.ForeignKey('religion.id'), primary_key=True, nullable=False)

    def __repr__(self): 
        return f"{self.race} -> {self.religion}"

class SkillToSkill(db.Model):
    TABLES.append(__qualname__)
    __tablename__ = 'skill_to_skill'
    
    one = db.Column(db.SmallInteger, db.ForeignKey('skill.id'), primary_key=True, nullable=False)
    two = db.Column(db.SmallInteger, db.ForeignKey('skill.id'), primary_key=True, nullable=False)

    def __repr__(self): 
        return f"{self.one} -> {self.two}"

class Sheet(db.Model):
    #INFO: Sheets should be seperate
    #TABLES.append(__qualname__)
    __tablename__ = 'sheet'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    race = db.Column(db.SmallInteger, db.ForeignKey("race.id"), nullable=False)
    religion = db.Column(db.SmallInteger, db.ForeignKey("religion.id"), nullable=False)
    sign = db.Column(db.SmallInteger, db.ForeignKey("sign.id"), nullable=False)
    personality = db.Column(db.SmallInteger, db.ForeignKey("personality.id"), nullable=False)
    start = db.Column(db.SmallInteger, db.ForeignKey("start.id"), nullable=False)
    specification = db.Column(db.SmallInteger, db.ForeignKey("specification.id"), nullable=True)
    skill_one = db.Column(db.SmallInteger, db.ForeignKey("skill.id"), nullable=False)
    skill_two = db.Column(db.SmallInteger, db.ForeignKey("skill.id"), nullable=False)
    skill_three = db.Column(db.SmallInteger, db.ForeignKey("skill.id"), nullable=False)        