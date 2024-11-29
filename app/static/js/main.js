/*
    Denver Crime Heatmap
        Konstantin Zaremski

    main.js

*/

// Center of Denver that I like: 39.74582° N, 104.98750° W
var map = L.map('map').setView([39.74582, -104.98750], 16.2);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    minZoom: 14,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

map.locate({setView: false, maxZoom: 16});

function onLocationFound(e) {
    var radius = e.accuracy;

    L.marker(e.latlng).addTo(map);

    L.circle(e.latlng, radius).addTo(map);
}

map.on('locationfound', onLocationFound);


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

window.addEventListener('load', function() {
    const spanElement = document.querySelector('span.menu-handle');
    spanElement.addEventListener('mousedown', toggleMenu);   // Bind to mousedown
    spanElement.addEventListener('dragstart', toggleMenu);   // Bind to dragstart
    spanElement.addEventListener('touchstart', toggleMenu);  // Bind to touchstart
});


