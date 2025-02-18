document.addEventListener('DOMContentLoaded', function() {
    const link = document.getElementById('link');
    const navMenu = document.getElementById('nav-menu');
    const menuLinks = document.querySelectorAll('.menu_item_links');

    

    // Ensure the activeLink is not null before proceeding
    const targetLink = document.querySelector('.target');
    console.log('Target Link:', targetLink);

    link.addEventListener('click', function() {
        navMenu.classList.toggle('target');
        link.classList.toggle('target');
    });

    menuLinks.forEach(link => {
        link.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            const menuItems = document.querySelectorAll('.menu-item');

            menuItems.forEach(item => {
                if (category === 'All' || item.getAttribute('data-category') === category) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });

    if (!targetLink) {
        console.error("target Link does not exist");
        return;
    }
});

