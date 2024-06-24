from __future__ import annotations
from typing import TYPE_CHECKING, Any
from collections.abc import Callable
if TYPE_CHECKING:
    from gamefiles.GameField import GameField
    from objects.GameObject import GameObject

from gamefiles.PlayerController import PlayerController
from gamefiles.EnemyController import EnemyController

from objects.Brick import Brick
from objects.Stone import Stone
from objects.Water import Water
from objects.Forest import Forest
from objects.Home import Home
from objects.Mirror import Mirror

from gamefiles.Signal import Signal

from resources.assetindex import ASSET_INDEX
from resources.stagesettings import STAGE_SETTINGS


'''
STAGE FORMAT:
    NOTE: Please see resources/stages/_TEST.txt for a complete example

    object discriminator
    separated by | for each column
    separated by NEWLINE for each row
    
    Object Disriminators:
        " " OR str(1 to 15) -- empty cell
            - numbers are for easier counting and positioning
            - this is only for the designer, as they can put any number in any designated empty cell regardless of where it is
        "Brick"
        "CrackedBrick"
        "Stone"
        "Water"
        "Forest"
        "Home"
        "MirrorNE" -- mirror, facing northeast side
        "MirrorSE" -- mirror, facing southeast side
        "Spawn" -- empty cell, but it's where the player spawns
        "EnemySpawn" -- empty cell, but it's where an enemy could (possibly) spawn
    
    EXAMPLE: (5x5 grid for brevity)

     | | | | 
    Spawn|2|3|4|5
    MirrorNE| | | | 
     | |Home| | 
     | | | |Water
     |EnemySpawn|EnemySpawn| | 

    NOTE: on the left and right edges, there must still be a space or number if you wish to specify an empty cell !!
    NOTE: Please see resources/stages/_TEST.txt for a complete example

'''



'''
Stage interface for GameField use

Stage
    name: str
        - descriptor for rendering or other managers
        - stage's name (without .txt extension)
    onStageGenerated: Signal[[], None]
    onPlayerAdded: Signal[[PlayerController], None]
    onPlayerRemoved: Signal[[PlayertController], None]
    onLifeChanged: Signal[[int], None]
    onEnemyAdded: Signal[[EnemyController], None]
    onEnemyRemoved: Signal[[EnemyController], None]

    init()

    generate_stage(filename: str)
        - defaults:
            - enemy spawn interval: 3.5

    get_lives() -> int
    set_lives(lives: int)
    get_spawn() -> tuple[int, int]
    get_player() -> PlayerController
    spawn_player()
        - fails if lives <= 0

    get_enemies() -> list[EnemyController]
    get_enemy_spawns() -> int
    get_remaining_enemy_spawns() -> int
    get_total_enemy_count() -> int
        - enemies on screen + remaining enemy spawns
    get_max_enemies() -> int
        - max number of enemies (how many enemies from start of stage)
    spawn_enemy(spawn_index: int)
    spawn_enemy_delayed(spawn_index: int)
        - delayed spawn with star effect
    
    update(frame_count: int)
        - called every game loop
        - handles periodic enemy spawning
    cleanup()
        - called before new stage is generated
'''

