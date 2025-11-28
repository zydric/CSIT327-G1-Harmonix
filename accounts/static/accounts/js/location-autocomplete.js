/**
 * Location Autocomplete Component
 * Provides Google Maps-like location suggestions with validation
 */

class LocationAutocomplete {
    constructor(inputElement, options = {}) {
        this.input = inputElement;
        this.options = {
            minLength: 2,
            maxSuggestions: 8,
            placeholder: 'Enter city, country (e.g., Cebu, Philippines)',
            validateFormat: true,
            ...options
        };
        
        this.suggestionsList = null;
        this.currentIndex = -1;
        this.isOpen = false;
        
        this.init();
    }
    
    init() {
        // Set placeholder if provided
        if (this.options.placeholder) {
            this.input.placeholder = this.options.placeholder;
        }
        
        // Create suggestions container
        this.createSuggestionsContainer();
        
        // Bind events
        this.bindEvents();
        
        // Add CSS classes for styling
        this.input.classList.add('location-autocomplete-input');
    }
    
    createSuggestionsContainer() {
        this.suggestionsList = document.createElement('div');
        this.suggestionsList.className = 'location-suggestions';
        this.suggestionsList.style.cssText = `
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 1px solid #d1d5db;
            border-top: none;
            border-radius: 0 0 8px 8px;
            max-height: 200px;
            overflow-y: auto;
            z-index: 1000;
            display: none;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        `;
        
        // Make input container relative
        this.input.parentElement.style.position = 'relative';
        this.input.parentElement.appendChild(this.suggestionsList);
    }
    
    bindEvents() {
        // Input events
        this.input.addEventListener('input', this.handleInput.bind(this));
        this.input.addEventListener('keydown', this.handleKeydown.bind(this));
        this.input.addEventListener('blur', this.handleBlur.bind(this));
        this.input.addEventListener('focus', this.handleFocus.bind(this));
        
        // Click outside to close
        document.addEventListener('click', (e) => {
            if (!this.input.contains(e.target) && !this.suggestionsList.contains(e.target)) {
                this.closeSuggestions();
            }
        });
    }
    
    async handleInput(e) {
        const value = e.target.value.trim();
        
        if (value.length >= this.options.minLength) {
            const suggestions = await this.getSuggestions(value);
            this.displaySuggestions(suggestions);
        } else {
            this.closeSuggestions();
        }
        
        // Validate format in real-time
        if (this.options.validateFormat) {
            this.validateFormat(value);
        }
    }
    
