from datetime import datetime
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    goal = models.TextField()
    total_hours_allocated = models.IntegerField()
    daily_hours = models.IntegerField()

class Timetable(models.Model):
    activity = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    # duration = models.DurationField(null=True, blank=True)
    # accumulated_time = models.DurationField(null=True, blank=True) # will add later 
    total_time = models.CharField(max_length=50, blank=True)  # Field to store the calculated total time


    def save(self, *args, **kwargs):
        # Calculate the total time before saving
        self.calculate_total_time()
        super().save(*args, **kwargs)

    def calculate_total_time(self):
        # Calculate the difference between end_time and start_time
        # Convert times to datetime objects (taking reference of today's date)
        start_datetime = datetime.combine(datetime.today(), self.start_time)
        end_datetime = datetime.combine(datetime.today(), self.end_time)
        # breakpoint()
        total_seconds = abs((start_datetime - end_datetime).total_seconds())
        # Convert total seconds to hours and minutes
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        #total time in string format
        self.total_time = f"{hours} hours {minutes} minutes"


    def __str__(self):
        return self.activity


class Quote(models.Model):
    text = models.TextField()
