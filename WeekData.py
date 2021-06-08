from DayData import DayData


class WeekData:
    def __init__(self, district_id):
        self.days_data = [DayData(1, district_id), DayData(2, district_id), DayData(3, district_id),
                          DayData(4, district_id)]
        self.messages = self.create_messages()

    def create_messages(self):
        messages = []
        for day_data in self.days_data:
            day_wise_messages = day_data.create_session_message()
            if len(day_wise_messages):
                messages += day_wise_messages
        return messages
