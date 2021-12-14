#!/usr/bin/env python3

import json
import os.path
from pathlib import Path
import sqlite3
import re
import os


# In AbstractMySQLDriver.php line 74:
#   An exception occurred while executing 'INSERT INTO subtype (code, name) VALUES (?, ?)
#   ' with params ["starfighter-x-wing", "Starfighter: X-wing"]:
#   SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry 'starfighter-x-
#   wing' for key 'type_code_idx'



json_details = {
  "cycles":   {"parsed":[], "out":[], "jsonOutFile": "cycles.json"},
  "rarities": {"parsed":[], "out":[], "jsonOutFile": "rarities.json"},
  "sets":     {"parsed":[], "out":[], "jsonOutFile": "sets.json"},
  "sides":    {"parsed":[], "out":[], "jsonOutFile": "sides.json"},
  "subtypes": {"parsed":[], "out":[], "jsonOutFile": "subtypes.json"},
  "types":    {"parsed":[], "out":[], "jsonOutFile": "types.json"},
}

cycles = {
           "full":{
             "code": "full",
             "name": "Full Sets",
             "position": 1,
             "size": 0
             },
           "premium":{
             "code": "premium",
             "name": "Premium Sets",
             "position": 2,
             "size": 0
             },
           "virtual":{
             "code": "virtual",
             "name": "Virtual Sets",
             "position": 3,
             "size": 0
             },
           "shields":{
             "code": "shields",
             "name": "Defensive Shields",
             "position": 4,
             "size": 0
             }
          }

swccgdb_dir = "swccgdb_json"
if not os.path.exists(swccgdb_dir):
  os.mkdir(swccgdb_dir)

swccgdb_db_filename = "swccgdb_json/swccgdb.db"
if os.path.isdir("swccgdb_json"):
  if os.path.isfile(swccgdb_db_filename):
    print("Removing stale %s" % swccgdb_db_filename)
    os.remove(swccgdb_db_filename)

con = sqlite3.connect(swccgdb_db_filename)
cur = con.cursor()


# sqlite> .tables
# Deck     SWD      SWDTEMP  VERSION

cur.execute('''
CREATE TABLE Deck(
  ID            INTEGER NOT NULL,
  Uniqueness    char(6),
  ReserveDeck   INTEGER,
  DeckName      char(100),
  Destiny       char(4),
  SubType       char(40),
  CardName      char(80) NOT NULL,
  CardType      char(18) NOT NULL,
  Expansion     char(33),
  StartingCards INTEGER,
  SideDeck      INTEGER,
  Rarity        char(15) NOT NULL,
  Inventory     int
);
''')
con.commit()
cur.execute("CREATE TABLE VERSION(Version VARCHAR(10) );")
con.commit()
cur.execute("INSERT INTO VERSION VALUES('1.7');")
con.commit()

