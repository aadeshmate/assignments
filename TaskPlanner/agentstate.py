from pydantic import BaseModel,Field
from typing import Literal,List,Optional

class SubTask(BaseModel):
    id:int=Field(description="Task Id")
    description:str=Field(description="Decomposition of complex task")
    status:Literal["pending","completed"]="pending"
    result:Optional[str]=None

class TaskPlan(BaseModel):
    tasks:List[SubTask]=Field(description="Ordered Sub Task")


class AgentState:
    def __init__(self,user_goal:str):
        self.user_goal = user_goal
        self.tasks:List[SubTask] = []

    def set_tasks(self,tasks:List[SubTask]):
        self.tasks = tasks

    def get_next_pending_task(self)->Optional[SubTask]:
        for task in self.tasks:
            if task.status=="pending":
                return task

        return None

    def complete_task(self,task_id:int,result:str):
        for task in self.tasks:
            if task.id==task_id:
                task.status='completed'
                task.result=result
                return task

        return None 

    def display_task(self):
        print(f"\nUser Goal : {self.user_goal}")
        print("-"*50)

        for task in self.tasks:
            print(f"Task ID : {task.id}")
            print(f"Description : {task.description}")
            print(f"Status : {task.description}")
            print(f"Result : {task.result}")
            print("-"*50)
        