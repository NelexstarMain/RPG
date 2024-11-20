import pygame
import math
import time
from typing import Any, List, Tuple, Optional, Union, Dict
from dataclasses import dataclass
from character import Character
from environment import Environment
from world_generator import WorldGenerator
from collections import deque
import numpy as np


@dataclass
class GameConfig:
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    BLOCK_SIZE: int = 50
    VERTICAL_OFFSET: int = 0  # Changed to 0 or a smaller value
    HEIGHT_OF_OFFSET: int = 15
    CHUNK_SIZE: int = 16
    GENERATION_RADIUS: int = 1
    MOVE_SPEED: int = 50
    TARGET_FPS: int = 60
    RENDER_DISTANCE: int = 2  # Liczba chunków widocznych w każdym kierunku
    
    


class PerformanceMonitor:
    def __init__(self, max_samples: int = 60):
        self.frame_times = deque(maxlen=max_samples)
        self.generation_times = deque(maxlen=max_samples)
        self.last_time = time.time()
        
    def update_frame_time(self) -> None:
        current_time = time.time()
        self.frame_times.append(current_time - self.last_time)
        self.last_time = current_time
            
    def get_fps(self) -> float:
        return len(self.frame_times) / (sum(self.frame_times) or 1e-6)
    
    def log_generation_time(self, generation_time: float) -> None:
        self.generation_times.append(generation_time)
            
    def get_avg_generation_time(self) -> float:
        return sum(self.generation_times) / (len(self.generation_times) or 1)

