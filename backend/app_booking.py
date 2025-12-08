#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paygo Booking.com Backend
تطبيق Flask للتكامل مع Booking.com API من RapidAPI
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import json
from datetime import datetime, timedelta
import logging
from functools import wraps

# إعداد التطبيق
app = Flask(__name__)
CORS(app)  # تمكين CORS للتطبيقات الأمامية

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
    
    def search_locations(self, query):
        """البحث عن المواقع والمدن"""
        try:
            url = f"{RAPIDAPI_BASE_URL}/locations/auto-complete"
            params = {
                'text': query,
                'languagecode': 'ar'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"تم البحث عن الموقع: {query}")
            
            return {
                'success': True,
                'data': data.get('data', [])
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"خطأ في البحث عن الموقع: {e}")
            return {
                'success': False,
                'error': str(e),
                'data': []
            }
    
    def search_hotels(self, dest_id, checkin, checkout, adults=2, rooms=1, currency='SAR'):
        """البحث عن الفنادق في وجهة محددة"""
        try:
            url = f"{RAPIDAPI_BASE_URL}/hotels/search"
            params = {
                'dest_id': dest_id,
                'search_type': 'CITY',
                'arrival_date': checkin,
                'departure_date': checkout,
                'adults': adults,
                'room_qty': rooms,
                'units': 'metric',
                'temperature_unit': 'c',
                'languagecode': 'ar',
                'currency_code': currency
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            hotels = data.get('data', {}).get('hotels', [])
            
            logger.info(f"تم البحث عن الفنادق في {dest_id}: {len(hotels)} نتيجة")
            
            # معالجة البيانات لتكون أكثر وضوحاً
            processed_hotels = []
            for hotel in hotels:
                try:
                    processed_hotel = {
                        'id': hotel.get('hotel_id'),
                        'name': hotel.get('hotel_name', 'فندق'),
                        'name_trans': hotel.get('hotel_name_trans', hotel.get('hotel_name', 'فندق')),
                        'address': hotel.get('address', ''),
                        'address_trans': hotel.get('address_trans', hotel.get('address', '')),
                        'city': hotel.get('city', ''),
                        'city_trans': hotel.get('city_trans', hotel.get('city', '')),
                        'country': hotel.get('country_trans', ''),
                        'latitude': hotel.get('latitude'),
                        'longitude': hotel.get('longitude'),
                        'rating': hotel.get('class', 0),
                        'review_score': hotel.get('review_score', 0),
                        'review_score_word': hotel.get('review_score_word', ''),
                        'review_count': hotel.get('review_nr', 0),
                        'image': hotel.get('main_photo_url', ''),
                        'price': hotel.get('min_total_price', 0),
                        'currency': hotel.get('currency_code', currency),
                        'distance': hotel.get('distance', 0),
                        'distance_to_cc': hotel.get('distance_to_cc', 0),
                        'url': hotel.get('url', ''),
                        'checkin': hotel.get('checkin', {}),
                        'checkout': hotel.get('checkout', {}),
                        'facilities': hotel.get('hotel_facilities', []),
                        'is_free_cancellable': hotel.get('is_free_cancellable', 0),
                        'is_genius_deal': hotel.get('is_genius_deal', 0)
                    }
                    processed_hotels.append(processed_hotel)
                except Exception as e:
                    logger.warning(f"خطأ في معالجة فندق: {e}")
                    continue
            
            return {
                'success': True,
                'data': processed_hotels,
                'total_results': len(processed_hotels),
                'search_params': {
                    'dest_id': dest_id,
                    'checkin': checkin,
                    'checkout': checkout,
                    'adults': adults,
                    'rooms': rooms
                }
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"خطأ في البحث عن الفنادق: {e}")
            return {
                'success': False,
                'error': str(e),
                'data': []
            }
    
    def get_hotel_details(self, hotel_id, checkin, checkout, adults=2, rooms=1, currency='SAR'):
        """الحصول على تفاصيل فندق محدد"""
        try:
            url = f"{RAPIDAPI_BASE_URL}/hotels/details"
            params = {
                'hotel_id': hotel_id,
                'arrival_date': checkin,
                'departure_date': checkout,
                'adults': adults,
                'room_qty': rooms,
                'units': 'metric',
                'temperature_unit': 'c',
                'languagecode': 'ar',
                'currency_code': currency
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            hotel_data = data.get('data', {})
            
            logger.info(f"تم الحصول على تفاصيل الفندق: {hotel_id}")
            
            # معالجة التفاصيل
            processed_data = {
                'id': hotel_data.get('hotel_id'),
                'name': hotel_data.get('hotel_name', ''),
                'description': hotel_data.get('hotel_description', ''),
                'address': hotel_data.get('address', ''),
                'city': hotel_data.get('city', ''),
                'country': hotel_data.get('country_trans', ''),
                'latitude': hotel_data.get('latitude'),
                'longitude': hotel_data.get('longitude'),
                'rating': hotel_data.get('class', 0),
                'review_score': hotel_data.get('review_score', 0),
                'review_score_word': hotel_data.get('review_score_word', ''),
                'review_count': hotel_data.get('review_nr', 0),
                'images': hotel_data.get('hotel_photos', []),
                'facilities': hotel_data.get('hotel_facilities', []),
                'rooms': hotel_data.get('rooms', []),
                'policies': hotel_data.get('hotel_policies', {}),
                'checkin': hotel_data.get('checkin', {}),
                'checkout': hotel_data.get('checkout', {}),
                'url': hotel_data.get('url', '')
            }
            
            return {
                'success': True,
                'data': processed_data
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"خطأ في الحصول على تفاصيل الفندق: {e}")
            return {
                'success': False,
                'error': str(e),
                'data': {}
            }
    
    def get_hotel_reviews(self, hotel_id, languagecode='ar'):
        """الحصول على مراجعات الفندق"""
        try:
            url = f"{RAPIDAPI_BASE_URL}/hotels/reviews"
            params = {
                'hotel_id': hotel_id,
                'languagecode': languagecode
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            reviews = data.get('data', {}).get('reviews', [])
            
            logger.info(f"تم الحصول على مراجعات الفندق: {hotel_id}")
            
            return {
                'success': True,
                'data': reviews,
                'total_reviews': len(reviews)
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"خطأ في الحصول على المراجعات: {e}")
            return {
                'success': False,
                'error': str(e),
                'data': []
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
            'search_locations': '/api/locations/search',
            'search_hotels': '/api/hotels/search',
            'hotel_details': '/api/hotels/details',
            'hotel_reviews': '/api/hotels/reviews',
            'health_check': '/api/health'
        }
    })

@app.route('/api/health')
def health_check():
    """فحص صحة النظام"""
    try:
        # اختبار الاتصال مع Booking.com API
        result = booking_api.search_locations('Dubai')
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'booking_api_connection': 'connected' if result['success'] else 'disconnected',
            'api_key_configured': bool(RAPIDAPI_KEY and RAPIDAPI_KEY != 'YOUR_RAPIDAPI_KEY_HERE')
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
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'معامل البحث query مطلوب'
            }), 400
        
        result = booking_api.search_locations(query)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"خطأ في البحث عن الموقع: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/hotels/search', methods=['POST'])
