"""
Module for procedural terrain generation using noise functions.
Provides height map and biome generation for chunk-based world creation.
"""

import numpy as np
import random
from typing import Dict, List, Union, Tuple


class Environment:

    """
    Environment - A class for procedural terrain generation with seamless chunk connections.

    This class handles the generation of terrain using noise functions to create
    height maps and biome distributions. It implements chunk-based world generation
    with caching and seamless connections between adjacent chunks.

    Attributes:
        seed (int): Random seed for terrain generation
        chunk_cache (dict): Cache storing generated chunks
        CHUNK_SIZE (int): Size of each chunk (default: 16)

    Methods:
        get_chunk(chunk_x, chunk_y): Retrieves or generates a chunk at given coordinates
        get_surrounding_chunks(center_x, center_y, radius): Gets coordinates of nearby chunks
        _generate_chunk(chunk_x, chunk_y): Internal method for chunk generation
        _generate_noise(x, y, scale, octaves): Generates continuous noise values
        _get_biome_for_height(height): Determines biome type based on height

    Examples:
        >>> env = Environment(seed=12345)
        >>> chunk = env.get_chunk(0, 0)
        >>> print(chunk['height_map'].shape)  # (16, 16)
        >>> print(len(chunk['biome_map']))    # 16

        # Get surrounding chunks
        >>> surrounding = env.get_surrounding_chunks(0, 0, radius=1)
        >>> print(len(surrounding))  # 9 chunks (3x3 area)

    Parameters:
        seed (int | None, optional): Seed for random generation. Defaults to None.

    Note:
        The terrain generation uses trigonometric functions with phase shifts to ensure
        smooth transitions between chunks. The biome distribution is determined by
        height thresholds, creating distinct terrain types.

    The chunk data structure contains:
        - height_map: numpy.ndarray of terrain heights
        - biome_map: List[List[str]] of biome types
    """
    def __init__(self, seed: int|None = None) -> None:
        """
        Initialize the Environment with optional seed.

        Args:
            seed (int, optional): Seed for terrain generation. If None, random seed is used.
        """
        self.seed: int = seed if seed is not None else np.random.randint(0, 1000000)
        self.chunk_cache: dict = {}  # Cache dla wygenerowanych chunków
        self.CHUNK_SIZE: int = 16

    
    def _generate_noise(self, x: float, y: float, scale: float = 50.0, octaves: int = 4) -> float:
        try:
            x = x / scale
            y = y / scale
            
            noise = 0  # Zmienione z 10 na 0 dla lepszej kontroli nad wysokością
            amplitude = 1.0
            frequency = 1.0
            max_value = 0
            
            # Zwiększamy liczbę oktaw dla bardziej szczegółowego terenu
            for i in range(octaves):
                phase_x = self.seed * (i + 1) * 2.5  # Zwiększone przesunięcie fazowe
                phase_y = self.seed * (i + 1) * 3.7
                
                # Dodajemy więcej funkcji trygonometrycznych dla bardziej złożonego terenu
                noise += amplitude * np.sin(x * frequency + phase_x)
                noise += amplitude * np.cos(y * frequency + phase_y)
                noise += amplitude * np.sin((x + y) * frequency * 0.5)
                
                max_value += amplitude * 3  # Dostosowane do trzech funkcji
                amplitude *= 0.5
                frequency *= 2.2  # Zwiększone dla bardziej dramatycznych zmian
            
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
        biome_map = [['' for _ in range(self.CHUNK_SIZE)] for _ in range(self.CHUNK_SIZE)]
        height_map = np.zeros((self.CHUNK_SIZE, self.CHUNK_SIZE))
        
        overlap = 1
        
        for y in range(-overlap, self.CHUNK_SIZE + overlap):
            for x in range(-overlap, self.CHUNK_SIZE + overlap):
                world_x = chunk_x * self.CHUNK_SIZE + x
                world_y = chunk_y * self.CHUNK_SIZE + y
                
                # Generowanie różnych warstw terenu
                base_height = self._generate_noise(world_x, world_y, scale=100.0, octaves=6)
                medium_detail = self._generate_noise(world_x, world_y, scale=50.0, octaves=4)
                fine_detail = self._generate_noise(world_x, world_y, scale=25.0, octaves=2)
                water_mask = self._generate_noise(world_x, world_y, scale=200.0, octaves=2)
                
                # Łączenie warstw z różnymi wagami
                height = (
                    base_height * 0.5 +
                    medium_detail * 0.3 +
                    fine_detail * 0.2
                )
                
                # Dodanie większej ilości wody
                if water_mask < 0.4:  # Zwiększona szansa na wodę
                    height *= 0.3  # Obniżenie terenu dla wody
                
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
        Zmodyfikowane progi wysokości dla lepszego rozkładu biomów
        """
        if height < 0.1:  # Zwiększony próg dla wody
            return "OCEAN"
        elif height < 0.3:
            return "BEACH"
        elif height < 0.45:
            return "PLAINS"
        elif height < 0.55:
            return "FOREST"
        elif height < 0.65:
            return "JUNGLE"
        elif height < 0.7:
            return "DESERT"
        elif height < 0.8:
            return "SWAMP"
        elif height < 0.9:
            return "TUNDRA"
        else:
            return "MOUNTAINS"
