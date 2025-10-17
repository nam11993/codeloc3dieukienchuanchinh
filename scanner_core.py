# Core scanner functionality
import os
import sys

class Scanner:
    def __init__(self):
        self.name = "Code Location Scanner"
        self.version = "1.0.0"
    
    def scan_directory(self, directory_path):
        """Scan a directory for files and return results"""
        results = []
        try:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    results.append({
                        'path': file_path,
                        'name': file,
                        'size': os.path.getsize(file_path)
                    })
        except Exception as e:
            print(f"Error scanning directory: {e}")
        
        return results
    
    def get_info(self):
        return f"{self.name} v{self.version}"

if __name__ == "__main__":
    scanner = Scanner()
    print(scanner.get_info())