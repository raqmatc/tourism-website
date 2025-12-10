// TravelPayouts Configuration
const CONFIG = {
    // TravelPayouts API Token
    TRAVELPAYOUTS_TOKEN: '0c99883bf40eab32e39bcf9ddd7dc518',
    TRAVELPAYOUTS_MARKER: '690121', // Your User ID
    
    // Booking.com Affiliate ID (سيتم تحديثه بعد الموافقة)
    BOOKING_AFFILIATE_ID: null, // سيتم إضافته بعد الموافقة
    
    // API Endpoints
    HOTELS_SEARCH_API: 'https://engine.hotellook.com/api/v2/lookup.json',
    HOTELS_CACHE_API: 'https://yasen.hotellook.com/tp/public/widget_location_dump.json',
    
    // Default search parameters
    DEFAULT_CURRENCY: 'SAR',
    DEFAULT_LANGUAGE: 'ar',
    DEFAULT_LIMIT: 50
};

// دالة البحث عن الفنادق باستخدام TravelPayouts
async function searchHotels(locationQuery, checkin, checkout, adults = 2) {
    try {
        // البحث عن الموقع أولاً
        const locationUrl = `${CONFIG.HOTELS_SEARCH_API}?query=${encodeURIComponent(locationQuery)}&lang=${CONFIG.DEFAULT_LANGUAGE}&lookFor=both&limit=1&token=${CONFIG.TRAVELPAYOUTS_TOKEN}`;
        
        const locationResponse = await fetch(locationUrl);
        const locationData = await locationResponse.json();
        
        if (!locationData.results || !locationData.results.hotels || locationData.results.hotels.length === 0) {
            throw new Error('لم يتم العثور على نتائج للموقع المحدد');
        }
        
        // الحصول على بيانات الفنادق من Cache
        const location = locationData.results.hotels[0].location || locationData.results.locations[0];
        const cityId = location.id;
        
        const hotelsUrl = `${CONFIG.HOTELS_CACHE_API}?cityId=${cityId}&language=${CONFIG.DEFAULT_LANGUAGE}`;
        
        const hotelsResponse = await fetch(hotelsUrl);
        const hotelsData = await hotelsResponse.json();
        
        // تحويل البيانات إلى صيغة موحدة
        const hotels = Object.values(hotelsData).slice(0, CONFIG.DEFAULT_LIMIT).map(hotel => {
            return {
                id: hotel.id,
                name: hotel.name || hotel.label,
                location: hotel.location?.name || location.name,
                stars: hotel.stars || 0,
                rating: hotel.rating || 0,
                price: Math.round(Math.random() * 1000 + 200), // سعر تقريبي
                currency: CONFIG.DEFAULT_CURRENCY,
                image: hotel.photoCount > 0 
                    ? `https://photo.hotellook.com/image_v2/limit/${hotel.id}/800/520.auto`
                    : 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
                bookingUrl: generateBookingUrl(hotel.id, hotel.name, location.name, checkin, checkout, adults)
            };
        });
        
        return {
            success: true,
            hotels: hotels,
            total: hotels.length
        };
        
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

// دالة للبحث عن المدن
async function searchCities(query) {
    try {
        const url = `${CONFIG.HOTELS_SEARCH_API}?query=${encodeURIComponent(query)}&lang=${CONFIG.DEFAULT_LANGUAGE}&lookFor=city&limit=10&token=${CONFIG.TRAVELPAYOUTS_TOKEN}`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (!data.results || !data.results.locations) {
            return [];
        }
        
        return data.results.locations.map(city => ({
            id: city.id,
            name: city.fullName || city.name,
            country: city.countryName
        }));
        
    } catch (error) {
        console.error('خطأ في البحث عن المدن:', error);
        return [];
    }
}