class Stage():
    def __init__(self, game: GameField):
        self.game = game

        self.name = ""
        self.onStageGenerated = Signal[[], None](game)
        self.onPlayerAdded = Signal[[PlayerController], None](game)
        self.onPlayerRemoved = Signal[[PlayerController], None](game)
        self.onLifeChanged = Signal[[int], None](game)
        self.onEnemyAdded = Signal[[EnemyController], None](game)
        self.onEnemyRemoved = Signal[[EnemyController], None](game)
    
    def init(self):
        # placeholder
        self._player = PlayerController(self.game, self.game.tankFactory.tank(x=0,y=0,team="player",tank_type="Normal"))
        self.generate_stage("_empty", lives=2, remaining_enemy_spawns=1)

    def generate_stage(self, filename: str, lives: int, remaining_enemy_spawns: int):
        spawnpoint: tuple[int, int] | None = None

        self._enemySpawns = list[tuple[int, int]]()
        self._homes = list[Home]()
        #filename="_kaRMa"
        stage = open(f"resources/stages/{filename}.txt", "r")
        lines = stage.readlines()
        for r in range(self.game.r):
            
            if len(lines) != self.game.r:
                raise ValueError(f"There must be {self.game.r} rows!")
            line = lines[r].rstrip("\n")
            
            objects = line.split("|")
            if len(objects) != self.game.c:
                raise ValueError(f"There must be {self.game.c} columns!")

            for c in range(self.game.c):
                
                id = objects[c]
                
                if id in [str(x) for x in range(1, 16)] or id == " ":
                    continue
                if id == "Brick":
                    Brick(self.game, c, r)
                elif id == "CrackedBrick":
                    Brick(self.game, x=c, y=r, cracked=True)
                elif id == "Stone":
                    Stone(self.game, c, r)
                elif id == "Water":
                    Water(self.game, c, r)
                elif id == "Forest":
                    Forest(self.game, c, r)
                elif id == "Home":
                    self._homes.append(Home(self.game, c, r))

                elif id == "MirrorNE":
                    Mirror(game=self.game, x=c, y=r, ref_ori="northeast")

                elif id == "MirrorSE":
                    Mirror(game=self.game, x=c, y=r, ref_ori="southeast")
                
                elif id == "Spawn":
                    if spawnpoint:
                        raise ValueError("Stage cannot have more than one player spawnpoint!")
                    spawnpoint = (c, r)
                elif id == "EnemySpawn":
                    self._enemySpawns.append((c,r))
                else:
                    raise ValueError(f"Invalid stage file! ID: \"{id}\", Row: {r+1}, Column: {c+1}")
                    
        if spawnpoint is None:
            raise ValueError("Please specify player spawn!")
        
        self.name = filename
        self._lives = lives
        self._remainingEnemySpawns = remaining_enemy_spawns
        self._enemies = list[EnemyController]()

        self._spawnpoint = spawnpoint
        self._maxEnemies = self.get_total_enemy_count()

        self._enemyDelayedSpawns = list[dict[str, Any]]()
        self._enemySpawnDelayInterval = 0.75

        self._eventCleanups = list[Callable[[], None]]()
        self._data: dict[str, Any] = {}

        self.spawn_player()
        self.onStageGenerated.fire()
        STAGE_SETTINGS[self.name]["init"](self.game, self, self._data)

    def get_lives(self):
        return self._lives
    
    def set_lives(self, lives: int):
        self._lives = lives

    def get_homes(self):
        return self._homes.copy()
    
    def add_home(self, home: Home):
        self._homes.append(home)
    def remove_home(self, home: Home):
        self._homes.remove(home)
    
    def get_spawn(self):
        return self._spawnpoint
    
    def get_player(self) -> PlayerController:
        return self._player
    
    def spawn_player(self):
        if self.get_lives() <= 0:
            return
        self.get_player().tank.destroy()

        (x, y) = self._spawnpoint
        def occupied_check(obj: GameObject) -> bool:
            for other in self.game[y, x].get_objects():
                    if obj == other:
                        continue
                    if obj.main_can_collide(other) and other.main_can_collide(obj):
                        return False
            return True
        player = PlayerController(
            game=self.game,
            tank=self.game.tankFactory.tank(x=x, y=y, team="player", tank_type="Normal",
                                            pre_added=occupied_check),
        )
        if player.tank.is_destroyed():
            return
        self._player = player
        
        def decrease_life():
            self.set_lives(self.get_lives()-1)
            self.onPlayerRemoved.fire(player)
            self.onLifeChanged.fire(self.get_lives())
        self._player.tank.onDestroy.add_listener(decrease_life)

        def remove_listener():
            self._player.tank.onDestroy.remove_listener(decrease_life)
        self._eventCleanups.append(remove_listener)

        def on_spawn():
            self.game.renderer.render_z(x=self.game.x(x), y=self.game.y(y), index=ASSET_INDEX["Spawning"][0], z_index=-1)
        self.game.renderer.render_custom(on_spawn, duration=0.25)
        
        self.onPlayerAdded.fire(player)

    
    def get_enemies(self):
        return self._enemies.copy()
    
    def get_enemy_spawns(self):
        return self._enemySpawns.copy()
    
    def get_remaining_enemy_spawns(self):
        return self._remainingEnemySpawns

    def get_total_enemy_count(self):
        return len(self._enemies) + self.get_remaining_enemy_spawns()

    def get_max_enemies(self):
        return self._maxEnemies

    def spawn_enemy(self, spawn_index: int, tank_type: str):
        if self._remainingEnemySpawns <= 0:
            return
        
        enemy_spawns = self.get_enemy_spawns()
        l = len(enemy_spawns)
        if l == 0:
            return
        
        x, y = enemy_spawns[spawn_index]

        def occupied_check(obj: GameObject) -> bool:
            for other in self.game[y, x].get_objects():
                    if obj == other:
                        continue
                    if obj.main_can_collide(other) and other.main_can_collide(obj):
                        return False
            return True
        enemy_tank = self.game.tankFactory.tank(x=x, y=y, team="enemy", tank_type=tank_type,
                                                pre_added = occupied_check)
        if enemy_tank.is_destroyed():
            return
        enemy = EnemyController(
            game=self.game,
            tank=enemy_tank
        )

        def remove_enemy():
            if enemy not in self._enemies:
                return
            self._enemies.remove(enemy)
            self.onEnemyRemoved.fire(enemy)
        enemy.tank.onDestroy.add_listener(remove_enemy)

        def remove_listener():
            enemy.tank.onDestroy.remove_listener(remove_enemy)
        self._eventCleanups.append(remove_listener)
        
        self._enemies.append(enemy)
        self._remainingEnemySpawns -= 1
        self.onEnemyAdded.fire(enemy)
    
    def spawn_enemy_delayed(self, spawn_index: int, tank_type: str):
        self._enemyDelayedSpawns.append({
            "frames": 0,
            "spawnIndex": spawn_index,
            "tankType": tank_type,
        })


    def update(self, frame_count: int):
        STAGE_SETTINGS[self.name]["update"](self.game, self, self._data, frame_count)
        
        for data in self._enemyDelayedSpawns.copy():
            data["frames"] += 1
            spawn_index = data["spawnIndex"]
            if data["frames"] > self.game.FPS * self._enemySpawnDelayInterval:
                self._enemyDelayedSpawns.remove(data)
                self.spawn_enemy(spawn_index=spawn_index, tank_type=data["tankType"])
            elif self.get_remaining_enemy_spawns() > 0:
                assert isinstance(data["spawnIndex"], int)
                l = len(self._enemySpawns)
                if l > 0 and spawn_index < l:
                    x, y = self._enemySpawns[data["spawnIndex"]]
                    self.game.renderer.render_z(x=self.game.x(x), y=self.game.y(y), index=ASSET_INDEX["Spawning"][0], z_index=-1)
                    

    
    def cleanup(self):
        STAGE_SETTINGS[self.name]["cleanup"](self.game, self, self._data)
        [f() for f in self._eventCleanups]
        [obj.destroy() for r in range(self.game.r) for c in range(self.game.c) for obj in self.game[r, c].get_objects()]


