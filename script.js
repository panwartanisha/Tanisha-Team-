/**
 * Electricity Consumption Analysis - JavaScript Functions
 * Custom JS for Flask web application interactivity
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips and popovers
    initializeTooltips();
    
    // Add smooth scroll behavior
    addSmoothScroll();
    
    // Add animation on scroll
    addScrollAnimations();
    
    // Initialize dashboard features
    initializeDashboardFeatures();
    
    // Add page load animation
    addPageLoadAnimation();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Add smooth scroll to anchor links
 */
function addSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Add animations when elements scroll into view
 */
function addScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all cards
    document.querySelectorAll('.card, .finding-card, .scenario-card').forEach(el => {
        observer.observe(el);
    });
}

/**
 * Initialize dashboard-specific features
 */
function initializeDashboardFeatures() {
    // Check if we're on the dashboard page
    if (document.getElementById('tableauContainer')) {
        addDashboardRefreshButton();
    }
    
    // Check if we're on the story page
    if (document.getElementById('storyContainer')) {
        addStoryNavigationHints();
    }
}

/**
 * Add dashboard refresh functionality
 */
function addDashboardRefreshButton() {
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            // Visual feedback
            this.innerHTML = '<i class="fas fa-sync-alt fa-spin"></i> Refreshing...';
            
            // Reload iframe
            const iframe = document.getElementById('tableauFrame');
            if (iframe) {
                iframe.src = iframe.src;
                
                // Reset button after 2 seconds
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh';
                }, 2000);
            }
        });
    }
}

/**
 * Add story navigation hints
 */
function addStoryNavigationHints() {
    console.log('Story page loaded - narrative visualization ready');
}

/**
 * Add page load animation
 */
function addPageLoadAnimation() {
    const body = document.body;
    body.style.opacity = '0';
    body.style.animation = 'fadeIn 0.5s ease-out forwards';
}

/**
 * Utility: Format number with commas
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Utility: Format percentage
 */
function formatPercentage(value) {
    return (value * 100).toFixed(2) + '%';
}

/**
 * Fetch and display API statistics
 */
function loadStatistics() {
    fetch('/api/statistics')
        .then(response => response.json())
        .then(data => {
            console.log('Statistics loaded:', data);
            updateStatisticsDisplay(data);
        })
        .catch(error => console.error('Error loading statistics:', error));
}

/**
 * Update statistics display
 */
function updateStatisticsDisplay(stats) {
    // This function can be used to dynamically update page elements
    // with the loaded statistics
    console.log('Statistics available for dynamic updates');
}

/**
 * Health check - verify API is running
 */
function checkHealthStatus() {
    fetch('/api/health')
        .then(response => response.json())
        .then(data => {
            console.log('API Status:', data.status);
            console.log('Service:', data.service);
        })
        .catch(error => console.warn('Health check failed:', error));
}

/**
 * Toggle dark mode (optional feature)
 */
function toggleDarkMode() {
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    const newDarkMode = !isDarkMode;
    
    localStorage.setItem('darkMode', newDarkMode);
    
    if (newDarkMode) {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showNotification('Failed to copy', 'error');
    });
}

/**
 * Show notification toast
 */
function showNotification(message, type = 'info') {
    const alertClass = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    }[type] || 'alert-info';
    
    const alertElement = document.createElement('div');
    alertElement.className = `alert ${alertClass} alert-dismissible fade show`;
    alertElement.style.position = 'fixed';
    alertElement.style.top = '20px';
    alertElement.style.right = '20px';
    alertElement.style.zIndex = '9999';
    alertElement.style.minWidth = '300px';
    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertElement);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        alertElement.remove();
    }, 5000);
}

/**
 * Initialize chart rendering (if using Chart.js)
 */
function initializeCharts() {
    console.log('Chart initialization ready');
    // Add chart-specific code here if needed
}

/**
 * Handle responsive navigation
 */
function handleResponsiveNav() {
    const navbar = document.querySelector('.navbar');
    if (window.innerWidth <= 768) {
        // Mobile-specific behavior
    } else {
        // Desktop-specific behavior
    }
}

/**
 * Add window resize listener for responsive behavior
 */
window.addEventListener('resize', function() {
    handleResponsiveNav();
});

/**
 * Export data functionality
 */
function exportData(format = 'json') {
    console.log('Export data as', format);
    // Implement export logic here
}

/**
 * Print page functionality
 */
function printPage() {
    window.print();
}

/**
 * Advanced filtering (if implemented)
 */
function applyFilter(filterType, filterValue) {
    console.log(`Applying ${filterType} filter: ${filterValue}`);
    // Implement filter logic here
}

/**
 * Search functionality
 */
function searchData(searchTerm) {
    console.log('Searching for:', searchTerm);
    // Implement search logic here
}

// Initialize health check on page load
window.addEventListener('load', function() {
    checkHealthStatus();
    loadStatistics();
});

// Log page analytics (optional)
console.log('Electricity Consumption Analysis - Web Application Loaded');
console.log('Dashboard ready for interaction');
