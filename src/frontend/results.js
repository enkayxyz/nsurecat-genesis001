// results.js - Handle results page

document.addEventListener('DOMContentLoaded', () => {
    const savings = JSON.parse(localStorage.getItem('savings'));
    if (savings) {
        document.getElementById('savingsDisplay').innerHTML = `
            <p>You Save: $${savings.savings_6mo} for 6 months!</p>
            <p>New Carrier: ${savings.new_carrier}</p>
        `;
    }
});

document.getElementById('saveNowButton').addEventListener('click', () => {
    window.location.href = 'checkout.html';
});