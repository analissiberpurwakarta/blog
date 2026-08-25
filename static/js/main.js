document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.getElementById('navMenu');

    if (!menuToggle || !navMenu) return;

    // Toggle menu saat tombol hamburger diklik
    menuToggle.addEventListener('click', () => {
        menuToggle.classList.toggle('is-active');
        navMenu.classList.toggle('nav-active');
    });

    // Tutup menu secara otomatis saat klik di luar area header/menu
    document.addEventListener('click', (event) => {
        const isClickInside = menuToggle.contains(event.target) || navMenu.contains(event.target);
        
        if (!isClickInside && navMenu.classList.contains('nav-active')) {
            menuToggle.classList.remove('is-active');
            navMenu.classList.remove('nav-active');
        }
    });
});