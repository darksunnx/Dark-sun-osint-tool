import os
import json
import csv
import sqlite3
from rich.console import Console

class SearchEngine:
    def __init__(self):
        self.console = Console()
        self.database_dir = "database"
        
    def validate_input(self, query, query_type):
        if query_type == "phone":
            return query.isdigit() and len(query) >= 10
        elif query_type == "passport":
            return len(query) >= 6 and query.replace(" ", "").isalnum()
        elif query_type == "snils":
            return query.isdigit() and len(query) == 11
        return True
    
    def search_files(self, query, query_type):
        if not self.validate_input(query, query_type):
            self.console.print("[red]Invalid input format![/red]")
            return []
        
        results = []
        
        for root, _, files in os.walk(self.database_dir):
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                
                try:
                    if ext == '.txt':
                        results.extend(self.search_txt(file_path, query))
                    elif ext == '.csv':
                        results.extend(self.search_csv(file_path, query))
                    elif ext == '.json':
                        results.extend(self.search_json(file_path, query))
                    elif ext == '.sql':
                        results.extend(self.search_sql(file_path, query))
                except Exception as e:
                    self.console.print(f"[red]Error processing {file}: {str(e)}[/red]")
                    
        return results
    
    def search_txt(self, file_path, query):
        results = []
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if query.lower() in line.lower():
                    results.append({"source": file_path, "data": line.strip()})
        return results
    
    def search_csv(self, file_path, query):
        results = []
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            for row in reader:
                if any(query.lower() in str(cell).lower() for cell in row):
                    results.append({"source": file_path, "data": ",".join(row)})
        return results
    
    def search_json(self, file_path, query):
        results = []
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    if self.search_json_object(item, query):
                        results.append({"source": file_path, "data": str(item)})
            elif isinstance(data, dict):
                if self.search_json_object(data, query):
                    results.append({"source": file_path, "data": str(data)})
        return results
    
    def search_json_object(self, obj, query):
        return str(obj).lower().find(query.lower()) != -1
    
    def search_sql(self, file_path, query):
        results = []
        try:
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                
                for row in rows:
                    if any(query.lower() in str(cell).lower() for cell in row):
                        results.append({"source": f"{file_path}:{table_name}", "data": str(row)})
                        
            conn.close()
        except sqlite3.Error as e:
            self.console.print(f"[red]SQLite error: {str(e)}[/red]")
        return results
