from typing import List, Dict, Optional
import random
from data.names import TRIBES_NAMES

def adjust_suffix(root: str, suffix: str) -> str:
    """
    Adjusts the root word ending before adding a suffix according to Polish language rules.
    
    Args:
        root (str): Base word to be modified
        suffix (str): Suffix to be added to the root
        
    Returns:
        str: Modified root with proper ending combined with suffix
    """
    special_cases: Dict[str, str] = {
        'woj': 'wojo',
        'mir': 'miro', 
        'sław': 'sławo',
        'gród': 'grodo',
        'miecz': 'mieczo',
        'świt': 'świto',
        'mrok': 'mroczo',
        'grom': 'gromo',
        'dąb': 'dębo',
        'wilk': 'wilko',
    }
    
    if root in special_cases:
        return special_cases[root] + suffix
        
    # Standard rules for root modification
    if root[-1] in 'aąeęioóuy':
        root = root[:-1]
    if root[-1] in 'wrnmłśćźż':
        root += 'o'
    if root[-1] in 'kg':
        root += 'o'
        
    return root + suffix

def generate_tribe_name() -> str:
    """
    Generates a random tribe name using predefined components and rules.
    
    The name consists of:
    - Optional prefix (40% chance)
    - Mandatory root with suffix
    - Up to 2 additional elements (location, title, etc.) with weighted probabilities
    
    Returns:
        str: Generated tribe name
    """
    elements: List[str] = []
    
    # Add prefix (40% chance)
    if random.random() < 0.4:
        prefix = random.choice(TRIBES_NAMES['prefiksy'])
        if not prefix.endswith(('o', 'i')):
            prefix += 'o'
        elements.append(prefix)
    
    # Add root and suffix (mandatory)
    root = random.choice(TRIBES_NAMES['rdzenie'])
    suffix = random.choice(TRIBES_NAMES['sufiksy'])
    base_name = adjust_suffix(root, suffix)
    elements.append(base_name)
    
    # Category weights for additional elements
    category_weights: Dict[str, float] = {
        'tereny': 0.4,
        'przydomki': 0.3,
        'tytuly': 0.2,
        'elementy': 0.2,
        'cechy': 0.2,
        'zwierzeta': 0.25,
        'miejsca_swiete': 0.15,
        'zjawiska': 0.15
    }
    
    # Select up to 2 additional elements
    available_categories = list(category_weights.keys())
    selected: List[str] = []
    
    def is_compatible(new_element: str, existing: List[str]) -> bool:
        """Check if new element is compatible with existing ones."""
        if not existing:
            return True
        return not (new_element in existing or 
                   any(e.split()[-1] in new_element for e in existing))
    
    for _ in range(2):
        if not available_categories:
            break
            
        category = random.choice(available_categories)
        if random.random() < category_weights[category]:
            element = random.choice(TRIBES_NAMES[category])
            if is_compatible(element, selected):
                selected.append(element)
                
        available_categories.remove(category)
    
    # Add selected elements and ensure max length
    if selected:
        elements.extend(selected)
    if len(elements) > 3:
        elements = elements[:3]
        
    return " ".join(elements)

def generate_multiple_names(count: int = 10) -> List[str]:
    """
    Generates multiple unique tribe names.
    
    Args:
        count (int): Number of names to generate. Defaults to 10.
        
    Returns:
        List[str]: List of generated tribe names
    """
    return [generate_tribe_name() for _ in range(count)]