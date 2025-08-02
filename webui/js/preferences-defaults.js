// Set permanent default preferences for Father Ted interface
document.addEventListener('DOMContentLoaded', function() {
    // Set defaults on page load
    const setDefaults = () => {
        // Autoscroll always on
        if (window.toggleAutoScroll) {
            window.toggleAutoScroll(true);
        }
        
        // Dark mode always on (with Irish theme)
        localStorage.setItem('darkMode', 'true');
        document.body.classList.add('dark-mode');
        
        // Speech off
        localStorage.setItem('speech', 'false');
        if (window.toggleSpeech) {
            window.toggleSpeech(false);
        }
        
        // Show thoughts off
        if (window.toggleThoughts) {
            window.toggleThoughts(false);
        }
        
        // Show JSON off
        if (window.toggleJson) {
            window.toggleJson(false);
        }
        
        // Show utility messages off
        if (window.toggleUtils) {
            window.toggleUtils(false);
        }
    };
    
    // Run immediately
    setDefaults();
    
    // Also run after a short delay to ensure all functions are loaded
    setTimeout(setDefaults, 500);
    
    // Override localStorage to prevent changes to dark mode
    const originalSetItem = localStorage.setItem;
    localStorage.setItem = function(key, value) {
        if (key === 'darkMode') {
            // Always force dark mode to true
            originalSetItem.call(this, key, 'true');
        } else {
            originalSetItem.call(this, key, value);
        }
    };
});