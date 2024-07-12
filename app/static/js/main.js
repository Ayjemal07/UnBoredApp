document.addEventListener('DOMContentLoaded', function () {
    const suggestButton = document.getElementById('suggest-button');
    const nextSuggest = document.getElementById('next-suggest');
    const activityContainer = document.getElementById('activity-container');
    let player; // Variable to store the YouTube player
    let playerReady = false; // Flag to indicate if the player is ready
    let currentVideoId = ''; // Store the current video ID
    let clickCount = 0;





    //note to myself: try removing auto from the playVars
    //and try this function loadNewVideo():
    //if player{player.cueVideobyId(videoId)}
    //check chatgpt for this suggestion from last convo


    // Function to initialize the YouTube player
    function initializePlayer(videoId) {
        player = new YT.Player('player', {
            height: '315',
            width: '560',
            videoId: videoId,
            playerVars: {
                'controls': 1,
                'rel': 0,
                'showinfo': 0,
                'origin': window.location.origin
            },
            events: {
                'onReady': onPlayerReady,
                'onStateChange': onPlayerStateChange
            }
        });
    }

    // Function to load a new video in the player
    function loadNewVideo(videoId) {
        if (playerReady) {
            player.cueVideoById(videoId);
        } else {
            console.error('Player is not ready yet.');
        }
    }

    // Function to handle player ready event
    function onPlayerReady(event) {
        playerReady = true;
        // Load video when player is ready
        if (currentVideoId) {
            loadNewVideo(currentVideoId);
        }
    }

    // Function to handle player state changes
    function onPlayerStateChange(event) {
        if (event.data == YT.PlayerState.ENDED) {
            console.log('Video has ended.');
            // Optionally handle video end event
        } else if (event.data == YT.PlayerState.PAUSED) {
            console.log('Video is paused.');
            // Optionally handle video pause event
        } else if (event.data == YT.PlayerState.PLAYING) {
            console.log('Video is playing.');
            // Optionally handle video play event
        }
    }

    // Load the YouTube IFrame Player API asynchronously
    var tag = document.createElement('script');
    tag.src = 'https://www.youtube.com/iframe_api';
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    // Event listener for initial suggestion
    suggestButton.addEventListener('click', async () => {
        clickCount = 0;
        console.log('Suggest button clicked');
        await fetchActivity();
    }, { passive: true }); // Add passive: true

    // Event listener for next suggestion
    nextSuggest.addEventListener('click', async () => {
        clickCount += 1;
        console.log('Next suggest button clicked');
        await fetchActivity();
    }, { passive: true }); // Add passive: true


    // Function to fetch activity data
    const fetchActivity = async () => {
        try {
            const response = await fetch(`/suggest_activity?clickCount=${clickCount}`);
            const data = await response.json();

            console.log('Activity fetched:', data);

            // Clear previous content
            activityContainer.innerHTML = '';

            // Display activity details
            const activityCard = document.createElement('div');
            activityCard.className = 'activity-card';
            activityCard.innerHTML = `
                <h2>${data.name}</h2>
                <p>${data.description}</p>
                <p>Why it's worth doing this activity: ${data.why_worth}</p>
                <div id="player"></div>
                <a href="${data.youtube}" target="_blank">Watch this activity in action</a><br>
                <a href="${data.meetup}" target="_blank">Join a Meetup</a><br>
                <a href="${data.google}" target="_blank">Google this activity near me</a>
            `;

            activityContainer.appendChild(activityCard);

            // Extract video ID from YouTube URL
            const urlParams = new URL(data.youtube).searchParams;
            currentVideoId = urlParams.get('v');

            if (!currentVideoId) {
                console.error('Could not extract video ID from URL:', data.youtube);
                return;
            }

            // Initialize or load the YouTube player with the new video
            if (typeof YT !== 'undefined' && YT.loaded) {
                if (player) {
                    player.destroy(); // Destroy the existing player before creating a new one
                    initializePlayer(currentVideoId); // Reinitialize the player with the new video
                } else {
                    initializePlayer(currentVideoId);
                }
            } else {
                console.error('YouTube API not yet loaded.');
            }


            // Show the next button
            nextSuggest.style.display = 'inline-block';

            // Hide the suggest button
            suggestButton.style.display = 'none';
        } catch (error) {
            console.error('Error fetching activity:', error);
        }
    };


    // Check if the YouTube IFrame API is loaded, and reinitialize the player if necessary
    window.onYouTubeIframeAPIReady = function() {
        if (currentVideoId) {
            initializePlayer(currentVideoId);
        }
    };

});






//Session Handling logic 
let sessionTimeout;

window.addEventListener("beforeunload", function (e) {
    // Send a request to invalidate the session 10 minutes after tab is closed
    navigator.sendBeacon("/reset_session");
});

window.addEventListener("blur", function() {
    // Clear the timeout if the tab is closed or navigated away
    clearTimeout(sessionTimeout);
    sessionTimeout = setTimeout(function() {
        navigator.sendBeacon("/reset_session");
    }, 3600000); // 1 hour delay after navigating away
});

// Optional: Handle page load
window.addEventListener("load", function() {
    // Reset any existing session timeouts on load
    clearTimeout(sessionTimeout);

});