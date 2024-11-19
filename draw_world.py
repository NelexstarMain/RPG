import pygame
from typing import Any, List, Tuple, Optional, Union
from character import Character
from environment import Environment
from world_generator import WorldGenerator



class Draw:
    BLOCK_SIZE = 30
    def __init__(self) -> None:
        self.environment = Environment(16)
        self.character = Character(100, 100, {"ATT": 10})
        self.world = WorldGenerator(16)
        self.screen = pygame.display.set_mode((800, 600))
        self.chunks: List = []
        self.seen_chunks: List = []
    
    def map_to_integers(self, value: float, min_val: float = 0.0, max_val: float = 10.0, 
                        out_min: int = 0, out_max: int = 100) -> int:
        """
        Maps a float value from range 0-10 to integers.
        
        Args:
            value: Input value to map (between 0-10)
            min_val: Minimum input value (default 0.0)
            max_val: Maximum input value (default 10.0)
            out_min: Minimum output value (default 0)
            out_max: Maximum output value (default 100)
        
        Returns:
            Mapped integer value
        """
        return int((value - min_val) * (out_max - out_min) / (max_val - min_val) + out_min)

    def control(self) -> Union[Tuple[int, int], str]:
        try:
            # Oblicz pozycję chunka na podstawie pozycji postaci
            chunk_x = int(self.character.x / (self.BLOCK_SIZE * self.world.chunk_size))
            chunk_y = int(self.character.y / (self.BLOCK_SIZE * self.world.chunk_size))
            return (chunk_x, chunk_y)
            
        except Exception as e:
            return str(e)
            
    def update_world(self) -> None:
        """
        Aktualizuje świat wokół postaci, generując nowe chunki w zasięgu
        i dodając je do listy wygenerowanych chunków.
        """
        try:
            current_chunk = self.control()
            if isinstance(current_chunk, str):  
                return
                
            chunk_x, chunk_y = current_chunk
        
            nearby_chunks = self.environment.get_surrounding_chunks(chunk_x, chunk_y, radius=1)
            
            for chunk_pos in nearby_chunks:
                if chunk_pos not in self.seen_chunks:
                    chunk_data = self.world.generate_chunk(chunk_pos[0], chunk_pos[1])
                    self.seen_chunks.append(chunk_pos)
                    self.chunks.append({
                        'position': chunk_pos,
                        'data': chunk_data
                    })

        except Exception as e:
            print(f"Błąd podczas aktualizacji świata: {e}")


d = Draw()

print(d.control())