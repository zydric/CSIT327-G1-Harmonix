/**
 * Password Strength Component
 * Handles password strength indication and validation
 */

// Make PasswordStrength available globally
window.PasswordStrength = function(passwordFieldId, strengthIndicatorId) {
    this.passwordField = document.getElementById(passwordFieldId);
    this.strengthIndicator = document.getElementById(strengthIndicatorId);
    this.strengthBar = document.getElementById('strength-bar');
    this.strengthText = document.getElementById('strength-text');
    this.requirements = document.getElementById('password-requirements');
    
    var self = this;
    
    if (this.passwordField) {
        this.passwordField.addEventListener('input', function() {
            self.checkStrength();
        });
    }
};

window.PasswordStrength.prototype.checkStrength = function() {
    const password = this.passwordField.value;
    
    if (password.length === 0) {
        this.strengthIndicator.classList.add('hidden');
        return;
    }
    
    this.strengthIndicator.classList.remove('hidden');
    
    let score = 0;
    
    // Check requirements
    const requirements = {
        'req-length': password.length >= 8,
        'req-lower': /[a-z]/.test(password),
        'req-upper': /[A-Z]/.test(password),
        'req-number': /[0-9]/.test(password),
        'req-special': /[!@#$%^&*(),.?":{}|<>]/.test(password)
    };
    
    // Update requirement indicators
    Object.entries(requirements).forEach(([id, met]) => {
        const element = document.getElementById(id);
        if (element) {
            if (met) {
                element.classList.remove('text-gray-500');
                element.classList.add('text-green-600');
                score++;
            } else {
                element.classList.remove('text-green-600');
                element.classList.add('text-gray-500');
            }
        }
    });
    
    // Calculate strength and update display
    this.updateStrengthDisplay(score);
};

window.PasswordStrength.prototype.updateStrengthDisplay = function(score) {
    let strength, color, width;
    
    if (score <= 1) {
        strength = 'Very Weak';
        color = '#dc2626';
        width = '20%';
    } else if (score === 2) {
        strength = 'Weak';
        color = '#ea580c';
        width = '40%';
    } else if (score === 3) {
        strength = 'Fair';
        color = '#d97706';
        width = '60%';
    } else if (score === 4) {
        strength = 'Good';
        color = '#16a34a';
        width = '80%';
    } else {
        strength = 'Strong';
        color = '#059669';
        width = '100%';
    }
    
    if (this.strengthBar) {
        this.strengthBar.style.backgroundColor = color;
        this.strengthBar.style.width = width;
    }
    
    if (this.strengthText) {
        this.strengthText.textContent = strength;
        this.strengthText.style.color = color;
    }
};