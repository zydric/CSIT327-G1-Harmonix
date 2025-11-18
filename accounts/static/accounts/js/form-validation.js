/**
 * Form Validation Utilities
 * Reusable validation functions for forms across the application
 */

// Make FormValidator available globally
window.FormValidator = {
    /**
     * Update field validation styling based on validity
     * @param {HTMLElement} field - The form field element
     * @param {boolean} isValid - Whether the field is valid
     */
    updateFieldValidation: function(field, isValid) {
        if (!field) return;
        
        if (field.value.trim() === '') {
            // Don't show validation for empty fields
            field.classList.remove('border-red-500', 'bg-red-50', 'border-green-500', 'bg-green-50');
            field.classList.add('border-gray-300');
            return;
        }
        
        if (isValid) {
            field.classList.remove('border-red-500', 'bg-red-50', 'border-gray-300');
            field.classList.add('border-green-500', 'bg-green-50');
        } else {
            field.classList.remove('border-green-500', 'bg-green-50', 'border-gray-300');
            field.classList.add('border-red-500', 'bg-red-50');
        }
    },

    /**
     * Validate username format
     * @param {string} username - The username to validate
     * @returns {boolean} - Whether the username is valid
     */
    validateUsername: function(username) {
        const trimmed = username.trim();
        return trimmed.length >= 3 && /^[a-zA-Z0-9_]+$/.test(trimmed);
    },

    /**
     * Validate email format
     * @param {string} email - The email to validate
     * @returns {boolean} - Whether the email is valid
     */
    validateEmail: function(email) {
        const trimmed = email.trim();
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmed);
    },

    /**
     * Validate password strength
     * @param {string} password - The password to validate
     * @returns {boolean} - Whether the password meets requirements
     */
    validatePassword: function(password) {
        return password.length >= 8 && 
               /[a-z]/.test(password) && 
               /[A-Z]/.test(password) && 
               /[0-9]/.test(password) && 
               /[!@#$%^&*(),.?":{}|<>]/.test(password);
    },

    /**
     * Scroll to and focus the first error field
     */
    scrollToFirstError: function() {
        const firstErrorField = document.querySelector('.border-red-500');
        if (firstErrorField) {
            firstErrorField.scrollIntoView({ behavior: 'smooth', block: 'center' });
            firstErrorField.focus();
        }
    }
};