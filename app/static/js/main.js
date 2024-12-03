/*
    Denver Crime Heatmap
        Konstantin Zaremski

    main.js

*/

function locateUserAndZoom() {
    window.leaflet.locate({setView: true, maxZoom: 16});
}

function locateDenverAndZoom() {
    window.leaflet.setView([39.74582, -104.98750], 14);
}

function toggleMenu() {
    const menuElement = document.querySelector('#menu');
    const mapElement = document.querySelector('#map');

    if (menuElement.className === 'expanded') {
        menuElement.className = '';
        mapElement.className = '';
    } else {
        menuElement.className = 'expanded';
        mapElement.className = 'darkened';
    }
}

// Actions to take upon window load 
window.addEventListener('load', function() {
    // ** Setup Leaflet Map
    // Define the leaflet map object
    var map = L.map('map', {
        zoomControl: false
    }).setView([39.74582, -104.98750], 16.2); // Center of Denver that I like: 39.74582° N, 104.98750° W

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        minZoom: 14,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);

    L.control.zoom({
        position: 'topright'
    }).addTo(map);

    window.heat = L.heatLayer([], {radius: 50}).addTo(map);

    map.locate({setView: false, maxZoom: 16});

    function onLocationFound(e) {
        var radius = e.accuracy;
        L.circle(e.latlng, radius).addTo(map);
    }

    map.on('locationfound', onLocationFound);
    
    // Set a global variable to reference this map object
    window.leaflet = map;

    // ** Bind the toggle menu action to the menu handle bar
    const spanElement = document.querySelector('span.menu-handle');
    spanElement.addEventListener('mousedown', toggleMenu);   // Bind to mousedown
    spanElement.addEventListener('dragstart', toggleMenu);   // Bind to dragstart
    spanElement.addEventListener('touchstart', toggleMenu);  // Bind to touchstart

    // ** Bind the locate user button to the locate user action
    const locateUserButton = document.querySelector('#center-on-user-location-button');
    locateUserButton.addEventListener('click', locateUserAndZoom);
    locateUserButton.addEventListener('click', toggleMenu);
    // ** Bind the locate Denver button to the locate user action
    const locateDenverButton = document.querySelector('#center-on-denver-button');
    locateDenverButton.addEventListener('click', locateDenverAndZoom);
    locateDenverButton.addEventListener('click', toggleMenu);

    queryPredictionsAPI(0);
    clearTimeout(window.debounceTimer);
});

// ** Form Handling
const timeDeltaInput = document.getElementById('time_delta');
const timeDeltaLabel = document.getElementById('time_delta_label');

window.debounceTimer = 0; // Timer for debouncing the API call

// Function to update the label based on slider value
function updateTimeLabel() {
    clearTimeout(window.debounceTimer)

    const currentTime = new Date();
    const timeDelta = parseInt(timeDeltaInput.value); // get the time delta value

    // Add the delta value (in hours) to the current time
    const adjustedTime = new Date(currentTime);
    adjustedTime.setHours(adjustedTime.getHours() + timeDelta);

    // Get the time string in a readable format
    const timeString = adjustedTime.toLocaleString([], {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: true
    });

    // Calculate the absolute difference in hours
    const absDelta = Math.abs(timeDelta);
    let label = "";

    if (timeDelta === 0) {
        label = "(+0) Current Time";
    } else if (timeDelta < 0) { // Past times
        if (absDelta >= 24) {
            const daysAgo = Math.floor(absDelta / 24);
            label = `${daysAgo} day${daysAgo > 1 ? 's' : ''} ago (${timeString})`;
        } else {
            label = `${absDelta} hour${absDelta > 1 ? 's' : ''} ago (${timeString})`;
        }
    } else { // Future times
        const daysFromNow = Math.floor(absDelta / 24);
        const hoursFromNow = absDelta % 24;
        
        if (absDelta >= 24) {
            // If it's more than 1 day in the future, show days and hours
            if (hoursFromNow > 0) {
                label = `${daysFromNow} day${daysFromNow > 1 ? 's' : ''}, ${hoursFromNow} hour${hoursFromNow > 1 ? 's' : ''} from now (${timeString})`;
            } else {
                label = `${daysFromNow} day${daysFromNow > 1 ? 's' : ''} from now (${timeString})`;
            }
        } else {
            label = `${absDelta} hour${absDelta > 1 ? 's' : ''} from now (${timeString})`;
        }
    }

    // Update the label
    timeDeltaLabel.value = label;

    window.debounceTimer = setTimeout(() => queryPredictionsAPI(timeDelta), 3000);
}

