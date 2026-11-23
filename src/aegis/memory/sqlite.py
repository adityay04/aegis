import sqlite3
from typing import List
from aegis.schemas import IterationResult, TestCategory
from aegis.memory.base import BaseMemory

class SQLiteMemory(BaseMemory):
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS iteration_results (
                id TEXT PRIMARY KEY,
                category TEXT,
                score_total REAL,
                data TEXT
            )
        ''')
        self.conn.commit()

    def save(self, result: IterationResult) -> None:
        result_id = f"{result.test_case.id}_{result.model_response.id}"
        self.cursor.execute(
            "INSERT OR REPLACE INTO iteration_results (id, category, score_total, data) VALUES (?, ?, ?, ?)",
            (result_id, result.test_case.category.value, result.score.total, result.model_dump_json())
        )
        self.conn.commit()

    def get_all(self) -> List[IterationResult]:
        self.cursor.execute("SELECT data FROM iteration_results")
        rows = self.cursor.fetchall()
        return [IterationResult.model_validate_json(row[0]) for row in rows]

    def get_by_category(self, category: TestCategory) -> List[IterationResult]:
        self.cursor.execute("SELECT data FROM iteration_results WHERE category = ?", (category.value,))
        rows = self.cursor.fetchall()
        return [IterationResult.model_validate_json(row[0]) for row in rows]

    def get_high_scoring(self, min_score: float) -> List[IterationResult]:
        self.cursor.execute("SELECT data FROM iteration_results WHERE score_total >= ?", (min_score,))
        rows = self.cursor.fetchall()
        return [IterationResult.model_validate_json(row[0]) for row in rows]