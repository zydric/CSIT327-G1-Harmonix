//A simple autocomplete widget for location input fields powered by a static list of location in my own server api
class SimpleLocationAutocomplete {

    constructor(inputElement) {
        this.input = inputElement;
        this.suggestionsList = null;
        this.searchTimeout = null;
        this.ignoreNextInput = false;
        
        this.init();
    }
    
    //Initialization Component
    init() {
        this.input.placeholder = 'Enter city, country (e.g., Cebu, Philippines)';
        this.createSuggestionsContainer(); //Creates Drop Down Container
        this.bindEvents(); //Even Listeners for User Interactions
    }
    

    createSuggestionsContainer() {
        // Position the suggestions container below the input and is set to hidden by default
        this.suggestionsList = document.createElement('div');
        this.suggestionsList.style.cssText = `
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 1px solid #d1d5db;
            border-top: none;
            max-height: 200px;
            overflow-y: auto;
            z-index: 1000;
            display: none;
        `;        
        this.input.parentNode.style.position = 'relative';
        this.input.parentNode.appendChild(this.suggestionsList);
    }
    
    //Bind all necessary event listeners
    bindEvents() {
        this.input.addEventListener('input', (e) => {

            // Ignore programmatically-triggered input after selection
            if (this.ignoreNextInput) {
                this.ignoreNextInput = false;
                return;
            }

            clearTimeout(this.searchTimeout);

            this.searchTimeout = setTimeout(() => {
                this.handleInput(e.target.value);
            }, 300);
        });

        this.input.addEventListener('blur', () => {
            setTimeout(() => this.closeSuggestions(), 150);
        });

        document.addEventListener('click', (e) => {
            if (!this.input.contains(e.target) && !this.suggestionsList.contains(e.target)) {
                this.closeSuggestions();
            }
        });
    }

    
    //Handle input changes and trigger search
    //@param {string} value - The current input value
    async handleInput(value) {
        const query = value ? value.trim() : '';
        
        // Only search if query has at least 2 characters
        if (query.length < 2) {
            this.closeSuggestions();
            return;
        }
        
        try {
            const suggestions = await this.searchLocations(query);
            this.displaySuggestions(suggestions);
        } catch (error) {
            console.error('Location search error:', error);
            this.closeSuggestions();
        }
    }
    
    
    //Searchers for Locations in the server API
    // quer - The search query, returns Promise of Array of location suggestions
    async searchLocations(query) {
        const url = `/accounts/api/location-search/?q=${encodeURIComponent(query)}&limit=8`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        return data.locations || [];
    }
    
    //Display the suggestions in the dropdown
    //@param {Array} suggestions - Array of location strings     
    displaySuggestions(suggestions) {
        this.suggestionsList.innerHTML = '';
        
        if (suggestions.length === 0) {
            this.closeSuggestions();
            return;
        }
        
        // Create suggestion items
        suggestions.forEach(suggestion => {
            const item = document.createElement('div');
            item.textContent = suggestion;
            item.style.cssText = 'padding: 10px 15px; cursor: pointer; border-bottom: 1px solid #f3f4f6;';
            
            // Handle click selection
            item.addEventListener('click', () => {
                this.input.value = suggestion;
                this.closeSuggestions();

                this.ignoreNextInput = true;
                this.input.dispatchEvent(new Event('input', { bubbles: true }));
            });
            
            item.addEventListener('mouseenter', () => {
                item.style.backgroundColor = '#f3f4f6';
            });
            
            item.addEventListener('mouseleave', () => {
                item.style.backgroundColor = 'white';
            });
            
            this.suggestionsList.appendChild(item);
        });
        
        this.suggestionsList.style.display = 'block';
    }
    
    closeSuggestions() {
        this.suggestionsList.style.display = 'none';
    }
}

// Export for backward compatibility with existing templates
window.LocationAutocomplete = SimpleLocationAutocomplete;