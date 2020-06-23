# Star Wars CCG Card Database  (JSON)
Welcome to the Star Wars CCG Card database! This database contains all of the current cards for Decipher's Star Wars Collectable Card Game.

For more information about Star Wars CCG, check out the SWCCG Players Committee website here: https://www.starwarsccg.org/


# Who Uses This?
This database is currently used by Scomp Link Access (https://scomp.starwarsccg.org/)

If you use this for your personal projects, please let us know so we can link ot your project!


# What Data Is Here?
Our goal is eventually to have everything in this database that one could need.
- Card Names
- Images
- Gametext
- Card Stats
- Characteristics
- Icons
- "Pulls X", "Pulled by X"
- Special notes for combos

Basically anything you could want to search for, it should be in here.


# Where Are The Images?
All of the images are hosted in the Holotable Git repository (https://github.com/swccgpc/holotable). This database links directly to those images.


# What Does It Look Like?
Here's a sample of Darth Vader from the Premiere Set:
```
{
      "id": 634,
      "side": "Dark",
      "rarity": "R1",
      "set": "Premiere",
      "front": {
        "title": "•Darth Vader",
        "imageUrl": "https://github.com/swccgpc/holotable/blob/master/Images-HT/starwars/Premiere-Dark/large/darthvader.gif?raw=true",
        "type": "Character",
        "subType": "Imperial",
        "uniqueness": "*",
        "destiny": 1,
        "power": 6,
        "ability": 6,
        "deploy": 6,
        "forfeit": 8,
        "icons": [
          "Pilot",
          "Warrior"
        ],
        "gametext": "When in battle, adds 1 to each of your battle destiny draws. Adds 3 to power of anything he pilots (or 4 to power and 3 to maneuver if Vader's Custom TIE). Immune to attrition < 5.",
        "lore": "Dark Lord of the Sith. Servant of Emperor's. Encased in armor with cybernetic life support. Student of Obi-Wan Kenobi. Was the best starpilot in the galaxy. Cunning warrior.",
        "extraText": [
          "Dark Jedi"
        ]
      },
      "pulledBy": [
        "Blizzard 4",
        "Sith Fury (V)",
        "The Empire's Back"
      ],
      "combo": [
        "Darth Vader + Grand Moff Tarkin Once per battle, Tarkin may cancel one opponent's destiny just drawn.",
        "Darth Vader + I Have You Now Add one battle destiny (two if Rebel is Luke) if a Dark Jedi and a Rebel with ability > 2 are involved in the same battle.",
        "Darth Vader + Force Field Cancels an attempt to target a Dark Jedi with a character weapon."
      ],
      "matching": [
        "Vader's Custom TIE",
        "Vader's Custom TIE (V)",
        "Vader's Personal Shuttle",
        "Vader's Personal Shuttle (V)"
      ],
      "matchingWeapon": [
        "Darth Vader's Lightsaber",
        "Darth Vader's Lightsaber (V)",
        "Vader's Lightsaber"
      ]
}
```


# Where did all this data come from?
This database combines data from a couple different sources:
- Holotable
- SWIP


# Why Another Database?
Keeping all of the SWCCG resources all in-sync is a daunting task. Many of the previous databases have been created in a format which is not easily editable by the average-joe.  
- Holotable works with a proprietary format with carefully-placed commas which need to be placed meticulously.  
- SWIP is extremly outdated and still runs with a SQLite 2 DB, which is extremly painful to update.

Neither of the previous databases are very easy for new applications to consume. Trying to maintain those two systems is just not a good long-term solution. 


# Why JSON?
JSON is easy to read.  It's just a bunch of human-readable labels. Anybody can copy-paste a new card into the database. There are tools available to edit JSON and there are tools to validate that the JSON is properly formatted


# Where Can I Ask Questions?
The best place to ask questions about this project is on the Star Wars CCG Players Committee Forums. Specifically, the "Resources" Sub-Form: https://forum.starwarsccg.org/viewforum.php?f=188


# How To Contribute?
If you see bugs in the current data, please contribute!

Here's a brief overview of what you will need to do:
1. Create a Fork of the code
2. Create a new branch inside your fok
3. Commit your changes in that branch
4. Create a pull request (PR)
5. Someone on the team will review your PR and get it merged?

There is a nice tutorial here:
https://www.thinkful.com/learn/github-pull-request-tutorial/Time-to-Submit-Your-First-PR#Time-to-Submit-Your-First-PR