cur.execute('''
CREATE TABLE SWD(
  id                       int not NULL,
  CardName                 char(80) not NULL,
  Grouping                 char(6) not NULL,
  CardType                 char(18) not NULL,
  Subtype                  char(40),
  ModelType                char(40),
  Expansion                char(33),
  Rarity                   char(15) not NULL,
  Uniqueness               char(6),
  Characteristics          char(60),
  Destiny                  char(4),
  Power                    char(4),
  Ferocity                 char(4),
  CreatureDefenseValue     char(4),
  CreatureDefenseValueName char(20),
  ObjectiveFront           text,
  ObjectiveBack            text,
  ObjectiveFrontName       char(80),
  ObjectiveBackName        char(80),
  Deploy                   char(4),
  Forfeit                  char(4),
  Armor                    char(5),
  Ability                  char(4),
  Hyperspeed               char(4),
  Landspeed                char(4),
  Politics                 char(4),
  Maneuver                 char(4),
  ForceAptitude            char(20),
  Lore                     text,
  Gametext                 text,
  JediTestNumber           char(4),
  LightSideIcons           char(4),
  DarkSideIcons            char(4),
  LightSideText            text,
  DarkSideText             text,
  Parsec                   char(4),
  Icons                    char(60),
  Planet                   char(4),
  Space                    char(4),
  Mobile                   char(4),
  Interior                 char(4),
  Exterior                 char(4),
  Underground              char(4),
  Creature                 char(4),
  Vehicle                  char(4),
  Starship                 char(4),
  Underwater               char(4),
  Pilot                    char(4),
  Warrior                  char(4),
  Astromech                char(4),
  PermanentWeapon          char(4),
  SelectiveCreature        char(4),
  Independent              char(4),
  ScompLink                char(4),
  Droid                    char(4),
  TradeFederation          char(4),
  Republic                 char(4),
  Episode1                 char(4),
  Information              text,
  Abbreviation             char(50),
  Pulls                    text,
  IsPulled                 text,
  Counterpart              char(50),
  Combo                    text,
  Matching                 char(50),
  MatchingWeapon           char(50),
  Rules                    text,
  Cancels                  text,
  IsCanceledBy             text,
  Inventory                int,
  Needs                    int,
  ExpansionV               VARCHAR(40),
  Influence                char(4),
  Grabber                  char(4),
  Errata                   char(4),
  CardNameV                char(80),
  UniquenessV              char(6)
);
''')
con.commit()


def icon_check(card, icon):
  if (icon in card):
    return "true"
  else:
    return ""


def merge_list(l):
  if (type(l) is list):
    #print(type(l), l, (",".join(l)).replace('"', "").replace("'", "") )
    return (",".join(l)).replace('"', "'")
  else:
    return l.replace('"', "'")


def get_val(card, key, ret=""):
  if key in card:
    return card[key]
  else:
    return ret


def make_code(orig):
  out = orig.replace(" ", "-").replace("'", "").replace(":", "").replace("/", "-").replace("#", "").lower()
  return out



