function navigateTo(url) {
    // Add click animation
    event.target.style.transform = 'scale(0.95)';
    setTimeout(() => {
        event.target.style.transform = '';
    }, 150);

    // Navigation logic
    setTimeout(() => {
        console.log('Navigating to:', url);
        window.location.href = url;
    }, 200); // Small delay for animation
}

// Add loading animation on page load
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.dashboard-btn');
    
    buttons.forEach((button, index) => {
        button.style.opacity = '0';
        button.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            button.style.transition = 'all 0.6s ease';
            button.style.opacity = '1';
            button.style.transform = 'translateY(0)';
        }, index * 200);
    });
});