// NsureCat Chat Application - Vanilla JavaScript
// Main chat interface with voice, wallet, and API integration

// Load configuration from config.js (included in HTML)
// Falls back to defaults if config.js not loaded
const API_BASE_URL = (typeof NsureCatConfig !== 'undefined')
    ? NsureCatConfig.API_BASE_URL
    : 'http://localhost:8000';
const FRONTEND_PORT = (typeof NsureCatConfig !== 'undefined')
    ? NsureCatConfig.FRONTEND_PORT
    : 8001;

// ============= Bilingual Support (EN/ES) =============
const translations = {
    en: {
        greeting: "Hi! I'm Cat. Let's find you better insurance. How would you like to share your policy details? Form, voice, or upload?",
        voiceReady: "Great! Click the microphone button and tell me about your policy.",
        processing: "Processing...",
        savings: "Great news! I found you savings of",
        carrier: "with carrier",
        formSubmit: "Submit",
        formCancel: "Cancel",
        connectWallet: "Connect Your Wallet",
        metaMask: "Connect with MetaMask",
        circle: "Connect with Circle Wallet",
        sendButton: "Send",
        placeholder: "Type your message...",
        formButton: "Form",
        voiceButton: "Voice"
    },
    es: {
        greeting: "¡Hola! Soy el Gato. Vamos a encontrarte un mejor seguro. ¿Cómo te gustaría compartir los detalles de tu póliza? ¿Formulario, voz o subir archivo?",
        voiceReady: "¡Genial! Haz clic en el botón del micrófono y cuéntame sobre tu póliza.",
        processing: "Procesando...",
        savings: "¡Buenas noticias! Te encontré ahorros de",
        carrier: "con la aseguradora",
        formSubmit: "Enviar",
        formCancel: "Cancelar",
        connectWallet: "Conecta Tu Billetera",
        metaMask: "Conectar con MetaMask",
        circle: "Conectar con Billetera Circle",
        sendButton: "Enviar",
        placeholder: "Escribe tu mensaje...",
        formButton: "Formulario",
        voiceButton: "Voz"
    }
};

let currentLanguage = 'en';

// Helper function to get translated text
function t(key) {
    return translations[currentLanguage][key] || translations.en[key] || key;
}

// Global State
const appState = {
    chatHistory: [],
    userData: {
        state: '',
        carrier: '',
        amount: 0,
        bodily_injury: '',
        property_damage: '',
        uninsured_motorist: '',
        collision: '',
        comprehensive: '',
        personal_injury_protection: ''
    },
    selectedResult: null,
    walletAddress: '',
    theme: 'light',
    language: 'en',
    isVoiceEnabled: false,
    recognition: null,
    isProcessing: false
};

// DOM Elements
let chatMessages, userInput, sendBtn, voiceBtn, themeToggleBtn, languageToggleBtn, loadingSpinner;
let policyFormModal, walletModal, errorToast;

// Initialize app on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    // Get DOM elements
    chatMessages = document.getElementById('chat-messages');
    userInput = document.getElementById('user-input');
    sendBtn = document.getElementById('send-btn');
    voiceBtn = document.getElementById('voice-btn');
    themeToggleBtn = document.getElementById('theme-toggle');
    languageToggleBtn = document.getElementById('language-toggle');
    loadingSpinner = document.getElementById('loading-spinner');
    policyFormModal = document.getElementById('policy-form-modal');
    walletModal = document.getElementById('wallet-modal');
    errorToast = document.getElementById('error-toast');

    // Load saved state from localStorage
    loadStateFromLocalStorage();

    // Initialize theme
    applyTheme(appState.theme);

    // Initialize language
    currentLanguage = appState.language || 'en';
    updateLanguageUI();

    // Set up event listeners
    setupEventListeners();

    // Check for Web Speech API support
    checkVoiceSupport();

    // Start chat with greeting
    if (appState.chatHistory.length === 0) {
        addCatMessage(t('greeting'), true);
        addQuickReplyButtons([t('formButton'), t('voiceButton')]);
    } else {
        // Restore chat history
        restoreChatHistory();
    }
}

