#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paygo Amadeus Backend
تطبيق Flask للتكامل مع Amadeus APIs
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import os
import json
from datetime import datetime, timedelta
import logging
from functools import wraps
import time

# إعداد التطبيق
app = Flask(__name__)
CORS(app)  # تمكين CORS للتطبيقات الأمامية

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# إعدادات Amadeus
AMADEUS_CONFIG = {
    'test': {
        'base_url': 'https://test.api.amadeus.com',
        'client_id': os.getenv('AMADEUS_TEST_CLIENT_ID', 'YOUR_TEST_CLIENT_ID'),
        'client_secret': os.getenv('AMADEUS_TEST_CLIENT_SECRET', 'YOUR_TEST_CLIENT_SECRET')
    },
    'production': {
        'base_url': 'https://api.amadeus.com',
        'client_id': os.getenv('AMADEUS_PROD_CLIENT_ID', 'YOUR_PROD_CLIENT_ID'),
        'client_secret': os.getenv('AMADEUS_PROD_CLIENT_SECRET', 'YOUR_PROD_CLIENT_SECRET')
    }
}

# استخدام بيئة الاختبار افتراضياً
CURRENT_ENV = os.getenv('AMADEUS_ENV', 'test')
AMADEUS_BASE_URL = AMADEUS_CONFIG[CURRENT_ENV]['base_url']
AMADEUS_CLIENT_ID = AMADEUS_CONFIG[CURRENT_ENV]['client_id']
AMADEUS_CLIENT_SECRET = AMADEUS_CONFIG[CURRENT_ENV]['client_secret']

class AmadeusAPI:
    """فئة للتعامل مع Amadeus APIs"""
    
    def __init__(self):
        self.access_token = None
        self.token_expires_at = None
        
    def get_access_token(self):
        """الحصول على access token من Amadeus"""
        try:
            # التحقق من صحة التوكن الحالي
            if self.access_token and self.token_expires_at:
                if datetime.now() < self.token_expires_at:
                    return self.access_token
            
            # طلب توكن جديد
            url = f"{AMADEUS_BASE_URL}/v1/security/oauth2/token"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'grant_type': 'client_credentials',
                'client_id': AMADEUS_CLIENT_ID,
                'client_secret': AMADEUS_CLIENT_SECRET
            }
            
            response = requests.post(url, headers=headers, data=data, timeout=30)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            
            # حساب وقت انتهاء التوكن
            expires_in = token_data.get('expires_in', 1799)  # افتراضي 30 دقيقة
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
            
            logger.info("تم الحصول على Amadeus access token بنجاح")
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"خطأ في الحصول على access token: {e}")
            raise Exception(f"فشل في المصادقة مع Amadeus: {str(e)}")
    
    def search_hotels(self, city_code, check_in, check_out, adults=1, currency='SAR'):
        """البحث عن الفنادق"""
        try:
            token = self.get_access_token()
            
            url = f"{AMADEUS_BASE_URL}/v3/shopping/hotel-offers"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            params = {
                'cityCode': city_code,
                'checkInDate': check_in,
                'checkOutDate': check_out,
                'adults': adults,
                'currency': currency,
                'lang': 'AR'  # اللغة العربية
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"تم البحث عن الفنادق في {city_code}: {len(data.get('data', []))} نتيجة")
            
            return {
                'success': True,
                'data': data.get('data', []),
                'meta': data.get('meta', {}),
                'total_results': len(data.get('data', []))
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"خطأ في البحث عن الفنادق: {e}")
            return {
                'success': False,
                'error': f"فشل في البحث: {str(e)}",
                'data': []
            }
    
    def get_hotel_details(self, hotel_ids, check_in, check_out, adults=1):
        """الحصول على تفاصيل فندق محدد"""
        try:
            token = self.get_access_token()
            
            url = f"{AMADEUS_BASE_URL}/v3/shopping/hotel-offers/by-hotel"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            params = {
                'hotelIds': hotel_ids,
                'checkInDate': check_in,
                'checkOutDate': check_out,
                'adults': adults,
                'currency': 'SAR',
                'lang': 'AR'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"تم الحصول على تفاصيل الفندق: {hotel_ids}")
            
            return {
                'success': True,
                'data': data.get('data', []),
                'meta': data.get('meta', {})
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"خطأ في الحصول على تفاصيل الفندق: {e}")
            return {
                'success': False,
                'error': f"فشل في الحصول على التفاصيل: {str(e)}",
                'data': []
            }
    
    def create_booking(self, booking_data):
        """إنشاء حجز فندق"""
        try:
            token = self.get_access_token()
            
            url = f"{AMADEUS_BASE_URL}/v1/booking/hotel-bookings"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, headers=headers, json=booking_data, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"تم إنشاء الحجز بنجاح: {data.get('data', {}).get('id', 'N/A')}")
            
            return {
                'success': True,
                'data': data.get('data', {}),
                'booking_id': data.get('data', {}).get('id')
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"خطأ في إنشاء الحجز: {e}")
            return {
                'success': False,
                'error': f"فشل في إنشاء الحجز: {str(e)}",
                'data': {}
            }

# إنشاء كائن Amadeus API
amadeus_api = AmadeusAPI()