def parse_json_file(json_file="Light.json"):

  global set_output_json_files
  global release_sets

  found_shields = list()

  print("Parsing %s" % json_file)
  with open(json_file) as json_data:
    side_json = json.load(json_data)
    for card in side_json['cards']:
      #print("  * "+card['front']['title'])
      ##
      #print("    ** Types")
      ## cat Dark.json | jq -r '.cards[].front.type' | sort | uniq
      ##
      if card['front']['type'].lower() not in json_details['types']['parsed']:
        json_details['types']['parsed'].append(card['front']['type'].lower())
        json_details['types']['out'].append({
          "code": make_code(card['front']['type']),
          "name": card['front']['type']
        })
      ##
      #print("    ** SubTypes")
      ## cat Dark.json | jq -r '.cards[].front.subType' | sort | uniq
      ##
      if ("subType" in card['front']):
        if card['front']['subType'].lower() not in json_details['subtypes']['parsed']:
          json_details['subtypes']['parsed'].append(card['front']['subType'].lower())
          json_details['subtypes']['out'].append({
            "code": make_code(card['front']['subType']),
            "name": card['front']['subType']
          })
      ##
      #print("    ** Sides")
      ## cat Dark.json | jq -r '.cards[].side'
      ##
      if card['side'].lower() not in json_details['sides']['parsed']:
        json_details['sides']['parsed'].append(card['side'].lower())
        json_details['sides']['out'].append({
          "code": make_code(card['side']),
          "name": card['side']
        })
      ##
      ## swccgdb.db
      ##
      cardid                   = int(get_val(card, 'id', 0))
      gempid                   = card["gempId"].split("_")
      side                     = card["side"].lower().capitalize()
      setcode                  = release_sets[card["set"]]["abbr"]
      cardname                 = get_val(card['front'], 'title')
      ## Generate a collecting code like they have with MTG.
      ## The collecting code is basically: ReleaseAbbr+Rarity+CardID
      ## The interesting part is that we have 3 different levels of "Unlimited" cards: U, U1, and U2.
      ## If you take the Card ID 14 and the rarity code of U, you get: U14
      ## If you take the Card ID 4 and the rarity code U1, you get: U14
      ##   •Lt. Poldin Lehuse            V11U14  V11 U1  4
      ##   •Trade Federation Tactics (V) V11U14  V11 U  14
      ## Ensure that the card ID is always 3 numbers:
      ##   •Lt. Poldin Lehuse        V11U1004  V11 U1  4
      ##   •Trade Federation Tactics (V) V11U014   V11 U 14
      collecting               = release_sets[card["set"]]["abbr"]+card["rarity"]+("000"+gempid[1])[-3:]
      #if (str(gempid[0]) == '211') and (str(gempid[1]) == '4'):
      #  collecting = release_sets[card["set"]]["abbr"]+card["rarity"]+"0"+gempid[1]
      if "(AI)" in cardname:
        collecting = collecting + "AI"
      if "(OAI)" in cardname:
        collecting = collecting + "OAI"

      ## VDSPM026  VDS PM  ['200', '26'] •Don't Do That Again (Tatooine) (V) 5492
      ## VDSPM026  VDS PM  ['200', '26'] •Don't Do That Again (V)  4404
      ##
      ## VDSPM032  VDS PM  ['200', '32'] •Your Insight Serves You Well (Death Star II) (V) 6048
      ## VDSPM032  VDS PM  ['200', '32'] •Your Insight Serves You Well (V) 4407
      ##
      ## VDSPM095  VDS PM  ['200', '95'] •Fanfare (Tatooine) (V) 6293
      ## VDSPM095  VDS PM  ['200', '95'] •Fanfare (V)  4402
      ##
      ## VDSPM005  VDS PM  ['301', '5']  •Your Ship? (V) 6787
      ## VDSPM005  VDS PM  ['216', '5']  •Crossfire (V)  6908

      if release_sets[card["set"]]["abbr"] == "VDS":
        found_shields.append(collecting)

      if (
           (str(gempid[0]) == '211') and ((str(gempid[1]) == '4') or (str(gempid[1]) == '14')) or
           (collecting in ["V3C027", "VDSPM026", "VDSPM032", "VDSPM095", "VDSPM005"])
           #((release_sets[card["set"]]["abbr"] == "VDS") and (card["rarity"] == "PM"))
         ):
        print(collecting + "\t" +
              release_sets[card["set"]]["abbr"] + "\t" + 
              card["rarity"] + "\t" + 
              str(gempid) + "\t" + 
              cardname + "\t" + str(cardid))

      imageurl                 = get_val(card['front'], 'imageUrl')
      grouping                 = get_val(card, 'side')
      cardtype                 = get_val(card['front'], 'type')
      subtype                  = get_val(card['front'], 'subType')
      modeltype                = merge_list(get_val(card['front'], 'extraText', ret=[]))
      expansion                = get_val(card, 'set')
      rarity                   = get_val(card, 'rarity')
      uniqueness               = get_val(card['front'], 'uniqueness')
      characteristics          = merge_list(get_val(card, 'characteristics', ret=[]))
      destiny                  = get_val(card['front'], 'destiny')
      power                    = get_val(card['front'], 'power')
      ferocity                 = get_val(card['front'], 'ferocity')
      creaturedefensevalue     = get_val(card['front'], 'defense')
      creaturedefensevaluename = "defense"
      if "Creature" in card['front']['type']:
        creaturedefensevaluename = merge_list(get_val(card['front'], 'extraText', ret=[]))

      objectivefront           = ""
      objectiveback            = ""
      objectivefrontname       = ""
      objectivebackname        = ""
      if (card['front']['type'].lower() == "objective"):
        objectivefront           = get_val(card['front'], 'gametext')
        objectiveback            = get_val(card['back'],  'gametext')
        objectivefrontname       = get_val(card['front'], 'title')
        objectivebackname        = get_val(card['back'],  'title')

      deploy                   = get_val(card['front'], 'deploy')
      forfeit                  = get_val(card['front'], 'forfeit')
      armor                    = get_val(card['front'], 'armor')
      ability                  = get_val(card['front'], 'ability')
      hyperspeed               = get_val(card['front'], "hyperspeed")
      landspeed                = get_val(card['front'], "landspeed")
      politics                 = get_val(card['front'], "politics")
      maneuver                 = get_val(card['front'], "maneuver")
      forceaptitude            = ""

      subtype   = get_val(card['front'], "subType")
      extraText = merge_list(get_val(card['front'], 'extraText', ret=[]))
      if (( \
         ( "Jedi"   in subtype)        or  \
         ( "Sith"   in subtype)        or  \
         ( "Force"  in subtype)        or  \
         ( "Knight" in subtype)        or  \
         ( "Dark"   in subtype)        or  \
         ( "Force-Attuned" in subtype)) \
         and ("Starfighter" not in subtype)):
          forceaptitude = re.sub(r'/.*', "", subtype)
      if (( \
         ( "Jedi"   in extraText) or
         ( "Sith"   in extraText) or
         ( "Force"  in extraText) or
         ( "Knight" in extraText) or
         ( "Dark"   in extraText) or
         ( "Force-Attuned" in extraText)) \
         and ("Starfighter" not in subtype)):
          forceaptitude = re.sub(r'/.*', "", extraText)



      lore                     = get_val(card['front'], "lore")
      gametext                 = get_val(card['front'], "gametext")
      jeditestnumber           = ""
      if ("Jedi Test" in get_val(card['front'], "type")):
        jeditestnumber         = re.sub(r'.*#', "\1", card['front']['type'])
        #print("     **", get_val(card['front'], "type"), ":", jeditestnumber)
      lightsideicons           = get_val(card['front'], "lightSideIcons")
      darksideicons            = get_val(card['front'], "darkSideIcons")
      lightsidetext            = get_val(card['front'], "gametext")
      darksidetext             = get_val(card['front'], "gametext")
      parsec                   = get_val(card['front'], "parsec")
      icons                    = merge_list(get_val(card['front'], 'icons', ret=[]))
      planet                   = icon_check(get_val(card['front'], 'icons', []), "Planet")
      space                    = icon_check(get_val(card['front'], 'icons', []), "Space")
      mobile                   = icon_check(get_val(card['front'], 'icons', []), "Mobile")
      interior                 = icon_check(get_val(card['front'], 'icons', []), "Interior")
      exterior                 = icon_check(get_val(card['front'], 'icons', []), "Exterior")
      underground              = icon_check(get_val(card['front'], 'icons', []), "Underground")
      creature                 = icon_check(get_val(card['front'], 'icons', []), "Creature")
      vehicle                  = icon_check(get_val(card['front'], 'icons', []), "Vehicle")
      starship                 = icon_check(get_val(card['front'], 'icons', []), "Starship")
      underwater               = icon_check(get_val(card['front'], 'icons', []), "Underwater")
      pilot                    = icon_check(get_val(card['front'], 'icons', []), "Pilot")
      warrior                  = icon_check(get_val(card['front'], 'icons', []), "Warrior")
      astromech                = icon_check(get_val(card['front'], 'icons', []), "Astromech")
      permanentweapon          = icon_check(get_val(card['front'], 'icons', []), "Permanentweapon")
      ##
      ## Many of the smaller, less ferocious creatures in the 
      ##   Star Wars universe are selective in their eating habits 
      ##   and thus do not attack their own kind.
      ## Selective creatures attack characters, creature vehicles,
      ##   or other species of creatures 
      ##   (those with a card title different from their own). 
      ## However, selective creatures with the same card title 
      ##   simply ignore each other for purposes of movement and attack.
      ## There is an icon on the card to indicate that the creature is selective.
      ##
      selectivecreature        = icon_check(get_val(card['front'], 'icons', []), "Selective Creature")
      independent              = icon_check(get_val(card['front'], 'icons', []), "Independent")
      scomplink                = icon_check(get_val(card['front'], 'icons', []), "Scomplink")
      droid                    = icon_check(get_val(card['front'], 'subType', []), "Droid")
      tradefederation          = icon_check(get_val(card['front'], 'characteristics', []), "Trade Federation")
      republic                 = icon_check(get_val(card['front'], 'icons', []), "Republic")
      episode1                 = icon_check(get_val(card['front'], 'icons', []), "Episode I")
      episode7                 = icon_check(get_val(card['front'], 'icons', []), "Episode VII")
      information              = ""
      abbreviation             = merge_list(get_val(card, "abbr", ret=[]))
      pulls                    = merge_list(get_val(card, 'pulls', ret=[]))
      ispulled                 = merge_list(get_val(card, "pulledBy", ret=[]))
      counterpart              = merge_list(get_val(card, "counterpart", ret=[]))
      combo                    = merge_list(get_val(card, "combo", ret=[]))
      matching                 = merge_list(get_val(card, "matching", ret=[]))
      matchingweapon           = merge_list(get_val(card, "matchingWeapon", ret=[]))
      rules                    = ""
      cancels                  = merge_list(get_val(card, "cancels", ret=[]))
      iscanceledby             = merge_list(get_val(card, "canceledBy", ret=[]))
      inventory                = 0
      needs                    = 0
      expansionv               = get_val(card, "set")
      influence                = ""
      grabber                  = icon_check(get_val(card['front'], 'icons', []), "Grabber")
      errata                   = get_val(card['front'], "gametext")
      cardnamev                = get_val(card['front'], "title")
      uniquenessv              = get_val(card['front'], "uniqueness")

      
      ##
      ## Some times there are TWO copies of the same defensive shield in the database.
      ## There can be TWO copies when a new VIRTUAL Defensive Shield is created
      ## from an effect AND a shield.
      ## For example: "Your Insight Serves You Well"
      ##   * In DeathStarII it was an EFFECT
      ##   * In Reflections3 it was a DEFENSIVE shield
      ##   * A VIRTUAL DEFENSIVE SHIELD C-Slip (Cover-All slip) was released for the EFFECT Version.
      ##   * A VIRTUAL DEFENSIVE SHIELD V-Slip (half slip) was released for the DEFENSIVE SHIELD Version.
      ## Since the ID's, stats, and images are the same,
      ## then there is no need to import the card twice.
      ##
      if collecting not in found_shields:

        cur.execute('''
        INSERT INTO SWD
          (id,cardname,grouping,cardtype,subtype,modeltype,expansion,rarity,uniqueness,characteristics,destiny,power,ferocity,creaturedefensevalue,creaturedefensevaluename,objectivefront,objectiveback,objectivefrontname,objectivebackname,deploy,forfeit,armor,ability,hyperspeed,landspeed,politics,maneuver,forceaptitude,lore,gametext,jeditestnumber,lightsideicons,darksideicons,lightsidetext,darksidetext,parsec,icons,planet,space,mobile,interior,exterior,underground,creature,vehicle,starship,underwater,pilot,warrior,astromech,permanentweapon,selectivecreature,independent,scomplink,droid,tradefederation,republic,episode1,information,abbreviation,pulls,ispulled,counterpart,combo,matching,matchingweapon,rules,cancels,iscanceledby,inventory,needs,expansionv,influence,grabber,errata,cardnamev,uniquenessv)
        VALUES(
           %i,  -- cardid
          "%s", -- cardname,
          "%s", -- grouping,
          "%s", -- cardtype,
          "%s", -- subtype,
          "%s", -- modeltype,
          "%s", -- expansion,
          "%s", -- rarity,
          "%s", -- uniqueness,
          "%s", -- characteristics,
          "%s", -- destiny,
          "%s", -- power,
          "%s", -- ferocity,
          "%s", -- creaturedefensevalue,
          "%s", -- creaturedefensevaluename,
          "%s", -- objectivefront,
          "%s", -- objectiveback,
          "%s", -- objectivefrontname,
          "%s", -- objectivebackname,
          "%s", -- deploy,
          "%s", -- forfeit,
          "%s", -- armor,
          "%s", -- ability,
          "%s", -- hyperspeed,
          "%s", -- landspeed,
          "%s", -- politics,
          "%s", -- maneuver,
          "%s", -- forceaptitude,
          "%s", -- lore,
          "%s", -- gametext,
          "%s", -- jeditestnumber,
          "%s", -- lightsideicons,
          "%s", -- darksideicons,
          "%s", -- lightsidetext,
          "%s", -- darksidetext,
          "%s", -- parsec,
          "%s", -- icons,
          "%s", -- planet,
          "%s", -- space,
          "%s", -- mobile,
          "%s", -- interior,
          "%s", -- exterior,
          "%s", -- underground,
          "%s", -- creature,
          "%s", -- vehicle,
          "%s", -- starship,
          "%s", -- underwater,
          "%s", -- pilot,
          "%s", -- warrior,
          "%s", -- astromech,
          "%s", -- permanentweapon,
          "%s", -- selectivecreature,
          "%s", -- independent,
          "%s", -- scomplink,
          "%s", -- droid,
          "%s", -- tradefederation,
          "%s", -- republic,
          "%s", -- episode1,
          "%s", -- information,
          "%s", -- abbreviation,
          "%s", -- pulls,
          "%s", -- ispulled,
          "%s", -- counterpart,
          "%s", -- combo,
          "%s", -- matching,
          "%s", -- matchingweapon,
          "%s", -- rules,
          "%s", -- cancels,
          "%s", -- iscanceledby,
           %i,  -- inventory, -- int
           %i,  -- needs,     -- int
          "%s", -- expansionv,
          "%s", -- influence,
          "%s", -- grabber,
          "%s", -- errata,
          "%s", -- cardnamev,
          "%s"  -- uniquenessv
        );
        ''' % (cardid,cardname,grouping,cardtype,subtype,modeltype,expansion,rarity,uniqueness,characteristics,destiny,power,ferocity,creaturedefensevalue,creaturedefensevaluename,objectivefront,objectiveback,objectivefrontname,objectivebackname,deploy,forfeit,armor,ability,hyperspeed,landspeed,politics,maneuver,forceaptitude,lore,gametext,jeditestnumber,lightsideicons,darksideicons,lightsidetext,darksidetext,parsec,icons,planet,space,mobile,interior,exterior,underground,creature,vehicle,starship,underwater,pilot,warrior,astromech,permanentweapon,selectivecreature,independent,scomplink,droid,tradefederation,republic,episode1,information,abbreviation,pulls,ispulled,counterpart,combo,matching,matchingweapon,rules,cancels,iscanceledby,inventory,needs,expansionv,influence,grabber,errata,cardnamev,uniquenessv)
        )
        con.commit()


        if setcode not in set_output_json_files:
          set_output_json_files[setcode] = list()
        row = dict()

        if characteristics:
          row["characteristics"] = characteristics
        if collecting:
          row["code"] = collecting
        if darksideicons:
          row["dark_side_icons"] = darksideicons
        if darksidetext:
          row["dark_side_text"] = darksidetext
        if episode1:
          row["episode_1"] = episode1
        if episode7:
          row["episode_7"] = episode7
        if gametext:
          row["gametext"] = gametext
        else:
          row["gametext"] = ""
        if True:
          row["has_errata"] = True
        if imageurl:
          row["image_url"] = imageurl
        if lightsideicons:
          row["light_side_icons"] = lightsideicons
        if lightsidetext:
          row["light_side_text"] = lightsidetext
        if lore:
          row["lore"] = lore
        if gametext:
          row["gametext"] = gametext
        if mobile:
          row["mobile"] = mobile
        if cardnamev:
          row["name"] = cardnamev
        if planet:
          row["planet"] = planet
        if cardid:
          row["position"] = cardid
        if rarity:
          row["rarity_code"] = rarity
        if scomplink:
          row["scomp_link"] = scomplink
        if setcode:
          row["set_code"] = setcode
        if side:
          row["side_code"] = side.lower()
        if creature:
          row["site_creature"] = creature
        if exterior:
          row["site_exterior"] = exterior
        if interior:
          row["site_interior"] = interior
        if starship:
          row["site_starship"] = starship
        if underground:
          row["site_underground"] = underground
        if underwater:
          row["site_underwater"] = underwater
        if vehicle:
          row["site_vehicle"] = vehicle
        if space:
          row["space"] = space
        if subtype:
          row["subtype_code"] = subtype.replace("#", "").replace("'", "").replace(" ", "-").replace(":", "").replace("/", "-").lower()
        if parsec:
          row["system_parsec"] = parsec
        if cardtype:
          row["type_code"] = cardtype.replace("#", "").replace("'", "").replace(" ", "-").replace(":", "").replace("/", "-").lower()
        #if uniqueness:
        row["uniqueness"] = uniquenessv

        set_output_json_files[setcode].append(row)