function setupEventListeners() {
    // Send message
    sendBtn.addEventListener('click', handleSendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSendMessage();
    });

    // Voice button
    voiceBtn.addEventListener('click', toggleVoiceInput);

    // Theme toggle
    themeToggleBtn.addEventListener('click', toggleTheme);

    // Language toggle
    if (languageToggleBtn) {
        languageToggleBtn.addEventListener('click', toggleLanguage);
    }

    // Policy form
    document.getElementById('close-form-modal').addEventListener('click', closePolicyFormModal);
    document.getElementById('cancel-form').addEventListener('click', closePolicyFormModal);
    document.getElementById('policy-form').addEventListener('submit', handlePolicyFormSubmit);

    // Wallet modal
    document.getElementById('close-wallet-modal').addEventListener('click', closeWalletModal);
    document.getElementById('connect-metamask').addEventListener('click', () => connectWallet('metamask'));
    document.getElementById('connect-circle').addEventListener('click', () => connectWallet('circle'));

    // Error toast
    document.getElementById('close-toast').addEventListener('click', closeErrorToast);
}

// ============= Chat Message Functions =============

function addCatMessage(text, withTTS = false) {
    const messageDiv = createMessageBubble('cat', text);
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
    
    const message = { role: 'cat', text, timestamp: Date.now() };
    appState.chatHistory.push(message);
    saveStateToLocalStorage();

    // Text-to-speech if enabled
    if (withTTS && appState.isVoiceEnabled) {
        speakText(text);
    }
}

function addUserMessage(text) {
    const messageDiv = createMessageBubble('user', text);
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
    
    const message = { role: 'user', text, timestamp: Date.now() };
    appState.chatHistory.push(message);
    saveStateToLocalStorage();
}

