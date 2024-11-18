"""
Module for procedural terrain generation using noise functions.
Provides height map and biome generation for chunk-based world creation.
"""

import numpy as np
import random
from typing import Dict, List, Union, Tuple


class Environment:
    """
    Environment class for generating infinite, seamless terrain and biomes.
    
    Uses continuous noise functions to create terrain that seamlessly connects
    between chunks, allowing for dynamic world generation during gameplay.
    """

    def __init__(self, seed: int = None) -> None:
        """
        Initialize the Environment with optional seed.

        Args:
            seed (int, optional): Seed for terrain generation. If None, random seed is used.
        """
        self.seed = seed if seed is not None else np.random.randint(0, 1000000)
        self.chunk_cache = {}  # Cache dla wygenerowanych chunków
        self.CHUNK_SIZE = 16

    def _generate_noise(self, x: float, y: float, scale: float = 50.0, octaves: int = 4) -> float:
        """
        Generate continuous noise value that seamlessly connects between chunks.
        
        Args:
            x (float): Global X coordinate.
            y (float): Global Y coordinate.
            scale (float): Base scale of the noise.
            octaves (int): Number of noise layers to combine.
        """
        try:
            x = x / scale
            y = y / scale
            
            noise = 0.0
            amplitude = 1.0
            frequency = 1.0
            max_value = 0.0
            
            # Używamy stałych przesunięć fazowych dla spójności między chunkami
            for i in range(octaves):
                # Używamy globalnych współrzędnych dla ciągłości
                phase_x = self.seed * (i + 1) * 1.5
                phase_y = self.seed * (i + 1) * 2.7
                
                # Funkcje trygonometryczne ze stałymi fazami
                noise += amplitude * np.sin(x * frequency + phase_x)
                noise += amplitude * np.cos(y * frequency + phase_y)
                
                max_value += amplitude * 2
                amplitude *= 0.5
                frequency *= 2.0
            
            noise = (noise / max_value + 1) / 2
            return np.clip(noise, 0, 1)
            
        except Exception as e:
            print(f"Error in noise generation: {e}")
            return 0.5

    def get_chunk(self, chunk_x: int, chunk_y: int) -> Dict[str, Union[List[List[str]], np.ndarray]]:
        """
        Get or generate a chunk at specified coordinates.
        
        Checks cache first, generates new chunk if not found.
        
        Args:
            chunk_x (int): Chunk X coordinate.
            chunk_y (int): Chunk Y coordinate.
        """
        chunk_key = (chunk_x, chunk_y)
        
        # Sprawdź czy chunk jest w cache
        if chunk_key in self.chunk_cache:
            return self.chunk_cache[chunk_key]
            
        # Jeśli nie, wygeneruj nowy chunk
        chunk_data = self._generate_chunk(chunk_x, chunk_y)
        self.chunk_cache[chunk_key] = chunk_data
        return chunk_data

    def _generate_chunk(self, chunk_x: int, chunk_y: int) -> Dict[str, Union[List[List[str]], np.ndarray]]:
        """
        Generate a new chunk with seamless connections to neighbors.
        """
        biome_map = [['' for _ in range(self.CHUNK_SIZE)] for _ in range(self.CHUNK_SIZE)]
        height_map = np.zeros((self.CHUNK_SIZE, self.CHUNK_SIZE))
        
        # Generuj wysokości z nakładką dla płynnych przejść
        overlap = 1  # Wielkość nakładki dla płynnych przejść
        
        for y in range(-overlap, self.CHUNK_SIZE + overlap):
            for x in range(-overlap, self.CHUNK_SIZE + overlap):
                world_x = chunk_x * self.CHUNK_SIZE + x
                world_y = chunk_y * self.CHUNK_SIZE + y
                
                # Generuj bazową wysokość
                height = self._generate_noise(world_x, world_y, scale=25.0)
                # Dodaj detale
                detail = self._generate_noise(world_x, world_y, scale=10.0, octaves=2)
                height = height * 0.8 + detail * 0.2
                
                # Zapisz tylko dane dla właściwego chunka
                if 0 <= x < self.CHUNK_SIZE and 0 <= y < self.CHUNK_SIZE:
                    height_map[y][x] = height
                    biome_map[y][x] = self._get_biome_for_height(height)
        
        return {
            "biome_map": biome_map,
            "height_map": height_map
        }

    def get_surrounding_chunks(self, center_x: int, center_y: int, radius: int = 1) -> List[Tuple[int, int]]:
        """
        Get coordinates of chunks surrounding a center point.
        
        Args:
            center_x (int): Center chunk X coordinate.
            center_y (int): Center chunk Y coordinate.
            radius (int): How many chunks in each direction to include.
        """
        chunks = []
        for y in range(center_y - radius, center_y + radius + 1):
            for x in range(center_x - radius, center_x + radius + 1):
                chunks.append((x, y))
        return chunks

    def _get_biome_for_height(self, height: float) -> str:
        """
        Determine biome type based on terrain height.

        Args:
            height (float): Terrain height value between 0 and 1.

        Returns:
            str: Biome type identifier.
        """
        if height < 0.3:
            return "plains"
        elif height < 0.5:
            return "desert"
        elif height < 0.7:
            return "forest"
        else:
            return "mountains"