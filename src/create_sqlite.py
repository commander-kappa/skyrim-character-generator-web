import sqlalchemy, sqlite3
from sqlalchemy import text, Table, Column, Boolean,  Integer, SmallInteger, String, MetaData, ForeignKey, select, insert, func
from sqlalchemy import create_engine
from os import path, getcwd
from sqlalchemy.orm import sessionmaker, mapper, relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import IntegrityError

DIR_PATH = f"{path.dirname(path.abspath(__file__))}"
DB_NAME = 'chargen.db'
DB_PATH = path.join(DIR_PATH, DB_NAME)

ENGINE = create_engine(f"sqlite:///{DB_PATH}", connect_args={"autocommit": False})

meta = MetaData()
Base = declarative_base()
Session = sessionmaker(bind=ENGINE)

race_table = Table(
    "race",
    meta,
    Column("id", SmallInteger, primary_key=True, nullable=False, autoincrement=True),
    Column("name", String(32), nullable=False)
)

sign_table = Table(
    "sign",
    meta,
    Column("id", SmallInteger, primary_key=True, nullable=False, autoincrement=True),
    Column("name", String(32), nullable=False),                                  
    Column("class_name", String(16), nullable=True)                                  
)

skill_table = Table(
    "skill",
    meta,
    Column("id", SmallInteger, primary_key=True, nullable=False, autoincrement=True),
    Column("name", String(32), nullable=False),
    Column("class_name", String(16), nullable=False)                                  
)

personality_table = Table(
    "personality",
    meta,
    Column("id", SmallInteger, primary_key=True, nullable=False, autoincrement=True),
    Column("name", String(32), nullable=False)                                  
)

start_table = Table(
    "start",
    meta,
    Column("id", SmallInteger, primary_key=True, nullable=False, autoincrement=True),
    Column("name", String(64), nullable=False),                                  
    Column("race", SmallInteger, ForeignKey("race.id"), nullable=True),
    Column("specification", Boolean, nullable=False)

)

specification_table = Table(
    "specification",
    meta,
    Column("id", SmallInteger, primary_key=True, nullable=False, autoincrement=True),
    Column("start", SmallInteger, ForeignKey("start.id"), nullable=False),
    Column("name", String(64), nullable=False)
)

religion_table = Table(
    "religion",
    meta,
    Column("id", SmallInteger, primary_key=True, nullable=False, autoincrement=True),
    Column("name", String(32), nullable=False)                                  
)

race_religion_table = Table(
    "race_to_religion",
    meta,
    Column("race", SmallInteger, ForeignKey("race.id"), primary_key=True, nullable=False),
    Column("religion", SmallInteger, ForeignKey("religion.id"), primary_key=True, nullable=False)                                
)

skill_mn_table = Table(
    "skill_to_skill",
    meta,
    Column("one", SmallInteger, ForeignKey("skill.id"), primary_key=True, nullable=False),
    Column("two", SmallInteger, ForeignKey("skill.id"), primary_key=True, nullable=False),
)

sheet_table = Table(
    "sheet",
    meta,
    Column("id", Integer, primary_key=True, nullable=False, autoincrement=True),
    Column("name", String(32), nullable=False),
    Column("race", SmallInteger, ForeignKey("race.id"), nullable=False),
    Column("religion", SmallInteger, ForeignKey("religion.id"), nullable=False),
    Column("sign", SmallInteger, ForeignKey("sign.id"), nullable=False),
    Column("personality", SmallInteger, ForeignKey("personality.id"), nullable=False),
    Column("start", SmallInteger, ForeignKey("start.id"), nullable=False),
    Column("specification", SmallInteger, ForeignKey("specification.id"), nullable=True),
    Column("skill_one", SmallInteger, ForeignKey("skill.id"), nullable=False),
    Column("skill_two", SmallInteger, ForeignKey("skill.id"), nullable=False),
    Column("skill_three", SmallInteger, ForeignKey("skill.id"), nullable=False)        
)
meta.create_all(ENGINE)

def two_c(tab, arr):
    with Session() as se:
        i = 1
        for e in arr:
            st = insert(tab).values(id=i, name=e)
            se.execute(st)
            i = i +1
        se.commit()

