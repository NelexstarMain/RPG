from dataclasses import dataclass, field
from typing import List
import uuid
"""
Human Simulation System
======================

Ten moduł implementuje podstawową strukturę człowieka w systemie symulacji społecznej.
Zawiera definicję klasy Human, która reprezentuje pojedynczą osobę z jej cechami
charakteru, danymi osobowymi i inwentarzem.

Przykład użycia:
    >>> human = Human()
    >>> human.name = "Jan Kowalski"
    >>> human.intelligence = 0.8
    >>> human.job = "Nauczyciel"
"""
@dataclass
class Human:
    """
    Klasa reprezentująca człowieka w systemie symulacji społecznej.
    
    Atrybuty:
        name (str): Imię i nazwisko osoby
        age (int): Wiek osoby
        gender (str): Płeć osoby
        job (str): Zawód wykonywany przez osobę
        inventory (list): Lista przedmiotów posiadanych przez osobę
        
    Cechy charakteru (wszystkie w zakresie 0.0 - 1.0):
        intelligence (float): Poziom inteligencji - wpływa na podejmowanie decyzji
        charisma (float): Poziom charyzmy - wpływa na nawiązywanie relacji
        empathy (float): Poziom empatii - wpływa na jakość relacji międzyludzkich
        courage (float): Poziom odwagi - wpływa na podejmowanie ryzyka
        ambition (float): Poziom ambicji - wpływa na dążenie do celów
        loyalty (float): Poziom lojalności - wpływa na trwałość relacji
        creativity (float): Poziom kreatywności - wpływa na rozwiązywanie problemów
        patience (float): Poziom cierpliwości - wpływa na długoterminowe działania
        honesty (float): Poziom uczciwości - wpływa na zaufanie innych
        adaptability (float): Poziom adaptacyjności - wpływa na radzenie sobie ze zmianami
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    age: int = 10
    gender: str = "male"
    
    job: str = "worker"
    inventory: List = field(default_factory=list)
    
    intelligence: float = 0.0
    charisma: float = 0.0    
    empathy: float = 0.0       
    courage: float = 0.0        
    ambition: float = 0.0     
    loyalty: float = 0.0       
    creativity: float = 0.0     
    patience: float = 0.0      
    honesty: float = 0.0        
    adaptability: float = 0.0
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __eq__(self, other):
        if not isinstance(other, Human):
            return NotImplemented
        return self.id == other.id