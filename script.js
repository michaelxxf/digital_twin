// User Interface JavaScript for Digital Twin System
// Handles all desktop operations, window management, and activity tracking

// Global state management
const appState = {
    currentTheme: 'light',
    openWindows: new Set(),
    activeWindow: null,
    startMenuOpen: false,
    profileMenuOpen: false,
    currentEmailFolder: 'inbox',
    currentExplorerTab: 'work-server',
    currentSettingsTab: 'appearance',
    currentDocumentsFolder: 'recent',
    userActivity: [],
    systemPolicies: {
        allowFileUpload: true,
        allowFileDownload: true,
        allowFileDelete: true,
        allowExecutableFiles: false,
        allowInternetAccess: true,
        restrictToTrustedSites: true,
        allowThemeChange: true,
        allowWallpaperChange: true,
        enableActivityTracking: true,
        enableLocationServices: false,
        enforceMFA: true,
        limitConcurrentSessions: true,
        autoLockAfterFailedLogins: true,
        sessionTimeout: 30,
        passwordExpiry: 90,
        allowExternalEmail: true,
        allowEmailAttachments: true,
        allowNewFolderCreation: true,
        allowDocumentSharing: true,
        allowDocumentPrinting: false,
        adminApprovalForNewStaff: true,
        disableInactiveAccounts: true,
        inactiveAfterDays: 30,
        notifyAdminOfSuspiciousActivity: true,
        lockAfterFailedAttempts: 3,
        enforceFileEncryption: true,
        regularBackups: true,
        backupFrequency: 7,
        enableDetailedActivityLogging: true,
        retainLogs: 90
    }
};

// Activity tracking for admin monitoring
function logActivity(action, details = {}) {
    const activity = {
        timestamp: new Date().toISOString(),
        action: action,
        details: details,
        user: 'Alex Carter',
        sessionId: generateSessionId()
    };
    
    appState.userActivity.push(activity);
    
    // Send to admin dashboard (simulated)
    if (typeof sendToAdminDashboard === 'function') {
        sendToAdminDashboard(activity);
    }
    
    // Keep only last 100 activities
    if (appState.userActivity.length > 100) {
        appState.userActivity.shift();
    }
}

function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// Theme management
function toggleTheme() {
    const body = document.getElementById('body');
    const themeIcon = document.getElementById('theme-icon');
    const desktopBg = document.getElementById('desktop-bg');
    
    if (appState.currentTheme === 'light') {
        body.classList.add('dark');
        body.classList.remove('bg-win-bg-light');
        body.classList.add('bg-win-bg-dark');
        desktopBg.classList.remove('desktop-bg-light');
        desktopBg.classList.add('desktop-bg-dark');
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
        appState.currentTheme = 'dark';
    } else {
        body.classList.remove('dark');
        body.classList.remove('bg-win-bg-dark');
        body.classList.add('bg-win-bg-light');
        desktopBg.classList.remove('desktop-bg-dark');
        desktopBg.classList.add('desktop-bg-light');
        themeIcon.classList.remove('fa-sun');
        themeIcon.classList.add('fa-moon');
        appState.currentTheme = 'light';
    }
    
    logActivity('theme_changed', { newTheme: appState.currentTheme });
}

// Start menu functionality
function toggleStartMenu() {
    const startMenu = document.getElementById('start-menu');
    
    if (appState.startMenuOpen) {
        startMenu.classList.add('hidden');
        appState.startMenuOpen = false;
    } else {
        startMenu.classList.remove('hidden');
        appState.startMenuOpen = true;
    }
    
    logActivity('start_menu_toggled', { isOpen: appState.startMenuOpen });
}

// Profile menu functionality
function toggleProfileMenu() {
    const profileMenu = document.getElementById('profile-menu');
    
    if (appState.profileMenuOpen) {
        profileMenu.classList.add('hidden');
        appState.profileMenuOpen = false;
    } else {
        profileMenu.classList.remove('hidden');
        appState.profileMenuOpen = true;
    }
    
    logActivity('profile_menu_toggled', { isOpen: appState.profileMenuOpen });
}

