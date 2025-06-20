// Section switching logic for admin portal

document.addEventListener('DOMContentLoaded', function () {
    // Get all sidebar links with data-target
    const sidebarLinks = document.querySelectorAll('.sidebar-link[data-target]');
    // Get all main sections
    const mainSections = [
        '#main-dashboard',
        '#main-monitoring',
        '#main-file-management',
        '#main-system-policy',
        '#main-security-alerts',
        '#main-settings'
    ].map(id => document.querySelector(id)).filter(Boolean);

    sidebarLinks.forEach(link => {
        link.addEventListener('click', function () {
            // Remove highlight from all links
            sidebarLinks.forEach(l => l.classList.remove('bg-blue-50', 'dark:bg-[#23272F]', 'text-blue-600', 'dark:text-blue-400', 'font-semibold', 'shadow'));
            // Highlight the clicked link
            link.classList.add('bg-blue-50', 'dark:bg-[#23272F]', 'text-blue-600', 'dark:text-blue-400', 'font-semibold', 'shadow');

            // Hide all main sections
            mainSections.forEach(section => section.classList.add('hidden'));
            // Show the selected section
            const targetId = link.getAttribute('data-target');
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                targetSection.classList.remove('hidden');
            }
        });
    });
});
