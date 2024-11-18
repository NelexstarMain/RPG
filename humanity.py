import networkx as nx
from human import Human
import data.names
import random
class Humanity:
    PARENTS_AGE = 16
    MIN_TRIBE_SIZE = 5
    LEADER_MIN_AGE = 25
    def __init__(self) -> None:
        self.graph: nx.Graph = nx.Graph()
        self.humans: list = []
        
    def generate_name(self, gender) -> str|None:
        if gender in data.names.MEDIEVAL_NAMES_TITLES:
            name = random.choice(data.names.MEDIEVAL_NAMES[gender])
            
            add_title = random.choice(data.names.MEDIEVAL_DESCRIPTORS_TITLES)
            if gender == "female":
                if add_title in ["personality", "appearance"]:
                    title = random.choice(data.names.MEDIEVAL_DESCRIPTORS[add_title])
                    title = title[:-1] + "a"
                    return f"{name} {title}"
                
        
            title = random.choice(data.names.MEDIEVAL_DESCRIPTORS[add_title])
            return f"{name} {title}"
            
        print(gender)
        return None
            

    def create_human(self) -> None:
        gender = random.choice(["male", "female"])
        name = self.generate_name(gender)
        if name is not None:
            human = Human()
            human.name = name
            human.gender = gender
            human.age = random.randint(10, 90)
            
            
            human.job = "worker"
            
            human.intelligence = random.random()  
            human.charisma = random.random()      
            human.empathy = random.random()        
            human.courage = random.random()       
            human.ambition = random.random()     
            human.loyalty = random.random()     
            human.creativity = random.random()    
            human.patience = random.random()     
            human.honesty = random.random()     
            human.adaptability = random.random() 
            

            self.humans.append(human)
            self.graph.add_node(human, role="human")
            
        
    def create_family(self) -> None|Human:
        # Znajdź potencjalnych rodziców w odpowiednim wieku
        potential_parents = [
            human for human in self.humans 
            if human.age >= self.PARENTS_AGE
        ]
        
        # Filtruj tylko osoby bez małżonków
        available_parents = [
            h for h in potential_parents 
            if not any(data.get('relation') == 'spouse' 
                    for _, _, data in self.graph.edges(h, data=True))
        ]
        
        # Podziel na płcie
        males = [h for h in available_parents if h.gender == "male"]
        females = [h for h in available_parents if h.gender == "female"]
        
        if not males or not females:
            return None
        
        father = random.choice(males)
        mother = random.choice(females)
        
        # Reszta kodu pozostaje bez zmian
        gender = random.choice(["male", "female"])
        name = self.generate_name(gender)
        
        if name is not None:
            child = Human()
            child.name = name
            child.gender = gender
            child.age = 0
            
            # Dziedziczenie cech
            child.intelligence = (father.intelligence + mother.intelligence) / 2 + random.uniform(-0.1, 0.1)
            child.charisma = (father.charisma + mother.charisma) / 2 + random.uniform(-0.1, 0.1)
            child.empathy = (father.empathy + mother.empathy) / 2 + random.uniform(-0.1, 0.1)
            child.courage = (father.courage + mother.courage) / 2 + random.uniform(-0.1, 0.1)
            child.ambition = (father.ambition + mother.ambition) / 2 + random.uniform(-0.1, 0.1)
            
            # Normalizacja cech
            for attr in ['intelligence', 'charisma', 'empathy', 'courage', 'ambition']:
                setattr(child, attr, max(0, min(1, getattr(child, attr))))
            
            self.humans.append(child)
            self.graph.add_node(child, role="human")
            
            # Dodawanie relacji rodzinnych
            self.graph.add_edge(father, child, relation="father")
            self.graph.add_edge(mother, child, relation="mother")
            self.graph.add_edge(father, mother, relation="spouse")
            
            return child
        return None

    def is_in_family(self, human: Human) -> bool:
        """Sprawdza czy osoba jest już w jakiejś rodzinie"""
        return any(data.get('relation') in ['spouse', 'father', 'mother'] 
                for _, _, data in self.graph.edges(human, data=True))
        
    def create_tribe(self, name: str|None = None) -> dict|None:
        """Tworzy nowe plemię z losowym liderem"""
        # Debug print to check potential leaders
        potential_leaders = [
            h for h in self.humans 
            if h.age >= self.LEADER_MIN_AGE 
            and h.charisma >= 0.6
            and not any(data.get('relation') in ['leader', 'member'] 
                    for _, _, data in self.graph.edges(h, data=True))
        ]
        
        print(f"Found {len(potential_leaders)} potential leaders")  # Debug
        
        if not potential_leaders:
            return None
            
        leader = max(potential_leaders, 
                    key=lambda h: h.charisma + h.courage + h.intelligence)
        
        print(f"Selected leader: {leader.name}")  # Debug
        
        potential_members = [
            h for h in self.humans
            if not self.is_in_family(h)
            and not any(data.get('relation') in ['leader', 'member'] 
                    for _, _, data in self.graph.edges(h, data=True))
            and h != leader
        ]
        
        print(f"Found {len(potential_members)} potential members")  # Debug
        
        if len(potential_members) < self.MIN_TRIBE_SIZE:
            return None
        
        tribe_size = random.randint(self.MIN_TRIBE_SIZE, len(potential_members))
        members = random.sample(potential_members, tribe_size)
        
        # Create tribe structure
        tribe = {
            'name': name or f"Plemię {leader.name}",
            'leader': leader,
            'members': members,
            'strength': sum(m.courage for m in members) / len(members),
            'wisdom': sum(m.intelligence for m in members) / len(members)
        }
        
        # Add relationships to graph - changed this part
        for member in members:
            # Add only one-directional relationships
            self.graph.add_edge(leader, member, relation='leader')
            self.graph.add_edge(member, leader, relation='member')
        
        print(f"Created tribe with {len(members)} members")  # Debug
        return tribe
    
    def get_tribe_info(self, leader: Human) -> dict|None:
        """Zwraca informacje o plemieniu danego lidera"""
        if not any(data.get('relation') == 'leader' 
                  for _, _, data in self.graph.edges(leader, data=True)):
            return None
            
        members = [
            neighbor for neighbor, data in self.graph[leader].items()
            if data.get('relation') == 'member'
        ]
        
        return {
            'leader': leader,
            'members': members,
            'size': len(members),
            'strength': sum(m.courage for m in members) / len(members),
            'wisdom': sum(m.intelligence for m in members) / len(members)
        }
    
    def merge_tribes(self, leader1: Human, leader2: Human) -> bool:
        """Łączy dwa plemiona pod silniejszym liderem"""
        tribe1 = self.get_tribe_info(leader1)
        tribe2 = self.get_tribe_info(leader2)
        
        if not tribe1 or not tribe2:
            return False
            
        # Wybierz silniejszego lidera
        new_leader = leader1 if leader1.charisma > leader2.charisma else leader2
        old_leader = leader2 if new_leader == leader1 else leader1
        
        # Przenieś członków pod nowego lidera
        for member in self.graph[old_leader]:
            if self.graph[old_leader][member].get('relation') == 'member':
                # Usuń starą relację
                self.graph.remove_edge(old_leader, member)
                # Dodaj nową relację
                self.graph.add_edge(new_leader, member, relation='leader')
                self.graph.add_edge(member, new_leader, relation='member')
        
        return True

    def get_all_tribes(self) -> list:
        """Zwraca listę wszystkich plemion"""
        tribes = []
        
        # Sprawdź wszystkie krawędzie w grafie
        for node in self.graph.nodes():
            # Sprawdź czy węzeł ma relacje typu 'member'
            edges = self.graph.edges(node, data=True)
            is_member = False
            for _, _, data in edges:
                if data.get('relation') == 'member':
                    is_member = True
                    break
                    
            if is_member:
                # Znajdź lidera tego plemienia
                leader = None
                for _, leader, data in self.graph.edges(node, data=True):
                    if data.get('relation') == 'leader':
                        break
                
                if leader:  # Jeśli plemię ma lidera
                    # Znajdź wszystkich członków tego plemienia
                    members = []
                    for _, member, data in self.graph.edges(leader, data=True):
                        if data.get('relation') == 'member':
                            members.append(member)
                    
                    if members:  # Jeśli plemię ma członków
                        tribe = {
                            'name': f"Plemię {leader.name}",
                            'leader': leader,
                            'members': members,
                            'strength': sum(m.courage for m in members) / len(members),
                            'wisdom': sum(m.intelligence for m in members) / len(members)
                        }
                        tribes.append(tribe)
                        print(f"Found tribe: Leader={leader.name}, Members={len(members)}")  # Debug
        
        return tribes

p = Humanity()
for i in range(10):
    p.create_human()
p.create_tribe()
print(p.get_all_tribes())