// Window management
function openApp(appName) {
    if (!appState.systemPolicies.allowThemeChange && appName === 'settings') {
        showNotification('Settings access is restricted by system policy', 'warning');
        return;
    }
    
    const windowId = `window-${appName}`;
    
    if (appState.openWindows.has(windowId)) {
        // Bring window to front
        bringWindowToFront(windowId);
        return;
    }
    
    const template = document.getElementById(windowId);
    if (!template) {
        console.error(`Template not found for app: ${appName}`);
        return;
    }
    
    const windowsArea = document.getElementById('windows-area');
    const windowClone = template.content.cloneNode(true);
    windowsArea.appendChild(windowClone);
    
    appState.openWindows.add(windowId);
    appState.activeWindow = windowId;
    
    // Initialize app-specific functionality
    initializeApp(appName);
    
    logActivity('app_opened', { appName: appName, windowId: windowId });
}

function closeWindow(windowId) {
    const windowElement = document.getElementById(windowId);
    if (windowElement) {
        windowElement.remove();
        appState.openWindows.delete(windowId);
        
        if (appState.activeWindow === windowId) {
            appState.activeWindow = null;
        }
        
        logActivity('window_closed', { windowId: windowId });
    }
}

function bringWindowToFront(windowId) {
    const windowElement = document.getElementById(windowId);
    if (windowElement) {
        windowElement.style.zIndex = '50';
        appState.activeWindow = windowId;
        
        // Reset z-index for other windows
        appState.openWindows.forEach(id => {
            if (id !== windowId) {
                const otherWindow = document.getElementById(id);
                if (otherWindow) {
                    otherWindow.style.zIndex = '40';
                }
            }
        });
    }
}

// App-specific initialization
function initializeApp(appName) {
    switch (appName) {
        case 'email':
            initializeEmailApp();
            break;
        case 'file-explorer':
            initializeFileExplorer();
            break;
        case 'settings':
            initializeSettings();
            break;
        case 'documents':
            initializeDocuments();
            break;
        case 'browser':
            initializeBrowser();
            break;
    }
}

// Email functionality
function initializeEmailApp() {
    // Email data
    const emailData = {
        inbox: [
            {
                id: '1',
                from: 'John Doe',
                subject: 'Project Update: Q2 Results',
                preview: 'Here are the latest results for our Q2 project...',
                time: '10:30 AM',
                content: 'Dear Team,\n\nI hope this email finds you well. Here are the latest results for our Q2 project:\n\n- Revenue increased by 15%\n- Customer satisfaction improved\n- New features launched successfully\n\nBest regards,\nJohn'
            },
            {
                id: '2',
                from: 'Sarah Johnson',
                subject: 'Meeting Reminder',
                preview: 'Don\'t forget about our meeting tomorrow at 2 PM...',
                time: 'Yesterday',
                content: 'Hi Alex,\n\nJust a friendly reminder about our meeting tomorrow at 2 PM. Please prepare the quarterly report.\n\nThanks,\nSarah'
            }
        ],
        sent: [
            {
                id: '3',
                to: 'finance@company.com',
                subject: 'Budget Request',
                preview: 'Please review the attached budget proposal...',
                time: '2 days ago',
                content: 'Hello Finance Team,\n\nPlease review the attached budget proposal for the upcoming quarter.\n\nRegards,\nAlex'
            }
        ],
        drafts: []
    };
    
    window.emailData = emailData;
}