function createMessageBubble(role, text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-bubble ${role}-bubble`;
    messageDiv.setAttribute('data-testid', `${role}-message`);
    
    const textDiv = document.createElement('div');
    textDiv.className = 'bubble-text';
    textDiv.textContent = text;
    
    messageDiv.appendChild(textDiv);
    
    // Add TTS button for cat messages if voice enabled
    if (role === 'cat' && appState.isVoiceEnabled) {
        const ttsBtn = document.createElement('button');
        ttsBtn.className = 'tts-btn';
        ttsBtn.innerHTML = '🔊';
        ttsBtn.setAttribute('aria-label', 'Play audio');
        ttsBtn.onclick = () => speakText(text);
        messageDiv.appendChild(ttsBtn);
    }
    
    return messageDiv;
}

function addQuickReplyButtons(options) {
    const quickReplyDiv = document.createElement('div');
    quickReplyDiv.className = 'quick-replies';
    quickReplyDiv.setAttribute('data-testid', 'quick-replies');
    
    options.forEach(option => {
        const btn = document.createElement('button');
        btn.className = 'quick-reply-btn';
        btn.textContent = option;
        btn.onclick = () => handleQuickReply(option);
        quickReplyDiv.appendChild(btn);
    });
    
    chatMessages.appendChild(quickReplyDiv);
    scrollToBottom();
}

function handleQuickReply(option) {
    // Remove quick reply buttons
    const quickReplies = document.querySelectorAll('.quick-replies');
    quickReplies.forEach(qr => qr.remove());

    addUserMessage(option);

    // Handle both English and Spanish options
    const isFormOption = option === 'Form' || option === 'Formulario' || option === t('formButton');
    const isVoiceOption = option === 'Voice' || option === 'Voz' || option === t('voiceButton');

    if (isFormOption) {
        openPolicyFormModal();
    } else if (isVoiceOption) {
        addCatMessage(t('voiceReady'), true);
    }
}

function handleSendMessage() {
    const text = userInput.value.trim();
    if (!text || appState.isProcessing) return;
    
    addUserMessage(text);
    userInput.value = '';
    
    // Simple response logic (can be expanded)
    processUserInput(text);
}

function processUserInput(text) {
    const lowerText = text.toLowerCase();
    
    if (lowerText.includes('form')) {
        openPolicyFormModal();
    } else if (lowerText.includes('voice')) {
        addCatMessage("Great! Click the microphone button and tell me about your policy.", true);
    } else {
        addCatMessage("I'm not sure I understand. Would you like to use the form or voice input?", true);
        addQuickReplyButtons(['Form', 'Voice']);
    }
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function restoreChatHistory() {
    appState.chatHistory.forEach(msg => {
        const messageDiv = createMessageBubble(msg.role, msg.text);
        chatMessages.appendChild(messageDiv);
    });
    scrollToBottom();
}

// ============= Policy Form Functions =============

function openPolicyFormModal() {
    policyFormModal.style.display = 'flex';
    addCatMessage("Please fill out the form with your current policy details.", true);
}

function closePolicyFormModal() {
    policyFormModal.style.display = 'none';
}

async function handlePolicyFormSubmit(e) {
    e.preventDefault();
    
    if (appState.isProcessing) return;
    
    const formData = new FormData(e.target);
    
    // Update user data
    appState.userData.state = formData.get('state');
    appState.userData.carrier = formData.get('carrier');
    appState.userData.amount = parseFloat(formData.get('amount'));
    appState.userData.bodily_injury = formData.get('bodily_injury');
    appState.userData.property_damage = formData.get('property_damage');
    appState.userData.uninsured_motorist = formData.get('uninsured_motorist');
    appState.userData.collision = formData.get('collision');
    appState.userData.comprehensive = formData.get('comprehensive');
    appState.userData.personal_injury_protection = formData.get('personal_injury_protection');
    
    closePolicyFormModal();
    
    // Show summary
    const summary = `I see you have ${appState.userData.carrier} policy in ${appState.userData.state} paying $${appState.userData.amount} per six months. It's not bad, but let's see if we can do better.`;
    addCatMessage(summary, true);
    
    // Process with agents
    await processPolicyWithAgents();
}

async function processPolicyWithAgents() {
    appState.isProcessing = true;
    showLoading("Reaching out to carriers...");
    
    // Show animation message
    addCatMessage("Let me check with Progressive, Allstate, Liberty Mutual, State Farm, and others...", true);
    
    try {
        // Call Shop API
        const response = await fetch(`${API_BASE_URL}/v1/shop`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                bodily_injury: appState.userData.bodily_injury,
                property_damage: appState.userData.property_damage,
                uninsured_motorist: appState.userData.uninsured_motorist,
                collision: appState.userData.collision,
                comprehensive: appState.userData.comprehensive,
                personal_injury_protection: appState.userData.personal_injury_protection
            })
        });
        
        hideLoading();
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Store result
        appState.selectedResult = data;
        
        // Show result
        displaySavingsResult(data);
        
    } catch (error) {
        hideLoading();
        console.error('Shop API error:', error);
        showError('Server error. Please try again later.');
        addCatMessage("Oops, I had trouble reaching the carriers. Please try again.", true);
    } finally {
        appState.isProcessing = false;
    }
}

function displaySavingsResult(data) {
    const savings = data.savings_6mo;
    const carrier = data.new_carrier;
    
    const resultMessage = `Great news! I found a better option with ${carrier}. You could save $${savings.toFixed(2)} every 6 months!`;
    addCatMessage(resultMessage, true);
    
    // Add result card
    const resultCard = createResultCard(carrier, savings);
    chatMessages.appendChild(resultCard);
    scrollToBottom();
    
    // Nudge to choose
    setTimeout(() => {
        addCatMessage("Which one looks good? Click to choose.", true);
    }, 1000);
}

function createResultCard(carrier, savings) {
    const cardDiv = document.createElement('div');
    cardDiv.className = 'result-card';
    cardDiv.setAttribute('data-testid', 'result-card');
    
    cardDiv.innerHTML = `
        <div class="result-header">
            <h3>${carrier}</h3>
        </div>
        <div class="result-body">
            <p class="savings-amount">Save $${savings.toFixed(2)}/6mo</p>
            <button class="choose-btn" data-testid="choose-result-btn">Choose This</button>
        </div>
    `;
    
    cardDiv.querySelector('.choose-btn').addEventListener('click', () => handleResultChoice(carrier, savings));
    
    return cardDiv;
}

function handleResultChoice(carrier, savings) {
    addUserMessage(`I'll choose ${carrier}`);
    addCatMessage("Great! Now connect your wallet to switch and save.", true);
    openWalletModal();
}

