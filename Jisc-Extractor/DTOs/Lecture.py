from datetime import datetime

class Lecture:
    def __init__(self, time, name, eventId) -> None:
        if isinstance(time, str):
            self.time = datetime.fromisoformat(time[:-1])  
        else:
            self.time = time  
    
        self.name = name
        self.eventId = eventId
    
    def __str__(self):
        formatted_time = self.time.strftime("%H:%M %d/%m/%Y")
        return f"{self.name}: {formatted_time}, Id: {self.eventId}"

    def __repr__(self):
        return self.__str__()