function switchEmailFolder(folder) {
    appState.currentEmailFolder = folder;
    
    // Update active tab styling
    document.querySelectorAll('[id^="email-folder-"]').forEach(btn => {
        btn.classList.remove('text-blue-600', 'bg-blue-100', 'dark:bg-blue-900/40', 'font-medium');
        btn.classList.add('text-gray-600', 'dark:text-gray-200', 'hover:bg-blue-100', 'dark:hover:bg-blue-950');
    });
    
    const activeBtn = document.getElementById(`email-folder-${folder}`);
    if (activeBtn) {
        activeBtn.classList.remove('text-gray-600', 'dark:text-gray-200', 'hover:bg-blue-100', 'dark:hover:bg-blue-950');
        activeBtn.classList.add('text-blue-600', 'bg-blue-100', 'dark:bg-blue-900/40', 'font-medium');
    }
    
    // Update email list
    updateEmailList(folder);
    
    logActivity('email_folder_changed', { folder: folder });
}

function updateEmailList(folder) {
    const emailList = document.getElementById('email-list');
    if (!emailList || !window.emailData) return;
    
    const emails = window.emailData[folder] || [];
    
    emailList.innerHTML = emails.map(email => `
        <div onclick="openEmail('${email.id}')" class="p-3 border-b border-gray-100 dark:border-gray-800 hover:bg-blue-50 dark:hover:bg-blue-950 cursor-pointer">
            <div class="flex justify-between items-start">
                <span class="font-medium text-gray-800 dark:text-gray-100">${folder === 'sent' ? email.to : email.from}</span>
                <span class="text-xs text-gray-500">${email.time}</span>
            </div>
            <div class="text-sm font-medium text-gray-700 dark:text-gray-300 truncate">${email.subject}</div>
            <div class="text-xs text-gray-500 dark:text-gray-400 truncate">${email.preview}</div>
        </div>
    `).join('');
}

function openEmail(emailId) {
    const emailContent = document.getElementById('email-content');
    if (!emailContent || !window.emailData) return;
    
    const emails = window.emailData[appState.currentEmailFolder] || [];
    const email = emails.find(e => e.id === emailId);
    
    if (email) {
        emailContent.innerHTML = `
            <div class="mb-4">
                <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100">${email.subject}</h3>
                <div class="flex items-center gap-4 mt-2 text-sm text-gray-600 dark:text-gray-400">
                    <span><strong>From:</strong> ${email.from}</span>
                    <span><strong>Time:</strong> ${email.time}</span>
                </div>
            </div>
            <div class="prose prose-sm max-w-none">
                <pre class="whitespace-pre-wrap text-gray-700 dark:text-gray-300">${email.content}</pre>
            </div>
        `;
        
        logActivity('email_opened', { emailId: emailId, folder: appState.currentEmailFolder });
    }
}

// File Explorer functionality
function initializeFileExplorer() {
    const fileData = {
        'work-server': [
            { name: 'Project_Plan.docx', type: 'word', icon: 'fa-file-word', color: 'blue' },
            { name: 'Budget_2024.xlsx', type: 'excel', icon: 'fa-file-excel', color: 'green' }
        ],
        'personal-space': [
            { name: 'Personal_Notes.txt', type: 'text', icon: 'fa-file-lines', color: 'gray' },
            { name: 'Photos.zip', type: 'archive', icon: 'fa-file-zipper', color: 'purple' }
        ]
    };
    
    window.fileData = fileData;
}

function switchExplorerTab(tab) {
    appState.currentExplorerTab = tab;
    
    // Update active tab styling
    document.querySelectorAll('[id^="fe-tab-"]').forEach(btn => {
        btn.classList.remove('text-blue-600', 'bg-blue-100', 'dark:bg-blue-900/40', 'font-semibold');
        btn.classList.add('text-gray-600', 'dark:text-gray-200', 'hover:bg-blue-100', 'dark:hover:bg-blue-950');
    });
    
    const activeBtn = document.getElementById(`fe-tab-${tab}`);
    if (activeBtn) {
        activeBtn.classList.remove('text-gray-600', 'dark:text-gray-200', 'hover:bg-blue-100', 'dark:hover:bg-blue-950');
        activeBtn.classList.add('text-blue-600', 'bg-blue-100', 'dark:bg-blue-900/40', 'font-semibold');
    }
    
    // Update file list
    updateFileList(tab);
    
    logActivity('explorer_tab_changed', { tab: tab });
}

