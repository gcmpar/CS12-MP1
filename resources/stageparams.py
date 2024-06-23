from typing import Any
'''
REQUIRED:
lives
remainingEnemySpawns

OPTIONAL:
winText
winTextColor
nextText
nextTextColor

loseText
    - will default to detecting if home cell was destroyed/if player died
loseTextColor
'''

STAGE_PARAMS: dict[str, dict[str, Any]] = {
    "1": {
        "lives": 2,
        "remainingEnemySpawns": 5,

        "winText": "VICTORY",
    },
    "2": {
        "lives": 2,
        "remainingEnemySpawns": 3,

        "winText": "VICTORY",

    },
    "3": {
        "lives": 2,
        "remainingEnemySpawns": 5,

        "winText": "GAME WON!!! :D",
        "winTextColor": 10,

        "nextText": "Repeat",
    },
    "kaRMa": {
        "lives": 1,
        "remainingEnemySpawns": 15,

        "winText": "- The Limitless Garden. -",
        "winTextColor": 8,

        "nextText": "Suffer.",

        "loseText": "- The Limitless Garden. -",
    },
    "_TEST": {
        "lives": 999,
        "remainingEnemySpawns": 999,
    }
}


for name, d in STAGE_PARAMS.items():
    d.setdefault("winText", "STAGE FINISHED")
    d.setdefault("winTextColor", 12)

    d.setdefault("nextText", "Advance")
    d.setdefault("nextTextColor", 11)

    d.setdefault("loseTextColor", 8)