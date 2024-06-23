from typing import Any
'''
REQUIRED:
lives
enemySpawns

OPTIONAL:
winText
winTextColor
nextText
nextTextColor

loseText
    - will default to detecting if home cell was destroyed/if player died
loseTextColor
'''

STAGE_SETTINGS: dict[str, dict[str, Any]] = {
    "1": {
        "lives": 2,
        "enemySpawns": 1,

        "winText": "VICTORY",
    },
    "2": {
        "lives": 2,
        "enemySpawns": 3,

        "winText": "VICTORY",

    },
    "3": {
        "lives": 2,
        "enemySpawns": 5,

        "winText": "GAME WON!!! :D",
        "winTextColor": 10,

        "nextText": "Repeat",
    },






    "_kaRMa": {
        "lives": 1,
        "enemySpawns": 13,

        "winText": "- The Limitless Garden. -",
        "winTextColor": 8,

        "nextText": "Suffer.",

        "loseText": "- The Limitless Garden. -",
    },



    "_empty": {
        "lives": 1,
        "enemySpawns": 0,
    },
    "_TEST": {
        "lives": 999,
        "enemySpawns": 999,
    }
}


for d in STAGE_SETTINGS.values():
    d.setdefault("winText", "STAGE FINISHED")
    d.setdefault("winTextColor", 12)

    d.setdefault("nextText", "Advance")
    d.setdefault("nextTextColor", 11)

    d.setdefault("loseTextColor", 8)