function updateFileList(tab) {
    const filePane = document.getElementById('file-explorer-pane');
    if (!filePane || !window.fileData) return;
    
    const files = window.fileData[tab] || [];
    const tabName = tab === 'work-server' ? 'Work Server Files' : 'Personal Space Files';
    
    filePane.innerHTML = `
        <div class="text-sm font-semibold text-gray-500 dark:text-gray-300 mb-2">${tabName}</div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            ${files.map(file => `
                <div class="flex items-center gap-3 bg-gray-100 dark:bg-[#23283e] rounded-lg p-3">
                    <i class="fa-solid ${file.icon} text-${file.color}-500 text-2xl"></i>
                    <span class="flex-1 text-gray-800 dark:text-gray-100">${file.name}</span>
                    <button onclick="downloadFile('${file.name}')" class="px-2 py-1 text-xs rounded bg-blue-100 dark:bg-blue-900/30 text-blue-600 hover:bg-blue-200 dark:hover:bg-blue-950 transition-all">Download</button>
                    <button onclick="deleteFile('${file.name}')" class="px-2 py-1 ml-1 text-xs rounded bg-red-100 dark:bg-red-900/25 text-red-500 hover:bg-red-200 dark:hover:bg-red-950 transition-all">Delete</button>
                </div>
            `).join('')}
        </div>
        <div class="mt-5">
            <label class="block text-xs font-medium text-gray-500 dark:text-gray-300 mb-2">Upload a file</label>
            <input type="file" onchange="handleFileUpload(event)" class="block w-full text-sm text-gray-500 dark:text-gray-300 file:mr-3 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 dark:file:bg-blue-900/40 dark:file:text-blue-200 dark:hover:file:bg-blue-900/60" />
        </div>
    `;
}

function downloadFile(fileName) {
    if (!appState.systemPolicies.allowFileDownload) {
        showNotification('File downloads are restricted by system policy', 'warning');
        return;
    }
    
    logActivity('file_downloaded', { fileName: fileName, location: appState.currentExplorerTab });
    showNotification(`Downloading ${fileName}...`, 'success');
}

function deleteFile(fileName) {
    if (!appState.systemPolicies.allowFileDelete) {
        showNotification('File deletion is restricted by system policy', 'warning');
        return;
    }
    
    logActivity('file_deleted', { fileName: fileName, location: appState.currentExplorerTab });
    showNotification(`${fileName} deleted successfully`, 'success');
    
    // Remove from file list
    if (window.fileData && window.fileData[appState.currentExplorerTab]) {
        window.fileData[appState.currentExplorerTab] = window.fileData[appState.currentExplorerTab].filter(f => f.name !== fileName);
        updateFileList(appState.currentExplorerTab);
    }
}

function handleFileUpload(event) {
    if (!appState.systemPolicies.allowFileUpload) {
        showNotification('File uploads are restricted by system policy', 'warning');
        return;
    }
    
    const file = event.target.files[0];
    if (file) {
        // Check for executable files
        if (file.name.endsWith('.exe') && !appState.systemPolicies.allowExecutableFiles) {
            showNotification('Executable files are not allowed by system policy', 'error');
            return;
        }
        
        logActivity('file_uploaded', { fileName: file.name, fileSize: file.size, location: appState.currentExplorerTab });
        showNotification(`${file.name} uploaded successfully`, 'success');
        
        // Add to file list
        if (window.fileData && window.fileData[appState.currentExplorerTab]) {
            const fileType = getFileType(file.name);
            const newFile = {
                name: file.name,
                type: fileType.type,
                icon: fileType.icon,
                color: fileType.color
            };
            window.fileData[appState.currentExplorerTab].push(newFile);
            updateFileList(appState.currentExplorerTab);
        }
    }
}

