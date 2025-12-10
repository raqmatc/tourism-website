#!/usr/bin/env python3
"""
Tourism Website Backend - Hotels.com Provider API Integration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import logging

# تحميل متغيرات البيئة
load_dotenv('.env.booking')

# إعداد Flask
app = Flask(__name__)
CORS(app)

# إعداد Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# إعدادات API
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = "hotels-com-provider.p.rapidapi.com"
BASE_URL = f"https://{RAPIDAPI_HOST}"

# Headers مشتركة
HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

# الإعدادات الافتراضية
DEFAULT_DOMAIN = "US"
DEFAULT_LOCALE = "en_US"


@app.route('/')
def home():
    """الصفحة الرئيسية"""
    return jsonify({
        "status": "running",
        "message": "Tourism Website Backend - Hotels.com API",
        "version": "2.0.0",
        "endpoints": {
            "locations": "/api/locations/search",
            "hotels": "/api/hotels/search"
        }
    })


@app.route('/api/locations/search', methods=['GET'])
def search_locations():
    """
    البحث عن المواقع (مدن، مطارات، أحياء)
    
    Parameters:
        query (str): نص البحث
        domain (str): النطاق (افتراضي: US)
        locale (str): اللغة (افتراضي: en_US)
    
    Returns:
        JSON: قائمة المواقع
    """
    try:
        # الحصول على المعاملات
        query = request.args.get('query', '')
        domain = request.args.get('domain', DEFAULT_DOMAIN)
        locale = request.args.get('locale', DEFAULT_LOCALE)
        
        if not query:
            return jsonify({
                "success": False,
                "error": "Query parameter is required"
            }), 400
        
        logger.info(f"Searching locations: query={query}, domain={domain}, locale={locale}")
        
        # استدعاء API
        url = f"{BASE_URL}/v2/regions"
        params = {
            "query": query,
            "domain": domain,
            "locale": locale
        }
        
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # معالجة البيانات
            locations = []
            if 'data' in data:
                for item in data['data']:
                    location = {
                        "id": str(item.get('gaiaId', '')),
                        "name": item.get('regionNames', {}).get('fullName', ''),
                        "type": item.get('type', ''),
                        "country": item.get('regionNames', {}).get('primaryDisplayName', '')
                    }
                    locations.append(location)
            
            logger.info(f"Found {len(locations)} locations")
            
            return jsonify({
                "success": True,
                "data": locations
            })
        else:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return jsonify({
                "success": False,
                "error": f"API returned status code {response.status_code}"
            }), response.status_code
            
    except Exception as e:
        logger.error(f"Exception in search_locations: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/hotels/search', methods=['GET'])
def search_hotels():
    """
    البحث عن الفنادق
    
    Parameters:
        region_id (str): معرف المنطقة
        checkin_date (str): تاريخ تسجيل الوصول (YYYY-MM-DD)
        checkout_date (str): تاريخ تسجيل المغادرة (YYYY-MM-DD)
        adults_number (int): عدد البالغين (افتراضي: 2)
        room_number (int): عدد الغرف (افتراضي: 1)
        page_number (int): رقم الصفحة (افتراضي: 1)
        domain (str): النطاق (افتراضي: US)
        locale (str): اللغة (افتراضي: en_US)
        currency (str): العملة (افتراضي: USD)
    
    Returns:
        JSON: قائمة الفنادق
    """
    try:
        # الحصول على المعاملات
        region_id = request.args.get('region_id', request.args.get('dest_id', ''))
        checkin_date = request.args.get('checkin_date', request.args.get('checkin', ''))
        checkout_date = request.args.get('checkout_date', request.args.get('checkout', ''))
        adults_number = int(request.args.get('adults_number', request.args.get('adults', 2)))
        room_number = int(request.args.get('room_number', request.args.get('rooms', 1)))
        page_number = int(request.args.get('page_number', 1))
        domain = request.args.get('domain', DEFAULT_DOMAIN)
        locale = request.args.get('locale', DEFAULT_LOCALE)
        currency = request.args.get('currency', 'USD')
        
        if not region_id or not checkin_date or not checkout_date:
            return jsonify({
                "success": False,
                "error": "region_id, checkin_date, and checkout_date are required"
            }), 400
        
        logger.info(f"Searching hotels: region_id={region_id}, checkin={checkin_date}, checkout={checkout_date}, page={page_number}")
        
        # استدعاء API
        url = f"{BASE_URL}/v3/hotels/search"
        params = {
            "region_id": region_id,
            "checkin_date": checkin_date,
            "checkout_date": checkout_date,
            "adults_number": adults_number,
            "room_number": room_number,
            "page_number": page_number,
            "domain": domain,
            "locale": locale,
            "sort_order": "REVIEW"
        }
        
        response = requests.get(url, headers=HEADERS, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # معالجة البيانات
            hotels = []
            if 'data' in data and 'properties' in data['data']:
                for item in data['data']['properties']:
                    # السعر
                    price = 0
                    price_currency = currency
                    if 'price' in item and item['price']:
                        price_lead = item['price'].get('lead', {})
                        if price_lead:
                            price = price_lead.get('amount', 0)
                            currency_info = price_lead.get('currencyInfo', {})
                            if currency_info:
                                price_currency = currency_info.get('code', currency)
                    
                    # التقييم
                    rating = 0
                    review_count = 0
                    if 'guestRating' in item and item['guestRating']:
                        rating_str = item['guestRating'].get('rating', '0')
                        try:
                            rating = float(rating_str)
                        except:
                            rating = 0
                        
                        # استخراج عدد التقييمات من phrases
                        phrases = item['guestRating'].get('phrases', [])
                        if len(phrases) > 1:
                            review_text = phrases[1]  # مثل "2 reviews"
                            try:
                                review_count = int(review_text.split()[0])
                            except:
                                review_count = 0
                    
                    # الصور
                    image_url = ""
                    if 'propertyImage' in item and item['propertyImage']:
                        image_data = item['propertyImage'].get('image', {})
                        if image_data:
                            image_url = image_data.get('url', '')
                    
                    # النجوم
                    star_rating = 0
                    if 'star' in item:
                        try:
                            star_rating = float(item['star'])
                        except:
                            star_rating = 0
                    
                    hotel = {
                        "id": str(item.get('id', '')),
                        "name": item.get('name', ''),
                        "price": price,
                        "currency": price_currency,
                        "rating": rating,
                        "review_count": review_count,
                        "star_rating": star_rating,
                        "image": image_url,
                        "location": ', '.join(item.get('messages', [])),
                        "amenities": item.get('short_amenities', []),
                        "link": item.get('link', '')
                    }
                    hotels.append(hotel)
            
            logger.info(f"Found {len(hotels)} hotels")
            
            return jsonify({
                "success": True,
                "data": hotels,
                "page": page_number
            })
        else:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return jsonify({
                "success": False,
                "error": f"API returned status code {response.status_code}"
            }), response.status_code
            
    except Exception as e:
        logger.error(f"Exception in search_hotels: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Tourism Website Backend on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
