// Product Recommendation System JavaScript

class ProductRecommendationApp {
    constructor() {
        this.form = document.getElementById('recommendationForm');
        this.submitBtn = document.getElementById('submitBtn');
        this.resultsContainer = document.getElementById('resultsContainer');
        this.resultCard = document.getElementById('resultCard');
        this.errorContainer = document.getElementById('errorContainer');
        this.errorText = document.getElementById('errorText');
        
        this.apiUrl = 'http://127.0.0.1:5000/predict-product';
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupFormValidation();
    }

    bindEvents() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Add input event listeners for real-time validation
        const inputs = this.form.querySelectorAll('select, input');
        inputs.forEach(input => {
            input.addEventListener('change', () => this.validateForm());
            input.addEventListener('input', () => this.validateForm());
        });
    }

    setupFormValidation() {
        this.validateForm();
    }

    validateForm() {
        const formData = new FormData(this.form);
        const data = Object.fromEntries(formData);
        
        // Check if all required fields are filled
        const requiredFields = ['region', 'gender', 'user_age_group', 'user_preferences', 'season', 'product_keywords', 'previous_buy'];
        const isValid = requiredFields.every(field => data[field] && data[field].trim() !== '');
        
        this.submitBtn.disabled = !isValid;
        
        return isValid;
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        if (!this.validateForm()) {
            this.showError('Please fill in all required fields.');
            return;
        }

        this.setLoadingState(true);
        this.hideResults();
        this.hideError();

        try {
            const formData = new FormData(this.form);
            const data = Object.fromEntries(formData);
            
            // Clean and format the data
            const requestData = this.formatRequestData(data);
            
            const response = await this.makeApiRequest(requestData);
            
            if (response.predicted_product) {
                this.showResults(response.predicted_product, requestData);
            } else {
                throw new Error('No recommendation received from server');
            }
            
        } catch (error) {
            console.error('Error:', error);
            this.showError(this.getErrorMessage(error));
        } finally {
            this.setLoadingState(false);
        }
    }

    formatRequestData(data) {
        return {
            region: data.region.trim(),
            gender: data.gender.trim(),
            user_age_group: data.user_age_group.trim(),
            user_preferences: data.user_preferences.trim(),
            season: data.season.trim(),
            product_keywords: data.product_keywords.trim(),
            previous_buy: data.previous_buy.trim()
        };
    }

    async makeApiRequest(data) {
        const response = await fetch(this.apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    }

    showResults(product, userData) {
        const productIcon = this.getProductIcon(product);
        const productName = this.formatProductName(product);
        
        this.resultCard.innerHTML = `
            <div class="product-icon">${productIcon}</div>
            <div class="product-name">${productName}</div>
            <div class="recommendation-text">
                Perfect for ${userData.user_preferences} in ${userData.season.toLowerCase()}!
            </div>
        `;
        
        this.resultsContainer.style.display = 'block';
        this.resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    getProductIcon(product) {
        const icons = {
            'tshirt': '👕',
            't-shirt': '👕',
            'shirt': '👔',
            'jeans': '👖',
            'shoes': '👟',
            'joggers': '🏃‍♂️',
            'shorts': '🩳',
            'flipflop': '🩴',
            'flip flop': '🩴',
            'boots': '🥾',
            'leggings': '🧘‍♀️',
            'coat': '🧥',
            'jacket': '🧥',
            'dress': '👗',
            'skirt': '👗',
            'top': '👚',
            'hoodie': '👘',
            'sweater': '🧥'
        };
        
        const normalizedProduct = product.toLowerCase().trim();
        return icons[normalizedProduct] || '👕';
    }

    formatProductName(product) {
        return product.split(' ')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
            .join(' ');
    }

    showError(message) {
        this.errorText.textContent = message;
        this.errorContainer.style.display = 'block';
        this.errorContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    hideError() {
        this.errorContainer.style.display = 'none';
    }

    hideResults() {
        this.resultsContainer.style.display = 'none';
    }

    setLoadingState(isLoading) {
        if (isLoading) {
            this.submitBtn.classList.add('loading');
            this.submitBtn.disabled = true;
        } else {
            this.submitBtn.classList.remove('loading');
            this.submitBtn.disabled = false;
        }
    }

    getErrorMessage(error) {
        if (error.message.includes('Failed to fetch')) {
            return 'Unable to connect to the server. Please make sure the Flask API is running on http://127.0.0.1:5000';
        } else if (error.message.includes('HTTP 400')) {
            return 'Invalid input data. Please check your entries and try again.';
        } else if (error.message.includes('HTTP 500')) {
            return 'Server error occurred. Please try again later.';
        } else {
            return error.message || 'An unexpected error occurred. Please try again.';
        }
    }
}

// Utility functions for enhanced user experience
class UIEnhancements {
    static addInputAnimations() {
        const inputs = document.querySelectorAll('select, input');
        
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.classList.remove('focused');
            });
        });
    }

    static addKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Enter key to submit form when focused on any input
            if (e.key === 'Enter' && e.target.tagName !== 'BUTTON') {
                const submitBtn = document.getElementById('submitBtn');
                if (!submitBtn.disabled) {
                    submitBtn.click();
                }
            }
        });
    }

    static addProductKeywordsSuggestions() {
        const keywordsInput = document.getElementById('product_keywords');
        const suggestions = [
            'fashion,shoes,shirts,jeans',
            'sports,shoes,tshirt,shorts',
            'formal,shirts,trousers,leather',
            'casual,fashion,shoes,shirts',
            'party,shirt,jeans,boots',
            'fitness,leggings,shoes,top',
            'syndo,shoes,tshirt,flipflop'
        ];

        keywordsInput.addEventListener('focus', function() {
            if (!this.value) {
                const randomSuggestion = suggestions[Math.floor(Math.random() * suggestions.length)];
                this.placeholder = `e.g., ${randomSuggestion}`;
            }
        });
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ProductRecommendationApp();
    UIEnhancements.addInputAnimations();
    UIEnhancements.addKeyboardShortcuts();
    UIEnhancements.addProductKeywordsSuggestions();
    
    // Add a subtle animation to the header
    const header = document.querySelector('.header h1');
    if (header) {
        setTimeout(() => {
            header.style.transform = 'scale(1.05)';
            setTimeout(() => {
                header.style.transform = 'scale(1)';
            }, 200);
        }, 500);
    }
});