Origin_Race = ["Altmer", "Argonian", "Bosmer", "Breton", "Dunmer", "Imperial", "Khajiit", "Nord", "Orc", "Redguard"]
two_c(race_table, Origin_Race)

bm = "Mage"; bt ="Thief"; bw ="Warrior"
Origin_Birthsign = [
    ["The Ritual", bm],
    ["The Lover", bt],
    ["The Lord", bw],
    ["The Mage", bm],
    ["The Shadow", bt],
    ["The Steed", bw],
    ["The Apprentice", bm],
    ["The Warrior", bw],
    ["The Lady", bw],
    ["The Tower", bt],
    ["The Atronarch", bm],
    ["The Thief", bt],
    ["The Serpent", None]
]

with Session() as se:
    i = 1
    for sign in Origin_Birthsign:
        kw = {
            'id': i,
            'name': sign[0],
            'class_name': sign[1]
        }
        st = insert(sign_table).values(**kw)
        se.execute(st)
        i = i + 1
    se.commit()

Origin_Personality = ["Lawful Good", "Neutral Good", "Chaotic Good", "Lawful Neutral", "Lawful Evil", "Chaotic Neutral", "Chaotic Evil", "Neutral Evil", "True Neutral"]
two_c(personality_table, Origin_Personality)

rel_race = [
    ["Auriel", "Jephre", "Magnus", "Phynaster", "Stendarr", "Trinimac", "Xarxes", "Syrabane"],
    ["Sithis", "The Hist"],
    ["Arkay", "Auriel", "Hircine", "Jephre", "Mangus", "Mara", "Stendarr", "Xarxes", "Z'en"],
    ["Arkay", "Akatosh", "Magnus", "Mara", "Dibella", "Phynaster", "Xarxes", "Zenithar", "Stendarr"],
    ["Mephala", "Boethia", "Azura", "Molag Bal", "Malacath", "Mehrunes Dagon", "Sheogorath"],
    ["Akatosh", "Arkay", "Stendarr", "Julianos", "Dibella", "Mara", "Kynareth", "Zenithar", "Talos"],
    ["Azura", "Akatosh", "Mehrunes Dagon", "Kynareth", "Mephala", "Sheogorath", "Rajhin", "Riddle'Thar"],
    ["Akatosh", "Arkay", "Kynareth", "Mara", "Dibella", "Zenithar", "Stendarr", "Talos", "Shor"],
    ["Malacath", "Trinimac"],
    ["Leki", "Morwha", "Satakal", "Tall Papa", "The HoonDing"]
]
rel_mn = []; rel_out = []


for i in range(len(rel_race)):
    for e in rel_race[i]:
        if e not in rel_out:
            rel_out.append(e)
        j = rel_out.index(e)
        rel_mn.append([i+1, j+1])


two_c(religion_table, rel_out)

with Session() as se:
    for e in rel_mn:
        st = insert(race_religion_table).values(race=e[0], religion=e[1])
        se.execute(st)
    se.commit()


MageSkills = ["Alteration", "Conjuration", "Destruction", "Enchanting", "Illusion", "Restoration"]
WarriorSkills = ["Archery", "Block", "Heavy Armor", "Smithing", "One Handed", "Two Handed"]
ThiefSkills = ["Sneak", "Speechcraft", "Pickpocket", "Lockpicking", "Light Armor", "Alchemy"]
AllSkills = [MageSkills, WarriorSkills, ThiefSkills]
AllNames = ["Mage", "Warrior", "Thief"]

with Session() as se:
    c = 1
    for i in range(3):
        for j in range(len(AllSkills[i])):
            kw = {
                'id': c,
                'name': AllSkills[i][j],
                'class_name': AllNames[i]
            }
            st = insert(skill_table).values(**kw)
            se.execute(st)
            c = c + 1
    se.commit()


allSkill2 = MageSkills + WarriorSkills + ThiefSkills
print(allSkill2)
skillDict = {
    allSkill2.index("Archery"): [allSkill2.index("Block")],
    allSkill2.index("One Handed"): [allSkill2.index("Two Handed")],
    allSkill2.index("Heavy Armor"): [allSkill2.index("Light Armor"),
                                     allSkill2.index("Sneak"),
                                     allSkill2.index("Pickpocket")]
}

