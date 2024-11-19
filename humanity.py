"""
Medieval Community Simulation Module
==================================

This module provides functionality for simulating a medieval community with family 
and tribal relationships. It manages human creation, family formation, and tribal organization.

Key Features:
- Human creation with random traits
- Family formation and growth
- Tribal organization and management
- Relationship tracking using graph structure

Example Usage:
-------------

Basic Setup:
>>> from humanity import Humanity
>>> world = Humanity()

Creating Humans:
>>> world.create_human()  # Creates random human
>>> len(world.humans)
1

Creating Families:
>>> # Create multiple humans first
>>> for _ in range(10):
...     world.create_human()
>>> family = world.create_family()
>>> if family:
...     print(f"New family: {family['father'].name} + {family['mother'].name}")
New family: Mieszko Waleczny + Dobrawa z Pomorza

Growing Families:
>>> # Assuming we have a married couple
>>> child = world.grow_family(family['father'])
>>> if child:
...     print(f"New child born: {child.name}")
New child born: Bolesław Mądry

Creating Tribes:
>>> # Create more humans for tribe formation
>>> for _ in range(20):
...     world.create_human()
>>> tribe = world.create_tribe("Northern Warriors")
>>> if tribe:
...     print(f"New tribe formed under {tribe['leader'].name}")
...     print(f"Members: {len(tribe['members'])}")
New tribe formed under Kazimierz Nieustraszony
Members: 7

Getting Tribe Information:
>>> leader = tribe['leader']
>>> tribe_info = world.get_tribe_info(leader)
>>> if tribe_info:
...     print(f"Tribe strength: {tribe_info['strength']:.2f}")
...     print(f"Tribe wisdom: {tribe_info['wisdom']:.2f}")
Tribe strength: 0.75
Tribe wisdom: 0.68

Merging Tribes:
>>> # Assuming we have two tribes
>>> tribe2 = world.create_tribe("Southern Warriors")
>>> if tribe2:
...     merged = world.merge_tribes(tribe['leader'], tribe2['leader'])
...     print(f"Tribes merged: {merged}")
Tribes merged: True

Getting All Tribes:
>>> all_tribes = world.get_all_tribes()
>>> for tribe in all_tribes:
...     print(f"Tribe: {tribe['name']}")
...     print(f"Members: {len(tribe['members'])}")
Tribe: Tribe of Kazimierz Nieustraszony
Members: 12

Checking Family Status:
>>> human = world.humans[0]
>>> has_family = world.is_in_family(human)
>>> print(f"{human.name} has family: {has_family}")
Mieszko Waleczny has family: True

Classes:
--------
Humanity
    Main class for managing the medieval community simulation.

Constants:
----------
PARENTS_AGE: int = 16
    Minimum age required to become a parent
MIN_TRIBE_SIZE: int = 5
    Minimum number of members required to form a tribe
LEADER_MIN_AGE: int = 25
    Minimum age required to become a tribe leader

Dependencies:
------------
- networkx
- random
- typing
- data.names (internal module)
- human (internal module)

Notes:
------
- All character traits are normalized between 0.0 and 1.0
- Tribal leadership is based on charisma, courage, and intelligence
- Family relations are bidirectional in the graph structure
- Names are generated using medieval Polish and European name patterns
"""


import networkx as nx
from human import Human
import data.names
import random
from name_generator import generate_tribe_name
from typing import Optional, Dict, List, Any


