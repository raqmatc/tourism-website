/**
 * RateHawk Integration Script for Paygo.com
 * This script handles the integration with RateHawk booking system
 * Author: Manus AI
 * Version: 1.0.0
 */

class RateHawkIntegration {
    constructor(config) {
        this.config = {
            partnerId: '282088.affiliate.dd55',
            baseUrl: 'https://www.zenhotels.com',
            widgetId: '2a4f00af0f91dc4e0a4ad28a321021c9',
            trackingEnabled: true,
            ...config
        };
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadAnalytics();
        console.log('RateHawk Integration initialized successfully');
    }

    setupEventListeners() {
        // Handle search form submissions
        const searchForm = document.getElementById('hotelSearchForm');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => this.handleSearch(e));
        }

        // Handle destination card clicks
        document.querySelectorAll('.destination-card').forEach(card => {
            card.addEventListener('click', (e) => this.handleDestinationClick(e));
        });
    }

    handleSearch(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const searchData = {
            destination: formData.get('destination'),
            checkin: formData.get('checkin'),
            checkout: formData.get('checkout'),
            guests: formData.get('guests')
        };

        if (this.validateSearchData(searchData)) {
            this.performSearch(searchData);
        }
    }

    validateSearchData(data) {
        if (!data.destination || !data.checkin || !data.checkout) {
            this.showError('يرجى ملء جميع الحقول المطلوبة');
            return false;
        }

        const checkinDate = new Date(data.checkin);
        const checkoutDate = new Date(data.checkout);
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        if (checkinDate < today) {
            this.showError('تاريخ الوصول يجب أن يكون اليوم أو في المستقبل');
            return false;
        }

        if (checkoutDate <= checkinDate) {
            this.showError('تاريخ المغادرة يجب أن يكون بعد تاريخ الوصول');
            return false;
        }

        return true;
    }

    performSearch(searchData) {
        this.showLoading(true);
        
        // Track the search
        this.trackEvent('hotel_search', searchData);

        // Generate RateHawk URL
        const searchUrl = this.generateSearchUrl(searchData);

        // Simulate loading time for better UX
        setTimeout(() => {
            this.showLoading(false);
            this.showSuccess('تم العثور على عروض رائعة! سيتم توجيهك إلى صفحة النتائج...');
            
            setTimeout(() => {
                this.redirectToRateHawk(searchUrl);
            }, 1500);
        }, 2000);
    }

    generateSearchUrl(searchData) {
        const cityName = searchData.destination.split('،')[0].trim();
        
        const params = new URLSearchParams({
            'destination': cityName,
            'checkin': searchData.checkin,
            'checkout': searchData.checkout,
            'guests': searchData.guests,
            'partner_id': this.config.partnerId,
            'utm_source': 'paygo',
            'utm_medium': 'website',
            'utm_campaign': 'hotel_search',
            'widget_id': this.config.widgetId
        });

        return `${this.config.baseUrl}/search?${params.toString()}`;
    }

    redirectToRateHawk(url) {
        // Track the redirect
        this.trackEvent('ratehawk_redirect', { url });
        
        // Open in new tab to keep user on our site
        window.open(url, '_blank', 'noopener,noreferrer');
    }

    handleDestinationClick(event) {
        const card = event.currentTarget;
        const destination = card.querySelector('h3').textContent;
        
        // Fill the search form
        const destinationInput = document.getElementById('destination');
        if (destinationInput) {
            destinationInput.value = destination;
            destinationInput.scrollIntoView({ behavior: 'smooth' });
        }

        // Track destination selection
        this.trackEvent('destination_selected', { destination });
    }

    showLoading(show) {
        const loadingElement = document.getElementById('loading');
        if (loadingElement) {
            loadingElement.style.display = show ? 'block' : 'none';
        }
    }

    showSuccess(message) {
        const successElement = document.getElementById('successMessage');
        if (successElement) {
            successElement.textContent = message;
            successElement.style.display = 'block';
            
            // Hide after 3 seconds
            setTimeout(() => {
                successElement.style.display = 'none';
            }, 3000);
        }
    }

    showError(message) {
        alert(message); // You can replace this with a better error display
    }

    trackEvent(eventName, data) {
        if (!this.config.trackingEnabled) return;

        // Google Analytics tracking
        if (typeof gtag !== 'undefined') {
            gtag('event', eventName, {
                ...data,
                partner: 'ratehawk',
                timestamp: new Date().toISOString()
            });
        }

        // Custom analytics endpoint
        this.sendToAnalytics(eventName, data);
    }

    async sendToAnalytics(eventName, data) {
        try {
            await fetch('/api/analytics', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    event: eventName,
                    data,
                    timestamp: new Date().toISOString(),
                    partner: 'ratehawk',
                    partnerId: this.config.partnerId
                })
            });
        } catch (error) {
            console.log('Analytics tracking failed:', error);
        }
    }

    loadAnalytics() {
        // Load Google Analytics if not already loaded
        if (typeof gtag === 'undefined' && this.config.trackingEnabled) {
            const script = document.createElement('script');
            script.async = true;
            script.src = 'https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID';
            document.head.appendChild(script);

            script.onload = () => {
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());
                gtag('config', 'GA_MEASUREMENT_ID');
            };
        }
    }

    // Utility methods
    static formatDate(date) {
        return new Date(date).toISOString().split('T')[0];
    }

    static getDefaultDates() {
        const today = new Date();
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        const dayAfter = new Date(today);
        dayAfter.setDate(dayAfter.getDate() + 2);

        return {
            checkin: this.formatDate(tomorrow),
            checkout: this.formatDate(dayAfter)
        };
    }
}

