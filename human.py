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

    def __init__(self) -> None:
        """
        Inicjalizuje nowy obiekt klasy Human z domyślnymi wartościami.
        Wszystkie cechy charakteru są początkowo ustawione na 0.0,
        a dane osobowe są puste.
        """
        self.name: str = ""
        self.age: int = 0
        self.gender: str = ""
        
        self.job: str = ""
        self.inventory: list = []
        
        self.intelligence: float = 0.0    
        self.charisma: float = 0.0       
        self.empathy: float = 0.0        
        self.courage: float = 0.0        
        self.ambition: float = 0.0     
        self.loyalty: float = 0.0        
        self.creativity: float = 0.0     
        self.patience: float = 0.0      
        self.honesty: float = 0.0        
        self.adaptability: float = 0.0