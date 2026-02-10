// Finance App - Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize wallet type toggle
    initializeWalletTypeToggle();
    
    // Initialize transfer form
    initializeTransferForm();
    
    // Auto-hide alerts
    autoHideAlerts();
    
    // Format currency inputs
    formatCurrencyInputs();
});

// Initialize Bootstrap Tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Toggle wallet type fields
function initializeWalletTypeToggle() {
    const walletTypeSelect = document.getElementById('id_wallet_type');
    const cardTypeField = document.querySelector('[data-field="card_type"]');
    const titleField = document.querySelector('[data-field="title"]');

    if (walletTypeSelect) {
        walletTypeSelect.addEventListener('change', function() {
            const type = this.value;
            
            if (type === 'naqd') {
                if (cardTypeField) cardTypeField.style.display = 'none';
                if (titleField) titleField.style.display = 'none';
            } else if (type === 'karta') {
                if (cardTypeField) cardTypeField.style.display = 'block';
                if (titleField) titleField.style.display = 'block';
            }
        });
        
        // Trigger change on load
        walletTypeSelect.dispatchEvent(new Event('change'));
    }
}

// Transfer form - update available to_wallets
function initializeTransferForm() {
    const fromWalletSelect = document.getElementById('id_from_wallet');
    const toWalletSelect = document.getElementById('id_to_wallet');

    if (fromWalletSelect && toWalletSelect) {
        fromWalletSelect.addEventListener('change', function() {
            const selectedId = this.value;
            const options = toWalletSelect.querySelectorAll('option');
            
            options.forEach(option => {
                if (option.value === selectedId) {
                    option.style.display = 'none';
                } else if (option.value === '') {
                    option.style.display = 'block';
                } else {
                    option.style.display = 'block';
                }
            });
        });
        
        // Trigger change on load
        fromWalletSelect.dispatchEvent(new Event('change'));
    }
}

// Auto-hide Bootstrap alerts after 5 seconds
function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

// Format currency input values
function formatCurrencyInputs() {
    const currencyInputs = document.querySelectorAll('[data-currency]');
    
    currencyInputs.forEach(input => {
        input.addEventListener('blur', function() {
            let value = parseFloat(this.value);
            if (!isNaN(value)) {
                this.value = value.toFixed(2);
            }
        });
    });
}

// Utility function to format currency
function formatCurrency(amount, currency = 'UZS') {
    const formatter = new Intl.NumberFormat('uz-UZ', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
    
    return formatter.format(amount);
}

// Utility function to show toast notification
function showToast(message, type = 'info') {
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'info'} border-0" 
             role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    const toastElement = toastContainer.lastElementChild;
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove the element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

// Create toast container if it doesn't exist
function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
}

// Confirm action before delete
function confirmDelete(message = 'Ishonchingiz komil? Bu amalni bekor qilib bo\'lmaydi.') {
    return confirm(message);
}

// For transfers - show/hide exchange_rate field based on currency
function toggleExchangeRateField() {
    const fromWalletSelect = document.getElementById('id_from_wallet');
    const toWalletSelect = document.getElementById('id_to_wallet');
    const exchangeRateField = document.querySelector('[data-field="exchange_rate"]');
    
    if (!fromWalletSelect || !toWalletSelect || !exchangeRateField) return;
    
    function updateExchangeRateVisibility() {
        const fromWalletId = fromWalletSelect.value;
        const toWalletId = toWalletSelect.value;
        
        // Fetch wallet data to check currencies
        if (window.walletsData && fromWalletId && toWalletId) {
            const fromWallet = window.walletsData[fromWalletId];
            const toWallet = window.walletsData[toWalletId];
            
            if (fromWallet && toWallet) {
                if (fromWallet.currency === toWallet.currency) {
                    exchangeRateField.style.display = 'none';
                    document.querySelector('#id_exchange_rate').value = '';
                } else {
                    exchangeRateField.style.display = 'block';
                }
            }
        }
    }
    
    fromWalletSelect.addEventListener('change', updateExchangeRateVisibility);
    toWalletSelect.addEventListener('change', updateExchangeRateVisibility);
    updateExchangeRateVisibility();
}

// For transactions - show/hide exchange_rate field based on currency
function toggleTransactionExchangeRateField() {
    const walletSelect = document.getElementById('id_wallet');
    const currencySelect = document.getElementById('id_currency');
    const exchangeRateField = document.querySelector('[data-field="exchange_rate"]');
    
    if (!walletSelect || !currencySelect || !exchangeRateField) return;
    
    function updateExchangeRateVisibility() {
        const walletId = walletSelect.value;
        const selectedCurrency = currencySelect.value;
        
        if (window.walletsData && walletId) {
            const wallet = window.walletsData[walletId];
            
            if (wallet && selectedCurrency === wallet.currency) {
                exchangeRateField.style.display = 'none';
                document.querySelector('#id_exchange_rate').value = '';
            } else if (selectedCurrency && wallet && selectedCurrency !== wallet.currency) {
                exchangeRateField.style.display = 'block';
            }
        }
    }
    
    walletSelect.addEventListener('change', updateExchangeRateVisibility);
    currencySelect.addEventListener('change', updateExchangeRateVisibility);
    updateExchangeRateVisibility();
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        toggleExchangeRateField();
        toggleTransactionExchangeRateField();
    });
} else {
    toggleExchangeRateField();
    toggleTransactionExchangeRateField();
}