// Popular cities data
const POPULAR_CITIES = [
    'الرياض، المملكة العربية السعودية',
    'جدة، المملكة العربية السعودية',
    'الدمام، المملكة العربية السعودية',
    'مكة المكرمة، المملكة العربية السعودية',
    'المدينة المنورة، المملكة العربية السعودية',
    'دبي، الإمارات العربية المتحدة',
    'أبوظبي، الإمارات العربية المتحدة',
    'الشارقة، الإمارات العربية المتحدة',
    'القاهرة، مصر',
    'الإسكندرية، مصر',
    'شرم الشيخ، مصر',
    'الغردقة، مصر',
    'بيروت، لبنان',
    'عمان، الأردن',
    'العقبة، الأردن',
    'الدوحة، قطر',
    'المنامة، البحرين',
    'مسقط، عمان',
    'الكويت، الكويت',
    'إسطنبول، تركيا',
    'أنطاليا، تركيا',
    'بودروم، تركيا',
    'لندن، المملكة المتحدة',
    'باريس، فرنسا',
    'روما، إيطاليا',
    'برشلونة، إسبانيا',
    'أمستردام، هولندا',
    'فيينا، النمسا',
    'براغ، التشيك',
    'بودابست، المجر',
    'نيويورك، الولايات المتحدة',
    'لوس أنجلوس، الولايات المتحدة',
    'ميامي، الولايات المتحدة',
    'طوكيو، اليابان',
    'سيول، كوريا الجنوبية',
    'بانكوك، تايلاند',
    'بوكيت، تايلاند',
    'كوالالمبور، ماليزيا',
    'سنغافورة',
    'بالي، إندونيسيا',
    'جاكرتا، إندونيسيا',
    'مانيلا، الفلبين',
    'هانوي، فيتنام',
    'هو تشي مين، فيتنام',
    'سيدني، أستراليا',
    'ملبورن، أستراليا'
];

// Auto-complete functionality
class AutoComplete {
    constructor(inputElement, suggestions) {
        this.input = inputElement;
        this.suggestions = suggestions;
        this.suggestionsContainer = null;
        this.init();
    }

    init() {
        this.createSuggestionsContainer();
        this.setupEventListeners();
    }

