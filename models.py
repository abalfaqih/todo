from datetime import datetime
import sqlite3

class Task:
    def __init__(self, id=None, title='', completed=False, created_at=None, category='General'):
        self.id = id
        self.title = title
        self.completed = completed
        self.created_at = created_at or datetime.now()
        self.category = category
    
    @staticmethod
    def init_db():
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                category TEXT DEFAULT 'General'
            )
        ''')
        
        # Add category column to existing tables (migration)
        try:
            cursor.execute('ALTER TABLE tasks ADD COLUMN category TEXT DEFAULT "General"')
            conn.commit()
        except sqlite3.OperationalError:
            # Column already exists
            pass
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_all():
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        tasks = []
        for row in cursor.fetchall():
            # Handle both old format (4 columns) and new format (5 columns)
            if len(row) == 4:
                tasks.append(Task(row[0], row[1], bool(row[2]), row[3], 'General'))
            else:
                tasks.append(Task(row[0], row[1], bool(row[2]), row[3], row[4] or 'General'))
        conn.close()
        return tasks
    
    def save(self):
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        if self.id:
            cursor.execute('UPDATE tasks SET title=?, completed=?, category=? WHERE id=?',
                         (self.title, self.completed, self.category, self.id))
        else:
            cursor.execute('INSERT INTO tasks (title, completed, category) VALUES (?, ?, ?)',
                         (self.title, self.completed, self.category))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()
    
    def delete(self):
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id=?', (self.id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_by_id(task_id):
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id=?', (task_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            # Handle both old format (4 columns) and new format (5 columns)
            if len(row) == 4:
                return Task(row[0], row[1], bool(row[2]), row[3], 'General')
            else:
                return Task(row[0], row[1], bool(row[2]), row[3], row[4] or 'General')
        return None
    
    @staticmethod
    def get_all_categories():
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT category FROM tasks WHERE category IS NOT NULL ORDER BY category')
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories if categories else ['General']