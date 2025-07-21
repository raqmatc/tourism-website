/**
 * RateHawk Integration Library for Paygo.com
 * Enhanced version with advanced features and analytics
 * Version: 2.0
 * Author: Manus AI
 * Date: 2025-07-21
 */

// RateHawk Configuration
const RATEHAWK_CONFIG = {
  partnerId: '282088.affiliate.dd55',
  baseUrl: 'https://www.zenhotels.com',
  trackingEnabled: true,
  debug: false
};

// Analytics and Tracking
class PaygoAnalytics {
  constructor() {
    this.sessionId = this.generateSessionId();
    this.events = [];
    this.startTime = Date.now();
  }

  generateSessionId() {
    return 'paygo_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  track(eventName, properties = {}) {
    const event = {
      event: eventName,
      properties: {
        ...properties,
        sessionId: this.sessionId,
        timestamp: Date.now(),
        url: window.location.href,
        userAgent: navigator.userAgent,
        partnerId: RATEHAWK_CONFIG.partnerId
      }
    };

    this.events.push(event);

    if (RATEHAWK_CONFIG.debug) {
      console.log('Paygo Analytics:', event);
    }

    // Send to Google Analytics if available
    if (typeof gtag !== 'undefined') {
      gtag('event', eventName, properties);
    }

    // Send to RateHawk tracking (if they provide an endpoint)
    this.sendToRateHawk(event);
  }

  sendToRateHawk(event) {
    // In a real implementation, this would send to RateHawk's tracking endpoint
    if (RATEHAWK_CONFIG.trackingEnabled) {
      // Placeholder for RateHawk tracking API
      console.log('Tracking event to RateHawk:', event);
    }
  }

  getSessionStats() {
    return {
      sessionId: this.sessionId,
      duration: Date.now() - this.startTime,
      eventsCount: this.events.length,
      events: this.events
    };
  }
}

// Initialize Analytics
const analytics = new PaygoAnalytics();

