import json
import os
import datetime
from abc import ABC, abstractmethod
from typing import List

# Abstraction: We define a base template (AttendanceRecord) with a strict contract.
# This ensures that any type of record we create in the future will definitely have a status_label method.
class AttendanceRecord(ABC):
    def __init__(self, student_name: str, date_str: str):
        self.student_name = student_name
        self.date_str = date_str

    @abstractmethod
    def status_label(self) -> str:
        pass

    def to_dict(self) -> dict:
        pass

# Inheritance: PresentRecord and AbsentRecord inherit the basic properties (student_name, date_str) 
# from AttendanceRecord. This prevents us from having to rewrite the __init__ logic in every subclass.
class PresentRecord(AttendanceRecord):
    def status_label(self) -> str:
        return "✅ Present"

    def to_dict(self) -> dict:
        return {"student_name": self.student_name, "date_str": self.date_str, "status": "present"}

class AbsentRecord(AttendanceRecord):
    def status_label(self) -> str:
        return "❌ Absent"

    def to_dict(self) -> dict:
        return {"student_name": self.student_name, "date_str": self.date_str, "status": "absent"}

# Encapsulation: The tracker protects its internal list of records by making it private (_records).
# Outside code must use controlled methods like mark_attendance() to interact with the data safely.
class AttendanceTracker:
    def __init__(self, file_path: str = "attendance.json"):
        self.file_path = file_path
        self._records: List[AttendanceRecord] = []
        self._load_records()

    def mark_attendance(self, student_name: str, status: str):
        date_str = datetime.date.today().isoformat()
        if status == "present":
            self._records.append(PresentRecord(student_name, date_str))
        else:
            self._records.append(AbsentRecord(student_name, date_str))
        self._save_records()

    def get_all_records(self) -> List[AttendanceRecord]:
        return list(reversed(self._records))

    def get_attendance_rate(self, student_name: str) -> float:
        student_records = [r for r in self._records if r.student_name == student_name]
        if not student_records:
            return 0.0
        
        present_count = sum(1 for r in student_records if isinstance(r, PresentRecord))
        return (present_count / len(student_records)) * 100

    def _save_records(self):
        data = [record.to_dict() for record in self._records]
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def _load_records(self):
        if not os.path.exists(self.file_path):
            return
        
        with open(self.file_path, 'r') as f:
            try:
                data = json.load(f)
                for item in data:
                    if item.get("status") == "present":
                        self._records.append(PresentRecord(item["student_name"], item["date_str"]))
                    else:
                        self._records.append(AbsentRecord(item["student_name"], item["date_str"]))
            except json.JSONDecodeError:
                pass
