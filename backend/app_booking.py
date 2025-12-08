#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paygo Booking.com Backend v2.0
تطبيق Flask للتكامل مع Booking.com API من RapidAPI
تم تحديثه ليستخدم endpoints الصحيحة: /stays/auto-complete و /stays/search
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import logging
from datetime import datetime

# إعداد التطبيق
app = Flask(__name__)
CORS(app)

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# إعدادات Booking.com API
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', 'ed731333c1mshea92aa884b20792p16f38ajsn52efc429d7bc')
RAPIDAPI_HOST = 'booking-com18.p.rapidapi.com'
RAPIDAPI_BASE_URL = f'https://{RAPIDAPI_HOST}'

class BookingAPI:
    """فئة للتعامل مع Booking.com API"""
    
    def __init__(self):
        self.headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': RAPIDAPI_HOST
        }
    
    def search_locations(self, query, language_code='ar'):
        """البحث عن المواقع والمدن باستخدام stays/auto-complete"""
        try:
            url = f"{RAPIDAPI_BASE_URL}/stays/auto-complete"
            params = {
                'query': query,
                'languageCode': language_code
            }
            
            logger.info(f"🔍 البحث عن الموقع: {query}")
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # تنسيق البيانات
            locations = []
            if 'data' in data:
                for item in data['data']:
                    locations.append({
                        'dest_id': item.get('id', ''),
                        'dest_type': item.get('dest_type', ''),
                        'name': item.get('name', ''),
                        'city_name': item.get('city_name', ''),
                        'country': item.get('country', ''),
                        'region': item.get('region', ''),
                        'label': item.get('label', ''),
                        'latitude': item.get('latitude'),
                        'longitude': item.get('longitude')
                    })
            
            logger.info(f"✅ تم العثور على {len(locations)} موقع")
            
            return {
                'success': True,
                'data': locations
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ خطأ في البحث عن الموقع: {e}")
            return {
                'success': False,
                'error': str(e),
                'data': []
            }
    
    def search_hotels(self, location_id, arrival_date, departure_date, adults=2, 
                     room_qty=1, page_number=1, sort_by='popularity', 
                     units='metric', temperature_unit='c', language_code='ar', 
                     currency_code='SAR'):
        """البحث عن الفنادق باستخدام stays/search"""
        try:
            url = f"{RAPIDAPI_BASE_URL}/stays/search"
            params = {
                'locationId': location_id,
                'checkIn': arrival_date,
                'checkOut': departure_date,
                'adults': str(adults),
                'rooms': str(room_qty),
                'page_number': str(page_number),
                'sort_by': sort_by,
                'units': units,
                'temperature_unit': temperature_unit,
                'languagecode': language_code,
                'currency_code': currency_code
            }
            
            logger.info(f"🏨 البحث عن الفنادق في {location_id} من {arrival_date} إلى {departure_date}")
            response = requests.get(url, headers=self.headers, params=params, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            
            # معالجة البيانات
            hotels = []
            if 'data' in data and 'result' in data['data']:
                for hotel in data['data']['result']:
                    try:
                        # معلومات أساسية
                        hotel_id = hotel.get('hotel_id', '')
                        property_data = hotel.get('property', {})
                        
                        # الاسم
                        hotel_name = property_data.get('name', hotel.get('hotel_name', 'فندق'))
                        
                        # الصور
                        images = []
                        if 'photoUrls' in property_data:
                            images = property_data['photoUrls']
                        elif 'max_photo_url' in hotel:
                            images = [hotel['max_photo_url']]
                        
                        # السعر
                        price_breakdown = hotel.get('composite_price_breakdown', {})
                        gross_amount = price_breakdown.get('gross_amount_per_night', {})
                        price = gross_amount.get('value', 0)
                        currency = gross_amount.get('currency', currency_code)
                        
                        # التقييم
                        review_score = hotel.get('review_score', 0)
                        review_count = hotel.get('review_nr', 0)
                        review_word = hotel.get('review_score_word', '')
                        
                        # الموقع
                        city = hotel.get('city', '')
                        address = hotel.get('address', '')
                        distance = hotel.get('distance', '')
                        
                        # المرافق
                        amenities = []
                        if 'property' in hotel and 'facilities' in hotel['property']:
                            amenities = [f.get('name', '') for f in hotel['property']['facilities'][:10]]
                        
                        # النجوم
                        stars = hotel.get('class', 0)
                        
                        # بناء كائن الفندق
                        processed_hotel = {
                            'id': hotel_id,
                            'name': hotel_name,
                            'location': city,
                            'address': address,
                            'price': price,
                            'currency': currency,
                            'rating': review_score,
                            'reviews': review_count,
                            'review_word': review_word,
                            'stars': stars,
                            'images': images,
                            'amenities': amenities,
                            'distance_from_center': distance,
                            'latitude': hotel.get('latitude'),
                            'longitude': hotel.get('longitude'),
                            'is_free_cancellable': hotel.get('is_free_cancellable', 0),
                            'booking_url': f"https://www.booking.com/hotel/{hotel.get('cc1', 'ae')}/{hotel_id}.html"
                        }
                        
                        hotels.append(processed_hotel)
                        
                    except Exception as e:
                        logger.warning(f"⚠️ خطأ في معالجة فندق: {e}")
                        continue
            
            logger.info(f"✅ تم العثور على {len(hotels)} فندق")
            
            return {
                'success': True,
                'data': hotels,
                'total': len(hotels)
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ خطأ في البحث عن الفنادق: {e}")
            return {
                'success': False,
                'error': str(e),
                'data': []
            }
    
    def get_hotel_details(self, hotel_id, arrival_date, departure_date, 
                         adults=2, room_qty=1, language_code='ar', currency_code='SAR'):
        """الحصول على تفاصيل فندق محدد"""
        try:
            url = f"{RAPIDAPI_BASE_URL}/stays/detail"
            params = {
                'hotel_id': hotel_id,
                'arrival_date': arrival_date,
                'departure_date': departure_date,
                'adults': str(adults),
                'room_qty': str(room_qty),
                'languagecode': language_code,
                'currency_code': currency_code
            }
            
            logger.info(f"📋 الحصول على تفاصيل الفندق: {hotel_id}")
            response = requests.get(url, headers=self.headers, params=params, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'success': True,
                'data': data.get('data', {})
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ خطأ في الحصول على تفاصيل الفندق: {e}")
            return {
                'success': False,
                'error': str(e),
                'data': {}
            }

# إنشاء كائن Booking API
booking_api = BookingAPI()

@app.route('/')
def home():
    """الصفحة الرئيسية للـ API"""
    return jsonify({
        'message': 'Paygo Booking.com Backend API',
        'version': '2.0.0',
        'status': 'running',
        'api_provider': 'Booking.com via RapidAPI',
        'endpoints': {
            'search_locations': '/api/locations/search?query=Dubai',
            'search_hotels': '/api/hotels/search?dest_id=XXX&checkin=2025-12-09&checkout=2025-12-10&adults=2',
            'hotel_details': '/api/hotels/details?hotel_id=XXX&checkin=2025-12-09&checkout=2025-12-10',
            'health_check': '/api/health'
        }
    })

@app.route('/api/health')
def health_check():
    """فحص صحة النظام"""
    try:
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'api_key_configured': bool(RAPIDAPI_KEY),
            'version': '2.0.0'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 500

@app.route('/api/locations/search', methods=['GET'])
def search_locations():
    """البحث عن المواقع والمدن"""
    try:
        query = request.args.get('query', '')
        language_code = request.args.get('languageCode', 'ar')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'معامل البحث query مطلوب',
                'data': []
            }), 400
        
        result = booking_api.search_locations(query, language_code)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ خطأ في endpoint البحث عن الموقع: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'data': []
        }), 500

