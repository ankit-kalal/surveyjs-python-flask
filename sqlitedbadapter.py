import sqlite3
import json
import copy
from demo_surveys import demo_data
from typing import List, Dict, Any, Optional

class SQLiteDBAdapter:
    def __init__(self, db_path: str = "surveyjs.db"):
        self.db_path = db_path
        self.init_database()
        self.populate_demo_data()

    def get_connection(self):
        """Get a database connection"""
        return sqlite3.connect(self.db_path)

    def init_database(self):
        """Initialize the database with required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create surveys table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS surveys (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    json_data TEXT DEFAULT '{}'
                )
            ''')
            
            # Create results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    id TEXT PRIMARY KEY,
                    data TEXT DEFAULT '[]'
                )
            ''')
            
            conn.commit()

    def populate_demo_data(self):
        """Populate the database with demo data if it's empty"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if surveys table is empty
            cursor.execute('SELECT COUNT(*) FROM surveys')
            survey_count = cursor.fetchone()[0]
            
            if survey_count == 0:
                # Insert demo surveys
                for survey in demo_data["surveys"]:
                    # Convert json field to string if it's a dict
                    json_data = survey.get("json", "{}")
                    if isinstance(json_data, dict):
                        json_data = json.dumps(json_data)
                    elif not isinstance(json_data, str):
                        json_data = "{}"
                    
                    cursor.execute('''
                        INSERT INTO surveys (id, name, json_data)
                        VALUES (?, ?, ?)
                    ''', (survey["id"], survey["name"], json_data))
                
                # Insert demo results
                for result in demo_data["results"]:
                    cursor.execute('''
                        INSERT INTO results (id, data)
                        VALUES (?, ?)
                    ''', (result["id"], json.dumps(result["data"])))
                
                conn.commit()

    def get_surveys(self) -> List[Dict[str, Any]]:
        """Get all surveys from the database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, json_data FROM surveys')
            rows = cursor.fetchall()
            
            surveys = []
            for row in rows:
                surveys.append({
                    "id": row[0],
                    "name": row[1],
                    "json": row[2]
                })
            
            return surveys

    def get_survey(self, survey_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific survey by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, json_data FROM surveys WHERE id = ?', (survey_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "json": row[2]
                }
            return None

    def add_survey(self, name: Optional[str] = None) -> Dict[str, Any]:
        """Add a new survey to the database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get the next available ID
            cursor.execute('SELECT MAX(CAST(id AS INTEGER)) FROM surveys')
            max_id = cursor.fetchone()[0]
            new_id = str((max_id or 0) + 1)
            
            new_name = name or f"{demo_data['default_name']} {new_id}"
            
            cursor.execute('''
                INSERT INTO surveys (id, name, json_data)
                VALUES (?, ?, ?)
            ''', (new_id, new_name, "{}"))
            
            conn.commit()
            
            return {
                "id": new_id,
                "name": new_name,
                "json": "{}"
            }

    def change_name(self, survey_id: str, name: str) -> Optional[Dict[str, Any]]:
        """Change the name of a survey"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE surveys SET name = ? WHERE id = ?', (name, survey_id))
            conn.commit()
            
            if cursor.rowcount > 0:
                return self.get_survey(survey_id)
            return None

    def store_survey(self, survey_id: str, name: Optional[str], json_data: Optional[str]) -> Dict[str, Any]:
        """Store or update a survey"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if survey exists
            cursor.execute('SELECT id FROM surveys WHERE id = ?', (survey_id,))
            exists = cursor.fetchone()
            
            if exists:
                # Update existing survey
                cursor.execute('''
                    UPDATE surveys 
                    SET json_data = ?
                    WHERE id = ?
                ''', (json_data, survey_id))
            else:
                # Create new survey
                survey_name = name or str(survey_id)
                cursor.execute('''
                    INSERT INTO surveys (id, name, json_data)
                    VALUES (?, ?, ?)
                ''', (survey_id, survey_name, json_data))
            
            conn.commit()
            return self.get_survey(survey_id)

    def delete_survey(self, survey_id: str) -> Optional[Dict[str, Any]]:
        """Delete a survey from the database"""
        survey = self.get_survey(survey_id)
        if survey:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM surveys WHERE id = ?', (survey_id,))
                conn.commit()
        return survey

    def post_results(self, post_id: str, survey_result: Dict[str, Any]) -> Dict[str, Any]:
        """Post survey results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get existing results or create new entry
            cursor.execute('SELECT data FROM results WHERE id = ?', (post_id,))
            row = cursor.fetchone()
            
            if row:
                # Update existing results
                existing_data = json.loads(row[0])
                existing_data.append(survey_result)
                cursor.execute('UPDATE results SET data = ? WHERE id = ?', 
                            (json.dumps(existing_data), post_id))
            else:
                # Create new results entry
                cursor.execute('INSERT INTO results (id, data) VALUES (?, ?)',
                            (post_id, json.dumps([survey_result])))
            
            conn.commit()
            return {}

    def get_results(self, post_id: str) -> Optional[Dict[str, Any]]:
        """Get survey results by post ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, data FROM results WHERE id = ?', (post_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "id": row[0],
                    "data": json.loads(row[1])
                }
            return None 