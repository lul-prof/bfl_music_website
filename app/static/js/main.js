// Payment Processing
function processPayPalPayment(amount) {
    // PayPal payment logic
    paypal.Buttons({
        createOrder: function(data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: amount
                    }
                }]
            });
        },
        onApprove: function(data, actions) {
            return actions.order.capture().then(function(details) {
                alert('Transaction completed by ' + details.payer.name.given_name);
                // Call your server to save the transaction
                saveTransaction(details.id, amount, 'paypal');
            });
        }
    }).render('#paypal-button-container');
}

// M-Pesa Payment
function processMPesaPayment() {
    const phone = document.getElementById('mpesa-phone').value;
    const amount = document.getElementById('mpesa-amount').value;
    
    fetch('/process-mpesa', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            phone: phone,
            amount: amount
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            alert('Please check your phone for the M-Pesa prompt');
        } else {
            alert('Error processing payment');
        }
    });
}

// Audio Player
function initAudioPlayer() {
    const audioPlayers = document.querySelectorAll('.audio-player');
    audioPlayers.forEach(player => {
        player.addEventListener('play', function() {
            audioPlayers.forEach(p => {
                if(p !== player) p.pause();
            });
        });
    });
}

// Admin Dashboard Charts
function initAdminCharts() {
    if(document.getElementById('statsChart')) {
        const ctx = document.getElementById('statsChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Monthly Donations',
                    data: [12, 19, 3, 5, 2, 3],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            }
        });
    }
}

// Initialize components
document.addEventListener('DOMContentLoaded', function() {
    initAudioPlayer();
    initAdminCharts();
});