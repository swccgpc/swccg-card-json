Star Wars CCG Card JSON Database
================================

The Star Wars CCG Card JSON database contains all of the current cards for Decipher's Star Wars Collectable Card Game.

For more information about Star Wars CCG, check out the SWCCG Players Committee website here: https://www.starwarsccg.org/

## Where is the JSON used?
This database is currently used by:
* [Scomp Link Access](https://scomp.starwarsccg.org/)
* [Comlink Android app](https://play.google.com/store/apps/details?id=com.hatfat.swccg)
* Please do not use this database without notifying the SWCCG Players Committee.

## What data is in the JSON files?
Our goal is eventually to have everything in this database that one could need.
- Card Names
- Images
- Gametext
- Card Stats
- Characteristics
- Icons
- "Pulls X", "Pulled by X"
- Special notes for combos

All JSON properties should be listed alphabetically.  This helps minimize diffs when creating pull requests.  If you find a piece of data or metadata you think is missing and should be added, please submit a pull request adding it! 

## Where are the images?
* All of the images originate in the [Holotable Git repository](https://github.com/swccgpc/holotable).
* The holotable images are hosted from `res.starwarsccg.org`.

## What does it look like?
Here's a sample of Darth Vader from the Premiere Set:
```json
{
  "abbr": [
    "Math Vader",
    "Space Vader"
  ],
  "combo": [
    "Darth Vader + Grand Moff Tarkin Once per battle, Tarkin may cancel one opponent's destiny just drawn.",
    "Darth Vader + I Have You Now Add one battle destiny (two if Rebel is Luke) if a Dark Jedi and a Rebel with ability > 2 are involved in the same battle.",
    "Darth Vader + Force Field Cancels an attempt to target a Dark Jedi with a character weapon."
  ],
  "front": {
    "ability": "6",
    "deploy": "6",
    "destiny": "1",
    "extraText": [
      "Dark Jedi"
    ],
    "forfeit": "8",
    "gametext": "When in battle, adds 1 to each of your battle destiny draws. Adds 3 to power of anything he pilots (or 4 to power and 3 to maneuver if Vader's Custom TIE). Immune to attrition < 5.",
    "icons": [
      "Pilot",
      "Warrior"
    ],
    "imageUrl": "https://res.starwarsccg.org/cards/Premiere-Dark/large/darthvader.gif",
    "lore": "Dark Lord of the Sith. Servant of Emperor's. Encased in armor with cybernetic life support. Student of Obi-Wan Kenobi. Was the best starpilot in the galaxy. Cunning warrior.",
    "power": "6",
    "subType": "Imperial",
    "title": "•Darth Vader",
    "type": "Character",
    "uniqueness": "*"
  },
  "gempId": "1_168",
  "id": 634,
  "legacy": false,
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
  ],
  "printings": [
    {
      "set": "1"
    }
  ],
  "pulledBy": [
    "Blizzard 4",
    "Sith Fury (V)",
    "The Empire's Back"
  ],
  "rarity": "R1",
  "rulings": [
    "This card is a Black Squadron pilot."
  ],
  "set": "1",
  "side": "Dark"
}
```

## Where did all this data come from?
This database combines data from Holotable and SWIP.

## Why another database?
Keeping all of the SWCCG resources all in-sync is a daunting task. Many of the previous databases have been created in a format which is not easily editable by the average-joe.  
- Holotable works with a proprietary format with carefully-placed commas which need to be placed meticulously.  
- SWIP is extremly outdated and still runs with a SQLite 2 DB, which is extremly painful to update.

Neither of the previous databases are very easy for new applications to consume. Trying to maintain those two systems is just not a good long-term solution. 

## Why JSON?
JSON is easy to read.  It's just a bunch of human-readable labels. Anybody can copy-paste a new card into the database. There are tools available to edit JSON and there are tools to validate that the JSON is properly formatted

## How to contribute
If you see bugs in the current data, please contribute!

Here's a brief overview of what you will need to do:
1. Fork this repo
2. Create a new branch inside your fork
3. Commit your changes to that branch
4. Create a pull request (PR)
5. Someone on the team will review your PR and (hopefully) merge it!

The data relies on several Unicode characters. Be sure that your changes are always UTF-8 encoded. (This is the standard in most text editors.)

Here are several useful symbols used throughout the data: • π ¼ ½

## Attribution
We would like to thank the authors of Holotable and SWIP for the initial data this project was seeded with! Without that initial data, none of this would have been possible.

Also a special thanks to all of those who help with updating this database and the corresponding images in Holotable!
