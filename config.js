// TravelPayouts Configuration
const CONFIG = {
    // Backend API URL
    BACKEND_URL: 'https://tourism-website-tyis.onrender.com',
    
    // Default search parameters
    DEFAULT_CURRENCY: 'SAR',
    DEFAULT_LANGUAGE: 'ar'
};

// دالة البحث عن الفنادق باستخدام Backend
async function searchHotels(locationQuery, checkin, checkout, adults = 2) {
    try {
        const url = `${CONFIG.BACKEND_URL}/api/search/hotels?location=${encodeURIComponent(locationQuery)}&checkin=${checkin}&checkout=${checkout}&adults=${adults}`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        return data;
        
    } catch (error) {
        console.error('خطأ في البحث:', error);
        return {
            success: false,
            error: error.message,
            hotels: []
        };
    }
}

// دالة لإنشاء رابط Booking.com
function generateBookingUrl(hotelId, hotelName, cityName, checkin, checkout, adults) {
    const params = new URLSearchParams({
        ss: cityName, // البحث بالمدينة
        checkin: checkin,
        checkout: checkout,
        group_adults: adults,
        no_rooms: 1,
        selected_currency: CONFIG.DEFAULT_CURRENCY
    });
    
    // إذا كان لدينا Affiliate ID، نضيفه
    if (CONFIG.BOOKING_AFFILIATE_ID) {
        params.append('aid', CONFIG.BOOKING_AFFILIATE_ID);
    }
    
    return `https://www.booking.com/searchresults.html?${params.toString()}`;
}

// دالة للبحث عن المدن باستخدام Backend
async function searchCities(query) {
    try {
        const url = `${CONFIG.BACKEND_URL}/api/search/cities?query=${encodeURIComponent(query)}`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success && data.data) {
            return data.data;
        }
        
        return [];
        
    } catch (error) {
        console.error('خطأ في البحث عن المدن:', error);
        return [];
    }
}
