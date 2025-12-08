// تكوين API للموقع
const API_CONFIG = {
    // رابط Backend - سيتم تحديثه بعد النشر على Render
    BACKEND_URL: 'http://localhost:5000',  // للتطوير المحلي
    // BACKEND_URL: 'https://paygo-booking-api.onrender.com',  // للإنتاج
    
    // إعدادات الطلبات
    TIMEOUT: 30000,  // 30 ثانية
    
    // العملة الافتراضية
    DEFAULT_CURRENCY: 'SAR',
    
    // اللغة الافتراضية
    DEFAULT_LANGUAGE: 'ar',
    
    // معرفات المدن الشهيرة
    CITY_IDS: {
        'DXB': '-782831',  // دبي
        'AUH': '-782832',  // أبوظبي
        'RUH': '-782833',  // الرياض
        'JED': '-782834',  // جدة
        'CAI': '-782835',  // القاهرة
        'IST': '-782836',  // إسطنبول
        'LON': '-782837',  // لندن
        'PAR': '-782838',  // باريس
        'NYC': '-782839',  // نيويورك
        'TYO': '-782840'   // طوكيو
    }
};

// دالة للحصول على رابط API الكامل
function getApiUrl(endpoint) {
    return `${API_CONFIG.BACKEND_URL}${endpoint}`;
}

// دالة لإرسال طلب GET
async function apiGet(endpoint, params = {}) {
    try {
        const url = new URL(getApiUrl(endpoint));
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            timeout: API_CONFIG.TIMEOUT
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API GET Error:', error);
        throw error;
    }
}

// دالة لإرسال طلب POST
async function apiPost(endpoint, data = {}) {
    try {
        const response = await fetch(getApiUrl(endpoint), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
            timeout: API_CONFIG.TIMEOUT
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API POST Error:', error);
        throw error;
    }
}

// دوال API محددة

// البحث عن المواقع
async function searchLocations(query) {
    return await apiGet('/api/locations/search', { query });
}

// البحث عن الفنادق
async function searchHotels(destId, checkin, checkout, adults = 2, rooms = 1) {
    return await apiPost('/api/hotels/search', {
        dest_id: destId,
        checkin,
        checkout,
        adults,
        rooms,
        currency: API_CONFIG.DEFAULT_CURRENCY
    });
}

// الحصول على تفاصيل الفندق
async function getHotelDetails(hotelId, checkin, checkout, adults = 2, rooms = 1) {
    return await apiGet('/api/hotels/details', {
        hotel_id: hotelId,
        checkin,
        checkout,
        adults,
        rooms,
        currency: API_CONFIG.DEFAULT_CURRENCY
    });
}

// الحصول على مراجعات الفندق
async function getHotelReviews(hotelId) {
    return await apiGet('/api/hotels/reviews', {
        hotel_id: hotelId,
        languagecode: API_CONFIG.DEFAULT_LANGUAGE
    });
}

// فحص صحة API
async function checkApiHealth() {
    try {
        const response = await apiGet('/api/health');
        return response.status === 'healthy';
    } catch (error) {
        return false;
    }
}
