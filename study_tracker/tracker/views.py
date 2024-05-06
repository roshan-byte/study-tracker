from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Timetable
from django.http import JsonResponse
import pandas as pd
import re


def homepage(request):
    return render(request, 'homepage.html')

def upload_timetable(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        if excel_file.name.endswith('.xlsx'):
            # Clean the database: Delete all existing entries
            Timetable.objects.all().delete()
            # Read Excel file using pandas
            df = pd.read_excel(excel_file)
            timetable_entries = []
            # Iterate through rows and save data to database
            for index, row in df.iterrows():
                activity = row['Activity']
                start_time = row['Start Time']
                end_time = row['End Time']
                timetable_entry = Timetable(activity=activity, start_time=start_time, end_time=end_time)
                timetable_entry.save()
                timetable_entries.append(timetable_entry)
            # Redirecting to homepage
            return render(request, 'upload_timetable.html', {'timetable_entries': timetable_entries})
        else:
            return render(request, 'upload_timetable.html', {'error_message': 'Please upload a valid Excel file.'})
    return render(request, 'upload_timetable.html')


def time_in_seconds(total_time:str)->int:
    # breakpoint()
    time = re.findall('(\d+)\shours\s(\d+)\sminutes',total_time)
    return int(time[0][0])*60*60+int(time[0][1])*60

def get_timetable_data(request):
    # Fetch timetable data from the database
    timetable_entries = Timetable.objects.all().order_by('start_time')
    # Convert timetable data to JSON format
    data = [{
        'name': entry.activity,
        'duration': time_in_seconds(entry.total_time),  # total_time is in seconds
    } for entry in timetable_entries]

    # Return JSON response
    return JsonResponse(data, safe=False)

def download_template(request):
    """it will create a sample template to fill timetable"""
    df = pd.DataFrame(columns=['Activity', 'Start Time', 'End Time'])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="timetable_template.xlsx"'
    df.to_excel(response, index=False)
    return response
