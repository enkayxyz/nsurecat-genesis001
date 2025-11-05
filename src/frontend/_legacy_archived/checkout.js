// checkout.js - Handle checkout page

let walletAddress = null;

document.getElementById('createWallet').addEventListener('click', async () => {
    // Placeholder for Circle Wallets SDK
    // const wallet = await Circle.createWallet({/* options */});
    // walletAddress = wallet.address;
    alert('Wallet creation not implemented yet');
    document.getElementById('walletStep').style.display = 'none';
    document.getElementById('fundStep').style.display = 'block';
});

document.getElementById('connectWallet').addEventListener('click', async () => {
    // Placeholder for MetaMask or ethers.js
    if (window.ethereum) {
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
        walletAddress = accounts[0];
        document.getElementById('walletStep').style.display = 'none';
        document.getElementById('fundStep').style.display = 'block';
    } else {
        alert('MetaMask not detected');
    }
});

document.getElementById('confirmPay').addEventListener('click', async () => {
    if (!walletAddress) {
        alert('No wallet connected');
        return;
    }
    try {
        const response = await fetch('http://localhost:8000/v1/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ wallet_address: walletAddress })
        });
        const result = await response.json();
        if (result.status === 'success') {
            window.location.href = 'success.html';
        } else {
            alert('Payment failed');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});