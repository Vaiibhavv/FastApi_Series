from datetime import datetime
class TaskClass:
    id:int
    name: str
    taskid: int
    status: str
    createdat: datetime

    def __init__(self,id,name,taskid,status) -> None:
        self.id=id
        self.name=name
        self.taskid=taskid
        self.status=status
        self.createdat=datetime.now()