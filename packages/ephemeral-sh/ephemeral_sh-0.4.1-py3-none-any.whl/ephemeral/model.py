from dataclasses import asdict, dataclass, field
import datetime
import json
from pathlib import Path
from typing import List
import uuid


@dataclass
class Task:
    task: str
    start_ts: int = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    end_ts: int | None = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    @property
    def json(self) -> dict:
        data = asdict(self)
        data["id"] = str(data["id"])
        return data


class Tracker:
    def __init__(self) -> None:
        self.path = Path.home() / ".config" / "ephemeral"
        self.current_task: Task | None = None
        self.history: List[Task] = []

    @classmethod
    def load(self) -> "Tracker":
        tracker = Tracker()
        if not tracker.path.is_file():
            tracker.path.parent.mkdir(exist_ok=True)
            tracker.path.write_text("{}")
        data = json.loads(tracker.path.read_text())
        tracker.current_task = None
        if data.get("current_task") is not None:
            tracker.current_task = Task(**data.get("current_task"))
        _history = data.get("history", [])
        tracker.history = [Task(**_task) for _task in _history]
        return tracker

    def save(self) -> None:
        _history = [_task.json for _task in self.history]
        data: dict = {"history": _history}
        if self.current_task is not None:
            data["current_task"] = self.current_task.json
        self.path.write_text(json.dumps(data))

    def update(self, new_task: Task | None = None, save_to_history: bool = True) -> None:
        # add current task to history
        if save_to_history and self.current_task is not None:
            self.current_task.end_ts = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
            self.history.append(self.current_task)
        # update current task
        self.current_task = new_task

    def clear(self, task: bool = True, history: bool = True) -> None:
        """clear all information from the system"""
        if task:
            self.current_task = None
        if history:
            self.history = []
