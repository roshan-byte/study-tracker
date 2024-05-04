from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Timetable
import pandas as pd


def homepage(request):
    return HttpResponse("here is the homepage.")

def upload_timetable(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        if excel_file.name.endswith('.xlsx'):
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
            # Redirect to homepage or display success message
            return render(request, 'upload_timetable.html', {'timetable_entries': timetable_entries})
        else:
            return render(request, 'upload_timetable.html', {'error_message': 'Please upload a valid Excel file.'})
    return render(request, 'upload_timetable.html')

def download_template(request):
    # Create a template Excel file
    df = pd.DataFrame(columns=['Activity', 'Start Time', 'End Time'])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="timetable_template.xlsx"'
    df.to_excel(response, index=False)
    return response