// ============= Wallet Functions =============

function openWalletModal() {
    walletModal.style.display = 'flex';
}

function closeWalletModal() {
    walletModal.style.display = 'none';
}

async function connectWallet(type) {
    const statusDiv = document.getElementById('wallet-status');
    
    if (type === 'metamask') {
        // Check for MetaMask
        if (typeof window.ethereum === 'undefined') {
            statusDiv.textContent = 'MetaMask not detected. Please install MetaMask.';
            statusDiv.className = 'wallet-status error';
            return;
        }
        
        try {
            statusDiv.textContent = 'Connecting to MetaMask...';
            statusDiv.className = 'wallet-status';
            
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            appState.walletAddress = accounts[0];
            
            statusDiv.textContent = `Connected: ${appState.walletAddress.substring(0, 10)}...`;
            statusDiv.className = 'wallet-status success';
            
            // Process payment
            await processPayment();
            
        } catch (error) {
            console.error('MetaMask error:', error);
            statusDiv.textContent = 'Failed to connect MetaMask.';
            statusDiv.className = 'wallet-status error';
        }
    } else if (type === 'circle') {
        statusDiv.textContent = 'Circle integration coming soon.';
        statusDiv.className = 'wallet-status';
    }
}

async function processPayment() {
    try {
        showLoading("Processing payment...");
        
        const savings = appState.selectedResult.savings_6mo;
        const feeDollars = savings * 0.10; // 10% fee in dollars
        const feeUSDC = feeDollars * 1000000; // Convert to USDC smallest units (6 decimals)
        const netSavings = savings - feeDollars;
        
        // Call Save API with fee amount
        const response = await fetch(`${API_BASE_URL}/v1/save`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                wallet_address: appState.walletAddress,
                fee_amount: Math.round(feeUSDC) // Round to nearest whole number
            })
        });
        
        hideLoading();
        
        if (!response.ok) {
            throw new Error(`Save API error: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.status === 'pending' && data.tx_data) {
            // Handle transaction signing
            await handleTransactionSigning(data.tx_data, netSavings);
        } else if (data.status === 'success') {
            // Fallback for direct backend signing
            closeWalletModal();
            addCatMessage(`Perfect! Payment processed. You have saved $${netSavings.toFixed(2)} (90% of savings). Welcome to ${appState.selectedResult.new_carrier}!`, true);
        }
        
    } catch (error) {
        hideLoading();
        console.error('Payment error:', error);
        showError('Payment failed. Please try again.');
        addCatMessage("Oops, payment failed. Please try again.", true);
    }
}

async function handleTransactionSigning(txData, netSavings) {
    try {
        // First, approve USDC spending
        const feeAmount = Math.round(netSavings * 1000000 * 0.1); // 10% fee in USDC units
        await approveUSDCSpending(txData.from, txData.to, feeAmount);
        
        showLoading("Please sign the payment transaction in MetaMask...");
        
        // Then send the payFee transaction
        const txHash = await window.ethereum.request({
            method: 'eth_sendTransaction',
            params: [txData],
        });
        
        showLoading("Waiting for transaction confirmation...");
        
        // Wait for transaction confirmation
        await waitForTransaction(txHash);
        
        hideLoading();
        closeWalletModal();
        
        addCatMessage(`Perfect! Payment processed. Transaction: ${txHash.substring(0, 10)}... You have saved $${netSavings.toFixed(2)} (90% of savings). Welcome to ${appState.selectedResult.new_carrier}!`, true);
        
    } catch (error) {
        hideLoading();
        console.error('Transaction signing error:', error);
        if (error.code === 4001) {
            // User rejected transaction
            showError('Transaction cancelled by user.');
            addCatMessage("Transaction cancelled. You can try again anytime.", true);
        } else {
            showError('Transaction failed. Please try again.');
            addCatMessage("Oops, transaction failed. Please try again.", true);
        }
    }
}

async function approveUSDCSpending(userAddress, contractAddress, amount) {
    // USDC contract address on Arc Testnet (placeholder - needs to be updated)
    const USDC_ADDRESS = '0x...'; // TODO: Get real USDC address
    
    showLoading("Please approve USDC spending in MetaMask...");
    
    // Encode approve function call: approve(address,uint256)
    const spender = contractAddress.replace('0x', '').padStart(64, '0');
    const approveAmount = amount.toString(16).padStart(64, '0');
    const data = `0x095ea7b3${spender}${approveAmount}`;
    
    const approveTx = {
        to: USDC_ADDRESS,
        from: userAddress,
        data: data,
        gas: '100000'
    };
    
    const approveTxHash = await window.ethereum.request({
        method: 'eth_sendTransaction',
        params: [approveTx],
    });
    
    showLoading("Waiting for approval confirmation...");
    await waitForTransaction(approveTxHash);
}

async function waitForTransaction(txHash) {
    return new Promise((resolve, reject) => {
        const checkReceipt = async () => {
            try {
                const receipt = await window.ethereum.request({
                    method: 'eth_getTransactionReceipt',
                    params: [txHash],
                });
                
                if (receipt) {
                    if (receipt.status === '0x1') {
                        resolve(receipt);
                    } else {
                        reject(new Error('Transaction failed'));
                    }
                } else {
                    // Keep checking
                    setTimeout(checkReceipt, 2000);
                }
            } catch (error) {
                reject(error);
            }
        };
        
        checkReceipt();
    });
}

// ============= Voice Functions =============

function checkVoiceSupport() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        appState.recognition = new SpeechRecognition();
        appState.recognition.continuous = false;
        appState.recognition.interimResults = false;
        appState.recognition.lang = 'en-US';
        
        appState.recognition.onresult = handleVoiceResult;
        appState.recognition.onerror = handleVoiceError;
        appState.recognition.onend = () => {
            voiceBtn.textContent = '🎤';
        };
        
        appState.isVoiceEnabled = true;
    } else {
        voiceBtn.disabled = true;
        voiceBtn.title = 'Voice not supported in this browser';
    }
}

function toggleVoiceInput() {
    if (!appState.recognition) return;
    
    if (voiceBtn.textContent === '🎤') {
        appState.recognition.start();
        voiceBtn.textContent = '⏹️';
        addCatMessage("I'm listening...", false);
    } else {
        appState.recognition.stop();
        voiceBtn.textContent = '🎤';
    }
}

function handleVoiceResult(event) {
    const transcript = event.results[0][0].transcript;
    addUserMessage(transcript);
    processUserInput(transcript);
}

function handleVoiceError(event) {
    console.error('Voice recognition error:', event.error);
    showError('Voice recognition failed. Please try typing instead.');
    voiceBtn.textContent = '🎤';
}

async function speakText(text) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/text-to-speech`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                voice_id: '21m00Tcm4TlvDq8ikWAM'
            })
        });
        
        if (!response.ok) {
            throw new Error('TTS API error');
        }
        
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
        
    } catch (error) {
        console.error('TTS error:', error);
        // Fallback to text-only
    }
}

