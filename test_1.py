"""
Module for visualizing procedurally generated terrain with different biomes.
Provides a pygame-based visualization of height maps and biomes.
"""

import pygame
import numpy as np
from environment import Environment
from typing import Dict, Tuple

class MapVisualizer:
    """
    A class for visualizing terrain maps with different biomes using pygame.
    
    Attributes:
        BIOME_COLORS (Dict[str, Tuple[int, int, int]]): Color mapping for different biomes.
        width (int): Width of the map in tiles.
        height (int): Height of the map in tiles.
        tile_size (int): Size of each tile in pixels.
        screen_width (int): Total width of the screen in pixels.
        screen_height (int): Total height of the screen in pixels.
        screen (pygame.Surface): Pygame surface for drawing.
    """
    
    BIOME_COLORS: Dict[str, Tuple[int, int, int]] = {
        "forest": (34, 139, 34),     # Dark green
        "desert": (238, 214, 175),   # Sandy color
        "mountains": (139, 137, 137), # Gray
        "plains": (124, 252, 0)      # Light green
    }

    def __init__(self, width: int, height: int, tile_size: int = 4) -> None:
        """
        Initialize the MapVisualizer.

        Args:
            width (int): Width of the map in tiles.
            height (int): Height of the map in tiles.
            tile_size (int, optional): Size of each tile in pixels. Defaults to 4.
        """
        pygame.init()
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.screen_width = width * tile_size
        self.screen_height = height * tile_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("World Map Visualization")

    def draw_map(self, environment: Environment) -> None:
        """
        Draw the entire map using data from the environment.

        Args:
            environment (Environment): Environment object containing terrain data.
        """
        self.screen.fill((0, 0, 0))  # Clear screen with black

        chunk_size = 16
        for chunk_y in range(self.height // chunk_size):
            for chunk_x in range(self.width // chunk_size):
                chunk = environment.generate_chunk(chunk_x, chunk_y)
                self._draw_chunk(chunk, chunk_x * chunk_size, chunk_y * chunk_size)

        pygame.display.flip()

    def _draw_chunk(self, chunk_data: dict, start_x: int, start_y: int) -> None:
        """
        Draw a single chunk of the map.

        Args:
            chunk_data (dict): Dictionary containing biome_map and height_map.
            start_x (int): Starting X coordinate for the chunk.
            start_y (int): Starting Y coordinate for the chunk.
        """
        biome_map = chunk_data["biome_map"]
        height_map = chunk_data["height_map"]
        
        for y in range(len(biome_map)):
            for x in range(len(biome_map[0])):
                self._draw_tile(
                    x, y, 
                    biome_map[y][x], 
                    height_map[y][x], 
                    start_x, start_y
                )

    def _draw_tile(self, x: int, y: int, biome: str, height: float, 
                  start_x: int, start_y: int) -> None:
        """
        Draw a single tile with appropriate color and shading.

        Args:
            x (int): X coordinate of the tile within the chunk.
            y (int): Y coordinate of the tile within the chunk.
            biome (str): Biome type of the tile.
            height (float): Height value of the tile (0.0 to 1.0).
            start_x (int): Chunk's starting X coordinate.
            start_y (int): Chunk's starting Y coordinate.
        """
        base_color = self.BIOME_COLORS.get(biome, (128, 128, 128))
        
        # Calculate brightness based on height
        brightness = height
        if height > 0.7:
            brightness *= 1.0
        elif height < 0.3:
            brightness *= 0.3
        
        # Apply brightness to base color
        color = tuple(min(255, int(c * brightness)) for c in base_color)
        
        # Draw the tile
        rect = pygame.Rect(
            (start_x + x) * self.tile_size,
            (start_y + y) * self.tile_size,
            self.tile_size,
            self.tile_size
        )
        pygame.draw.rect(self.screen, color, rect)

    def run(self) -> None:
        """
        Run the visualization loop. Handles user input and display updates.
        Exits on ESC key or window close.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
        pygame.quit()

def main() -> None:
    """
    Main function to run the map visualization.
    Sets up the environment and visualizer with appropriate parameters.
    """
    WIDTH = 1200
    HEIGHT = 800
    TILE_SIZE = 1
    
    try:
        environment = Environment(WIDTH, HEIGHT)
        visualizer = MapVisualizer(WIDTH, HEIGHT, TILE_SIZE)
        visualizer.draw_map(environment)
        visualizer.run()
    except Exception as e:
        print(f"Error in main: {e}")
        pygame.quit()

if __name__ == "__main__":
    main()