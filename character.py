from typing import Any, Optional
class Character:
    """
    A class representing a character in an RPG game.
    
    Class Attributes:
        MAX_HEALTH (int): Maximum character health (100)
        BASE_EXP (int): Base experience required per level (100)
        SCALING_FACTOR (float): Experience scaling factor for leveling (1.3)
        
    Instance Attributes:
        x (int): Character's X position on the map
        y (int): Character's Y position on the map
        health (int): Current character health (0-100)
        status (dict[str, int]): Dictionary of status effects and their remaining duration
        alive (bool): Whether the character is alive
        exp (int): Current character experience
        lvl (int): Current character level
        inventory (dict[str, Any]): Character's inventory
        
    Methods:
        change_status(item: str, value: int) -> None:
            Modifies the duration of a status effect.
            
        change_inventory(key: str, item: Optional[object], action: str) -> None:
            Manages character inventory (add/delete/change items).
            
        change_exp(value: int) -> None:
            Modifies character's experience points.
            
        change_health(value: int) -> None:
            Modifies character health within 0-100 range.
            
        get_health() -> int:
            Returns current character health.
            
        get_status(item: Optional[str]) -> Union[dict, int, None]:
            Returns information about character's status effects.
            
        get_pos() -> tuple[int, int]:
            Returns current character position (x, y).
            
        get_inventory(item: Optional[str]) -> Union[dict, Any, None]:
            Returns information about character's inventory.
            
        get_level_max_exp() -> int:
            Calculates required experience for next level.
            
        update() -> None:
            Updates character state (health, level).
    """
    MAX_HEALTH = 100
    BASE_EXP = 100  
    SCALING_FACTOR = 1.3 
    
    def __init__(self,
        x: int,
        y: int,
        status: dict) -> None:
        
        self.x: int = x
        self.y: int = y
        
        self.health: int = 100
        self.status: dict[str, int] = status
        
        self.alive: bool = True
        
        self.exp: int = 0
        
        self.lvl: int = 0
        
        self.inventory: dict[str, Any] = {}
        
        # # PLUGINS
        # self.plugins = []
        # for p in self.plugins:
        #     self.load_plugin(p)
        
    def change_status(self, item: str, value: int) -> None:
        if item in self.status:
            self.status[item] = max(0, self.status[item] + value)

        
    def change_inventory(self, key: str = "basic", item: Optional[object] = None, action: str = "a") -> None:
        actions = {
            "a": "add",      # ADD
            "d": "delete",   # DELETE (poprawiona literówka)
            "c": "change"    # CHANGE
        }
        
        if action not in actions:
            return None
            
        if action == "a":
            if key not in self.inventory or self.inventory[key] is None:
                self.inventory[key] = item
            else:
                return None  # slot zajęty
                
        elif action == "d":
            if key in self.inventory:
                self.inventory[key] = None
                
        elif action == "c":
            if key in self.inventory:
                self.inventory[key] = item
                
            
    
    def change_exp(self, value: int) -> None:
        self.exp = min(max(0, self.exp + value), self.get_level_max_exp())
        
    def change_health(self, value: int) -> None:
        self.health = min(max(0, self.health + value), self.MAX_HEALTH)
        
    def get_health(self) -> int:
        return self.health
    
    def get_status(self, item: None|str = None) -> dict|int|None:
        if item is None:
            return self.status
        
        if isinstance(item, str):
            try:
                return self.status[item]
            except KeyError:
                return None
        
    def get_pos(self) -> tuple[int, int]:
        return (self.x, self.y)

    def get_inventory(self, item: None|str = None) -> dict|Any|None:
        if item is None:
            return self.inventory
        
        if isinstance(item, str):
            try:
                return self.inventory[item]
            
            except KeyError:
                return None
            
    def get_level_max_exp(self) -> int:
        return int(self.BASE_EXP * (self.SCALING_FACTOR ** self.lvl))
        
    def update(self) -> None:
        if self.health <= 0:
            self.alive = False
            
        max_level = self.get_level_max_exp()
        if self.exp >= max_level:
            self.exp -= max_level
            self.lvl += 1

    