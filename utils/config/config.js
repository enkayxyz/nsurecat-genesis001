// NsureCat Configuration - JavaScript
// Import this in frontend JavaScript files for consistent configuration

const NsureCatConfig = {
    // Ports
    BACKEND_PORT: 8000,
    FRONTEND_PORT: 8001,
    
    // URLs
    get BACKEND_URL() {
        return `http://localhost:${this.BACKEND_PORT}`;
    },
    
    get FRONTEND_URL() {
        return `http://localhost:${this.FRONTEND_PORT}`;
    },
    
    get API_BASE_URL() {
        return this.BACKEND_URL;
    },
    
    // Environment
    ENV_NAME: 'nsurecat',
    
    // Testing
    TEST_TIMEOUT: 30000,
    
    // Display configuration
    show() {
        console.log('=== NsureCat Configuration ===');
        console.log(`Backend: ${this.BACKEND_URL}`);
        console.log(`Frontend: ${this.FRONTEND_URL}`);
        console.log(`Environment: ${this.ENV_NAME}`);
        console.log('=============================');
    }
};

// For Node.js environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NsureCatConfig;
}

// For browser environments
if (typeof window !== 'undefined') {
    window.NsureCatConfig = NsureCatConfig;
}