class WorldRenderer:
    def __init__(self, config: GameConfig):
        self.config = config
        self.environment = Environment(config.CHUNK_SIZE)
        self.character = Character(100, 100, {"ATT": 10})
        self.world = WorldGenerator(config.CHUNK_SIZE)
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.performance = PerformanceMonitor()
        
        # Używamy słownika zamiast listy dla szybszego dostępu
        self.chunks: Dict[Tuple[int, int], Dict] = {}
        
        self.offset_x = 0
        self.offset_y = 0
        
        # Bufor renderowania
        self.render_buffer = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        
        self.load_assets()
        self.initialize_world()
        
        # Predefiniowane kolory i powierzchnie
        self._prepare_cached_surfaces()

    def _prepare_cached_surfaces(self):
        """Przygotowuje wstępnie przetworzone powierzchnie dla każdego biomu"""
        self.cached_surfaces = {}
        for biome, color in self.biome_colors.items():
            for height in range(10):  # Cache dla różnych wysokości
                brightness = max(150, min(255, int((height/10) * 255)))
                surface = self.block_images['higher'].copy()
                final_color = tuple(int(c * brightness / 255) for c in color)
                surface.fill(final_color, special_flags=pygame.BLEND_MULT)
                self.cached_surfaces[(biome, height)] = surface

    def load_assets(self):
        self.block_images = {
            'normal': pygame.image.load('./data/photos/02.png').convert_alpha(),
            'higher': pygame.image.load('./data/photos/01.png').convert_alpha()
        }
        
        self.biome_colors = {
            'OCEAN': (64, 164, 223),
            'BEACH': (238, 214, 175),
            'FOREST': (34, 180, 34),
            'JUNGLE': (80, 200, 80),
            'DESERT': (238, 232, 170),
            'TUNDRA': (225, 225, 225),
            'MOUNTAINS': (180, 180, 180),
            'PLAINS': (144, 252, 80),
            'SWAMP': (147, 179, 179)
        }
        
        
    

    def initialize_world(self):
        start_time = time.time()
        for x in range(-self.config.GENERATION_RADIUS, self.config.GENERATION_RADIUS + 1):
            for y in range(-self.config.GENERATION_RADIUS, self.config.GENERATION_RADIUS + 1):
                self._generate_chunk(x, y)
        self.performance.log_generation_time(time.time() - start_time)

    def _generate_chunk(self, chunk_x: int, chunk_y: int) -> None:
        chunk_key = (chunk_x, chunk_y)
        if chunk_key not in self.chunks:
            chunk_data = self.world.generate_chunk(chunk_x, chunk_y)
            self.chunks[chunk_key] = {
                'position': chunk_key,
                'data': chunk_data
            }

    def _is_chunk_visible(self, chunk_pos: Tuple[int, int]) -> bool:
        """Sprawdza czy chunk jest w zasięgu renderowania z większym marginesem"""
        chunk_size_pixels = self.config.CHUNK_SIZE * self.config.BLOCK_SIZE
        screen_x = chunk_pos[0] * chunk_size_pixels + self.offset_x 
        screen_y = chunk_pos[1] * chunk_size_pixels + self.offset_y
        
        # Zwiększamy margines do kilku chunków
        margin = chunk_size_pixels # Możesz dostosować mnożnik (3) według potrzeb
        
        return (
            screen_x + chunk_size_pixels + margin >= -self.config.SCREEN_WIDTH and 
            screen_x - margin <= self.config.SCREEN_WIDTH * 2 and
            screen_y + chunk_size_pixels + margin >= -self.config.SCREEN_HEIGHT and 
            screen_y - margin <= self.config.SCREEN_HEIGHT * 2
        )

    def render_world(self) -> None:
        self.render_buffer.fill((0, 0, 0))
        
        # Renderuj tylko widoczne chunki
        visible_chunks = {pos: chunk for pos, chunk in self.chunks.items() 
                        if self._is_chunk_visible(pos)}

        for chunk in visible_chunks.values():
            self._render_chunk(chunk)
            
        self.screen.blit(self.render_buffer, (0, 0))
        

    def _render_chunk(self, chunk: Dict) -> None:
        chunk_pos = chunk['position']
        chunk_data = chunk['data']
        height_map = chunk_data['height_map']
        biome_map = chunk_data['biome_map']
        
        # Poprawione obliczanie pozycji bazowej chunka
        base_x = (chunk_pos[0] * self.config.CHUNK_SIZE * self.config.BLOCK_SIZE) + self.offset_x
        base_y = (chunk_pos[1] * self.config.CHUNK_SIZE * self.config.BLOCK_SIZE) + self.offset_y
        
        # Sprawdzanie widoczności chunka
        if not self._is_chunk_visible(chunk_pos):
            return
        
        # Optymalizacja renderowania - renderuj tylko widoczne kafelki
        for y in range(self.config.CHUNK_SIZE):
            for x in range(self.config.CHUNK_SIZE):              

                self._render_tile(
                    x, y,
                    height_map[y][x],
                    biome_map[y][x],
                    base_x, base_y
            )
        
    def _render_tile(self, x: int, y: int, height: float, biome: str, base_x: int, base_y: int) -> None:
        screen_x = base_x + x * self.config.BLOCK_SIZE
        screen_y = base_y + y * self.config.BLOCK_SIZE
        
        height_index = min(9, max(0, int(height * 10))) 
        cached_key = (biome, height_index)
        
        if cached_key in self.cached_surfaces:
            image = self.cached_surfaces[cached_key]
            height_offset = int(height * 50) * self.config.HEIGHT_OF_OFFSET
            self.render_buffer.blit(image, (screen_x, screen_y + height_offset))

    def update(self) -> None:
        self.render_world()
        self._render_debug_info()
        pygame.display.flip()
        self.performance.update_frame_time()
    
    def _update_chunks(self) -> None:
        # Obliczamy pozycję centralnego chunka z uwzględnieniem przesunięcia
        center_x = -int(self.offset_x / (self.config.BLOCK_SIZE * self.config.CHUNK_SIZE))
        center_y = -int(self.offset_y / (self.config.BLOCK_SIZE * self.config.CHUNK_SIZE))
        
        # Zwiększamy zasięg generowania o 1, aby uniknąć "wyskakiwania" chunków
        generation_range = self.config.RENDER_DISTANCE + 1
        
        # Generuj chunki w większym obszarze
        start_time = time.time()
        for x in range(center_x - generation_range, center_x + generation_range + 1):
            for y in range(center_y - generation_range, center_y + generation_range + 1):
                self._generate_chunk(x, y)
                
        # Usuwamy chunki, które są za daleko
        chunks_to_remove = []
        for chunk_pos in self.chunks.keys():
            dx = abs(chunk_pos[0] - center_x)
            dy = abs(chunk_pos[1] - center_y)
            if dx > generation_range + 1 or dy > generation_range + 1:
                chunks_to_remove.append(chunk_pos)
                
        for pos in chunks_to_remove:
            del self.chunks[pos]
            
        self.performance.log_generation_time(time.time() - start_time)

    def _render_debug_info(self) -> None:
        font = pygame.font.Font(None, 36)
        debug_info = [
            f"FPS: {self.performance.get_fps():.1f}",
            f"Gen Time: {self.performance.get_avg_generation_time()*1000:.1f}ms",
            f"Chunks: {len(self.chunks)}"
        ]
        
        for i, text in enumerate(debug_info):
            surface = font.render(text, True, (255, 255, 255))
            self.screen.blit(surface, (10, 10 + i * 30))

    def move(self, dx: int, dy: int) -> None:
        # Dodajemy płynniejsze przesuwanie
        self.offset_x += dx
        self.offset_y += dy
        
        # Aktualizujemy chunki tylko gdy przesunięcie przekroczy pewien próg
        chunk_update_threshold = self.config.BLOCK_SIZE // 2
        if (abs(self.offset_x) > chunk_update_threshold or 
            abs(self.offset_y) > chunk_update_threshold):
            self._update_chunks()


def main():
    pygame.init()
    config = GameConfig()
    renderer = WorldRenderer(config)
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    renderer.move(config.MOVE_SPEED, 0)
                elif event.key == pygame.K_RIGHT:
                    renderer.move(-config.MOVE_SPEED, 0)
                elif event.key == pygame.K_UP:
                    renderer.move(0, config.MOVE_SPEED)
                elif event.key == pygame.K_DOWN:
                    renderer.move(0, -config.MOVE_SPEED)
        
        renderer.update()
        clock.tick(config.TARGET_FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()