window.predictions = []

function updateHeatmap() {
    heatmap = [];
    window.heat.setLatLngs(heatmap);
    
    if (window.heatmapVariant == 'Likelihood') {
        const crimeCounts = window.predictions.map(point => Number(point.crime_count) || 0);
        const minCrimeCount = crimeCounts.reduce((min, count) => Math.min(min, count), Infinity);
        const maxCrimeCount = crimeCounts.reduce((max, count) => Math.max(max, count), -Infinity);
    
        for (const point of window.predictions) {
            const normalizedCrimeCount = (point.crime_count - minCrimeCount) / (maxCrimeCount - minCrimeCount);
            const intensity = normalizedCrimeCount ** 2;
            heatmap.push([point.lon, point.lat, intensity]);
        }
    } else if (window.heatmapVariant == 'Type') {
        const crimeTypes = window.predictions.map(point => Number(point.crime_type) || 0);
        const minCrimeType = crimeTypes.reduce((min, type) => Math.min(min, type), Infinity);
        const maxCrimeType = crimeTypes.reduce((max, type) => Math.max(max, type), -Infinity);
    
        for (const point of window.predictions) {
            const normalizedCrimeType = (point.crime_type - minCrimeType) / (maxCrimeType - minCrimeType);
            const intensity = normalizedCrimeType ** 2;
            heatmap.push([point.lon, point.lat, intensity]);
        }
    } else {
        const crimeTypes = window.predictions.map(point => Number(point.crime_type) || 0);
        const minCrimeType = crimeTypes.reduce((min, type) => Math.min(min, type), Infinity);
        const maxCrimeType = crimeTypes.reduce((max, type) => Math.max(max, type), -Infinity);
    
        const crimeCounts = window.predictions.map(point => Number(point.crime_count) || 0);
        const minCrimeCount = crimeCounts.reduce((min, count) => Math.min(min, count), Infinity);
        const maxCrimeCount = crimeCounts.reduce((max, count) => Math.max(max, count), -Infinity);
    
        for (const point of window.predictions) {
            const normalizedCrimeType = (point.crime_type - minCrimeType) / (maxCrimeType - minCrimeType);
            const normalizedCrimeCount = (point.crime_count - minCrimeCount) / (maxCrimeCount - minCrimeCount);
    
            const intensity = (normalizedCrimeCount ** 2 + ((normalizedCrimeType ** 2) / 2));
            heatmap.push([point.lon, point.lat, intensity]);
        }
    }
    
    window.heat.setLatLngs(heatmap);

    Toastify({
        text: "Finished Updating",
        position: "center",
        duration: 2500,
        style: {
            background: "green",
        },
    }).showToast();
}

window.heatmapVariant = "Combined";

document.getElementById("display_combined").addEventListener("change", function() {
    if (this.checked) {
        heatmapVariant = "Combined";
    }
    updateHeatmap();
});

document.getElementById("display_likelihood").addEventListener("change", function() {
    if (this.checked) {
        heatmapVariant = "Likelihood";
    }
    updateHeatmap();
});

document.getElementById("display_type").addEventListener("change", function() {
    if (this.checked) {
        heatmapVariant = "Type";
    }
    updateHeatmap();
});

async function queryPredictionsAPI(timeDelta) {
    try {
        Toastify({
            text: "Loading predictions",
            position: "center",
            duration: 2500
        }).showToast();

        const response = await fetch('/api/predictions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ time_delta: timeDelta }),
        });

        const data = await response.json();

        if ("message" in data) {
            Toastify({
                text: "Predictions not available for that time, please try again later.",
                position: "center",
                duration: 2500,
                style: {
                    background: "red",
                },
            }).showToast();
            return
        }

        if (response.ok) {
            //console.log('Predictions:', );
            window.predictions = data.predictions;
            updateHeatmap();
            Toastify({
                text: "Updating Heatmap",
                position: "center",
                duration: 2500
            }).showToast();
        } else {
            console.error('Error:', data);
            Toastify({
                text: "Error while getting predictions.",
                position: "center",
                duration: 2500,
                style: {
                    background: "red",
                },
            }).showToast();
        }
    } catch (error) {
        console.error('API Request Failed:', error);
        Toastify({
            text: "Error while getting predictions.",
            position: "center",
            duration: 2500,
            style: {
                background: "red",
            },
        }).showToast();
    }
}

// Attach event listener to the slider
timeDeltaInput.addEventListener('input', updateTimeLabel);

// Initial call to set the label on page load
updateTimeLabel();