function getFileType(fileName) {
    const ext = fileName.split('.').pop().toLowerCase();
    const types = {
        'doc': { type: 'word', icon: 'fa-file-word', color: 'blue' },
        'docx': { type: 'word', icon: 'fa-file-word', color: 'blue' },
        'xls': { type: 'excel', icon: 'fa-file-excel', color: 'green' },
        'xlsx': { type: 'excel', icon: 'fa-file-excel', color: 'green' },
        'pdf': { type: 'pdf', icon: 'fa-file-pdf', color: 'red' },
        'txt': { type: 'text', icon: 'fa-file-lines', color: 'gray' },
        'zip': { type: 'archive', icon: 'fa-file-zipper', color: 'purple' },
        'exe': { type: 'executable', icon: 'fa-file-code', color: 'yellow' }
    };
    return types[ext] || { type: 'unknown', icon: 'fa-file', color: 'gray' };
}

// Settings functionality
function initializeSettings() {
    // Load current settings
    loadSettings();
}

function switchSettingsTab(tab) {
    appState.currentSettingsTab = tab;
    
    // Hide all settings content
    document.querySelectorAll('#settings-content > div').forEach(div => {
        div.classList.add('hidden');
    });
    
    // Show selected tab content
    const selectedContent = document.getElementById(`${tab}-settings`);
    if (selectedContent) {
        selectedContent.classList.remove('hidden');
    }
    
    // Update active tab styling
    document.querySelectorAll('[id^="settings-tab-"]').forEach(btn => {
        btn.classList.remove('text-blue-600', 'bg-blue-100', 'dark:bg-blue-900/40', 'font-medium');
        btn.classList.add('text-gray-600', 'dark:text-gray-200', 'hover:bg-blue-100', 'dark:hover:bg-blue-950');
    });
    
    const activeBtn = document.getElementById(`settings-tab-${tab}`);
    if (activeBtn) {
        activeBtn.classList.remove('text-gray-600', 'dark:text-gray-200', 'hover:bg-blue-100', 'dark:hover:bg-blue-950');
        activeBtn.classList.add('text-blue-600', 'bg-blue-100', 'dark:bg-blue-900/40', 'font-medium');
    }
    
    logActivity('settings_tab_changed', { tab: tab });
}

function loadSettings() {
    // Load settings from localStorage or use defaults
    const savedSettings = localStorage.getItem('userSettings');
    if (savedSettings) {
        const settings = JSON.parse(savedSettings);
        // Apply settings to form elements
        Object.keys(settings).forEach(key => {
            const element = document.querySelector(`[data-setting="${key}"]`);
            if (element) {
                if (element.type === 'checkbox') {
                    element.checked = settings[key];
                } else {
                    element.value = settings[key];
                }
            }
        });
    }
}

function saveSettings() {
    const settings = {};
    
    // Collect all settings from form elements
    document.querySelectorAll('[data-setting]').forEach(element => {
        const key = element.getAttribute('data-setting');
        if (element.type === 'checkbox') {
            settings[key] = element.checked;
        } else {
            settings[key] = element.value;
        }
    });
    
    localStorage.setItem('userSettings', JSON.stringify(settings));
    showNotification('Settings saved successfully', 'success');
    
    logActivity('settings_saved', { settings: settings });
}