class Humanity:
    """
    Class managing medieval community simulation.
    
    Attributes:
        PARENTS_AGE (int): Minimum age required to become a parent
        MIN_TRIBE_SIZE (int): Minimum number of members in a tribe
        LEADER_MIN_AGE (int): Minimum age required to become a tribe leader
        graph (nx.Graph): Graph representing relationships between humans
        humans (list): List of all humans in simulation
    """
    
    PARENTS_AGE: int = 16
    MIN_TRIBE_SIZE: int = 5
    LEADER_MIN_AGE: int = 25

    def __init__(self) -> None:
        """Initialize a new instance of community simulation."""
        self.graph: nx.Graph = nx.Graph()
        self.humans: List[Human] = []
        self.tribes: List[Dict[str, Any]] = []

    def generate_name(self, gender: str) -> Optional[str]:
        """
        Generate a medieval name with title for given gender.
        
        Args:
            gender (str): Gender ('male' or 'female')
            
        Returns:
            Optional[str]: Generated name with title or None if error
        """
        if gender in data.names.MEDIEVAL_NAMES_TITLES:
            name = random.choice(data.names.MEDIEVAL_NAMES[gender])
            add_title = random.choice(data.names.MEDIEVAL_DESCRIPTORS_TITLES)
            
            if gender == "female" and add_title in ["personality", "appearance"]:
                title = random.choice(data.names.MEDIEVAL_DESCRIPTORS[add_title])
                title = title[:-1] + "a"
                return f"{name} {title}"
            
            title = random.choice(data.names.MEDIEVAL_DESCRIPTORS[add_title])
            return f"{name} {title}"
        return None

    def create_human(self, 
                gender: Optional[str] = None, 
                name: Optional[str] = None, 
                age: Optional[int] = None) -> Optional[Human]:
        """
        Create a new human with specified or random traits and add them to simulation.
        
        Args:
            gender (Optional[str]): Gender of human ('male' or 'female'). Random if None
            name (Optional[str]): Name of human. Generated if None
            age (Optional[int]): Age of human. Random (10-90) if None
            
        Returns:
            Optional[Human]: Created human instance or None if creation failed
            
        Example:
            >>> world = Humanity()
            >>> new_human = world.create_human(gender="male", age=25)
            >>> print(f"Created: {new_human.name}, Age: {new_human.age}")
            Created: Mieszko Waleczny, Age: 25
        """
        try:
            human_gender = random.choice(["male", "female"]) if gender is None else gender
            human_name = self.generate_name(human_gender) if name is None else name
            
            if human_name is None:
                return None
                
            human = Human()
            human.name = str(human_name)
            human.gender = str(human_gender)
            human.age = random.randint(10, 90) if age is None else age
            human.job = "worker"
            
            # Initialize character traits
            traits = [
                'intelligence', 'charisma', 'empathy', 'courage',
                'ambition', 'loyalty', 'creativity', 'patience',
                'honesty', 'adaptability'
            ]
            
            for trait in traits:
                setattr(human, trait, random.random())

            self.humans.append(human)
            self.graph.add_node(human, role="human")
            
            return human
            
        except Exception as e:
            # In a production environment, you might want to log this error
            return None

    def create_family(self) -> Optional[Dict[str, Human]]:
        """
        Create a new family by connecting two available humans.
        
        Returns:
            Optional[Dict[str, Human]]: Dictionary with parents or None if cannot create
        """
        potential_parents = [
            human for human in self.humans 
            if human.age >= self.PARENTS_AGE
        ]
        
        available_parents = [
            h for h in potential_parents 
            if not any(data.get('relation') == 'spouse' 
                    for _, _, data in self.graph.edges(h, data=True))
        ]
        
        males = [h for h in available_parents if h.gender == "male"]
        females = [h for h in available_parents if h.gender == "female"]
        
        if not males or not females:
            return None
        
        father = random.choice(males)
        mother = random.choice(females)
        
        self.graph.add_edge(father, mother, relation="spouse")
        return {"father": father, "mother": mother}

    def grow_family(self, human: Human) -> Optional[Human]:
        """
        Attempt to create a child for given human if they have a spouse.
        
        Args:
            human (Human): Parent for whom to create child
            
        Returns:
            Optional[Human]: Created child or None if cannot create
        """
        spouse = next((
            neighbor for neighbor, data in self.graph[human].items()
            if data.get('relation') == 'spouse'
        ), None)
        
        if not spouse or human.age < self.PARENTS_AGE or spouse.age < self.PARENTS_AGE:
            return None
            
        gender = random.choice(["male", "female"])
        name = self.generate_name(gender)
        
        if name is not None:
            child = Human()
            child.name = name
            child.gender = gender
            child.age = 0
            
            # Inherit traits with small variance
            traits = [
                'intelligence', 'charisma', 'empathy', 'courage',
                'ambition', 'loyalty', 'creativity', 'patience',
                'honesty', 'adaptability'
            ]
            
            for trait in traits:
                parent_avg = (getattr(human, trait) + getattr(spouse, trait)) / 2
                value = parent_avg + random.uniform(-0.1, 0.1)
                setattr(child, trait, max(0.0, min(1.0, value)))
            
            self.humans.append(child)
            self.graph.add_node(child, role="human")
            
            # Add family relations
            parent_type = "father" if human.gender == "male" else "mother"
            spouse_type = "mother" if parent_type == "father" else "father"
            
            self.graph.add_edge(human, child, relation=parent_type)
            self.graph.add_edge(spouse, child, relation=spouse_type)
            
            return child
        
        return None

    def is_in_family(self, human: Human) -> bool:
        """
        Check if human is already in a family.
        
        Args:
            human (Human): Human to check
            
        Returns:
            bool: True if human has family, False otherwise
        """
        return any(data.get('relation') in ['spouse', 'father', 'mother'] 
                for _, _, data in self.graph.edges(human, data=True))

    def create_tribe(self, name: str | None = None) -> Optional[Dict[str, Any]]:
        """
        Create new tribe with random leader and add it to tribes list.
        
        Args:
            name (str | None): Optional tribe name
            
        Returns:
            Dict[str, Any] | None: Dictionary with tribe info or None if cannot create
        """
        potential_leaders = [
            h for h in self.humans 
            if (h.age >= self.LEADER_MIN_AGE 
                and h.charisma >= 0.6
                and not any(data.get('relation') in ['leader', 'member'] 
                        for _, _, data in self.graph.edges(h, data=True)))
        ]
        
        if not potential_leaders:
            return None
            
        leader = max(potential_leaders, 
                    key=lambda h: h.charisma + h.courage + h.intelligence)
        
        potential_members = [
            h for h in self.humans 
            if (not any(data.get('relation') in ['leader', 'member'] 
                    for _, _, data in self.graph.edges(h, data=True))
                and h != leader)
        ]
        
        if len(potential_members) < self.MIN_TRIBE_SIZE:
            return None
        
        tribe_size = random.randint(self.MIN_TRIBE_SIZE, len(potential_members))
        members = random.sample(potential_members, tribe_size)
        
        tribe = {
            'name': name or generate_tribe_name(),
            'leader': leader,
            'members': members,
            'strength': sum(m.courage for m in members) / len(members),
            'wisdom': sum(m.intelligence for m in members) / len(members)
        }
        
        for member in members:
            self.graph.add_edge(leader, member, relation='leader')
            self.graph.add_edge(member, leader, relation='member')

        # Add the new tribe to tribes list
        self.tribes.append(tribe)

        return tribe

    def get_tribe_info(self, leader: Human) -> Optional[Dict[str, Any]]:
        """
        Get information about tribe of given leader.
        
        Args:
            leader (Human): Tribe leader
            
        Returns:
            Dict[str, Any] | None: Dictionary with tribe info or None if tribe doesn't exist
        """
        if not any(data.get('relation') == 'leader' 
                for _, _, data in self.graph.edges(leader, data=True)):
            return None
            
        members = [
            neighbor for neighbor, data in self.graph[leader].items()
            if data.get('relation') == 'member'
        ]
        
        if not members:
            return None
            
        return {
            'leader': leader,
            'members': members,
            'size': len(members),
            'strength': sum(m.courage for m in members) / len(members),
            'wisdom': sum(m.intelligence for m in members) / len(members)
        }

    def merge_tribes(self, leader1: Human, leader2: Human) -> bool:
        """
        Merge two tribes under stronger leader and update tribes list.
        
        Args:
            leader1 (Human): First tribe leader
            leader2 (Human): Second tribe leader
            
        Returns:
            bool: True if tribes were merged successfully, False otherwise
        """
        tribe1 = self.get_tribe_info(leader1)
        tribe2 = self.get_tribe_info(leader2)
        
        if not tribe1 or not tribe2:
            return False
            
        new_leader = leader1 if leader1.charisma > leader2.charisma else leader2
        old_leader = leader2 if new_leader == leader1 else leader1
        
        # Transfer members to new leader
        for member, data in list(self.graph[old_leader].items()):
            if data.get('relation') == 'member':
                self.graph.remove_edge(old_leader, member)
                self.graph.remove_edge(member, old_leader)
                self.graph.add_edge(new_leader, member, relation='leader')
                self.graph.add_edge(member, new_leader, relation='member')
        
        # Update tribes list
        self.tribes = [t for t in self.tribes if t['leader'] != old_leader]
        for tribe in self.tribes:
            if tribe['leader'] == new_leader:
                tribe['members'].extend([m for m in tribe2['members'] if m not in tribe['members']])
                tribe['strength'] = sum(m.courage for m in tribe['members']) / len(tribe['members'])
                tribe['wisdom'] = sum(m.intelligence for m in tribe['members']) / len(tribe['members'])
                break
        
        return True
    
    def get_all_tribes(self) -> List[Dict[str, Any]]:
        """
        Get list of all tribes in system.
        
        Returns:
            List[Dict[str, Any]]: List of dictionaries with tribe information
        """
        tribes = []
        processed_leaders = set()
        
        for node in self.graph.nodes():
            # Check if node is a leader
            if any(data.get('relation') == 'leader' 
                for _, _, data in self.graph.edges(node, data=True)):
                if node in processed_leaders:
                    continue
                    
                processed_leaders.add(node)
                members = [
                    neighbor for neighbor, data in self.graph[node].items()
                    if data.get('relation') == 'member'
                ]
                
                if members:
                    tribe = {
                        'name': f"Tribe of {node.name}",
                        'leader': node,
                        'members': members,
                        'strength': sum(m.courage for m in members) / len(members),
                        'wisdom': sum(m.intelligence for m in members) / len(members)
                    }
                    tribes.append(tribe)
        
        return tribes