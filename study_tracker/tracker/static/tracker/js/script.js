 // Function to start timer for each entry
 function startTimer(duration, activityName) {
    var timer = duration;
    var activityNameElement = document.getElementById("activity-name");
    var timerElement = document.getElementById("timer");
    activityNameElement.textContent = activityName; 

    var intervalId = setInterval(function () {
    var hours = Math.floor(timer / 3600);
    var minutes = Math.floor((timer % 3600) / 60);
    var seconds = timer % 60;
     
    var formattedTime = 
        (hours < 10 ? "0" + hours : hours) + ":" +
        (minutes < 10 ? "0" + minutes : minutes) + ":" +
        (seconds < 10 ? "0" + seconds : seconds);

    timerElement.textContent = formattedTime;

        if (--timer < 0) {
            clearInterval(intervalId); // Clear the interval
            // Move to the next activity
            var nextActivity = getNextActivity(activityName); // You need to implement this function
            if (nextActivity) {
                startTimer(nextActivity.duration, nextActivity.name);
            }
        }
    }, 1000);
}

// Function to start timer for all activities
function startAllTimers() {
    fetch('/get_timetable_data') // Endpoint to fetch timetable data from server
        .then(response => response.json())
        .then(data => {
            data.forEach(activity => {
                startTimer(activity.duration, activity.name);
            });
        })
        .catch(error => console.error('Error fetching timetable data:', error));
}

// Start all timers when the button is clicked
document.getElementById('start-timer-btn').addEventListener('click', startAllTimers);