// City Database for Suggestions
const CITIES_DATABASE = [
  // Saudi Arabia
  { name: 'الرياض', country: 'المملكة العربية السعودية', code: 'RUH', coordinates: [24.7136, 46.6753] },
  { name: 'جدة', country: 'المملكة العربية السعودية', code: 'JED', coordinates: [21.4858, 39.1925] },
  { name: 'الدمام', country: 'المملكة العربية السعودية', code: 'DMM', coordinates: [26.4207, 50.0888] },
  { name: 'مكة المكرمة', country: 'المملكة العربية السعودية', code: 'MKK', coordinates: [21.3891, 39.8579] },
  { name: 'المدينة المنورة', country: 'المملكة العربية السعودية', code: 'MED', coordinates: [24.5247, 39.5692] },
  { name: 'الطائف', country: 'المملكة العربية السعودية', code: 'TIF', coordinates: [21.2703, 40.4158] },
  { name: 'أبها', country: 'المملكة العربية السعودية', code: 'AHB', coordinates: [18.2164, 42.5053] },
  { name: 'تبوك', country: 'المملكة العربية السعودية', code: 'TUU', coordinates: [28.3998, 36.5700] },

  // UAE
  { name: 'دبي', country: 'الإمارات العربية المتحدة', code: 'DXB', coordinates: [25.2048, 55.2708] },
  { name: 'أبوظبي', country: 'الإمارات العربية المتحدة', code: 'AUH', coordinates: [24.4539, 54.3773] },
  { name: 'الشارقة', country: 'الإمارات العربية المتحدة', code: 'SHJ', coordinates: [25.3463, 55.4209] },
  { name: 'عجمان', country: 'الإمارات العربية المتحدة', code: 'AJM', coordinates: [25.4052, 55.5136] },
  { name: 'رأس الخيمة', country: 'الإمارات العربية المتحدة', code: 'RKT', coordinates: [25.7897, 55.9432] },
  { name: 'الفجيرة', country: 'الإمارات العربية المتحدة', code: 'FJR', coordinates: [25.1288, 56.3264] },

  // Egypt
  { name: 'القاهرة', country: 'مصر', code: 'CAI', coordinates: [30.0444, 31.2357] },
  { name: 'الإسكندرية', country: 'مصر', code: 'ALY', coordinates: [31.2001, 29.9187] },
  { name: 'شرم الشيخ', country: 'مصر', code: 'SSH', coordinates: [27.9158, 34.3300] },
  { name: 'الغردقة', country: 'مصر', code: 'HRG', coordinates: [27.2574, 33.8129] },
  { name: 'الأقصر', country: 'مصر', code: 'LXR', coordinates: [25.6872, 32.6396] },
  { name: 'أسوان', country: 'مصر', code: 'ASW', coordinates: [24.0889, 32.8998] },

  // Other Arab Countries
  { name: 'بيروت', country: 'لبنان', code: 'BEY', coordinates: [33.8938, 35.5018] },
  { name: 'عمان', country: 'الأردن', code: 'AMM', coordinates: [31.9454, 35.9284] },
  { name: 'العقبة', country: 'الأردن', code: 'AQJ', coordinates: [29.5321, 35.0063] },
  { name: 'الدوحة', country: 'قطر', code: 'DOH', coordinates: [25.2854, 51.5310] },
  { name: 'المنامة', country: 'البحرين', code: 'BAH', coordinates: [26.0667, 50.5577] },
  { name: 'مسقط', country: 'عمان', code: 'MCT', coordinates: [23.5859, 58.4059] },
  { name: 'الكويت', country: 'الكويت', code: 'KWI', coordinates: [29.3117, 47.4818] },
  { name: 'دمشق', country: 'سوريا', code: 'DAM', coordinates: [33.5138, 36.2765] },
  { name: 'بغداد', country: 'العراق', code: 'BGW', coordinates: [33.3152, 44.3661] },
  { name: 'الرباط', country: 'المغرب', code: 'RBA', coordinates: [34.0209, -6.8416] },
  { name: 'الدار البيضاء', country: 'المغرب', code: 'CMN', coordinates: [33.5731, -7.5898] },
  { name: 'مراكش', country: 'المغرب', code: 'RAK', coordinates: [31.6295, -7.9811] },
  { name: 'تونس', country: 'تونس', code: 'TUN', coordinates: [36.8065, 10.1815] },
  { name: 'الجزائر', country: 'الجزائر', code: 'ALG', coordinates: [36.7538, 3.0588] },

  // International Popular Destinations
  { name: 'إسطنبول', country: 'تركيا', code: 'IST', coordinates: [41.0082, 28.9784] },
  { name: 'أنطاليا', country: 'تركيا', code: 'AYT', coordinates: [36.8969, 30.7133] },
  { name: 'بودروم', country: 'تركيا', code: 'BJV', coordinates: [37.0344, 27.4305] },
  { name: 'لندن', country: 'المملكة المتحدة', code: 'LON', coordinates: [51.5074, -0.1278] },
  { name: 'باريس', country: 'فرنسا', code: 'PAR', coordinates: [48.8566, 2.3522] },
  { name: 'روما', country: 'إيطاليا', code: 'ROM', coordinates: [41.9028, 12.4964] },
  { name: 'برشلونة', country: 'إسبانيا', code: 'BCN', coordinates: [41.3851, 2.1734] },
  { name: 'أمستردام', country: 'هولندا', code: 'AMS', coordinates: [52.3676, 4.9041] },
  { name: 'فيينا', country: 'النمسا', code: 'VIE', coordinates: [48.2082, 16.3738] },
  { name: 'براغ', country: 'التشيك', code: 'PRG', coordinates: [50.0755, 14.4378] },
  { name: 'بودابست', country: 'المجر', code: 'BUD', coordinates: [47.4979, 19.0402] },
  { name: 'نيويورك', country: 'الولايات المتحدة', code: 'NYC', coordinates: [40.7128, -74.0060] },
  { name: 'لوس أنجلوس', country: 'الولايات المتحدة', code: 'LAX', coordinates: [34.0522, -118.2437] },
  { name: 'ميامي', country: 'الولايات المتحدة', code: 'MIA', coordinates: [25.7617, -80.1918] },
  { name: 'طوكيو', country: 'اليابان', code: 'TYO', coordinates: [35.6762, 139.6503] },
  { name: 'سيول', country: 'كوريا الجنوبية', code: 'SEL', coordinates: [37.5665, 126.9780] },
  { name: 'بانكوك', country: 'تايلاند', code: 'BKK', coordinates: [13.7563, 100.5018] },
  { name: 'بوكيت', country: 'تايلاند', code: 'HKT', coordinates: [7.8804, 98.3923] },
  { name: 'كوالالمبور', country: 'ماليزيا', code: 'KUL', coordinates: [3.1390, 101.6869] },
  { name: 'سنغافورة', country: 'سنغافورة', code: 'SIN', coordinates: [1.3521, 103.8198] },
  { name: 'بالي', country: 'إندونيسيا', code: 'DPS', coordinates: [-8.3405, 115.0920] },
  { name: 'جاكرتا', country: 'إندونيسيا', code: 'JKT', coordinates: [-6.2088, 106.8456] },
  { name: 'مانيلا', country: 'الفلبين', code: 'MNL', coordinates: [14.5995, 120.9842] },
  { name: 'هانوي', country: 'فيتنام', code: 'HAN', coordinates: [21.0285, 105.8542] },
  { name: 'هو تشي مين', country: 'فيتنام', code: 'SGN', coordinates: [10.8231, 106.6297] },
  { name: 'سيدني', country: 'أستراليا', code: 'SYD', coordinates: [-33.8688, 151.2093] },
  { name: 'ملبورن', country: 'أستراليا', code: 'MEL', coordinates: [-37.8136, 144.9631] }
];