    handleKeydown(e) {
        if (!this.isOpen) return;
        
        const suggestions = this.suggestionsList.querySelectorAll('.location-suggestion-item');
        
        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.currentIndex = Math.min(this.currentIndex + 1, suggestions.length - 1);
                this.updateSelection(suggestions);
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                this.currentIndex = Math.max(this.currentIndex - 1, -1);
                this.updateSelection(suggestions);
                break;
                
            case 'Enter':
                e.preventDefault();
                if (this.currentIndex >= 0 && suggestions[this.currentIndex]) {
                    this.selectSuggestion(suggestions[this.currentIndex].textContent);
                }
                break;
                
            case 'Escape':
                this.closeSuggestions();
                break;
        }
    }
    
    handleBlur() {
        // Delay closing to allow clicking on suggestions
        setTimeout(() => {
            this.closeSuggestions();
        }, 200);
    }
    
    handleFocus() {
        const value = this.input.value.trim();
        if (value.length >= this.options.minLength) {
            this.getSuggestions(value).then(suggestions => {
                this.displaySuggestions(suggestions);
            });
        }
    }
    
    async getSuggestions(query) {
        // This method can be overridden to use different data sources
        return this.getLocalSuggestions(query);
    }
    
    getLocalSuggestions(query) {
        const locations = this.getLocationData();
        const queryLower = query.toLowerCase();
        
        const matches = locations.filter(location => {
            const locationLower = location.toLowerCase();
            return locationLower.includes(queryLower) || 
                   location.split(',')[0].toLowerCase().startsWith(queryLower);
        });
        
        return matches.slice(0, this.options.maxSuggestions);
    }
    
    displaySuggestions(suggestions) {
        this.suggestionsList.innerHTML = '';
        
        if (suggestions.length === 0) {
            this.closeSuggestions();
            return;
        }
        
        suggestions.forEach((suggestion, index) => {
            const item = document.createElement('div');
            item.className = 'location-suggestion-item';
            item.textContent = suggestion;
            item.style.cssText = `
                padding: 12px 16px;
                cursor: pointer;
                border-bottom: 1px solid #f3f4f6;
                transition: background-color 0.2s;
            `;
            
            item.addEventListener('mouseenter', () => {
                this.currentIndex = index;
                this.updateSelection(this.suggestionsList.querySelectorAll('.location-suggestion-item'));
            });
            
            item.addEventListener('click', () => {
                this.selectSuggestion(suggestion);
            });
            
            this.suggestionsList.appendChild(item);
        });
        
        this.openSuggestions();
    }
    
    updateSelection(suggestions) {
        suggestions.forEach((item, index) => {
            if (index === this.currentIndex) {
                item.style.backgroundColor = '#f3f4f6';
            } else {
                item.style.backgroundColor = 'white';
            }
        });
    }
    
    selectSuggestion(suggestion) {
        this.input.value = suggestion;
        this.closeSuggestions();
        
        // Trigger change event
        this.input.dispatchEvent(new Event('change', { bubbles: true }));
        
        // Validate the selected suggestion
        if (this.options.validateFormat) {
            this.validateFormat(suggestion);
        }
    }
    
    openSuggestions() {
        this.suggestionsList.style.display = 'block';
        this.isOpen = true;
        this.currentIndex = -1;
    }
    
    closeSuggestions() {
        this.suggestionsList.style.display = 'none';
        this.isOpen = false;
        this.currentIndex = -1;
    }
    
    validateFormat(value) {
        const isValid = this.isValidLocationFormat(value);
        
        // Update input styling based on validation
        if (value.length > 0) {
            if (isValid) {
                this.input.classList.remove('location-invalid');
                this.input.classList.add('location-valid');
            } else {
                this.input.classList.remove('location-valid');
                this.input.classList.add('location-invalid');
            }
        } else {
            this.input.classList.remove('location-valid', 'location-invalid');
        }
        
        return isValid;
    }
    
    isValidLocationFormat(location) {
        if (!location || location.trim().length === 0) return true; // Empty is okay
        
        // Check for "City, Country" format
        const parts = location.split(',');
        if (parts.length !== 2) return false;
        
        const city = parts[0].trim();
        const country = parts[1].trim();
        
        // Both parts should be non-empty and contain only valid characters
        const validNamePattern = /^[a-zA-Z\s\-.'()]+$/;
        
        return city.length > 0 && country.length > 0 && 
               validNamePattern.test(city) && validNamePattern.test(country);
    }
    
    getLocationData() {
        // Static location data - can be replaced with API call
        return [
            // Philippines
            'Manila, Philippines',
            'Cebu, Philippines',
            'Davao, Philippines',
            'Quezon City, Philippines',
            'Makati, Philippines',
            'Pasig, Philippines',
            'Taguig, Philippines',
            'Antipolo, Philippines',
            'Pasay, Philippines',
            'Cagayan de Oro, Philippines',
            'Iloilo, Philippines',
            'Bacolod, Philippines',
            'Baguio, Philippines',
            'Zamboanga, Philippines',
            'Caloocan, Philippines',
            
            // Major world cities
            'New York, United States',
            'Los Angeles, United States',
            'Chicago, United States',
            'Houston, United States',
            'Miami, United States',
            'San Francisco, United States',
            'Seattle, United States',
            'Boston, United States',
            'Las Vegas, United States',
            'Atlanta, United States',
            
            'London, United Kingdom',
            'Manchester, United Kingdom',
            'Birmingham, United Kingdom',
            'Liverpool, United Kingdom',
            'Edinburgh, United Kingdom',
            
            'Tokyo, Japan',
            'Osaka, Japan',
            'Kyoto, Japan',
            'Yokohama, Japan',
            
            'Seoul, South Korea',
            'Busan, South Korea',
            
            'Beijing, China',
            'Shanghai, China',
            'Guangzhou, China',
            'Shenzhen, China',
            
            'Singapore, Singapore',
            'Kuala Lumpur, Malaysia',
            'Bangkok, Thailand',
            'Jakarta, Indonesia',
            'Ho Chi Minh City, Vietnam',
            'Hanoi, Vietnam',
            
            'Sydney, Australia',
            'Melbourne, Australia',
            'Brisbane, Australia',
            'Perth, Australia',
            
            'Toronto, Canada',
            'Vancouver, Canada',
            'Montreal, Canada',
            
            'Paris, France',
            'Berlin, Germany',
            'Rome, Italy',
            'Madrid, Spain',
            'Amsterdam, Netherlands',
            'Vienna, Austria',
            'Zurich, Switzerland',
            
            'Mumbai, India',
            'Delhi, India',
            'Bangalore, India',
            'Chennai, India',
            'Hyderabad, India',
            'Pune, India',
            
            'São Paulo, Brazil',
            'Rio de Janeiro, Brazil',
            'Buenos Aires, Argentina',
            'Mexico City, Mexico',
            
            'Dubai, United Arab Emirates',
            'Doha, Qatar',
            'Riyadh, Saudi Arabia',
            
            'Cairo, Egypt',
            'Cape Town, South Africa',
            'Lagos, Nigeria',
        ];
    }
}

// CSS Styles to be added
const locationAutocompleteStyles = `
    .location-autocomplete-input.location-valid {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 1px #10b981;
    }
    
    .location-autocomplete-input.location-invalid {
        border-color: #ef4444 !important;
        box-shadow: 0 0 0 1px #ef4444;
    }
    
    .location-suggestion-item:hover {
        background-color: #f3f4f6 !important;
    }
    
    .location-suggestion-item:last-child {
        border-bottom: none;
    }
`;

// Add styles to document
if (!document.querySelector('#location-autocomplete-styles')) {
    const style = document.createElement('style');
    style.id = 'location-autocomplete-styles';
    style.textContent = locationAutocompleteStyles;
    document.head.appendChild(style);
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LocationAutocomplete;
}