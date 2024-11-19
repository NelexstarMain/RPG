

import numpy as np
from environment import Environment

class WorldGenerator:
    """
    WorldGenerator - A class responsible for generating and managing world chunks.

    This class handles the generation and storage of game world chunks, where each chunk
    contains information about biomes and terrain height. It uses the Environment class
    for the actual chunk data generation.

    Attributes:
        chunk_size (int): Size of a single chunk (default 16x16)
        environment (Environment): Instance of Environment class for chunk data generation
        generated_chunks (dict): Dictionary storing generated chunks

    Methods:
        generate_chunk(chunk_x, chunk_y): Generates or retrieves a chunk at given coordinates
        get_chunk_info(chunk_x, chunk_y): Returns detailed information about a specific chunk

    Examples:
        Basic usage:
        >>> from world_generator import WorldGenerator
        >>> generator = WorldGenerator(chunk_size=16)
        >>> chunk_data = generator.generate_chunk(0, 0)
        >>> print(chunk_data['biome_map'])  # View biome distribution
        >>> print(chunk_data['height_map'])  # View height map

        Getting chunk information:
        >>> chunk_info = generator.get_chunk_info(0, 0)
        >>> print(chunk_info['position'])  # (0, 0)
        >>> print(chunk_info['average_height'])  # Average terrain height
        >>> print(chunk_info['biome_distribution'])  # Count of each biome type

        Generating multiple chunks:
        >>> # Generate a 3x3 grid of chunks
        >>> for x in range(-1, 2):
        ...     for y in range(-1, 2):
        ...         generator.generate_chunk(x, y)
        
        Accessing existing chunks:
        >>> # Second call will return cached chunk
        >>> same_chunk = generator.generate_chunk(0, 0)

    Note:
        Each chunk is identified by coordinate pair (x, y) and contains
        two main data structures:
        - biome_map: map of biomes in the chunk
        - height_map: terrain height map
    """
    def __init__(self, chunk_size=16):
        self.chunk_size = chunk_size
        self.environment = Environment()
        self.generated_chunks = {}

    def generate_chunk(self, chunk_x, chunk_y):
        """
        Generuje chunk świata dla podanych współrzędnych.
        
        Args:
            chunk_x (int): Współrzędna X chunka
            chunk_y (int): Współrzędna Y chunka
            
        Returns:
            dict: Słownik zawierający dane chunka (biome_map i height_map)
        """
        chunk_key = (chunk_x, chunk_y)
        
        # Sprawdź czy chunk już istnieje
        if chunk_key in self.generated_chunks:
            return self.generated_chunks[chunk_key]
        
        # Jeśli nie, wygeneruj nowy chunk
        chunk_data = self.environment.get_chunk(chunk_x, chunk_y)
        self.generated_chunks[chunk_key] = chunk_data
        return chunk_data

    def get_chunk_info(self, chunk_x, chunk_y):
        """
        Zwraca informacje o chunku w czytelnej formie.
        
        Args:
            chunk_x (int): Współrzędna X chunka
            chunk_y (int): Współrzędna Y chunka
        """
        chunk_data = self.generated_chunks[chunk_x, chunk_y]
        biome_map = chunk_data["biome_map"]
        height_map = chunk_data["height_map"]
        
        # Zlicz biomy w chunku
        biome_counts = {}
        for row in biome_map:
            for biome in row:
                biome_counts[biome] = biome_counts.get(biome, 0) + 1
                
        return {
            "position": (chunk_x, chunk_y),
            "biome_distribution": biome_counts,
            "average_height": np.mean(height_map)
        }

    
    