@app.route('/api/hotels/search', methods=['GET'])
def search_hotels():
    """البحث عن الفنادق"""
    try:
        # الحصول على المعاملات (دعم كل من dest_id و locationId)
        location_id = request.args.get('dest_id') or request.args.get('locationId')
        arrival_date = request.args.get('checkin') or request.args.get('arrival_date')
        departure_date = request.args.get('checkout') or request.args.get('departure_date')
        adults = int(request.args.get('adults', 2))
        room_qty = int(request.args.get('room_qty', 1))
        page_number = int(request.args.get('page_number', 1))
        sort_by = request.args.get('sort_by', 'popularity')
        units = request.args.get('units', 'metric')
        temperature_unit = request.args.get('temperature_unit', 'c')
        language_code = request.args.get('languagecode', 'ar')
        currency_code = request.args.get('currency_code', 'SAR')
        
        # التحقق من المعاملات المطلوبة
        if not location_id:
            return jsonify({
                'success': False,
                'error': 'معامل dest_id أو locationId مطلوب',
                'data': []
            }), 400
            
        if not arrival_date or not departure_date:
            return jsonify({
                'success': False,
                'error': 'معاملات checkin و checkout مطلوبة',
                'data': []
            }), 400
        
        # البحث عن الفنادق
        result = booking_api.search_hotels(
            location_id=location_id,
            arrival_date=arrival_date,
            departure_date=departure_date,
            adults=adults,
            room_qty=room_qty,
            page_number=page_number,
            sort_by=sort_by,
            units=units,
            temperature_unit=temperature_unit,
            language_code=language_code,
            currency_code=currency_code
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ خطأ في endpoint البحث عن الفنادق: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'data': []
        }), 500

@app.route('/api/hotels/details', methods=['GET'])
def get_hotel_details():
    """الحصول على تفاصيل فندق محدد"""
    try:
        hotel_id = request.args.get('hotel_id')
        arrival_date = request.args.get('checkin') or request.args.get('arrival_date')
        departure_date = request.args.get('checkout') or request.args.get('departure_date')
        adults = int(request.args.get('adults', 2))
        room_qty = int(request.args.get('room_qty', 1))
        language_code = request.args.get('languagecode', 'ar')
        currency_code = request.args.get('currency_code', 'SAR')
        
        if not hotel_id:
            return jsonify({
                'success': False,
                'error': 'معامل hotel_id مطلوب'
            }), 400
            
        if not arrival_date or not departure_date:
            return jsonify({
                'success': False,
                'error': 'معاملات checkin و checkout مطلوبة'
            }), 400
        
        result = booking_api.get_hotel_details(
            hotel_id=hotel_id,
            arrival_date=arrival_date,
            departure_date=departure_date,
            adults=adults,
            room_qty=room_qty,
            language_code=language_code,
            currency_code=currency_code
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ خطأ في endpoint تفاصيل الفندق: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """معالج الأخطاء 404"""
    return jsonify({
        'success': False,
        'error': 'الصفحة غير موجودة'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """معالج الأخطاء 500"""
    return jsonify({
        'success': False,
        'error': 'خطأ داخلي في الخادم'
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🚀 بدء تشغيل Paygo Booking.com Backend v2.0 على المنفذ {port}")
    logger.info(f"🔑 مفتاح API مكون: {bool(RAPIDAPI_KEY)}")
    logger.info(f"📡 استخدام endpoints الجديدة: /stays/auto-complete و /stays/search")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
