import os
import json

class Config:
    def __init__(self):
        self.config_file = "leakosint.txt"
        self.database_dir = "database"
        
    def check_config(self):
        return os.path.exists(self.config_file)
    
    def create_config(self):
        config_data = {
            "api_key": input("Enter your LeakOSINT API key: "),
            "database_dir": self.database_dir
        }
        
        with open(self.config_file, "w") as f:
            json.dump(config_data, f, indent=4)
            
        # Create database directory if it doesn't exist
        if not os.path.exists(self.database_dir):
            os.makedirs(self.database_dir)
    
    def get_api_key(self):
        if not self.check_config():
            return None
            
        with open(self.config_file, "r") as f:
            config_data = json.load(f)
            return config_data.get("api_key")
