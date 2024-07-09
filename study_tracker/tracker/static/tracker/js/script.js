// Function to start timer for each entry
function startTimer(duration, activityName) {
    console.log(`Starting timer for activity: ${activityName} with duration: ${duration} seconds`);
    
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
            console.log(`Timer ended for activity: ${activityName}`);
            // Move to the next activity
            var nextActivity = getNextActivity();
            if (nextActivity) {
                console.log(`Starting next timer for activity: ${nextActivity.name}`);
                startTimer(nextActivity.duration, nextActivity.name);
            } else {
                console.log('All activities completed');
            }
        }
    }, 1000);
}

// Function to fetch and start timers for all activities sequentially based on the current time
function startAllTimers() {
    fetch('/get_timetable_data') // Endpoint to fetch timetable data from server
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Fetched data:', data);

            if (data.length > 0) {
                // Initialize activity index
                var currentIndex = 0;

                // Function to get the next activity
                function getNextActivity() {
                    currentIndex++;
                    if (currentIndex < data.length) {
                        return data[currentIndex];
                    } else {
                        return null;
                    }
                }

                // Convert start and end times to durations in seconds
                data.forEach(activity => {
                    let startTime = parseTime(activity.start_time);
                    let endTime = parseTime(activity.end_time);
                    let duration = (endTime - startTime) / 1000; // Convert to seconds
                    if (duration < 0) {
                        duration += 24 * 3600; // Handle overnight activities
                    }
                    activity.duration = duration;
                    activity.startTimestamp = startTime;
                });

                console.log('Processed data with durations:', data);

                // Calculate delay based on current time and start time of the first activity
                let currentTime = new Date();
                let firstActivity = data[currentIndex];
                let delay = (firstActivity.startTimestamp - currentTime) / 1000; // Delay in seconds

                if (delay < 0) {
                    // If the start time has already passed, start the timer immediately
                    delay = 0;
                }

                setTimeout(() => {
                    console.log('Starting first timer for:', data[currentIndex]);
                    startTimer(data[currentIndex].duration, data[currentIndex].name);
                }, delay * 1000); // Convert delay to milliseconds
            }
        })
        .catch(error => console.error('Error fetching timetable data:', error));
}

// Function to parse time string (e.g., "8 a.m." or "1 p.m.") to Date object
function parseTime(timeStr) {
    let timeParts = timeStr.split(' ');
    let time = timeParts[0].split(':');
    let hours = parseInt(time[0]);
    let minutes = time.length > 1 ? parseInt(time[1]) : 0;
    let period = timeParts[1];

    if (period === 'p.m.' && hours < 12) {
        hours += 12;
    } else if (period === 'a.m.' && hours === 12) {
        hours = 0;
    }

    let now = new Date();
    return new Date(now.getFullYear(), now.getMonth(), now.getDate(), hours, minutes, 0); // Use today's date
}

// Start all timers when the button is clicked
document.getElementById('start-timer-btn').addEventListener('click', startAllTimers);