// Documents functionality
function initializeDocuments() {
    const documentData = {
        'recent': [
            { name: 'Project_Report.docx', type: 'word', modified: '2 days ago' },
            { name: 'Budget_2024.xlsx', type: 'excel', modified: '1 week ago' },
            { name: 'Contract.pdf', type: 'pdf', modified: '3 weeks ago' },
            { name: 'Presentation.pptx', type: 'powerpoint', modified: '1 month ago' }
        ],
        'work': [
            { name: 'Work_Report.docx', type: 'word', modified: '1 day ago' },
            { name: 'Meeting_Notes.txt', type: 'text', modified: '3 days ago' }
        ],
        'personal': [
            { name: 'Personal_Notes.txt', type: 'text', modified: '1 week ago' },
            { name: 'Resume.pdf', type: 'pdf', modified: '2 weeks ago' }
        ]
    };
    
    window.documentData = documentData;
}

function switchDocumentsFolder(folder) {
    appState.currentDocumentsFolder = folder;
    
    // Update active tab styling
    document.querySelectorAll('[id^="documents-folder-"]').forEach(btn => {
        btn.classList.remove('text-blue-600', 'bg-blue-100', 'dark:bg-blue-900/40', 'font-medium');
        btn.classList.add('text-gray-600', 'dark:text-gray-200', 'hover:bg-blue-100', 'dark:hover:bg-blue-950');
    });
    
    const activeBtn = document.getElementById(`documents-folder-${folder}`);
    if (activeBtn) {
        activeBtn.classList.remove('text-gray-600', 'dark:text-gray-200', 'hover:bg-blue-100', 'dark:hover:bg-blue-950');
        activeBtn.classList.add('text-blue-600', 'bg-blue-100', 'dark:bg-blue-900/40', 'font-medium');
    }
    
    // Update documents list
    updateDocumentsList(folder);
    
    logActivity('documents_folder_changed', { folder: folder });
}

function updateDocumentsList(folder) {
    const documentsContent = document.querySelector('#window-documents-card .flex-1 .flex-1');
    if (!documentsContent || !window.documentData) return;
    
    const documents = window.documentData[folder] || [];
    const folderNames = {
        'recent': 'Recent Documents',
        'work': 'Work Documents',
        'personal': 'Personal Documents'
    };
    
    documentsContent.innerHTML = `
        <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100">${folderNames[folder]}</h3>
            <button onclick="createNewFolder()" class="px-3 py-1 text-sm rounded-lg bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-200 flex items-center gap-1">
                <i class="fa-solid fa-plus"></i> New Folder
            </button>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            ${documents.map(doc => {
                const iconColors = {
                    'word': 'blue',
                    'excel': 'green',
                    'pdf': 'red',
                    'powerpoint': 'yellow',
                    'text': 'gray'
                };
                const icons = {
                    'word': 'fa-file-word',
                    'excel': 'fa-file-excel',
                    'pdf': 'fa-file-pdf',
                    'powerpoint': 'fa-file-powerpoint',
                    'text': 'fa-file-lines'
                };
                return `
                    <div onclick="openDocument('${doc.name}')" class="flex flex-col items-center p-3 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-950 cursor-pointer">
                        <div class="bg-${iconColors[doc.type]}-100 dark:bg-${iconColors[doc.type]}-900/30 rounded-xl p-4 mb-2">
                            <i class="fa-solid ${icons[doc.type]} text-${iconColors[doc.type]}-500 text-3xl"></i>
                        </div>
                        <span class="text-sm font-medium text-gray-800 dark:text-gray-200 text-center">${doc.name}</span>
                        <span class="text-xs text-gray-500">Modified: ${doc.modified}</span>
                    </div>
                `;
            }).join('')}
        </div>
    `;
}

function openDocument(docName) {
    logActivity('document_opened', { documentName: docName, folder: appState.currentDocumentsFolder });
    showNotification(`Opening ${docName}...`, 'success');
}

function createNewFolder() {
    if (!appState.systemPolicies.allowNewFolderCreation) {
        showNotification('Folder creation is restricted by system policy', 'warning');
        return;
    }
    
    const folderName = prompt('Enter folder name:');
    if (folderName) {
        logActivity('folder_created', { folderName: folderName, location: appState.currentDocumentsFolder });
        showNotification(`Folder "${folderName}" created successfully`, 'success');
    }
}

