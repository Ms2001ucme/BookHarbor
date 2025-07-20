// Add this to a file in static/js/navbar.js
document.addEventListener('DOMContentLoaded', function() {
    // Add mobile toggle button to the navbar
    const navbarContainer = document.querySelector('.navbar-container');
    const mobileToggle = document.createElement('button');
    mobileToggle.className = 'mobile-toggle';
    mobileToggle.innerHTML = '☰';
    navbarContainer.insertBefore(mobileToggle, document.querySelector('.navbar-links'));
    
    // Handle mobile toggle click
    mobileToggle.addEventListener('click', function() {
        document.querySelector('.navbar-links').classList.toggle('active');
        document.querySelector('.navbar form').classList.toggle('active');
    });
    
    // Handle dropdown clicks on mobile
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            if (window.innerWidth <= 992) {
                e.preventDefault();
                this.closest('.dropdown').classList.toggle('active');
            }
        });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown.active').forEach(dropdown => {
                dropdown.classList.remove('active');
            });
        }
    });
    
    // Update navbar on window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 992) {
            document.querySelector('.navbar-links').classList.remove('active');
            document.querySelector('.navbar form').classList.remove('active');
            document.querySelectorAll('.dropdown.active').forEach(dropdown => {
                dropdown.classList.remove('active');
            });
        }
    });
});