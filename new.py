import re
import github

class Reader:
    def __init__(self) -> None:
        self.pattern = r'class\s+\w+\s*:'  # Pattern to find class definitions
        
    def find_pattern(self, code: str) -> list:
        """
        Search for pattern matches in the provided code.
        
        Args:
            code (str): The source code to search through
            
        Returns:
            list: List of found matches
        """
        matches = re.findall(self.pattern, code)
        return matches

# Example usage:
reader = Reader()
code_sample = '''
class MyClass:
    def method(self):
        pass

class AnotherClass:
    pass
'''

matches = reader.find_pattern(code_sample)
for match in matches:
    print(match)