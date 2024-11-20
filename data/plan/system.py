from typing import List, Dict
from dataclasses import dataclass
import random
from data.plan.plans import medieval_tasks, basic_items, all_gives

"""
Medieval Task Management System
=============================

This module provides tools for managing and planning daily activities 
for medieval professions. It allows creating work schedules, checking
required resources, and optimizing plans for specific rewards.

Classes
-------
Task
    Dataclass representing a single task with its requirements and rewards.

MedievalTaskManager
    Main class for managing medieval profession tasks and creating work plans.

Example Usage
------------
Basic usage:
    >>> from medieval_task_manager import MedievalTaskManager
    >>> manager = MedievalTaskManager()
    
    # Create a daily plan for blacksmith
    >>> blacksmith_plan = manager.create_daily_plan("blacksmith")
    >>> for task in blacksmith_plan:
    ...     print(f"{task.name}: {task.time}h")
    Morning prayer: 1h
    Evening prayer: 1h
    Light forge: 1h
    Make weapons: 6h
    
    # Check required items for the plan
    >>> required_items = manager.check_required_items(blacksmith_plan)
    >>> print(required_items)
    ['prayer book', 'wood', 'tools', 'metal']

Advanced usage:
    # Create plan optimized for earning coins
    >>> money_plan = manager.create_optimized_plan("merchant", "coins")
    >>> rewards = manager.calculate_rewards(money_plan)
    >>> print(rewards)
    {'coins': 4, 'new goods': 3}
    
    # Get all possible tasks for healer
    >>> healer_tasks = manager.get_profession_tasks("healer")
    >>> for task in healer_tasks:
    ...     print(f"{task.name} - Needs: {task.needs}")
    Gather herbs - Needs: ['basket', 'knife']
    Make medicine - Needs: ['herbs', 'pot', 'tools']
    Treat patients - Needs: ['potions', 'cloth', 'tools']

Available Professions
-------------------
- warrior
- blacksmith
- healer
- merchant

Each profession has specific tasks with:
- Time requirements (in hours)
- Required items
- Rewards/outcomes

Common tasks like prayers and meals are automatically included
in daily plans for all professions.

Notes
-----
- Daily plans are limited by available hours (default 12)
- Common tasks are always added first
- Professional tasks are randomly shuffled for variety
- Optimized plans prioritize specific rewards
"""

@dataclass
class Task:
    name: str
    time: int
    needs: List[str]
    gives: List[str]


class MedievalTaskManager:
    def __init__(self):
        self.tasks = medieval_tasks
        self.basic_items = basic_items
        self.all_gives = all_gives
        
    def create_daily_plan(self, profession: str, hours_available: int = 12) -> List[Task]:
        """Tworzy dzienny plan zadań dla danego zawodu."""
        plan = []
        time_left = hours_available
        
        common_tasks = self.tasks["common_tasks"].copy()
        random.shuffle(common_tasks)
        
        for common_task in common_tasks:
            if time_left >= common_task["time"]:
                plan.append(Task(
                    name=common_task["task"],
                    time=common_task["time"],
                    needs=common_task["needs"],
                    gives=common_task["gives"]
                ))
                time_left -= common_task["time"]
        
        # Dodaj zadania specyficzne dla zawodu
        profession_tasks = self.tasks[profession].copy()
        random.shuffle(profession_tasks)
        
        for task in profession_tasks:
            if time_left >= task["time"]:
                plan.append(Task(
                    name=task["task"],
                    time=task["time"],
                    needs=task["needs"],
                    gives=task["gives"]
                ))
                time_left -= task["time"]
                
        return plan

    def check_required_items(self, plan: List[Task]) -> List[str]:
        """Sprawdza jakie przedmioty są potrzebne do wykonania planu."""
        required_items = set()
        for task in plan:
            required_items.update(task.needs)
        return list(required_items)

    def calculate_rewards(self, plan: List[Task]) -> Dict[str, int]:
        """Oblicza łączne nagrody z planu."""
        rewards: dict = {}
        for task in plan:
            for reward in task.gives:
                rewards[reward] = rewards.get(reward, 0) + 1
        return rewards

    def get_profession_tasks(self, profession: str) -> List[Task]:
        """Zwraca wszystkie możliwe zadania dla danego zawodu."""
        if profession not in self.tasks:
            return []
        return [Task(
            name=task["task"],
            time=task["time"],
            needs=task["needs"],
            gives=task["gives"]
        ) for task in self.tasks[profession]]

    def create_optimized_plan(self, profession: str, 
                            target_reward: str, 
                            hours_available: int = 12) -> List[Task]:
        """Tworzy plan zoptymalizowany pod kątem konkretnej nagrody."""
        plan = []
        time_left = hours_available
        
        # Sortuj zadania według ilości danej nagrody
        profession_tasks = self.tasks[profession].copy()
        profession_tasks.sort(
            key=lambda x: 1 if target_reward in x["gives"] else 0,
            reverse=True
        )
        
        for task in profession_tasks:
            if time_left >= task["time"]:
                plan.append(Task(
                    name=task["task"],
                    time=task["time"],
                    needs=task["needs"],
                    gives=task["gives"]
                ))
                time_left -= task["time"]
                
        return plan