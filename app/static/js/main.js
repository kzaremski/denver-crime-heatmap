/*
    Denver Crime Heatmap
        Konstantin Zaremski

    main.js

*/

function locateUserAndZoom() {
    window.leaflet.locate({setView: true, maxZoom: 16});
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

    map.locate({setView: false, maxZoom: 16});

    function onLocationFound(e) {
        var radius = e.accuracy;

        L.marker(e.latlng).addTo(map);

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
});