global set_output_json_files
set_output_json_files = dict()




##
## Sets
## cat sets.json | jq -r '.cards[].side'
##
print("Parsing sets")
release_sets = dict()
json_file = "sets.json"
with open(json_file) as json_data:
  set_json = json.load(json_data)

  for s in set_json:
    release_sets[s["id"]] = {"name":s["name"], "abbr":s["abbr"]}
    if s['id'].lower() not in json_details['sets']['parsed']:
      s_id = int(s['id'].replace("d", ""))
      if ((s_id < 400) or (s_id > 499)) and (s_id < 1000):
        json_details['sets']['parsed'].append(s['id'].lower())
        cycle_code = s['cycle_code']
        if ("virtual" in s['name'].lower()):
          cycle_code = "virtual"
        if ("shields" in s['name'].lower()):
          cycle_code = "shields"
        
        date_releae = "1970-01-01"
        if (s['date_release'] != "0000-00-00"):
          date_release = s['date_release']
        json_details['sets']['out'].append({
          "code": s['abbr'],
          "cycle_code": cycle_code,
          "date_release": date_release,
          "name": s['name'],
          "position": s['position'],
          "size": s['size']
        })
        cycle = cycle_code
        cycles[cycle]['size'] = cycles[cycle]['size'] + 1



parse_json_file("Light.json")
parse_json_file("Dark.json")