def require_api_key(f):
    """ديكوريتر للتحقق من مفتاح API (اختياري للحماية)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        expected_key = os.getenv('PAYGO_API_KEY')
        
        if expected_key and api_key != expected_key:
            return jsonify({'error': 'مفتاح API غير صحيح'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    """الصفحة الرئيسية للـ API"""
    return jsonify({
        'message': 'Paygo Amadeus Backend API',
        'version': '1.0.0',
        'status': 'running',
        'environment': CURRENT_ENV,
        'endpoints': {
            'search_hotels': '/api/hotels/search',
            'hotel_details': '/api/hotels/details',
            'create_booking': '/api/bookings/create',
            'health_check': '/api/health'
        }
    })

@app.route('/api/health')
def health_check():
    """فحص صحة النظام"""
    try:
        # اختبار الاتصال مع Amadeus
        token = amadeus_api.get_access_token()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'amadeus_connection': 'connected' if token else 'disconnected',
            'environment': CURRENT_ENV
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e),
            'environment': CURRENT_ENV
        }), 500

@app.route('/api/hotels/search', methods=['POST'])
def search_hotels():
    """البحث عن الفنادق"""
    try:
        data = request.get_json()
        
        # التحقق من البيانات المطلوبة
        required_fields = ['cityCode', 'checkInDate', 'checkOutDate']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'الحقل {field} مطلوب'
                }), 400
        
        # استخراج البيانات
        city_code = data['cityCode']
        check_in = data['checkInDate']
        check_out = data['checkOutDate']
        adults = data.get('adults', 1)
        currency = data.get('currency', 'SAR')
        
        # التحقق من صحة التواريخ
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
            
            if check_in_date >= check_out_date:
                return jsonify({
                    'success': False,
                    'error': 'تاريخ المغادرة يجب أن يكون بعد تاريخ الوصول'
                }), 400
                
            if check_in_date < datetime.now().date():
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
        result = amadeus_api.search_hotels(
            city_code=city_code,
            check_in=check_in,
            check_out=check_out,
            adults=adults,
            currency=currency
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"خطأ في البحث عن الفنادق: {e}")
        return jsonify({
            'success': False,
            'error': 'حدث خطأ داخلي في الخادم',
            'details': str(e)
        }), 500

@app.route('/api/hotels/details', methods=['POST'])
def get_hotel_details():
    """الحصول على تفاصيل فندق محدد"""
    try:
        data = request.get_json()
        
        # التحقق من البيانات المطلوبة
        required_fields = ['hotelIds', 'checkInDate', 'checkOutDate']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'الحقل {field} مطلوب'
                }), 400
        
        # استخراج البيانات
        hotel_ids = data['hotelIds']
        check_in = data['checkInDate']
        check_out = data['checkOutDate']
        adults = data.get('adults', 1)
        
        # الحصول على تفاصيل الفندق
        result = amadeus_api.get_hotel_details(
            hotel_ids=hotel_ids,
            check_in=check_in,
            check_out=check_out,
            adults=adults
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على تفاصيل الفندق: {e}")
        return jsonify({
            'success': False,
            'error': 'حدث خطأ داخلي في الخادم',
            'details': str(e)
        }), 500

@app.route('/api/bookings/create', methods=['POST'])
def create_booking():
    """إنشاء حجز فندق"""
    try:
        data = request.get_json()
        
        # التحقق من البيانات المطلوبة
        required_fields = ['offerId', 'guests']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'الحقل {field} مطلوب'
                }), 400
        
        # إنشاء الحجز
        result = amadeus_api.create_booking(data)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"خطأ في إنشاء الحجز: {e}")
        return jsonify({
            'success': False,
            'error': 'حدث خطأ داخلي في الخادم',
            'details': str(e)
        }), 500

@app.route('/api/cities/search', methods=['GET'])
def search_cities():
    """البحث عن المدن (قاعدة بيانات محلية)"""
    query = request.args.get('q', '').lower()
    
    cities = [
        {'name': 'دبي', 'code': 'DXB', 'country': 'الإمارات العربية المتحدة'},
        {'name': 'الرياض', 'code': 'RUH', 'country': 'المملكة العربية السعودية'},
        {'name': 'القاهرة', 'code': 'CAI', 'country': 'مصر'},
        {'name': 'الدوحة', 'code': 'DOH', 'country': 'قطر'},
        {'name': 'الكويت', 'code': 'KWI', 'country': 'الكويت'},
        {'name': 'بيروت', 'code': 'BEY', 'country': 'لبنان'},
        {'name': 'عمان', 'code': 'AMM', 'country': 'الأردن'},
        {'name': 'مسقط', 'code': 'MCT', 'country': 'عمان'},
        {'name': 'المنامة', 'code': 'BAH', 'country': 'البحرين'},
        {'name': 'الدار البيضاء', 'code': 'CMN', 'country': 'المغرب'},
        {'name': 'تونس', 'code': 'TUN', 'country': 'تونس'},
        {'name': 'الجزائر', 'code': 'ALG', 'country': 'الجزائر'},
        {'name': 'لندن', 'code': 'LON', 'country': 'المملكة المتحدة'},
        {'name': 'باريس', 'code': 'PAR', 'country': 'فرنسا'},
        {'name': 'نيويورك', 'code': 'NYC', 'country': 'الولايات المتحدة'}
    ]
    
    if query:
        filtered_cities = [
            city for city in cities 
            if query in city['name'].lower() or query in city['country'].lower()
        ]
    else:
        filtered_cities = cities
    
    return jsonify({
        'success': True,
        'data': filtered_cities[:10]  # أول 10 نتائج
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'الصفحة غير موجودة',
        'status_code': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'خطأ داخلي في الخادم',
        'status_code': 500
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"""
🚀 Paygo Amadeus Backend API
🌐 Environment: {CURRENT_ENV}
🔗 Base URL: {AMADEUS_BASE_URL}
📡 Port: {port}
🐛 Debug: {debug}
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)

