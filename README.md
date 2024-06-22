# Battle Tanks Bootleg™
~~(Oh wait it was named Battle City)~~
To run the game, please run [main.py](main.py)

## Contributors
+ **Glenn Paragas**
    - **GitHub Account:** gcmpar
    - **Contributions:**
        - Code structure (foundation)
        - Game objects and Managers
        - Game loop
        - Stage file format
+ **Neil Alcantara**
    - **GitHub Account:** AlphaUMi-git
    - **Contributions:**
        - Sprites and effects
        - SFX
        - Enemy AI
        - StageFile

## Highest Phase: Phase 3
## Controls:
+ **W, A, S, D**
    - Move tank towards north, west, south, and east respectively
+ **SPACE**
    - Fire bullet
+ **R**
    - Respawn if dead
+ **1**
    - Restart game on Stage 1
+ **2**
    - Advance to next stage if won

## GOD Commands (DEBUG MODE):
***NOTE: Hold CTRL for all keys below***
+ **L**
    - Extra life
    - Respawns player (if dead) and continues game even if win/lose
+ **K**
    - Smites all enemies present on field
+ **Z**
    - Automatically win the game
+ **P**
    - Keep yourself safe
+ **X**
    - Spawn a random powerup


## Stage File Format

The stage file a **15x15** grid consisting of object discriminators for specifying each cell type and spawnpoint. Each descriminator is separated by:<br>
A bar ("**|**") for each **COLUMN**<br>
A **newline** for each **ROW**<br>
<br>

**Object Discriminators:**
+ **EMPTY CELL:** " " OR str(1 to  15)
    - The discriminator can either be a **SPACE** or a number from 1 to 15.
    - Numbers are for easier counting and positioning
    - This is only for the designer, as they can put any number in any designated empty cell regardless of where it is
+ **BRICK:** Brick
+ **CRACKED BRICK:** CrackedBrick
+ **STONE:** Stone
+ **WATER:** Water
+ **FOREST:** Forest
+ **HOME:** Home
+ **MIRROR CELL (Northeast side):** MirrorNE
+ **MIRROR CELL (Southeast side):** MirrorSE
+ **PLAYER SPAWNPOINT:** Spawn
+ **ENEMY SPAWNPOINT:** EnemySpawn

<br>

**Additional Notes:**
+ On the left and right edges, there must still be a space or number if you wish to specify an empty cell.
+ Please see [resources/stages/_TEST.txt](resources/stages/_TEST.txt) for a complete example.

## Video Demo
**Link to video demo:** [Video Demo](https://drive.google.com/file/d/1crLGKkDuElTDd-_8w_MuMgPRSOfbxdGt/view?usp=sharing)


## Game Info
**Powerups:**
+ **Extra Life**
    - Gives the player an extra life that carries over to the next stage
+ **Zoooom**
    - Gives the player extra speed that can carry over to the next stage
+ **The World**
    - :)
+ **Mirage**
    - Float out of this Reality.

<br>

**Enemy Tanks:**
+ **Normal**
    - Normal tank that takes 1 hit to destroy
+ **Armored**
    - A slow tank that takes multiple hits to destroy
+ **Light**
    - A very fast tank that takes a few hits to destroy

## Other Info
<details>
<summary>API Reference</summary>

</details>

<br>
<br>
<br>

***and after that...***
<br>
<br>
***...let's think of something.***
![Our Spiral.](https://drive.google.com/uc?export=view&id=1E2eW1mRyY0Hhv_J3BPIXDXaafsEwl7uK)