##
## rarities
##
print("Parsing rarities")
json_file = "rarity.json"
with open(json_file) as json_data:
  rarity_json = json.load(json_data)
  for r in rarity_json:
    if r.lower() not in json_details['rarities']['parsed']:
      json_details['rarities']['parsed'].append(r.lower())
      json_details['rarities']['out'].append({
        "code": r,
        "name": rarity_json[r]
      })






##
## cycles
##
print("Parsing cycles")
cout = []
for c in cycles:
  cout.append(cycles[c])
json_details['cycles']['out'] = cout





##
## Write the swccgdb json
##
if not os.path.isdir("swccgdb_json"):
  print("Creating swccgdb_json directory")
  os.mkdir("swccgdb_json")

print("Writing the swccgdb json files:")
for jd in json_details:
  json_filename = "swccgdb_json/" + json_details[jd]["jsonOutFile"]
  print("  * " + json_filename)
  fh = open(json_filename, "w")
  fh.write(json.dumps(json_details[jd]["out"], indent=2))
  fh.close()



##
## Write set files
##
print("Writing set files:")
if not os.path.isdir("swccgdb_json"):
  os.mkdir("swccgdb_json")

if not os.path.isdir("swccgdb_json/set"):
  os.mkdir("swccgdb_json/set")
else:
  for fil in os.scandir("swccgdb_json/set/"):
    #print("removing stale file",fil)
    os.remove(fil)

#print(type(set_output_json_files))

for expansion in set_output_json_files:
  print("  * "+expansion)
  expansion_filename = "swccgdb_json/set/" + expansion.lower() + ".json"
  fh = open(expansion_filename, "w")
  fh.write(json.dumps(set_output_json_files[expansion], indent=2))
  fh.close()




