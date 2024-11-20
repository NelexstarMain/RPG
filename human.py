from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Union
import uuid
from data.plan.system import MedievalTaskManager
from data.job import JOB_TO_HOUR
import random


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

    def distance(self, x: int, y: int) -> int:
        return abs(x - self.x) + abs(y - self.y)


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
    memory: dict = field(default_factory=dict)
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
        
        
    
# class HumanMenager:
#     def __init__(self):
#         self.body: HumanBody = HumanBody()
#         self.mind: Human = Human()
        
class Actions: 
    """
    Medieval Task Management System Data
    ==================================

    This module contains core data structures for medieval professions, tasks, items and rewards.

    Professions & Tasks
    ------------------
    common_tasks:
        - Morning/Evening prayer (1h): needs prayer book -> blessing, morale
        - Prepare meals (2h): needs pot, food, wood -> meal, energy
        - Clean workspace (1h): needs broom, cloth -> clean space

    warrior:
        - Training, maintenance, guard duty, patrol (2-6h)
        - Needs: sword, armor, cloth, oil, brush, food
        - Gives: combat skill, strength, coins, experience

    blacksmith:
        - Forge work, repairs, crafting (1-8h) 
        - Needs: wood, tools, metal, leather
        - Gives: weapons, armor, coins, repairs

    healer:
        - Gathering herbs, making medicine, treating patients (2-5h)
        - Needs: herbs, tools, potions, cloth, book
        - Gives: knowledge, coins, experience, healing items

    merchant:
        - Trading, negotiating, traveling (1-12h)
        - Needs: goods, coins, horse, book
        - Gives: coins, new goods, better prices

    Basic Items
    ----------
    Combat: sword, armor
    Tools: tools, knife, broom, brush
    Materials: cloth, wood, metal, leather
    Trade: goods, coins
    Medical: herbs, potions
    Other: book, horse, pot, basket, oil, food

    Possible Rewards
    --------------
    Resources: coins, new goods, herbs, potions
    Skills: knowledge, experience, combat skill
    Status: blessing, morale, better prices
    Items: weapons, armor, tools, bandages
    Effects: clean space, maintained equipment, healthy horse

    Time Requirements
    ---------------
    Short tasks: 1-3 hours
    Medium tasks: 4-6 hours
    Long tasks: 8-12 hours

    Notes
    -----
    - Common tasks are available to all professions
    - Each profession has 4-6 specific tasks
    - Tasks require specific items and give specific rewards
    - Time requirements vary by task complexity
    """
    def __init__(self, body, mind) -> None:
        self.body: HumanBody = body
        self.mind: Human = mind
        self.mind.plan_menagment()
        self.action = self.mind.plan




    def prayer(self) -> Optional[Tuple[int, int, Optional[Union[List, bool]]]]:
        if "praing book" not in self.body.inventory:
            return None
        if "praying" not in self.mind.memory:
            x, y = self.body.x, self.body.y
            radius = (random.randint(-50, 50), random.randint(-50, 50))
            self.mind.memory["praying"] = (x + radius[0], y + radius[1])
            pass
    
        x, y = self.mind.memory["praying"]
        if self.body.distance(x, y) > 100:
            return None
        else:
            return (x, y, True)
