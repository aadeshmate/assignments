from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class SubTask(BaseModel):
    id:int=Field("Id for each subtask")
    description:str=Field("Description for each subtask")
    status:Literal["pending","completed","failed"]="pending"
    result:Optional[str] = None

class TaskPlan(BaseModel):
    tasks: List[SubTask] = Field(description="ordered sub task")


class AgentState(BaseModel):
    user_goal: str
    tasks: List[SubTask] = Field(default_factory=list)

    def set_tasks(self, tasks: List[SubTask]):
        self.tasks = tasks

    def get_next_pending_task(self) -> Optional[SubTask]:
        for task in self.tasks:
            if task.status == "pending":
                return task
        return None

    def complete_task(self, task_id: int, result: str):
        for task in self.tasks:
            if task.id == task_id:
                task.status = "completed"
                task.result = result
        return None

    def get_completed_context(self) -> str:
        completed_tasks = []
        for task in self.tasks:
            if task.status == "completed":
                completed_tasks.append(
                    f"""
                    Task ID: {task.id}
                    Description: {task.description}
                    Result: {task.result}
                    """
                )
        return "\n".join(completed_tasks)

    def display_board(self):
        print(f"\nUser Goal : {self.user_goal}")
        print("-" * 50)
        for task in self.tasks:
            print(f"Task ID : {task.id}")
            print(f"Description : {task.description}")
            print(f"Status : {task.status}")
            print(f"Result : {task.result}")
            print("-" * 50)
