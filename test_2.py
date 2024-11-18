import pygame
import numpy as np
from environment import Environment

class WorldRenderer:
    """
    A class responsible for rendering the procedurally generated world.

    This class handles the initialization of the Pygame window, rendering of chunks,
    drawing of the mini-map, and managing the main game loop.

    Attributes:
        window (pygame.Surface): The main game window.
        chunk_size (int): The size of each chunk in tiles.
        tile_size (int): The size of each tile in pixels.
        environment (Environment): The environment object for world generation.
        colors (dict): A dictionary mapping biome names to RGB color tuples.
        camera_x (int): The x-coordinate of the camera in the world.
        camera_y (int): The y-coordinate of the camera in the world.
        font (pygame.font.Font): The font used for rendering text.
        chunks_generated (int): Counter for the number of chunks generated in a frame.
        fps (float): The current frames per second.
        mini_map_size (int): The size of the mini-map in pixels.
        mini_map_surface (pygame.Surface): The surface for rendering the mini-map.
        explored_chunks (set): A set of tuples representing explored chunk coordinates.
    """

    def __init__(self, window_size=(800, 600), chunk_size=16, tile_size=32):
        """
        Initialize the WorldRenderer.

        Args:
            window_size (tuple): The size of the game window (width, height).
            chunk_size (int): The size of each chunk in tiles.
            tile_size (int): The size of each tile in pixels.
        """
        pygame.init()
        self.window = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Procedural World Generator")
        
        self.chunk_size = chunk_size
        self.tile_size = tile_size
        self.environment = Environment()
        
        self.colors = {
            "plains": (124, 252, 0),    # Light green
            "desert": (255, 223, 186),  # Sand color
            "forest": (34, 139, 34),    # Forest green
            "mountains": (169, 169, 169) # Gray
        }
        
        self.camera_x = 0
        self.camera_y = 0
        
        self.font = pygame.font.Font(None, 24)
        self.chunks_generated = 0
        self.fps = 0

        # Mini map setup
        self.mini_map_size = 150
        self.mini_map_surface = pygame.Surface((self.mini_map_size, self.mini_map_size))
        self.explored_chunks = set()

    def draw_chunk(self, chunk_x, chunk_y):
        """
        Draw a single chunk on the main window and update the mini-map.

        Args:
            chunk_x (int): The x-coordinate of the chunk.
            chunk_y (int): The y-coordinate of the chunk.
        """
        chunk_data = self.environment.get_chunk(chunk_x, chunk_y)
        self.chunks_generated += 1
        biome_map = chunk_data["biome_map"]
        height_map = chunk_data["height_map"]

        self.explored_chunks.add((chunk_x, chunk_y))

        for y in range(self.chunk_size):
            for x in range(self.chunk_size):
                world_x = chunk_x * self.chunk_size + x
                world_y = chunk_y * self.chunk_size + y
                screen_x = (world_x - self.camera_x) * self.tile_size
                screen_y = (world_y - self.camera_y) * self.tile_size

                if 0 <= screen_x < self.window.get_width() and 0 <= screen_y < self.window.get_height():
                    biome = biome_map[y][x]
                    height = height_map[y][x]
                    color = self.colors[biome]
                    
                    # Adjust color based on height for more detail
                    adjusted_color = tuple(max(0, min(255, c * (0.5 + height))) for c in color)
                    
                    pygame.draw.rect(self.window, adjusted_color, 
                                     (screen_x, screen_y, self.tile_size, self.tile_size))

    def render_visible_chunks(self):
        """Render all visible chunks on the screen."""
        chunks_x = self.window.get_width() // (self.chunk_size * self.tile_size) + 2
        chunks_y = self.window.get_height() // (self.chunk_size * self.tile_size) + 2

        start_chunk_x = self.camera_x // self.chunk_size
        start_chunk_y = self.camera_y // self.chunk_size

        for cy in range(start_chunk_y - 1, start_chunk_y + chunks_y + 1):
            for cx in range(start_chunk_x - 1, start_chunk_x + chunks_x + 1):
                self.draw_chunk(cx, cy)

    def draw_info(self):
        """Draw information text on the screen."""
        info_texts = [
            f"Camera Position: ({self.camera_x}, {self.camera_y})",
            f"Current Chunk: ({self.camera_x // self.chunk_size}, {self.camera_y // self.chunk_size})",
            f"Chunks Generated: {self.chunks_generated}",
            f"FPS: {self.fps:.2f}"
        ]
        
        for i, text in enumerate(info_texts):
            surface = self.font.render(text, True, (255, 255, 255))
            self.window.blit(surface, (10, 10 + i * 25))

    def draw_mini_map(self):
        """Draw the mini-map with colored chunks."""
        self.mini_map_surface.fill((0, 0, 0))
        
        if not self.explored_chunks:
            return

        min_x = min(chunk[0] for chunk in self.explored_chunks)
        max_x = max(chunk[0] for chunk in self.explored_chunks)
        min_y = min(chunk[1] for chunk in self.explored_chunks)
        max_y = max(chunk[1] for chunk in self.explored_chunks)
        
        width = max(1, max_x - min_x + 1)
        height = max(1, max_y - min_y + 1)
        scale = min(self.mini_map_size / width, self.mini_map_size / height)
        
        for chunk_x, chunk_y in self.explored_chunks:
            chunk_data = self.environment.get_chunk(chunk_x, chunk_y)
            biome_map = chunk_data["biome_map"]
            avg_biome = max(set(biome for row in biome_map for biome in row), key=lambda x: sum(row.count(x) for row in biome_map))
            color = self.colors[avg_biome]
            
            x = int((chunk_x - min_x) * scale)
            y = int((chunk_y - min_y) * scale)
            pygame.draw.rect(self.mini_map_surface, color, (x, y, max(1, int(scale)), max(1, int(scale))))
        
        # Draw player position
        player_x = int((self.camera_x // self.chunk_size - min_x) * scale)
        player_y = int((self.camera_y // self.chunk_size - min_y) * scale)
        pygame.draw.rect(self.mini_map_surface, (255, 0, 0), (player_x, player_y, 3, 3))
        
        self.window.blit(self.mini_map_surface, (self.window.get_width() - self.mini_map_size - 10, 10))

    def run(self):
        """Run the main game loop."""
        clock = pygame.time.Clock()
        running = True

        while running:
            start_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.camera_x -= 1
                    elif event.key == pygame.K_RIGHT:
                        self.camera_x += 1
                    elif event.key == pygame.K_UP:
                        self.camera_y -= 1
                    elif event.key == pygame.K_DOWN:
                        self.camera_y += 1

            self.window.fill((0, 0, 0))  # Clear the screen
            self.chunks_generated = 0  # Reset counter for this frame
            self.render_visible_chunks()
            self.draw_info()
            self.draw_mini_map()
            pygame.display.flip()
            
            # Calculate FPS
            end_time = pygame.time.get_ticks()
            frame_time = (end_time - start_time) / 1000.0
            self.fps = 1.0 / frame_time if frame_time > 0 else 0
            
            clock.tick(60)
            
            # Print information to console
            print(f"Camera: ({self.camera_x}, {self.camera_y}), Chunks: {self.chunks_generated}, FPS: {self.fps:.2f}")

        pygame.quit()

if __name__ == "__main__":
    renderer = WorldRenderer()
    renderer.run()