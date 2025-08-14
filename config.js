// Digital Twin System Configuration
// Update these settings to match your backend setup

const CONFIG = {
    // Backend API Configuration
    API_BASE_URL: 'http://localhost:8000',
    WS_BASE_URL: 'ws://localhost:8000',
    
    // Authentication
    TOKEN_KEY: 'digital_twin_token',
    USER_KEY: 'digital_twin_user',
    
    // API Endpoints
    ENDPOINTS: {
        // Authentication
        LOGIN: '/token',
        REGISTER: '/register',
        
        // Admin Routes
        ADMIN_DASHBOARD: '/admin/dashboard/stats',
        ADMIN_USERS: '/admin/users',
        ADMIN_SECURITY_ALERTS: '/admin/security/alerts',
        ADMIN_ACTIVITIES: '/admin/activities',
        ADMIN_ANALYTICS: '/admin/analytics/activities',
        ADMIN_CREATE_STAFF: '/admin/staff/create',
        
        // Staff Routes
        STAFF_PROFILE: '/staff/profile',
        STAFF_DEPARTMENT_STATS: '/staff/department/stats',
        STAFF_ACTIVITY_SUMMARY: '/staff/activity/summary',
        STAFF_PERFORMANCE: '/staff/performance/metrics',
        STAFF_COLLEAGUES: '/staff/colleagues',
        
        // Activity Routes
        ACTIVITY_LOG: '/activity/log',
        ACTIVITY_USER: '/activity/user',
        ACTIVITY_ALL: '/activity/all',
        ACTIVITY_SUSPICIOUS: '/activity/suspicious',
        ACTIVITY_SUMMARY: '/activity/summary',
        
        // WebSocket
        WS_ADMIN: '/ws/admin',
        WS_STAFF: '/ws/staff',
        WS_USERS: '/ws/users'
    },
    
    // Default Users (for testing)
    DEFAULT_USERS: {
        ADMIN: {
            username: 'admin',
            password: 'admin123',
            role: 'admin'
        },
        STAFF: {
            username: 'staff1',
            password: 'staff123',
            role: 'staff'
        },
        USER: {
            username: 'user1',
            password: 'user123',
            role: 'user'
        }
    },
    
    // System Settings
    SETTINGS: {
        SESSION_TIMEOUT: 30 * 60 * 1000, // 30 minutes
        REFRESH_INTERVAL: 5000, // 5 seconds
        MAX_RETRY_ATTEMPTS: 3,
        WEBSOCKET_RECONNECT_DELAY: 3000 // 3 seconds
    },
    
    // Activity Types for Logging
    ACTIVITY_TYPES: {
        LOGIN: 'user_login',
        LOGOUT: 'user_logout',
        FILE_ACCESS: 'file_access',
        FILE_UPLOAD: 'file_upload',
        FILE_DOWNLOAD: 'file_download',
        FILE_DELETE: 'file_delete',
        SETTINGS_CHANGE: 'settings_change',
        USER_CREATED: 'user_created',
        USER_DELETED: 'user_deleted',
        USER_STATUS_CHANGED: 'user_status_changed',
        SECURITY_ALERT: 'security_alert',
        SUSPICIOUS_ACTIVITY: 'suspicious_activity',
        SYSTEM_ACCESS: 'system_access',
        ADMIN_ACTION: 'admin_action',
        STAFF_ACTION: 'staff_action'
    },
    
    // Security Alert Types
    SECURITY_ALERTS: {
        FAILED_LOGIN: 'failed_login',
        MULTIPLE_FAILED_LOGINS: 'multiple_failed_logins',
        UNAUTHORIZED_ACCESS: 'unauthorized_access',
        SUSPICIOUS_FILE_ACCESS: 'suspicious_file_access',
        BRUTE_FORCE_ATTEMPT: 'brute_force_attempt',
        UNUSUAL_ACTIVITY: 'unusual_activity'
    }
};

// Helper functions for API calls
const API = {
    // Get full API URL
    getUrl: (endpoint) => `${CONFIG.API_BASE_URL}${endpoint}`,
    
    // Get WebSocket URL
    getWsUrl: (clientType) => `${CONFIG.WS_BASE_URL}/ws/${clientType}`,
    
    // Get stored token
    getToken: () => localStorage.getItem(CONFIG.TOKEN_KEY),
    
    // Set token
    setToken: (token) => localStorage.setItem(CONFIG.TOKEN_KEY, token),
    
    // Remove token
    removeToken: () => localStorage.removeItem(CONFIG.TOKEN_KEY),
    
    // Get stored user
    getUser: () => {
        const userStr = localStorage.getItem(CONFIG.USER_KEY);
        return userStr ? JSON.parse(userStr) : null;
    },
    
    // Set user
    setUser: (user) => localStorage.setItem(CONFIG.USER_KEY, JSON.stringify(user)),
    
    // Remove user
    removeUser: () => localStorage.removeItem(CONFIG.USER_KEY),
    
    // Check if user is authenticated
    isAuthenticated: () => {
        const token = API.getToken();
        const user = API.getUser();
        return token && user;
    },
    
    // Get authorization header
    getAuthHeader: () => {
        const token = API.getToken();
        return token ? { 'Authorization': `Bearer ${token}` } : {};
    },
    
    // Make authenticated API request
    request: async (endpoint, options = {}) => {
        const url = API.getUrl(endpoint);
        const headers = {
            'Content-Type': 'application/json',
            ...API.getAuthHeader(),
            ...options.headers
        };
        
        try {
            const response = await fetch(url, {
                ...options,
                headers
            });
            
            if (response.status === 401) {
                // Token expired or invalid
                API.removeToken();
                API.removeUser();
                window.location.href = '/admin-auth.html';
                return null;
            }
            
            return response;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    },
    
    // Login function
    login: async (username, password) => {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await fetch(API.getUrl(CONFIG.ENDPOINTS.LOGIN), {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            API.setToken(data.access_token);
            return data;
        } else {
            throw new Error('Login failed');
        }
    },
    
    // Logout function
    logout: () => {
        API.removeToken();
        API.removeUser();
        window.location.href = '/admin-auth.html';
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CONFIG, API };
} else {
    // Browser environment
    window.DigitalTwinConfig = CONFIG;
    window.DigitalTwinAPI = API;
} 