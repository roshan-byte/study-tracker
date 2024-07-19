# views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Timetable
from django.http import JsonResponse
import pandas as pd
import re
from datetime import datetime

def homepage(request):
    return render(request, 'homepage.html')

def upload_timetable(request):
    timetable_entries = Timetable.objects.all().order_by('start_time')
    if request.method == 'POST' and request.FILES.get('excel_file'):
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
            return render(request, 'upload_timetable.html', {'timetable_entries': timetable_entries})
        else:
            return render(request, 'upload_timetable.html', {'error_message': 'Please upload a valid Excel file.', 'timetable_entries': timetable_entries})
    return render(request, 'upload_timetable.html', {'timetable_entries': timetable_entries})

def time_in_seconds(total_time: str) -> int:
    time = re.findall(r'(\d+)\shours\s(\d+)\sminutes', total_time)
    return int(time[0][0]) * 60 * 60 + int(time[0][1]) * 60

def get_timetable_data(request):
    timetable_entries = Timetable.objects.all().order_by('start_time')
    data = [{
        'name': entry.activity,
        'duration': time_in_seconds(entry.total_time),
    } for entry in timetable_entries]
    return JsonResponse(data, safe=False)

def download_template(request):
    df = pd.DataFrame(columns=['Activity', 'Start Time', 'End Time'])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="timetable_template.xlsx"'
    df.to_excel(response, index=False)
    return response

def edit_timetable(request):
    if request.method == 'POST':
        timetable_entries = Timetable.objects.all()
        for i, entry in enumerate(timetable_entries, start=1):
            activity = request.POST.get(f'activity_{i}')
            start_time_str = request.POST.get(f'start_time_{i}')
            end_time_str = request.POST.get(f'end_time_{i}')

            try:
                start_time = datetime.strptime(start_time_str, '%I %p').time()
                end_time = datetime.strptime(end_time_str, '%I %p').time()
            except ValueError:
                return render(request, 'upload_timetable.html', {
                    'timetable_entries': timetable_entries,
                    'error_message': 'Invalid time format. Please use the format "H AM/PM".'
                })

            entry.activity = activity
            entry.start_time = start_time
            entry.end_time = end_time
            entry.save()
        return redirect('upload_timetable')

    timetable_entries = Timetable.objects.all()
    return render(request, 'upload_timetable.html', {'timetable_entries': timetable_entries})