def search_hotels():
    """البحث عن الفنادق"""
    try:
        data = request.get_json()
        
        # التحقق من البيانات المطلوبة
        required_fields = ['dest_id', 'checkin', 'checkout']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'الحقل {field} مطلوب'
                }), 400
        
        # استخراج البيانات
        dest_id = data['dest_id']
        checkin = data['checkin']
        checkout = data['checkout']
        adults = data.get('adults', 2)
        rooms = data.get('rooms', 1)
        currency = data.get('currency', 'SAR')
        
        # التحقق من صحة التواريخ
        try:
            checkin_date = datetime.strptime(checkin, '%Y-%m-%d')
            checkout_date = datetime.strptime(checkout, '%Y-%m-%d')
            
            if checkout_date <= checkin_date:
                return jsonify({
                    'success': False,
                    'error': 'تاريخ المغادرة يجب أن يكون بعد تاريخ الوصول'
                }), 400
                
            if checkin_date < datetime.now():
                return jsonify({
                    'success': False,
                    'error': 'تاريخ الوصول لا يمكن أن يكون في الماضي'
                }), 400
                
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'تنسيق التاريخ غير صحيح. استخدم YYYY-MM-DD'
            }), 400
        
        # البحث عن الفنادق
        result = booking_api.search_hotels(
            dest_id=dest_id,
            checkin=checkin,
            checkout=checkout,
            adults=adults,
            rooms=rooms,
            currency=currency
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"خطأ في البحث عن الفنادق: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/hotels/details', methods=['GET'])
def get_hotel_details():
    """الحصول على تفاصيل فندق محدد"""
    try:
        hotel_id = request.args.get('hotel_id')
        checkin = request.args.get('checkin')
        checkout = request.args.get('checkout')
        adults = int(request.args.get('adults', 2))
        rooms = int(request.args.get('rooms', 1))
        currency = request.args.get('currency', 'SAR')
        
        if not all([hotel_id, checkin, checkout]):
            return jsonify({
                'success': False,
                'error': 'hotel_id, checkin, checkout مطلوبة'
            }), 400
        
        result = booking_api.get_hotel_details(
            hotel_id=hotel_id,
            checkin=checkin,
            checkout=checkout,
            adults=adults,
            rooms=rooms,
            currency=currency
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على تفاصيل الفندق: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/hotels/reviews', methods=['GET'])
def get_hotel_reviews():
    """الحصول على مراجعات الفندق"""
    try:
        hotel_id = request.args.get('hotel_id')
        languagecode = request.args.get('languagecode', 'ar')
        
        if not hotel_id:
            return jsonify({
                'success': False,
                'error': 'hotel_id مطلوب'
            }), 400
        
        result = booking_api.get_hotel_reviews(
            hotel_id=hotel_id,
            languagecode=languagecode
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على المراجعات: {e}")
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
    
    logger.info(f"🚀 بدء تشغيل Paygo Booking.com Backend على المنفذ {port}")
    logger.info(f"🔑 مفتاح API مكون: {bool(RAPIDAPI_KEY and RAPIDAPI_KEY != 'YOUR_RAPIDAPI_KEY_HERE')}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
