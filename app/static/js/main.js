// Define global variables
let currentVideoId = ''; // Store the current video ID
let clickCount = 0;
let sessionTimeout; // Define session timeout variable

// Reset session timeout function
function resetSessionTimeout() {
    // Clear any existing timeout
    clearTimeout(sessionTimeout);

    // Set a new timeout for 10 minutes
    sessionTimeout = setTimeout(function() {
        console.log("Session reset due to inactivity");
        navigator.sendBeacon("/reset_session");
    }, 600000); // 10 minutes
}

// Initial session timeout reset on page load
window.addEventListener("load", resetSessionTimeout);

// User interactions that reset the timeout
document.addEventListener('click', resetSessionTimeout);
document.addEventListener('scroll', resetSessionTimeout);

// Other existing event listeners here
document.addEventListener('DOMContentLoaded', function () {
    const suggestButton = document.getElementById('suggest-button');
    const activityContainer = document.getElementById('activity-container');
    const spinner = document.getElementById('spinner');

    // Create and initialize the next-suggest button
    const nextSuggestButton = document.createElement('button');
    nextSuggestButton.id = 'next-suggest';
    nextSuggestButton.className = 'next-suggest';
    nextSuggestButton.innerHTML = 'NEXT <span class="arrow-right"></span><span class="arrow-right"></span><span class="arrow-right"></span>';
    nextSuggestButton.style.display = 'none'; // Initially hidden
    nextSuggestButton.disabled = true; // Initially disabled

    // Event listener for next-suggest button
    nextSuggestButton.addEventListener('click', async () => {
        clickCount += 1;
        console.log('Next suggest button clicked');
        await fetchActivity();
    }, { passive: true });

    // Event listener for initial suggestion
    suggestButton.addEventListener('click', async () => {
        clickCount = 0;
        console.log('Suggest button clicked');
        await fetchActivity();
    }, { passive: true });

    // Function to fetch and display activity data
    const displayActivity = async (data) => {
        try {
            // Show spinner
            spinner.style.display = 'block';

            // Extract video ID from YouTube URL
            const urlParams = new URL(data.youtube).searchParams;
            currentVideoId = urlParams.get('v');
            console.log('YouTube URL:', data.youtube);

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
                            <a href="${data.meetup}" target="_blank">Meetup</a>
                            <a href="${data.google}" target="_blank">Google</a>
                        </div>
                    </div>
                </div>
                <div class="action-buttons-container">
                    <button id="like-button" class="like-button">
                        <span class="heart">&#9825;</span>
                        <span class="like-text">Like</span>
                    </button>
                    <button id="share-button" class="share-button">
                        <span <i class="fa-sharp-duotone fa-solid fa-arrow-up-from-bracket" 
                        style="--fa-primary-color: #376228; --fa-secondary-color: #376228;"></i></span> 
                        <span class="share-text">Share</span>
                    </button>
                    <button id="next-suggest" class="next-suggest">
                        Next
                        <span class="arrow-right"></span>
                        <span class="arrow-right"></span>
                        <span class="arrow-right"></span>
                    </button>
                </div>
            `;

            activityCard.appendChild(nextSuggestButton);
            activityContainer.appendChild(activityCard);

            // Show the activity container and the next button
            activityContainer.style.display = 'block';
            nextSuggestButton.style.display = 'inline-block'; // Make button visible
            nextSuggestButton.disabled = false; // Enable button

            spinner.style.display = 'none';

            // Event listener for like button (heart toggle)
            const likeButton = document.getElementById('like-button');
            likeButton.addEventListener('click', () => {
                if (likeButton.classList.contains('liked')) {
                    likeButton.classList.remove('liked');
                    likeButton.innerHTML = '&#9825;'; // Empty heart
                } else {
                    likeButton.classList.add('liked');
                    likeButton.innerHTML = '&#9829;'; // Filled red heart
                }
            });

            // Event listener for share button
            const shareButton = activityCard.querySelector('#share-button');
            shareButton.addEventListener('click', () => {
                const shareMessage = `
                    Check out this activity:
                    - Activity: ${upperCasedActivityName}
                    - Description: ${data.description}
                    - Why it's worth doing: ${data.why_worth}
                    - Join Meetups: ${data.meetup}
                    - Google this activity near you: ${data.google}
                `;
                
                // Copy shareMessage to clipboard (you can also use a messaging service)
                navigator.clipboard.writeText(shareMessage)
                    .then(() => {
                        alert('Activity details copied! Now share it with your friends.');
                    })
                    .catch(err => {
                        console.error('Error copying text: ', err);
                    });
            });
            

        } catch (error) {
            console.error('Error displaying activity:', error);
            spinner.style.display = 'none';
            nextSuggestButton.disabled = false; // Ensure button is enabled even if there's an error
        }
    };

    // Function to fetch activity data
    const fetchActivity = async () => {
        try {
            // Show spinner
            spinner.style.display = 'block';
            // Disable suggest button
            suggestButton.style.display = 'none';
            // Disable next-suggest button
            nextSuggestButton.disabled = true;

            const response = await fetch(`/suggest_activity?clickCount=${clickCount}`);
            const data = await response.json();

            console.log('Activity fetched:', data);
            await displayActivity(data);

        } catch (error) {
            console.error('Error fetching activity:', error);
            spinner.style.display = 'none';
            nextSuggestButton.disabled = false; // Ensure button is enabled even if there's an error
        }
    };

    // Function to handle 'Engage Now' button click
    const handleEngageNowClick = async (activityId) => {
        try {
            // Show spinner
            spinner.style.display = 'block';
            // Disable suggest button
            suggestButton.style.display = 'none';
            // Disable next-suggest button
            nextSuggestButton.disabled = true;

            const response = await fetch(`/activities/${activityId}`);
            const data = await response.json();

            console.log('Activity fetched:', data);
            await displayActivity(data);

        } catch (error) {
            console.error('Error fetching activity:', error);
            spinner.style.display = 'none';
            nextSuggestButton.disabled = false; // Ensure button is enabled even if there's an error
        }
    };

    // Event delegation for Engage Now button clicks
    document.addEventListener('click', async (event) => {
        if (event.target && event.target.classList.contains('engage-now')) {
            event.preventDefault(); // Prevent the default link action
            const activityId = event.target.getAttribute('data-activity-id');
            await handleEngageNowClick(activityId);
        }
    }, { passive: false });

    const upperCaseName = (act_name) => act_name.toUpperCase();
});

// Slider List Logic

document.addEventListener('DOMContentLoaded', function () {
    const sliderList = document.getElementById('slider-list');
    const prevButton = document.querySelector('.prev-button');
    const nextButton = document.querySelector('.next-button');
    let currentPage = 1;
    const perPage = 4; // Number of items per page

    // Function to fetch and display cherry-picked activities
    const fetchCherryPickedActivities = async (page) => {
        try {
            const response = await fetch(`/activityset?page=${page}&per_page=${perPage}`);
            const data = await response.json();

            if (data.length === 0) {
                console.log('No more activities to load.');
                nextButton.disabled = true; // Disable next button if no more activities
                return; // No more activities to load
            }

            sliderList.innerHTML = ''; // Clear previous content

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
                            <a class="button engage-now" data-activity-id="${activity.id}" aria-label="ENGAGE NOW">ENGAGE NOW</a>
                        </footer>
                    </article>
                `;
                sliderList.appendChild(listItem);
            });

            // Enable next button if there are more activities
            nextButton.disabled = false;

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

// Navbar Hiding when Scrolling

let lastScrollTop = 0;

document.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navigation');
    const currentScroll = window.scrollY || document.documentElement.scrollTop;

    if (currentScroll > lastScrollTop) {
        // Scrolling down
        navbar.classList.add('hidden');
    } else {
        // Scrolling up
        navbar.classList.remove('hidden');
    }

    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll; // For Mobile or negative scrolling
});

// Session Handling logic
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