// Browser functionality
function initializeBrowser() {
    // Browser is limited to trusted sites only
    logActivity('browser_opened', { note: 'Secure browsing limited to trusted work sites' });
}

// System time display
function updateSystemTime() {
    const timeElement = document.getElementById('system-time');
    if (timeElement) {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true 
        });
        timeElement.textContent = timeString;
    }
}

// Search functionality
function initializeSearch() {
    const searchBar = document.getElementById('search-bar');
    if (searchBar) {
        searchBar.addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            if (query.length > 2) {
                performSearch(query);
            }
        });
    }
}

function performSearch(query) {
    logActivity('search_performed', { query: query });
    // Search functionality would be implemented here
}

// Notification system
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 px-4 py-2 rounded-lg shadow-lg transition-all transform translate-x-full`;
    
    const colors = {
        success: 'bg-green-500 text-white',
        error: 'bg-red-500 text-white',
        warning: 'bg-yellow-500 text-white',
        info: 'bg-blue-500 text-white'
    };
    
    notification.classList.add(colors[type] || colors.info);
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Logout functionality
function logout() {
    logActivity('user_logout', { timestamp: new Date().toISOString() });
    
    // Clear any sensitive data
    localStorage.removeItem('userSettings');
    
    // Redirect to login page
    window.location.href = 'staff-auth.html';
}

// Click outside handlers
document.addEventListener('click', function(event) {
    // Close start menu if clicking outside
    if (appState.startMenuOpen && !event.target.closest('#start-menu') && !event.target.closest('#start-btn')) {
        toggleStartMenu();
    }
    
    // Close profile menu if clicking outside
    if (appState.profileMenuOpen && !event.target.closest('#profile-menu') && !event.target.closest('[onclick="toggleProfileMenu()"]')) {
        toggleProfileMenu();
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl+Alt+T to toggle theme
    if (event.ctrlKey && event.altKey && event.key === 't') {
        event.preventDefault();
        toggleTheme();
    }
    
    // Escape to close menus
    if (event.key === 'Escape') {
        if (appState.startMenuOpen) {
            toggleStartMenu();
        }
        if (appState.profileMenuOpen) {
            toggleProfileMenu();
        }
    }
});

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize system time
    updateSystemTime();
    setInterval(updateSystemTime, 1000);
    
    // Initialize search
    initializeSearch();
    
    // Log initial activity
    logActivity('session_started', { 
        userAgent: navigator.userAgent,
        screenResolution: `${screen.width}x${screen.height}`,
        theme: appState.currentTheme
    });
    
    // Check for system policies on load
    checkSystemPolicies();
});

// System policy enforcement
function checkSystemPolicies() {
    // Check if theme change is allowed
    if (!appState.systemPolicies.allowThemeChange) {
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.style.display = 'none';
        }
    }
    
    // Check if wallpaper change is allowed
    if (!appState.systemPolicies.allowWallpaperChange) {
        // Hide wallpaper options in settings
    }
    
    // Check if internet access is restricted
    if (!appState.systemPolicies.allowInternetAccess) {
        // Disable browser functionality
    }
    
    logActivity('system_policies_checked', { policies: appState.systemPolicies });
}

// Export functions for admin monitoring
window.getUserActivity = function() {
    return appState.userActivity;
};

window.getSystemPolicies = function() {
    return appState.systemPolicies;
};

window.getCurrentState = function() {
    return {
        currentTheme: appState.currentTheme,
        openWindows: Array.from(appState.openWindows),
        activeWindow: appState.activeWindow,
        currentEmailFolder: appState.currentEmailFolder,
        currentExplorerTab: appState.currentExplorerTab,
        currentSettingsTab: appState.currentSettingsTab,
        currentDocumentsFolder: appState.currentDocumentsFolder
    };
}; 