// RateHawk Integration Class
class RateHawkIntegration {
  constructor(config = {}) {
    this.config = { ...RATEHAWK_CONFIG, ...config };
    this.init();
  }

  init() {
    if (this.config.debug) {
      console.log('RateHawk Integration initialized:', this.config);
    }
    
    // Track page load
    analytics.track('page_view', {
      page: window.location.pathname,
      referrer: document.referrer
    });
  }

  // Generate RateHawk search URL
  generateSearchUrl(searchParams) {
    const {
      destination,
      checkin,
      checkout,
      guests = 2,
      rooms = 1,
      currency = 'SAR'
    } = searchParams;

    // Find city information
    const cityInfo = this.findCityInfo(destination);
    const cityName = cityInfo ? cityInfo.name : destination.split('،')[0].trim();

    const urlParams = new URLSearchParams({
      'destination': cityName,
      'checkin': checkin,
      'checkout': checkout,
      'guests': guests,
      'rooms': rooms,
      'currency': currency,
      'partner_id': this.config.partnerId,
      'utm_source': 'paygo',
      'utm_medium': 'search',
      'utm_campaign': 'hotel_search',
      'lang': 'ar'
    });

    return `${this.config.baseUrl}/search?${urlParams.toString()}`;
  }

  // Find city information from database
  findCityInfo(destination) {
    const searchTerm = destination.toLowerCase();
    return CITIES_DATABASE.find(city => 
      city.name.toLowerCase().includes(searchTerm) ||
      searchTerm.includes(city.name.toLowerCase())
    );
  }

  // Get city suggestions
  getCitySuggestions(query, limit = 8) {
    if (!query || query.length < 2) return [];

    const searchTerm = query.toLowerCase().trim();
    const suggestions = CITIES_DATABASE.filter(city => 
      city.name.toLowerCase().includes(searchTerm) ||
      city.country.toLowerCase().includes(searchTerm)
    ).slice(0, limit);

    return suggestions.map(city => ({
      display: `${city.name}، ${city.country}`,
      name: city.name,
      country: city.country,
      code: city.code,
      coordinates: city.coordinates
    }));
  }

  // Track search event
  trackSearch(searchParams) {
    analytics.track('hotel_search', {
      destination: searchParams.destination,
      checkin: searchParams.checkin,
      checkout: searchParams.checkout,
      guests: searchParams.guests,
      nights: this.calculateNights(searchParams.checkin, searchParams.checkout)
    });
  }

