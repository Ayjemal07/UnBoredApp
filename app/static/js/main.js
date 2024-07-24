// Define global variables
let currentVideoId = ''; // Store the current video ID
let clickCount = 0;


//Activity Suggestion Generation Logic
document.addEventListener('DOMContentLoaded', function () {
    const suggestButton = document.getElementById('suggest-button');
    const nextSuggest = document.getElementById('next-suggest');
    const activityContainer = document.getElementById('activity-container');
    let spinner = document.getElementById('spinner');


    // Event listener for initial suggestion
    suggestButton.addEventListener('click', async () => {
        clickCount = 0;
        console.log('Suggest button clicked');
        await fetchActivity();
    }, { passive: true });

    // Event listener for next suggestion
    nextSuggest.addEventListener('click', async () => {
        clickCount += 1;
        console.log('Next suggest button clicked');
        await fetchActivity();
    }, { passive: true });

    const upperCaseName = (act_name) => act_name.toUpperCase();

    // Function to fetch activity data
    const fetchActivity = async () => {
        try {
            console.log('Showing spinner');
            // Show spinner
            spinner.style.display = 'block';

            const response = await fetch(`/suggest_activity?clickCount=${clickCount}`);
            const data = await response.json();

            console.log('Activity fetched:', data);

            console.log(data.youtube)
            // Extract video ID from YouTube URL
            const urlParams = new URL(data.youtube).searchParams;
            currentVideoId = urlParams.get('v');

            const embedUrl = `https://www.youtube-nocookie.com/embed/${currentVideoId}?origin=${window.location.origin}`;

            // Clear previous content
            activityContainer.innerHTML = '';

            const upperCasedActivityName = upperCaseName(data.name);

            // Display activity details
            const activityCard = document.createElement('div');
            activityCard.className = 'activity-card';
            activityCard.innerHTML = `
                <div class="flex-container">
                    <div id="player-container">
                        <iframe
                            width="620"
                            height="550"
                            src="${embedUrl}"
                            frameborder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen>
                        </iframe>
                    </div>
                    <div class="details-container">
                        <h2>${upperCasedActivityName}</h2>
                        <p>${data.description}</p>
                        <p>Why should you do this activity?<br><span>${data.why_worth}</span></p>
                        <div class="button-container">
                            <a href="${data.meetup}" target="_blank">Join ${data.name} Meetup</a><br>
                            <a href="${data.google}" target="_blank">Google this activity near you</a>
                            <a href="https://www.youtube.com/results?search_query=what+is+${data.name}" target="_blank">Watch more videos of this activity</a><br>
                        </div>
                    </div>    
                </div>
            `;

            activityContainer.appendChild(activityCard);

            // Delay hiding the spinner 
            console.log('Hiding spinner');
            spinner.style.display = 'none';
            // Show the activity container and the next button
            activityContainer.style.display = 'block';
            nextSuggest.style.display = 'inline-block';

            // Hide the suggest button
            suggestButton.style.display = 'none';
        } catch (error) {
            console.error('Error fetching activity:', error);
            spinner.style.display = 'none';

        }
    };
});


//Slider List Logic

document.addEventListener('DOMContentLoaded', function () {
    const sliderList = document.getElementById('slider-list');
    const prevButton = document.querySelector('.prev-button');
    const nextButton = document.querySelector('.next-button');
    let currentPage = 1;
    const perPage = 6; // Number of items per page

    // Function to fetch and display cherry-picked activities
    const fetchCherryPickedActivities = async (page) => {
        try {
            const response = await fetch(`/activities?page=${page}&per_page=${perPage}`);
            const data = await response.json();

            if (data.length === 0) {
                console.log('No more activities to load.');
                nextButton.disabled = true; // Disable next button if no more activities
                return; // No more activities to load
            }

            data.forEach(activity => {
                const listItem = document.createElement('li');
                listItem.className = 'slider__item';
                listItem.innerHTML = `
                    <article class="card">
                        <div class="card__thumbnail">
                            <img alt="${activity.name}" src="./static/images/${activity.name}.jpg">
                        </div>
                        <header>
                            <div class="card__heading">
                                <p role="heading" aria-level="3">
                                    <span class="card__subtitle">${activity.name.toUpperCase()}</span>
                                    <span class="card__title">${activity.description}</span>
                                </p>
                            </div>
                        </header>
                        <footer class="card__footer">
                            <a class="button" href="${activity.google_link}" aria-label="ENGAGE NOW">ENGAGE NOW</a>
                        </footer>
                    </article>
                `;
                sliderList.appendChild(listItem);
            });
        } catch (error) {
            console.error('Error fetching cherry-picked activities:', error);
        }
    };

    // Function to handle next slide
    const loadNextSlide = () => {
        currentPage++;
        fetchCherryPickedActivities(currentPage);
    };

    // Function to handle previous slide
    const loadPreviousSlide = () => {
        if (currentPage > 1) {
            currentPage--;
            sliderList.innerHTML = ''; // Clear previous content
            fetchCherryPickedActivities(currentPage);
        }
    };

    // Load initial set of activities
    fetchCherryPickedActivities(currentPage);

    // Event listeners for navigation buttons
    nextButton.addEventListener('click', loadNextSlide);
    prevButton.addEventListener('click', loadPreviousSlide);
});



// Session Handling logic
let sessionTimeout;

window.addEventListener("beforeunload", function () {
    // Send a request to invalidate the session when the tab is closed
    navigator.sendBeacon("/reset_session");
});

window.addEventListener("blur", function() {
    // Clear the timeout if the tab is closed or navigated away
    clearTimeout(sessionTimeout);
    sessionTimeout = setTimeout(function() {
        navigator.sendBeacon("/reset_session");
    }, 3600000); 
});

// Optional: Handle page load
window.addEventListener("load", function() {
    // Reset any existing session timeouts on load
    clearTimeout(sessionTimeout);
});

// Example of optimized setTimeout usage
function performTasks() {
    setTimeout(() => {
        // Perform part of the task
        taskPart1();
        setTimeout(() => {
            // Continue with more tasks
            taskPart2();
        }, 0);
    }, 0);
}