/**
 * Registration Form Handler
 * Uses modular FormValidator and PasswordStrength components
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Registration form initializing...');
    
    // Get all the required elements
    const roleSelect = document.getElementById('role');
    const instrumentsField = document.getElementById('instruments-field');
    const genresField = document.getElementById('genres-field');
    const usernameField = document.getElementById('username');
    const emailField = document.getElementById('email');
    const password1Field = document.getElementById('password1');
    const password2Field = document.getElementById('password2');
    
    // Function to toggle musician/band fields
    function toggleMusicianFields() {
        if (!roleSelect || !instrumentsField || !genresField) {
            console.error('Required elements not found for toggleMusicianFields');
            return;
        }
        
        const genresHelperText = document.getElementById('genres-helper-text');
        
        if (roleSelect.value === 'musician') {
            // Show both instruments and genres for musicians
            instrumentsField.classList.remove('hidden');
            genresField.classList.remove('hidden');
            if (genresHelperText) {
                genresHelperText.textContent = 'Select your preferred musical genres';
            }
        } else if (roleSelect.value === 'band') {
            // Show only genres for bands (no instruments)
            instrumentsField.classList.add('hidden');
            genresField.classList.remove('hidden');
            if (genresHelperText) {
                genresHelperText.textContent = 'Select your band\'s musical genres';
            }
            
            // Clear instrument selections when switching to band
            const instrumentCheckboxes = instrumentsField.querySelectorAll('input[type="checkbox"]');
            instrumentCheckboxes.forEach(cb => cb.checked = false);
        } else {
            // Hide both for no selection
            instrumentsField.classList.add('hidden');
            genresField.classList.add('hidden');
        }
    }
    
    // Set up role selection handler
    if (roleSelect) {
        roleSelect.addEventListener('change', toggleMusicianFields);
        
        // Show fields on page load based on current role value
        if (roleSelect.value) {
            toggleMusicianFields();
        }
    }
    
    // Set up password strength (if PasswordStrength is available)
    if (password1Field && window.PasswordStrength) {
        new PasswordStrength('password1', 'password-strength');
    }
    
    // Set up form validation (if FormValidator is available)
    if (window.FormValidator) {
        // Username validation
        if (usernameField) {
            usernameField.addEventListener('input', function() {
                const isValid = FormValidator.validateUsername(this.value);
                FormValidator.updateFieldValidation(this, isValid);
            });
        }
        
        // Email validation
        if (emailField) {
            emailField.addEventListener('input', function() {
                const isValid = FormValidator.validateEmail(this.value);
                FormValidator.updateFieldValidation(this, isValid);
            });
        }
        
        // Password validation
        if (password1Field) {
            password1Field.addEventListener('input', function() {
                const isValid = FormValidator.validatePassword(this.value);
                FormValidator.updateFieldValidation(this, isValid);
                
                // Also check password confirmation if it has a value
                if (password2Field && password2Field.value) {
                    const passwordsMatch = this.value === password2Field.value;
                    FormValidator.updateFieldValidation(password2Field, passwordsMatch);
                }
            });
        }
        
        // Password confirmation validation
        if (password2Field) {
            password2Field.addEventListener('input', function() {
                const passwordsMatch = this.value === password1Field.value;
                FormValidator.updateFieldValidation(this, passwordsMatch);
            });
        }
        
        // Handle Django template errors (scroll to first error)
        if (window.hasFieldErrors) {
            FormValidator.scrollToFirstError();
        }
    }
    
    console.log('Registration form initialization complete');
});