  // Track booking attempt
  trackBookingAttempt(hotelData, searchParams) {
    analytics.track('booking_attempt', {
      hotel_name: hotelData.name,
      hotel_id: hotelData.id,
      destination: searchParams.destination,
      price: hotelData.price,
      currency: hotelData.currency,
      checkin: searchParams.checkin,
      checkout: searchParams.checkout,
      guests: searchParams.guests
    });
  }

  // Calculate number of nights
  calculateNights(checkin, checkout) {
    const checkinDate = new Date(checkin);
    const checkoutDate = new Date(checkout);
    const timeDiff = checkoutDate.getTime() - checkinDate.getTime();
    return Math.ceil(timeDiff / (1000 * 3600 * 24));
  }

  // Validate search parameters
  validateSearchParams(params) {
    const errors = [];
    
    if (!params.destination || params.destination.trim().length < 2) {
      errors.push('يرجى إدخال وجهة صحيحة');
    }
    
    if (!params.checkin) {
      errors.push('يرجى تحديد تاريخ الوصول');
    }
    
    if (!params.checkout) {
      errors.push('يرجى تحديد تاريخ المغادرة');
    }
    
    if (params.checkin && params.checkout) {
      const checkinDate = new Date(params.checkin);
      const checkoutDate = new Date(params.checkout);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      if (checkinDate < today) {
        errors.push('تاريخ الوصول يجب أن يكون اليوم أو في المستقبل');
      }
      
      if (checkoutDate <= checkinDate) {
        errors.push('تاريخ المغادرة يجب أن يكون بعد تاريخ الوصول');
      }
      
      const nights = this.calculateNights(params.checkin, params.checkout);
      if (nights > 30) {
        errors.push('لا يمكن الحجز لأكثر من 30 ليلة');
      }
    }
    
    const guests = parseInt(params.guests);
    if (isNaN(guests) || guests < 1 || guests > 20) {
      errors.push('عدد الضيوف يجب أن يكون بين 1 و 20');
    }
    
    return {
      isValid: errors.length === 0,
      errors: errors
    };
  }