// ============= Theme Functions =============

function toggleTheme() {
    appState.theme = appState.theme === 'light' ? 'dark' : 'light';
    applyTheme(appState.theme);
    saveStateToLocalStorage();
}

function applyTheme(theme) {
    const themeIcon = document.getElementById('theme-icon');
    if (theme === 'dark') {
        document.documentElement.classList.add('dark');
        themeIcon.textContent = '☀️';
    } else {
        document.documentElement.classList.remove('dark');
        themeIcon.textContent = '🌙';
    }
}

// ============= Language Functions =============

function toggleLanguage() {
    currentLanguage = currentLanguage === 'en' ? 'es' : 'en';
    appState.language = currentLanguage;
    updateLanguageUI();
    saveStateToLocalStorage();
}

function updateLanguageUI() {
    // Update language toggle button
    if (languageToggleBtn) {
        const enSpan = languageToggleBtn.querySelector('[data-lang="en"]');
        const esSpan = languageToggleBtn.querySelector('[data-lang="es"]');

        if (enSpan && esSpan) {
            if (currentLanguage === 'en') {
                enSpan.classList.add('active');
                esSpan.classList.remove('active');
            } else {
                esSpan.classList.add('active');
                enSpan.classList.remove('active');
            }
        }
    }

    // Update UI text elements
    userInput.placeholder = t('placeholder');
    const sendBtnText = sendBtn.querySelector('.btn-gradient-text');
    if (sendBtnText) {
        sendBtnText.textContent = t('sendButton');
    }

    // Update loading text
    const loadingText = loadingSpinner.querySelector('.loading-text');
    if (loadingText) {
        loadingText.textContent = t('processing');
    }

    // Update form buttons (if modal is open)
    const submitBtn = document.querySelector('[data-testid="submit-policy-form"]');
    const cancelBtn = document.getElementById('cancel-form');
    if (submitBtn) submitBtn.textContent = t('formSubmit');
    if (cancelBtn) cancelBtn.textContent = t('formCancel');

    // Update header tagline
    const tagline = document.querySelector('.header-tagline');
    if (tagline) {
        if (currentLanguage === 'es') {
            tagline.textContent = '¡Rebélate contra el seguro tradicional!';
        } else {
            tagline.textContent = 'Rebel against traditional insurance!';
        }
    }
}