with Session() as se:
    for key in skillDict.keys():
        for sk in skillDict[key]:
            st = insert(skill_mn_table).values(one=key + 1, two=sk + 1)
            se.execute(st)
    se.commit()

Origin_AlternateStart = [
    ["Caught Crossing the Border Illegally", 0], 
    ["Escaping the Cell", 0],
    ["Arrived by Ship", 1], 
    ["Property Owner", 1], 
    ["Guild Member", 1],
    ["Patron at an Inn", 1], 
   	["Outlaw in the Wilds", 0],
   	["Soldier in the Army", 1],
   	["Camping in the Woods", 0], 
   	["Shipwrecked off the Coast", 0], 
   	["Attacked and Left for Dead", 0], 
   	["Vampire in a Secluded Lair", 0], 
   	["Necromancer in a Hidden Lab", 0], 
   	["Vigilant of Stendarr", 0], 
   	["Warlock's Thrall", 0]
]

Origin_RaceStart = [
    ["Altmer Agent of the Thalmor", 1, 0],
    ["Argonian Dock Worker", 2, 0],
    ["Member of a Forsworn Tribe", 4, 0],
    ["Dunmer Refugee", 5, 1],
    ["Member of the Penitus Oculatus", 6, 0],
    ["Khajiit Caravan Guard", 7, 0],
    ["Erik the Slayer's Childhood Friend", 8, 0],
    ["Live in an Orc Stronghold", 9, 0],
    ["Redguard Alik'r Warrior", 10, 0]
]

def give_index(inStr):
    for i in range(len(Origin_AlternateStart)):
        if Origin_AlternateStart[i][0] == inStr:
            return i

def give_index2(inStr):
    for i in range(len(Origin_RaceStart)):
        if Origin_RaceStart[i][0] == inStr:
            return i


Origin_specification = [
    [["Arrived by Ship in Solitude", 
    "Arrived by Ship in Dawnstar", 
    "Arrived by Ship in Windhelm", 
    "Arrived by Ship in Raven Rock"], 
    give_index("Arrived by Ship") + 1],
    [["Owning Property in Whiterun", 
    "Owning Property in Solitude", 
    "Owning Property in Rifton", 
    "Owning Property in Markath", 
    "Owning Property in Falkreath", 
    "Owning Property in Morthal", 
    "Owning Property in Dawnstar", 
    "Owning a farmhouse"], 
    give_index("Property Owner") + 1],
    [["Member of the Mages College", 
    "Member of the Companions", 
    "Member of the Thieves Guild", 
    "Member of the Dark Brotherhood", 
    "Member of the Dawnguard", 
    "Member of Clan Volkihar"], 
    give_index("Guild Member") + 1],
    [["Patron at the Bannered Mare", 
    "Patron at the Sleeping Giant",
    "Patron at Nightgate Inn",
    "Patron at Candlehearth Hall",
    "Patron at Dead Man's Drink",
    "Patron at Four Shields Tavern",
    "Patron at The Winking Skeever",
    "Patron at Moorside Inn", 
    "Patron at Windpeak Inn",
    "Patron at Silver Blood Inn",
    "Patron at The Bee and Barb",
    "Patron at The Frozen Hearth"], 
    give_index("Patron at an Inn") + 1],
    [["Soldier of the Imperial Army", "Soldier of the Stormcloaks"],
    give_index("Soldier in the Army") + 1],
    [["Dunmer Refugee in Windhelm", "Dunmer Refugee in Raven Rock"],
    len(Origin_AlternateStart) + give_index2("Dunmer Refugee") +1]
]

with Session() as se:
    i = 1
    for e in Origin_AlternateStart:
        st = insert(start_table).values(id=i, name=e[0], specification=e[1])
        se.execute(st)
        i = i + 1
    se.commit()

with Session() as se:
    i = len(Origin_AlternateStart) + 1
    for e in Origin_RaceStart:
        st = insert(start_table).values(id=i, name=e[0], race=e[1], specification=e[2])
        se.execute(st)
        i = i + 1
    se.commit()

with Session() as se:
    i = 1
    for e in Origin_specification:
        for start in e[0]:
            st = insert(specification_table).values(id=i, name=start, start=e[1])
            se.execute(st)
            i = i + 1
        se.commit()