  // Format date for display
  formatDate(dateString, locale = 'ar-SA') {
    const date = new Date(dateString);
    return date.toLocaleDateString(locale, {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }

  // Format date range
  formatDateRange(checkin, checkout, locale = 'ar-SA') {
    const checkinDate = new Date(checkin);
    const checkoutDate = new Date(checkout);
    const options = { day: 'numeric', month: 'long' };
    
    const checkinFormatted = checkinDate.toLocaleDateString(locale, options);
    const checkoutFormatted = checkoutDate.toLocaleDateString(locale, options);
    
    return `${checkinFormatted} - ${checkoutFormatted} ${checkinDate.getFullYear()}`;
  }

  // Get analytics data
  getAnalytics() {
    return analytics.getSessionStats();
  }

  // Send conversion tracking
  trackConversion(conversionData) {
    analytics.track('conversion', {
      ...conversionData,
      conversion_time: Date.now(),
      partner: 'ratehawk'
    });
  }
}

// Initialize RateHawk Integration
const rateHawk = new RateHawkIntegration();

// Auto-suggestion functionality
class AutoSuggestion {
  constructor(inputElement, suggestionsElement) {
    this.input = inputElement;
    this.suggestions = suggestionsElement;
    this.selectedIndex = -1;
    this.currentSuggestions = [];
    
    this.init();
  }

  init() {
    this.input.addEventListener('input', this.handleInput.bind(this));
    this.input.addEventListener('keydown', this.handleKeydown.bind(this));
    this.input.addEventListener('focus', this.handleFocus.bind(this));
    
    // Hide suggestions when clicking outside
    document.addEventListener('click', (e) => {
      if (!this.input.contains(e.target) && !this.suggestions.contains(e.target)) {
        this.hideSuggestions();
      }
    });
  }

  handleInput(e) {
    const query = e.target.value.trim();
    
    if (query.length < 2) {
      this.hideSuggestions();
      return;
    }

    this.currentSuggestions = rateHawk.getCitySuggestions(query);
    this.showSuggestions();
    
    // Track search input
    analytics.track('search_input', {
      query: query,
      suggestions_count: this.currentSuggestions.length
    });
  }

  handleKeydown(e) {
    if (!this.isVisible()) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        this.selectedIndex = Math.min(this.selectedIndex + 1, this.currentSuggestions.length - 1);
        this.updateSelection();
        break;
      case 'ArrowUp':
        e.preventDefault();
        this.selectedIndex = Math.max(this.selectedIndex - 1, -1);
        this.updateSelection();
        break;
      case 'Enter':
        e.preventDefault();
        if (this.selectedIndex >= 0) {
          this.selectSuggestion(this.selectedIndex);
        }
        break;
      case 'Escape':
        this.hideSuggestions();
        break;
    }
  }

  handleFocus() {
    if (this.input.value.trim().length >= 2) {
      this.showSuggestions();
    }
  }

  showSuggestions() {
    if (this.currentSuggestions.length === 0) {
      this.hideSuggestions();
      return;
    }

    const suggestionsHTML = this.currentSuggestions.map((suggestion, index) => `
      <div class="suggestion-item ${index === this.selectedIndex ? 'selected' : ''}" 
           data-index="${index}"
           onclick="autoSuggestion.selectSuggestion(${index})">
        <i class="fas fa-map-marker-alt"></i>
        ${suggestion.display}
      </div>
    `).join('');

    this.suggestions.innerHTML = suggestionsHTML;
    this.suggestions.style.display = 'block';
  }

  hideSuggestions() {
    this.suggestions.style.display = 'none';
    this.selectedIndex = -1;
  }

  updateSelection() {
    const items = this.suggestions.querySelectorAll('.suggestion-item');
    items.forEach((item, index) => {
      item.classList.toggle('selected', index === this.selectedIndex);
    });
  }

  selectSuggestion(index) {
    if (index >= 0 && index < this.currentSuggestions.length) {
      const suggestion = this.currentSuggestions[index];
      this.input.value = suggestion.display;
      this.hideSuggestions();
      
      // Track suggestion selection
      analytics.track('suggestion_selected', {
        selected_city: suggestion.name,
        selected_country: suggestion.country,
        position: index
      });
    }
  }

  isVisible() {
    return this.suggestions.style.display === 'block';
  }
}

// Form validation and submission
class SearchForm {
  constructor(formElement) {
    this.form = formElement;
    this.init();
  }

  init() {
    this.form.addEventListener('submit', this.handleSubmit.bind(this));
    
    // Set default dates
    this.setDefaultDates();
  }

  setDefaultDates() {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    const dayAfter = new Date(today);
    dayAfter.setDate(dayAfter.getDate() + 2);

    const checkinInput = this.form.querySelector('#checkin');
    const checkoutInput = this.form.querySelector('#checkout');

    if (checkinInput && !checkinInput.value) {
      checkinInput.value = tomorrow.toISOString().split('T')[0];
    }
    
    if (checkoutInput && !checkoutInput.value) {
      checkoutInput.value = dayAfter.toISOString().split('T')[0];
    }
  }

  handleSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(this.form);
    const searchParams = {
      destination: formData.get('destination'),
      checkin: formData.get('checkin'),
      checkout: formData.get('checkout'),
      guests: formData.get('guests') || '2'
    };

    // Validate parameters
    const validation = rateHawk.validateSearchParams(searchParams);
    
    if (!validation.isValid) {
      this.showErrors(validation.errors);
      return;
    }

    // Track search
    rateHawk.trackSearch(searchParams);

    // Show loading state
    this.showLoading();

    // Simulate loading time and redirect to results
    setTimeout(() => {
      this.redirectToResults(searchParams);
    }, 2000);
  }

  showErrors(errors) {
    // Remove existing error messages
    this.form.querySelectorAll('.error-message').forEach(el => el.remove());
    
    errors.forEach(error => {
      const errorDiv = document.createElement('div');
      errorDiv.className = 'error-message';
      errorDiv.style.cssText = `
        color: #e74c3c;
        background: #fdf2f2;
        border: 1px solid #f5c6cb;
        padding: 10px;
        border-radius: 4px;
        margin: 10px 0;
        font-size: 0.9rem;
      `;
      errorDiv.textContent = error;
      this.form.appendChild(errorDiv);
    });

    // Track validation errors
    analytics.track('form_validation_error', {
      errors: errors
    });
  }