// ============= UI Helper Functions =============

function showLoading(text = null) {
    const loadingText = text || t('processing');
    loadingSpinner.querySelector('.loading-text').textContent = loadingText;
    loadingSpinner.style.display = 'flex';
}

function hideLoading() {
    loadingSpinner.style.display = 'none';
}

function showError(message) {
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = message;
    errorToast.style.display = 'flex';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        closeErrorToast();
    }, 5000);
}

function closeErrorToast() {
    errorToast.style.display = 'none';
}

// ============= LocalStorage Functions =============

function saveStateToLocalStorage() {
    try {
        localStorage.setItem('nsurecat_chat_history', JSON.stringify(appState.chatHistory));
        localStorage.setItem('nsurecat_user_data', JSON.stringify(appState.userData));
        localStorage.setItem('nsurecat_theme', appState.theme);
    } catch (error) {
        console.error('LocalStorage save error:', error);
    }
}

function loadStateFromLocalStorage() {
    try {
        const savedHistory = localStorage.getItem('nsurecat_chat_history');
        const savedUserData = localStorage.getItem('nsurecat_user_data');
        const savedTheme = localStorage.getItem('nsurecat_theme');
        
        if (savedHistory) {
            appState.chatHistory = JSON.parse(savedHistory);
        }
        if (savedUserData) {
            appState.userData = JSON.parse(savedUserData);
        }
        if (savedTheme) {
            appState.theme = savedTheme;
        }
    } catch (error) {
        console.error('LocalStorage load error:', error);
    }
}
