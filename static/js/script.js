// static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    // Handle image loading animation
    const images = document.querySelectorAll('.book-item img');
    
    // For images already loaded from cache
    images.forEach(img => {
        if (img.complete) {
            img.classList.add('loaded');
        }
    });
    
    // For images that load after DOM is ready
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.classList.add('loaded');
        });
    });
    
    // Add any other JavaScript functionality here
});