from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import uuid
from data.plan.system import MedievalTaskManager
from data.job import JOB_TO_HOUR


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
class HumanBody:
    x: int = 0
    y: int = 0
    health: int = 100
    status: dict = field(default_factory=dict)
    inventory: List = field(default_factory=list)
    alive: bool = True



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
    mtm: MedievalTaskManager = MedievalTaskManager()
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    age: int = 10
    gender: str = "male"
    
    job: str = "worker"
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
    memory: List = field(default_factory=list)
    future_plans: List = field(default_factory=list)
    plan: str = ""
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __eq__(self, other):
        if not isinstance(other, Human):
            return NotImplemented
        return self.id == other.id

    def _find_plan(self) -> List:
        return self.mtm.create_daily_plan(self.job, JOB_TO_HOUR[self.job])
    
    def _set_plan(self) -> None:
        self.plan = self.future_plans.pop(0)
        
    def plan_menagment(self) -> None:
        if self.plan:
            return
        
        self.future_plans.extend(self._find_plan())
        
        if self.plan:
            return
        
        self._set_plan()
        
        
    
class HumanMenager:
    def __init__(self):
        self.body: HumanBody = HumanBody()
        self.mind: Human = Human()
        
    def actions(self) -> Optional[Tuple[int, int, Optional[bool]]]
        self.mind.plan_menagment()
        action = self.mind.plan
        
    
