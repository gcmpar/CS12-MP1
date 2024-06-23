import pyxel
from typing import Any

CONTROLS: dict[str, dict[str, Any]] = {
    "east": {
        "name": "D",
        "btn": pyxel.KEY_D,
    },
    "north": {
        "name": "W",
        "btn": pyxel.KEY_W,
    },
    "west": {
        "name": "A",
        "btn": pyxel.KEY_A,
    },
    "south": {
        "name": "S",
        "btn": pyxel.KEY_S,
    },
    "fire": {
        "name": "SPACE",
        "btn": pyxel.KEY_SPACE,
    },

    "restart": {
        "name": "1",
        "btn": pyxel.KEY_1,
    },
    "next": {
        "name": "2",
        "btn": pyxel.KEY_2,
    },
    "respawn": {
        "name": "R",
        "btn": pyxel.KEY_R,
    },
}

DEBUG_CONTROLS: dict[str, dict[str, Any]] = {

    # What key to hold for debug
    "debug": {
        "name": "CTRL",
        "btn": pyxel.KEY_CTRL,
    },

    "life": {
        "name": "L",
        "btn": pyxel.KEY_L,
    },
    "smite": {
        "name": "K",
        "btn": pyxel.KEY_K,
    },
    "win": {
        "name": "Z",
        "btn": pyxel.KEY_Z,
    },
    "safe": {
        "name": "P",
        "btn": pyxel.KEY_P,
    },
    "powerup": {
        "name": "X",
        "btn": pyxel.KEY_X,
    },
    "test": {
        "name": "T",
        "btn": pyxel.KEY_T,
    },



    
    "???": {
        "name": "M",
        "btn": pyxel.KEY_M,
    }
}