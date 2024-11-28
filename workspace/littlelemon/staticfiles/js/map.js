document.addEventListener('DOMContentLoaded', function() {
    console.log('Map Page');
    const map = L.map('map').setView([41.8767252, -87.6250969], 17);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    const marker = L.marker([41.8767252, -87.6250969]).addTo(map);
});