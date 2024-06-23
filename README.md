# Battle Tanks Bootleg™
~~(Oh wait it was named Battle City)~~


**Installations**:
+ [Python](https://www.python.org/downloads/)
+ [Pyxel](https://github.com/kitao/pyxel)
+ [PyxelGrid](https://github.com/UPD-CS12-232/pyxelgrid)

**To run the game, please run [main.py](main.py)**
<br>
<br>

## Contributors
+ **Glenn Paragas**
    - **GitHub Account:** gcmpar
    - **Contributions:**
        - Code structure (foundation)
        - Game objects and Managers
        - Game loop
        - Stage file format
        - README
+ **Neil Alcantara**
    - **GitHub Account:** AlphaUMi-git
    - **Contributions:**
        - Sprites and effects
        - SFX
        - Enemy AI
        - StageFile
        - Video Demo

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
+ **L** - L I F E
    - Extra life
    - Respawns player (if dead) and continues game even if win/lose
+ **K** - S M I T E
    - Smites all enemies present on field
+ **Z** - W I N
    - Automatically win the game
+ **P** - S A F E
    - Keep yourself safe
+ **X** - P O W E R U P
    - Spawn a random powerup
+ **T** - T E S T
    - Warp to test stage

<br>
<br>

+ **M**
    - ???


## Stage File Format

The stage file is a **15x15** grid .txt file consisting of object discriminators for specifying each cell type and spawnpoint. Each descriminator is separated by:<br>
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
**Link to video demo:** [Video Demo](https://drive.google.com/drive/folders/1Yg5bWrrXWPdPOV6-iUUohP-61r_4qJi7?usp=sharing)


## Game Info
**Powerups:**

*Powerups start spawning for each enemy kill when there are less than half of the maximum number of enemies from the start of the stage.*

+ **ExtraLife**
    - Gives the player an extra life that carries over to the next stage
+ **Zoooom**
    - Gives the player extra speed that can carry over to the next stage
+ **TheWorld**
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
<summary>API Reference (SUMMARY)</summary>

<br>

*Please see in-code documentation for further details.*

<br>

**Singletons:**

`GameField` [GameField](gamefiles/GameField.py)
- the World class
- Container for the stage cells
- Handles the main game update loop, as well as input for stage loading
- Manages all other singletons

`GOD` [GOD](gamefiles/GOD.py)
- Handles debug mode and cheat codes

`PhysicsManager` [PhysicsManager](gamefiles/PhysicsManager.py)
- Handles object collision/touch physics triggering
- Handles entity movement

`Renderer` [Renderer](gamefiles/Renderer.py)
- Handles all rendering for grid, text displays, and effects

`SoundManager` [SoundManager](gamefiles/SoundManager.py)
- Handles audio for bullet firing, bullet exploding, and tank destruction

`StageFile` [StageFile](gamefiles/StageFile.py)
- Handles stage file format and loading/generation
- Handles player/enemy spawning
- Interface for checking current GameState

<br>

**Factories:**

`TankFactory` [TankFactory](gamefiles/TankFactory.py)
- Generates tanks with differing stats
- Please see [Game Info](#game-info) section for more details.

`PowerupFactory` [PowerupFactory](gamefiles/PowerupFactory.py)
- Generates powerups with differing effects
- Please see [Game Info](#game-info) section for more details.

<br>

**Other Game Files:**

`Cell` [Cell](gamefiles/Cell.py)
- Container for all game objects

`Signal` [Signal](gamefiles/Signal.py)
- Events implementation
- Cleanup is handled asynchronously

`Modifier` [Modifier](gamefiles/Modifier.py)
- Manipulator of the whole game
- Inteded for tank stat manipulation, as well as object collision/touch override
- Can also include other external updates
- Can be transferred between stages

`PlayerController` [PlayerController](gamefiles/PlayerController.py)
- Handles player input

`EnemyController` [EnemyController](gamefiles/EnemyController.py)
- Handles enemy AI

<br>

**Game Objects:**

`GameObject` [GameObject](objects/GameObject.py)
- Base class for all game objects
- Interface for physics collision/touch, and modifiers

`Entity` [Entity](objects/Entity.py)
- Base class for all objects with velocity (orientation + speed)

`Bullet` [Bullet](objects/Bullet.py)
- Constantly moving projectile
- Can collide with other bullets

`Tank` [Tank](objects/Tank.py)
- Contains Stats and can fire Bullets
- Controlled by PlayerController or EnemyController
- Can be destroyed by a bullet


`Item` [Item](objects/Item.py)
- Base class for all objects that determines a cell's type
- Only one Item can be in a cell at a time as a consequence

`Brick` [Brick](objects/Brick.py)

`Stone` [Stone](objects/Stone.py)

`Water` [Water](objects/Water.py)

`Forest` [Forest](objects/Forest.py)

`Home` [Home](objects/Home.py)
- Ends game immediately if one is destroyed

`Mirror` [Mirror](objects/Mirror.py)
- Reflects bullets
- Can reflect northeast or southeast

**Miscellaneous:**

`util` [util](misc/util.py)
- Contains utilities for tank team, orientation, mirror reflect orientation, and GameState as well as other functions

`Stat` [Stat](misc/Stat.py)
- Container for base and current stat values

**Resource Files:**

`resource` [resource](resources/resource.pyxres)
- The pyxel resource file

`assetindex` [assetindex](resources/assetindex.py)
- Contains indices for sprite loading (u, v) map

`controls` [controls](resources/controls.py)
- Contains player and debug controls

`stagesettings` [stagesettings](resources/stagesettings.py)
- Contains stage parameters and settings

`stagefunctions` [stagefunctions](resources/stagefunctions.py)
- Contains custom stage function specifications (init, update, cleanup)

`stages Folder` [stages](resources/stages)
- Container for all stage .txt files

<br>

</details>

<br>
<br>
<br>
<br>

***and after that...***
<br>
<br>

***...let's think of something.***
![ENDPOINT______Our Spiral.](https://drive.google.com/uc?export=view&id=1E2eW1mRyY0Hhv_J3BPIXDXaafsEwl7uK)
