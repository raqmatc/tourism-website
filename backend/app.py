from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # السماح بجميع الطلبات من أي مصدر

# TravelPayouts Configuration
TRAVELPAYOUTS_TOKEN = '0c99883bf40eab32e39bcf9ddd7dc518'
TRAVELPAYOUTS_MARKER = '690121'

# Booking.com Affiliate ID (سيتم تحديثه بعد الموافقة)
BOOKING_AFFILIATE_ID = None

@app.route('/')
def home():
    return jsonify({
        'status': 'healthy',
        'service': 'TravelPayouts Proxy API',
        'version': '1.0.0'
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/api/search/cities', methods=['GET'])
def search_cities():
    """البحث عن المدن باستخدام TravelPayouts API"""
    try:
        query = request.args.get('query', '')
        
        if not query or len(query) < 2:
            return jsonify({
                'success': False,
                'error': 'Query must be at least 2 characters'
            }), 400
        
        # استدعاء TravelPayouts API
        url = f'https://engine.hotellook.com/api/v2/lookup.json'
        params = {
            'query': query,
            'lang': 'ar',
            'lookFor': 'city',
            'limit': 10,
            'token': TRAVELPAYOUTS_TOKEN
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if 'results' in data and 'locations' in data['results']:
            cities = []
            for loc in data['results']['locations']:
                cities.append({
                    'id': loc.get('id'),
                    'name': loc.get('fullName') or loc.get('name'),
                    'country': loc.get('countryName', '')
                })
            
            return jsonify({
                'success': True,
                'data': cities
            })
        else:
            return jsonify({
                'success': True,
                'data': []
            })
            
    except Exception as e:
        print(f'Error in search_cities: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/search/hotels', methods=['GET'])
def search_hotels():
    """البحث عن الفنادق باستخدام TravelPayouts API"""
    try:
        location = request.args.get('location', '')
        checkin = request.args.get('checkin', '')
        checkout = request.args.get('checkout', '')
        adults = request.args.get('adults', 2)
        
        if not location or not checkin or not checkout:
            return jsonify({
                'success': False,
                'error': 'Missing required parameters'
            }), 400
        
        # البحث عن الموقع أولاً
        lookup_url = 'https://engine.hotellook.com/api/v2/lookup.json'
        lookup_params = {
            'query': location,
            'lang': 'ar',
            'lookFor': 'both',
            'limit': 1,
            'token': TRAVELPAYOUTS_TOKEN
        }
        
        lookup_response = requests.get(lookup_url, params=lookup_params, timeout=10)
        lookup_data = lookup_response.json()
        
        if not lookup_data.get('results') or not lookup_data['results'].get('hotels'):
            return jsonify({
                'success': False,
                'error': 'Location not found'
            }), 404
        
        # الحصول على معرف المدينة
        location_data = lookup_data['results']['hotels'][0].get('location') or lookup_data['results'].get('locations', [{}])[0]
        city_id = location_data.get('id')
        city_name = location_data.get('name', location)
        
        # الحصول على بيانات الفنادق من Cache
        hotels_url = 'https://yasen.hotellook.com/tp/public/widget_location_dump.json'
        hotels_params = {
            'cityId': city_id,
            'language': 'ar'
        }
        
        hotels_response = requests.get(hotels_url, params=hotels_params, timeout=15)
        hotels_data = hotels_response.json()
        
        # تحويل البيانات إلى قائمة
        hotels = []
        for hotel_id, hotel in list(hotels_data.items())[:50]:  # أول 50 فندق
            # إنشاء رابط Booking.com
            booking_url = generate_booking_url(
                hotel_id=hotel_id,
                hotel_name=hotel.get('name', hotel.get('label', '')),
                city_name=city_name,
                checkin=checkin,
                checkout=checkout,
                adults=adults
            )
            
            hotels.append({
                'id': hotel_id,
                'name': hotel.get('name') or hotel.get('label', 'فندق'),
                'location': hotel.get('location', {}).get('name', city_name),
                'stars': hotel.get('stars', 0),
                'rating': hotel.get('rating', 0),
                'price': 500,  # سعر تقريبي - سيتم تحديثه لاحقاً
                'currency': 'SAR',
                'image': f"https://photo.hotellook.com/image_v2/limit/{hotel_id}/800/520.auto" if hotel.get('photoCount', 0) > 0 else 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
                'bookingUrl': booking_url
            })
        
        return jsonify({
            'success': True,
            'hotels': hotels,
            'total': len(hotels)
        })
        
    except Exception as e:
        print(f'Error in search_hotels: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def generate_booking_url(hotel_id, hotel_name, city_name, checkin, checkout, adults):
    """إنشاء رابط Booking.com"""
    from urllib.parse import urlencode
    
    params = {
        'ss': city_name,
        'checkin': checkin,
        'checkout': checkout,
        'group_adults': adults,
        'no_rooms': 1,
        'selected_currency': 'SAR'
    }
    
    # إضافة Affiliate ID إذا كان متاحاً
    if BOOKING_AFFILIATE_ID:
        params['aid'] = BOOKING_AFFILIATE_ID
    
    return f"https://www.booking.com/searchresults.html?{urlencode(params)}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
