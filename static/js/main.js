document.addEventListener('DOMContentLoaded', () => {
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const header = document.querySelector('.header');

    if (mobileNavToggle) {
        mobileNavToggle.addEventListener('click', () => {
            header.classList.toggle('active');
            mobileNavToggle.classList.toggle('active');
        });
    }

    // Close mobile menu when a link is clicked
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (header.classList.contains('active')) {
                header.classList.remove('active');
                if (mobileNavToggle) {
                    mobileNavToggle.classList.remove('active');
                }
            }
        });
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (header && mobileNavToggle) {
            const isClickInsideHeader = header.contains(e.target);
            const isClickOnToggle = mobileNavToggle.contains(e.target);
            
            if (!isClickInsideHeader && !isClickOnToggle && header.classList.contains('active')) {
                header.classList.remove('active');
                mobileNavToggle.classList.remove('active');
            }
        }
    });
});