    createSuggestionsContainer() {
        this.suggestionsContainer = document.createElement('div');
        this.suggestionsContainer.className = 'suggestions';
        this.suggestionsContainer.id = 'suggestions';
        this.input.parentNode.appendChild(this.suggestionsContainer);
    }

    setupEventListeners() {
        this.input.addEventListener('input', (e) => this.handleInput(e));
        this.input.addEventListener('keydown', (e) => this.handleKeydown(e));
        document.addEventListener('click', (e) => this.handleDocumentClick(e));
    }

    handleInput(event) {
        const query = event.target.value.toLowerCase().trim();
        
        if (query.length < 2) {
            this.hideSuggestions();
            return;
        }

        const filteredSuggestions = this.suggestions.filter(suggestion => 
            suggestion.toLowerCase().includes(query)
        ).slice(0, 8);

        this.showSuggestions(filteredSuggestions);
    }

    handleKeydown(event) {
        const items = this.suggestionsContainer.querySelectorAll('.suggestion-item');
        const activeItem = this.suggestionsContainer.querySelector('.suggestion-item.active');
        
        switch (event.key) {
            case 'ArrowDown':
                event.preventDefault();
                if (activeItem) {
                    activeItem.classList.remove('active');
                    const next = activeItem.nextElementSibling || items[0];
                    next.classList.add('active');
                } else if (items.length > 0) {
                    items[0].classList.add('active');
                }
                break;
                
            case 'ArrowUp':
                event.preventDefault();
                if (activeItem) {
                    activeItem.classList.remove('active');
                    const prev = activeItem.previousElementSibling || items[items.length - 1];
                    prev.classList.add('active');
                }
                break;
                
            case 'Enter':
                if (activeItem) {
                    event.preventDefault();
                    this.selectSuggestion(activeItem.textContent);
                }
                break;
                
            case 'Escape':
                this.hideSuggestions();
                break;
        }
    }

    handleDocumentClick(event) {
        if (!this.input.contains(event.target) && !this.suggestionsContainer.contains(event.target)) {
            this.hideSuggestions();
        }
    }

    showSuggestions(suggestions) {
        if (suggestions.length === 0) {
            this.hideSuggestions();
            return;
        }

        this.suggestionsContainer.innerHTML = suggestions.map(suggestion => 
            `<div class="suggestion-item" onclick="autoComplete.selectSuggestion('${suggestion}')">${suggestion}</div>`
        ).join('');
        
        this.suggestionsContainer.style.display = 'block';
    }

    hideSuggestions() {
        this.suggestionsContainer.style.display = 'none';
    }

    selectSuggestion(suggestion) {
        this.input.value = suggestion;
        this.hideSuggestions();
        this.input.focus();
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize RateHawk integration
    window.rateHawkIntegration = new RateHawkIntegration();
    
    // Initialize auto-complete
    const destinationInput = document.getElementById('destination');
    if (destinationInput) {
        window.autoComplete = new AutoComplete(destinationInput, POPULAR_CITIES);
    }
    
    // Set default dates
    const defaultDates = RateHawkIntegration.getDefaultDates();
    const checkinInput = document.getElementById('checkin');
    const checkoutInput = document.getElementById('checkout');
    
    if (checkinInput) checkinInput.value = defaultDates.checkin;
    if (checkoutInput) checkoutInput.value = defaultDates.checkout;
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    console.log('Paygo.com with RateHawk integration loaded successfully!');
});

// Global functions for inline event handlers
function selectDestination(city) {
    if (window.autoComplete) {
        window.autoComplete.selectSuggestion(city);
    }
}

function searchDestination(city) {
    const destinationInput = document.getElementById('destination');
    if (destinationInput) {
        destinationInput.value = city;
        destinationInput.scrollIntoView({ behavior: 'smooth' });
    }
    
    if (window.rateHawkIntegration) {
        window.rateHawkIntegration.trackEvent('destination_selected', { destination: city });
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { RateHawkIntegration, AutoComplete, POPULAR_CITIES };
}
