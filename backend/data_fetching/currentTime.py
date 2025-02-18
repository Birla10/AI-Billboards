from datetime import datetime

class TimeClassifier:
    def __init__(self):
        self.current_month = datetime.now().month
        self.current_time = datetime.now().time()

    def get_time_period(self):
        if self.current_time >= datetime.strptime("05:00", "%H:%M").time() and self.current_time < datetime.strptime("07:00", "%H:%M").time():
            return "Dawn"
        elif self.current_time >= datetime.strptime("07:00", "%H:%M").time() and self.current_time < datetime.strptime("12:00", "%H:%M").time():
            return "Morning"
        elif self.current_time >= datetime.strptime("12:00", "%H:%M").time() and self.current_time < datetime.strptime("16:00", "%H:%M").time():
            return "Afternoon"
        elif self.current_time >= datetime.strptime("16:00", "%H:%M").time() and self.current_time < datetime.strptime("18:00", "%H:%M").time():
            return "Evening"
        elif self.current_time >= datetime.strptime("18:00", "%H:%M").time() and self.current_time < datetime.strptime("19:00", "%H:%M").time():
            return "Dusk"
        else:
            return "Night"
        
    def get_month(self):
        if(self.current_month >= 3 and self.current_month <= 5):
            return "Spring"
        elif(self.current_month >= 6 and self.current_month <= 8):
            return "Summer"
        elif(self.current_month >= 9 and self.current_month <= 11):
            return "Autumn/Fall"
        else:
            return "Winter"

