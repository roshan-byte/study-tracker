from datetime import datetime, timedelta
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    goal = models.TextField()
    total_hours_allocated = models.IntegerField()
    daily_hours = models.IntegerField()

    def __str__(self):
        return self.name

class Timetable(models.Model):
    activity = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_time = models.CharField(max_length=50, blank=True)  # Field to store the calculated total time

    def save(self, *args, **kwargs):
        # Calculate the total time before saving
        self.calculate_total_time()
        super().save(*args, **kwargs)

    def calculate_total_time(self):
        # Convert start_time and end_time to datetime.time objects if they are strings
        if isinstance(self.start_time, str):
            self.start_time = datetime.strptime(self.start_time, '%H:%M').time()
        if isinstance(self.end_time, str):
            self.end_time = datetime.strptime(self.end_time, '%H:%M').time()
        
        # Calculate the difference between end_time and start_time
        start_datetime = datetime.combine(datetime.today(), self.start_time)
        end_datetime = datetime.combine(datetime.today(), self.end_time)
        
        # Handle overnight activities
        if end_datetime < start_datetime:
            end_datetime += timedelta(days=1)
        
        total_seconds = (end_datetime - start_datetime).total_seconds()
        
        # Convert total seconds to hours and minutes
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        
        # Total time in string format
        self.total_time = f"{hours} hours {minutes} minutes"

    def __str__(self):
        return self.activity

class Quote(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text
