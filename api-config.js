// تكوين API
// للحصول على مفتاح API مجاني:
// 1. سجل في https://rapidapi.com
// 2. اشترك في Booking.com API
// 3. انسخ مفتاح API الخاص بك وضعه هنا

const API_CONFIG = {
    // ضع مفتاح RapidAPI الخاص بك هنا
    RAPIDAPI_KEY: 'YOUR_RAPIDAPI_KEY_HERE',
    RAPIDAPI_HOST: 'booking-com.p.rapidapi.com',
    
    // إعدادات Google Maps (اختياري)
    GOOGLE_MAPS_KEY: 'YOUR_GOOGLE_MAPS_KEY_HERE'
};

// دالة للتحقق من وجود مفتاح API
function isAPIConfigured() {
    return API_CONFIG.RAPIDAPI_KEY && API_CONFIG.RAPIDAPI_KEY !== 'YOUR_RAPIDAPI_KEY_HERE';
}

// تصدير التكوين
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API_CONFIG;
}
