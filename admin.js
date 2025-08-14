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
        '#main-settings',
        '#main-about',
        '#main-create-staff'
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

    // Initialize Security Events Chart
    initializeSecurityChart();
});

// Security Events Chart
function initializeSecurityChart() {
    const ctx = document.getElementById('security-events-chart');
    if (!ctx) return;

    // Check if dark mode is active
    const isDarkMode = document.body.classList.contains('dark') || 
                      window.matchMedia('(prefers-color-scheme: dark)').matches;

    // Chart configuration
    const config = {
        type: 'line',
        data: {
            labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'],
            datasets: [
                {
                    label: 'Normal Activities',
                    data: [12, 8, 25, 45, 38, 22, 15],
                    borderColor: isDarkMode ? '#10B981' : '#059669',
                    backgroundColor: isDarkMode ? 'rgba(16, 185, 129, 0.1)' : 'rgba(5, 150, 105, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Suspicious Activities',
                    data: [2, 1, 5, 8, 6, 3, 2],
                    borderColor: isDarkMode ? '#F59E0B' : '#D97706',
                    backgroundColor: isDarkMode ? 'rgba(245, 158, 11, 0.1)' : 'rgba(217, 119, 6, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Security Threats',
                    data: [0, 0, 2, 3, 1, 0, 1],
                    borderColor: isDarkMode ? '#EF4444' : '#DC2626',
                    backgroundColor: isDarkMode ? 'rgba(239, 68, 68, 0.1)' : 'rgba(220, 38, 38, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            layout: {
                padding: {
                    top: 20,
                    right: 20,
                    bottom: 20,
                    left: 20
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    align: 'start',
                    labels: {
                        color: isDarkMode ? '#E5E7EB' : '#374151',
                        usePointStyle: true,
                        padding: 20,
                        font: {
                            size: 12,
                            family: 'Inter',
                            weight: '500'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: isDarkMode ? '#1F2937' : '#FFFFFF',
                    titleColor: isDarkMode ? '#E5E7EB' : '#111827',
                    bodyColor: isDarkMode ? '#D1D5DB' : '#374151',
                    borderColor: isDarkMode ? '#374151' : '#E5E7EB',
                    borderWidth: 1,
                    cornerRadius: 8,
                    displayColors: true,
                    padding: 12,
                    callbacks: {
                        title: function(context) {
                            return 'Time: ' + context[0].label;
                        },
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y + ' events';
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: isDarkMode ? '#374151' : '#E5E7EB',
                        drawBorder: false,
                        display: true
                    },
                    ticks: {
                        color: isDarkMode ? '#9CA3AF' : '#6B7280',
                        font: {
                            size: 11,
                            family: 'Inter'
                        },
                        maxRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 7
                    },
                    border: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: isDarkMode ? '#374151' : '#E5E7EB',
                        drawBorder: false,
                        display: true
                    },
                    ticks: {
                        color: isDarkMode ? '#9CA3AF' : '#6B7280',
                        font: {
                            size: 11,
                            family: 'Inter'
                        },
                        callback: function(value) {
                            return value + '';
                        },
                        maxTicksLimit: 6
                    },
                    border: {
                        display: false
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            },
            elements: {
                point: {
                    radius: 4,
                    hoverRadius: 6,
                    borderWidth: 2,
                    borderColor: function(context) {
                        return context.dataset.borderColor;
                    }
                },
                line: {
                    borderWidth: 3
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeInOutQuart'
            },
            transitions: {
                active: {
                    animation: {
                        duration: 400
                    }
                }
            }
        }
    };

    // Create the chart
    const securityChart = new Chart(ctx, config);

    // Handle window resize to maintain layout
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            securityChart.resize();
        }, 250);
    });

    // Update chart on dark mode toggle
    const modeToggle = document.getElementById('modeToggle');
    if (modeToggle) {
        modeToggle.addEventListener('click', function() {
            setTimeout(() => {
                updateChartTheme(securityChart);
            }, 100);
        });
    }

    // Simulate real-time updates with layout preservation
    setInterval(() => {
        updateChartData(securityChart);
    }, 30000); // Update every 30 seconds

    // Return chart instance for potential external access
    return securityChart;
}

// Update chart theme based on dark/light mode
function updateChartTheme(chart) {
    const isDarkMode = document.body.classList.contains('dark');
    
    // Update colors for each dataset
    chart.data.datasets[0].borderColor = isDarkMode ? '#10B981' : '#059669';
    chart.data.datasets[0].backgroundColor = isDarkMode ? 'rgba(16, 185, 129, 0.1)' : 'rgba(5, 150, 105, 0.1)';
    
    chart.data.datasets[1].borderColor = isDarkMode ? '#F59E0B' : '#D97706';
    chart.data.datasets[1].backgroundColor = isDarkMode ? 'rgba(245, 158, 11, 0.1)' : 'rgba(217, 119, 6, 0.1)';
    
    chart.data.datasets[2].borderColor = isDarkMode ? '#EF4444' : '#DC2626';
    chart.data.datasets[2].backgroundColor = isDarkMode ? 'rgba(239, 68, 68, 0.1)' : 'rgba(220, 38, 38, 0.1)';

    // Update legend colors
    chart.options.plugins.legend.labels.color = isDarkMode ? '#E5E7EB' : '#374151';
    
    // Update axis colors
    chart.options.scales.x.grid.color = isDarkMode ? '#374151' : '#E5E7EB';
    chart.options.scales.x.ticks.color = isDarkMode ? '#9CA3AF' : '#6B7280';
    chart.options.scales.y.grid.color = isDarkMode ? '#374151' : '#E5E7EB';
    chart.options.scales.y.ticks.color = isDarkMode ? '#9CA3AF' : '#6B7280';
    
    // Update tooltip colors
    chart.options.plugins.tooltip.backgroundColor = isDarkMode ? '#1F2937' : '#FFFFFF';
    chart.options.plugins.tooltip.titleColor = isDarkMode ? '#E5E7EB' : '#111827';
    chart.options.plugins.tooltip.bodyColor = isDarkMode ? '#D1D5DB' : '#374151';
    chart.options.plugins.tooltip.borderColor = isDarkMode ? '#374151' : '#E5E7EB';
    
    chart.update();
}

// Simulate real-time data updates
function updateChartData(chart) {
    // Add small random variations to simulate real-time data
    chart.data.datasets.forEach(dataset => {
        dataset.data = dataset.data.map(value => {
            const variation = Math.random() * 6 - 3; // -3 to +3
            return Math.max(0, Math.round(value + variation));
        });
    });
    
    chart.update('none'); // Update without animation for smoother real-time feel
}