  showLoading() {
    const loadingElement = document.getElementById('loading');
    const successElement = document.getElementById('successMessage');
    
    if (loadingElement) {
      loadingElement.style.display = 'block';
    }
    
    setTimeout(() => {
      if (loadingElement) {
        loadingElement.style.display = 'none';
      }
      if (successElement) {
        successElement.style.display = 'block';
      }
    }, 1500);
  }

  redirectToResults(searchParams) {
    const urlParams = new URLSearchParams(searchParams);
    window.location.href = `results.html?${urlParams.toString()}`;
  }
}

// Utility functions
const PaygoUtils = {
  // Format currency
  formatCurrency(amount, currency = 'SAR', locale = 'ar-SA') {
    return new Intl.NumberFormat(locale, {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  },

  // Format number
  formatNumber(number, locale = 'ar-SA') {
    return new Intl.NumberFormat(locale).format(number);
  },

  // Debounce function
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  // Get device type
  getDeviceType() {
    const width = window.innerWidth;
    if (width < 768) return 'mobile';
    if (width < 1024) return 'tablet';
    return 'desktop';
  },

  // Check if user is on mobile
  isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  }
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Initialize auto-suggestions if elements exist
  const destinationInput = document.getElementById('destination');
  const suggestionsDiv = document.getElementById('suggestions');
  
  if (destinationInput && suggestionsDiv) {
    window.autoSuggestion = new AutoSuggestion(destinationInput, suggestionsDiv);
  }

  // Initialize search form if it exists
  const searchForm = document.getElementById('hotelSearchForm');
  if (searchForm) {
    window.searchForm = new SearchForm(searchForm);
  }

  // Track device and browser info
  analytics.track('session_start', {
    device_type: PaygoUtils.getDeviceType(),
    is_mobile: PaygoUtils.isMobile(),
    screen_resolution: `${screen.width}x${screen.height}`,
    viewport_size: `${window.innerWidth}x${window.innerHeight}`,
    language: navigator.language,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
  });
});

// Export for global access
window.RateHawkIntegration = RateHawkIntegration;
window.PaygoAnalytics = PaygoAnalytics;
window.PaygoUtils = PaygoUtils;
window.rateHawk = rateHawk;
window.analytics = analytics;

// Global functions for backward compatibility
window.selectDestination = function(city) {
  if (window.autoSuggestion) {
    const input = document.getElementById('destination');
    if (input) {
      input.value = city;
      window.autoSuggestion.hideSuggestions();
    }
  }
};

window.searchDestination = function(city) {
  const input = document.getElementById('destination');
  if (input) {
    input.value = city;
    input.scrollIntoView({ behavior: 'smooth' });
    
    // Track popular destination click
    analytics.track('popular_destination_click', {
      destination: city
    });
  }
};

// Performance monitoring
window.addEventListener('load', function() {
  // Track page load performance
  setTimeout(() => {
    const perfData = performance.getEntriesByType('navigation')[0];
    if (perfData) {
      analytics.track('page_performance', {
        load_time: perfData.loadEventEnd - perfData.loadEventStart,
        dom_content_loaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
        first_paint: performance.getEntriesByType('paint').find(entry => entry.name === 'first-paint')?.startTime || 0,
        first_contentful_paint: performance.getEntriesByType('paint').find(entry => entry.name === 'first-contentful-paint')?.startTime || 0
      });
    }
  }, 1000);
});

// Error tracking
window.addEventListener('error', function(e) {
  analytics.track('javascript_error', {
    message: e.message,
    filename: e.filename,
    line: e.lineno,
    column: e.colno,
    stack: e.error?.stack
  });
});

// Unload tracking
window.addEventListener('beforeunload', function() {
  analytics.track('session_end', {
    session_duration: Date.now() - analytics.startTime,
    page_views: analytics.events.filter(e => e.event === 'page_view').length,
    searches: analytics.events.filter(e => e.event === 'hotel_search').length,
    bookings: analytics.events.filter(e => e.event === 'booking_attempt').length
  });
});

