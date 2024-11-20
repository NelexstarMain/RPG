"""
Game World Rendering and Management System

This module implements the core rendering and world management system for a 2D terrain-based game.
It provides classes for handling game configuration, performance monitoring, and world rendering.

Key Components:
    GameConfig: Dataclass storing game configuration parameters
    PerformanceMonitor: Tracks and analyzes game performance metrics
    WorldRenderer: Main class handling world generation and rendering

Technical Details:
    - Uses pygame for rendering
    - Implements chunk-based world generation
    - Supports dynamic loading/unloading of chunks
    - Features performance monitoring and optimization
    - Includes debug visualization options

Dependencies:
    - pygame: Graphics and window management
    - numpy: Array operations for terrain generation
    - character: Custom Character class implementation
    - environment: Environment generation system
    - world_generator: Chunk generation system

Example Usage:
    Basic game setup:
    >>> from game_renderer import GameConfig, WorldRenderer
    >>> config = GameConfig(SCREEN_WIDTH=1024, SCREEN_HEIGHT=768)
    >>> renderer = WorldRenderer(config)
    
    Main game loop:
    >>> import pygame
    >>> running = True
    >>> clock = pygame.time.Clock()
    >>> while running:
    ...     for event in pygame.event.get():
    ...         if event.type == pygame.QUIT:
    ...             running = False
    ...     renderer.update()
    ...     clock.tick(config.TARGET_FPS)

Performance Considerations:
    - Uses surface caching for improved rendering speed
    - Implements chunk visibility checking
    - Dynamic chunk loading based on view distance
    - Optimized terrain generation with buffering

World Generation Features:
    - Procedural terrain generation
    - Multiple biome types
    - Height-based terrain rendering
    - Smooth chunk transitions

Controls:
    - Arrow keys: Move camera
    - ESC: Exit game

Notes:
    - Chunk size and render distance can be configured in GameConfig
    - Performance metrics are available through PerformanceMonitor
    - Debug information can be toggled in WorldRenderer
"""



import pygame
import math
import time
from typing import  Tuple, Dict
from dataclasses import dataclass
from character import Character
from environment import Environment
from world_generator import WorldGenerator
from collections import deque



@dataclass
class GameConfig:
    """
    Configuration settings for the game.
    
    Attributes:
        SCREEN_WIDTH (int): Width of game window in pixels
        SCREEN_HEIGHT (int): Height of game window in pixels 
        BLOCK_SIZE (int): Size of a single terrain block in pixels
        VERTICAL_OFFSET (int): Vertical offset for terrain rendering
        HEIGHT_OF_OFFSET (int): Height multiplier for terrain elevation
        CHUNK_SIZE (int): Size of world chunks (e.g. 16x16 blocks)
        GENERATION_RADIUS (int): Radius of chunks to generate around player
        MOVE_SPEED (int): Player movement speed
        TARGET_FPS (int): Target frames per second
        RENDER_DISTANCE (int): Number of chunks visible in each direction
        
    Example:
        >>> config = GameConfig()
        >>> print(config.SCREEN_WIDTH)  # 800
        >>> print(config.CHUNK_SIZE)    # 16
        
        # Custom config
        >>> custom_config = GameConfig(
        ...     SCREEN_WIDTH=1024,
        ...     SCREEN_HEIGHT=768,
        ...     RENDER_DISTANCE=3
        ... )
        """
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
    """
    Monitors and tracks game performance metrics.
    
    Tracks frame times and chunk generation times to calculate FPS
    and generation performance.
    
    Attributes:
        frame_times (deque[float]): Recent frame render times
        generation_times (deque[float]): Recent chunk generation times
        last_time (float): Timestamp of last frame
        
    Methods:
        update_frame_time(): Records time taken for current frame
        get_fps(): Calculates current FPS
        log_generation_time(): Records chunk generation time
        get_avg_generation_time(): Calculates average generation time
        
    Example:
        >>> monitor = PerformanceMonitor(max_samples=60)
        >>> monitor.update_frame_time()
        >>> current_fps = monitor.get_fps()
        >>> print(f"FPS: {current_fps:.1f}")
        
        # Track chunk generation
        >>> start = time.time()
        >>> # ... generate chunk ...
        >>> monitor.log_generation_time(time.time() - start)
        >>> avg_time = monitor.get_avg_generation_time()
        """
    def __init__(self, max_samples: int = 60):
        self.frame_times: deque[float] = deque(maxlen=max_samples)
        self.generation_times: deque[float] = deque(maxlen=max_samples)
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
    """
    Handles rendering of the game world and manages game state.
    
    Manages world chunks, rendering, asset loading and game loop.
    Provides methods for world interaction and visualization.
    
    Attributes:
        config (GameConfig): Game configuration settings
        environment (Environment): Environment generation system
        character (Character): Player character instance
        world (WorldGenerator): World chunk generator
        screen (Surface): Pygame display surface
        performance (PerformanceMonitor): Performance tracking
        chunks (Dict): Currently loaded world chunks
        
    Methods:
        update(): Updates game state and renders frame
        move(dx, dy): Moves view by given offset
        render_world(): Renders visible world chunks
        
    Example:
        >>> config = GameConfig()
        >>> renderer = WorldRenderer(config)
        
        # Game loop
        >>> running = True
        >>> while running:
        ...     # Handle input
        ...     renderer.move(-50, 0)  # Move left
        ...     renderer.update()
        ...     pygame.display.flip()
        
        # Access world data
        >>> chunk = renderer.chunks[(0,0)]
        >>> height = chunk['data']['height_map'][0][0]
    """
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