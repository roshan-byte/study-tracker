FROM python:3 
WORKDIR /studyTrackerApp
COPY requirements.txt /studyTrackerApp/
RUN pip install -r requirements.txt 
COPY . /studyTrackerApp/ 
CMD python manage.py runserver
# Make port 8000 available to the world outside this container
EXPOSE 8000
# Define environment variable
ENV PYTHONUNBUFFERED 1