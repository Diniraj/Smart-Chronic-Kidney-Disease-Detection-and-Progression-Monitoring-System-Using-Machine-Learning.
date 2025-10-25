// Smart CKD Health Management System - Main JavaScript

// Global variables
let currentLanguage = 'en';
let currentTheme = 'light';
let translations = {};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    initializeLanguage();
    initializeTooltips();
    initializeFormValidation();
});

// Theme management
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
}

function toggleTheme() {
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
}

function setTheme(theme) {
    currentTheme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        themeIcon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
    }
}

// Language management
async function initializeLanguage() {
    const savedLanguage = localStorage.getItem('language') || 'en';
    await setLanguage(savedLanguage);
}

async function changeLanguage(language) {
    await setLanguage(language);
}

async function setLanguage(language) {
    currentLanguage = language;
    localStorage.setItem('language', language);
    
    const currentLanguageSpan = document.getElementById('current-language');
    if (currentLanguageSpan) {
        currentLanguageSpan.textContent = language === 'en' ? 'English' : 'ಕನ್ನಡ';
    }
    
    // Send language preference to server
    try {
        await fetch('/api/set-language', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({language: language})
        });
    } catch (error) {
        console.error('Error setting language preference:', error);
    }
    
    // Fetch translations from server
    try {
        const response = await fetch(`/api/get-translations/${language}`);
        const data = await response.json();
        
        if (data.success) {
            translations = data.translations;
            updatePageLanguage(language);
        }
    } catch (error) {
        console.error('Error fetching translations:', error);
    }
}

function updatePageLanguage(language) {
    // Update all elements with data-translate attribute
    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        const translation = translations[key] || key;
        element.textContent = translation;
    });
    
    // Update form placeholders
    document.querySelectorAll('[data-placeholder]').forEach(element => {
        const key = element.getAttribute('data-placeholder');
        const translation = translations[key] || key;
        element.placeholder = translation;
    });
    
    // Update page title
    const titleElement = document.querySelector('title');
    if (titleElement && translations['page_title']) {
        titleElement.textContent = translations['page_title'];
    }
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Utility functions
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container') || createAlertContainer();
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function createAlertContainer() {
    const container = document.createElement('div');
    container.id = 'alert-container';
    container.className = 'position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1050';
    document.body.appendChild(container);
    return container;
}

// Loading states
function showLoading(element) {
    if (element) {
        element.disabled = true;
        const originalText = element.innerHTML;
        element.innerHTML = '<span class="loading"></span> Loading...';
        element.setAttribute('data-original-text', originalText);
    }
}

function hideLoading(element) {
    if (element) {
        element.disabled = false;
        const originalText = element.getAttribute('data-original-text');
        if (originalText) {
            element.innerHTML = originalText;
            element.removeAttribute('data-original-text');
        }
    }
}

// API helper functions
async function apiCall(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const mergedOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, mergedOptions);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'An error occurred');
        }
        
        return data;
    } catch (error) {
        console.error('API call failed:', error);
        showAlert(`Error: ${error.message}`, 'danger');
        throw error;
    }
}

// Chart helper functions
function createChart(canvasId, config) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`Canvas with id '${canvasId}' not found`);
        return null;
    }
    
    return new Chart(ctx, config);
}

// Table helper functions
function filterTable(tableId, searchTerm, columnIndex = -1) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const tbody = table.querySelector('tbody');
    if (!tbody) return;
    
    const rows = tbody.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        let shouldShow = false;
        
        if (columnIndex === -1) {
            // Search all columns
            shouldShow = Array.from(cells).some(cell => 
                cell.textContent.toLowerCase().includes(searchTerm.toLowerCase())
            );
        } else {
            // Search specific column
            const cell = cells[columnIndex];
            if (cell) {
                shouldShow = cell.textContent.toLowerCase().includes(searchTerm.toLowerCase());
            }
        }
        
        row.style.display = shouldShow ? '' : 'none';
    });
}

// Modal helper functions
function showModal(modalId) {
    const modal = new bootstrap.Modal(document.getElementById(modalId));
    modal.show();
}

function hideModal(modalId) {
    const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
    if (modal) {
        modal.hide();
    }
}

// Local storage helpers
function saveToLocalStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
        console.error('Error saving to localStorage:', error);
    }
}

function loadFromLocalStorage(key, defaultValue = null) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
        console.error('Error loading from localStorage:', error);
        return defaultValue;
    }
}

// Date formatting
function formatDate(date, format = 'short') {
    const d = new Date(date);
    
    if (format === 'short') {
        return d.toLocaleDateString();
    } else if (format === 'long') {
        return d.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    } else if (format === 'datetime') {
        return d.toLocaleString();
    }
    
    return d.toString();
}

// Number formatting
function formatNumber(number, decimals = 2) {
    return parseFloat(number).toFixed(decimals);
}

function formatPercentage(number, decimals = 1) {
    return `${(number * 100).toFixed(decimals)}%`;
}

// Validation helpers
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[\+]?[1-9][\d]{0,15}$/;
    return re.test(phone.replace(/\s/g, ''));
}

function validateAge(age) {
    const num = parseInt(age);
    return !isNaN(num) && num >= 0 && num <= 150;
}

// Health parameter validation
function validateHealthParameter(value, min = 0, max = 1000) {
    const num = parseFloat(value);
    return !isNaN(num) && num >= min && num <= max;
}

// Export functions for use in other scripts
window.CKDApp = {
    showAlert,
    showLoading,
    hideLoading,
    apiCall,
    createChart,
    filterTable,
    showModal,
    hideModal,
    saveToLocalStorage,
    loadFromLocalStorage,
    formatDate,
    formatNumber,
    formatPercentage,
    validateEmail,
    validatePhone,
    validateAge,
    validateHealthParameter,
    toggleTheme,
    changeLanguage,
    currentLanguage,
    currentTheme
};
