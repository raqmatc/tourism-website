# 🏨 Paygo Amadeus Hotel Booking System
## نظام حجز الفنادق المتكامل مع Amadeus

![Paygo Logo](https://img.shields.io/badge/Paygo-Hotel%20Booking-blue?style=for-the-badge&logo=hotel)
![Amadeus](https://img.shields.io/badge/Powered%20by-Amadeus-orange?style=for-the-badge)
![Arabic](https://img.shields.io/badge/Language-Arabic-green?style=for-the-badge)

---

## 📋 نظرة عامة

نظام حجز فنادق متكامل يربط موقع Paygo بشبكة Amadeus العالمية، مما يوفر الوصول إلى أكثر من **150,000 فندق** حول العالم مع واجهة عربية كاملة.

### ✨ المميزات الرئيسية

- 🌍 **شبكة عالمية**: أكثر من 150,000 فندق في 200+ دولة
- 🔍 **بحث متقدم**: فلاتر ذكية وترتيب متعدد الخيارات
- 💰 **أسعار تنافسية**: أفضل الأسعار مع خصومات حصرية
- 🛡️ **حجز آمن**: تقنية Amadeus المتقدمة للحماية
- 📱 **تصميم متجاوب**: يعمل على جميع الأجهزة
- 🌐 **واجهة عربية**: دعم كامل للغة العربية

---

## 🏗️ هيكل المشروع

```
paygo-amadeus-hotel-booking/
├── 📄 FILE_01_paygo_amadeus_integration.html    # الصفحة الرئيسية
├── 📄 FILE_02_amadeus_results.html              # صفحة النتائج
├── 📄 FILE_03_amadeus_hotel_details.html        # صفحة تفاصيل الفندق
├── 📁 backend/
│   ├── 📄 app.py                                # Backend Python/Flask
│   ├── 📄 requirements.txt                      # متطلبات Python
│   └── 📄 .env.example                          # مثال المتغيرات البيئية
└── 📄 README.md                                 # هذا الملف
```

---

## 🚀 التشغيل السريع

### 1️⃣ متطلبات النظام
- Python 3.8+
- حساب Amadeus Developer (مجاني)
- متصفح حديث

### 2️⃣ إعداد Backend

```bash
# 1. استنساخ المشروع
git clone https://github.com/raqmatc/paygo-amadeus-hotel-booking.git
cd paygo-amadeus-hotel-booking

# 2. إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate     # Windows

# 3. تثبيت المتطلبات
cd backend
pip install -r requirements.txt

# 4. إعداد المتغيرات البيئية
cp .env.example .env
# عدّل ملف .env وأضف مفاتيح Amadeus API

# 5. تشغيل الخادم
python app.py
```

### 3️⃣ فتح Frontend
```bash
# افتح الملف في المتصفح
open FILE_01_paygo_amadeus_integration.html
```

---

## 🔑 الحصول على مفاتيح Amadeus API

### خطوات التسجيل:
1. **اذهب إلى**: https://developers.amadeus.com
2. **أنشئ حساب مجاني** أو سجل دخول
3. **أنشئ تطبيق جديد** في "My Apps"
4. **انسخ API Key و API Secret**
5. **أضفهما في ملف `.env`**:

```bash
AMADEUS_TEST_CLIENT_ID=your_api_key_here
AMADEUS_TEST_CLIENT_SECRET=your_api_secret_here
```

---

## 🌐 APIs المتاحة

### 🔍 البحث عن الفنادق
```http
POST /api/hotels/search
Content-Type: application/json

{
  "cityCode": "DXB",
  "checkInDate": "2025-03-15",
  "checkOutDate": "2025-03-17",
  "adults": 2,
  "currency": "SAR"
}
```

### 🏨 تفاصيل الفندق
```http
POST /api/hotels/details
Content-Type: application/json

{
  "hotelIds": "HOTEL123",
  "checkInDate": "2025-03-15",
  "checkOutDate": "2025-03-17",
  "adults": 2
}
```

### 📅 إنشاء حجز
```http
POST /api/bookings/create
Content-Type: application/json

{
  "offerId": "OFFER123",
  "guests": [
    {
      "name": {
        "firstName": "أحمد",
        "lastName": "محمد"
      }
    }
  ]
}
```

### 🏙️ البحث عن المدن
```http
GET /api/cities/search?q=دبي
```

---

## 🎨 الصفحات والمكونات

### 🏠 الصفحة الرئيسية
- **الملف**: `FILE_01_paygo_amadeus_integration.html`
- **الوظائف**: بحث الفنادق، اقتراحات المدن، التحقق من البيانات
- **التقنيات**: HTML5, CSS3, JavaScript ES6

### 📊 صفحة النتائج
- **الملف**: `FILE_02_amadeus_results.html`
- **الوظائف**: عرض النتائج، فلاتر متقدمة، ترتيب، تصفح الصفحات
- **المميزات**: تصميم متجاوب، تحميل تدريجي

### 🏨 صفحة تفاصيل الفندق
- **الملف**: `FILE_03_amadeus_hotel_details.html`
- **الوظائف**: معرض صور، تبويبات، حاسبة الأسعار، نظام الحجز
- **المكتبات**: Swiper.js للمعرض

---

## 🛠️ التقنيات المستخدمة

### Frontend
- **HTML5** - هيكل الصفحات
- **CSS3** - التصميم والتنسيق
- **JavaScript ES6** - التفاعل والوظائف
- **Swiper.js** - معرض الصور
- **Font Awesome** - الأيقونات
- **Google Fonts** - خط Cairo العربي

### Backend
- **Python 3.8+** - لغة البرمجة
- **Flask** - إطار العمل
- **Flask-CORS** - دعم CORS
- **Requests** - استدعاءات HTTP
- **Amadeus APIs** - بيانات الفنادق

---

## 🌍 المدن المدعومة

### 🇸🇦 المملكة العربية السعودية
- الرياض (RUH)
- جدة (JED)
- الدمام (DMM)

### 🇦🇪 الإمارات العربية المتحدة
- دبي (DXB)
- أبوظبي (AUH)
- الشارقة (SHJ)

### 🇪🇬 مصر
- القاهرة (CAI)
- الإسكندرية (ALY)
- شرم الشيخ (SSH)

### 🌍 مدن عالمية
- لندن (LON)
- باريس (PAR)
- نيويورك (NYC)
- طوكيو (TYO)
- **+15 مدينة أخرى**

---

## 📱 التوافق

### المتصفحات المدعومة
- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

### الأجهزة
- 📱 الهواتف الذكية
- 📱 الأجهزة اللوحية
- 💻 أجهزة الكمبيوتر
- 🖥️ الشاشات الكبيرة

---

## 🔧 التخصيص والتطوير

### إضافة مدن جديدة
```javascript
// في ملف JavaScript
const cities = [
    { name: 'مدينة جديدة', code: 'NEW', country: 'الدولة' },
    // ... باقي المدن
];
```

### تخصيص الألوان
```css
/* في ملف CSS */
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #ff6b6b;
}
```

### إضافة لغات جديدة
```javascript
// نظام الترجمة
const translations = {
    'ar': { /* النصوص العربية */ },
    'en': { /* النصوص الإنجليزية */ }
};
```

---

## 🚀 النشر والاستضافة

### GitHub Pages (مجاني)
1. فعّل GitHub Pages في إعدادات المستودع
2. اختر branch `main`
3. احصل على الرابط: `https://raqmatc.github.io/paygo-amadeus-hotel-booking/`

### Netlify (مجاني)
1. ربط المستودع بـ Netlify
2. نشر تلقائي عند كل تحديث
3. دومين مخصص متاح

### Heroku (Backend)
```bash
# إنشاء تطبيق Heroku
heroku create paygo-amadeus-backend

# نشر Backend
git subtree push --prefix backend heroku main
```

---

## 📊 الإحصائيات والتحليلات

### المميزات المتاحة
- 📈 تتبع البحثات
- 📊 إحصائيات الحجوزات
- 🎯 تحليل سلوك المستخدمين
- 📱 تتبع الأجهزة والمتصفحات

### التكامل مع Google Analytics
```javascript
// إضافة كود التتبع
gtag('event', 'hotel_search', {
    'destination': cityName,
    'check_in': checkinDate,
    'check_out': checkoutDate
});
```

---

## 🛡️ الأمان والحماية

### الممارسات الآمنة
- 🔐 تشفير البيانات الحساسة
- 🛡️ التحقق من صحة المدخلات
- 🔑 إدارة آمنة لمفاتيح API
- 🚫 حماية من هجمات CSRF

### متغيرات البيئة
```bash
# لا تشارك هذه المعلومات أبداً
AMADEUS_CLIENT_SECRET=your_secret_here
PAYGO_API_KEY=your_api_key_here
```

---

## 🤝 المساهمة والتطوير

### كيفية المساهمة
1. **Fork** المشروع
2. إنشاء **branch** جديد للميزة
3. **Commit** التغييرات
4. **Push** إلى Branch
5. إنشاء **Pull Request**

### إرشادات الكود
- استخدم أسماء متغيرات واضحة
- أضف تعليقات باللغة العربية
- اتبع معايير JavaScript ES6
- اختبر الكود قبل الإرسال

---

## 📞 الدعم والمساعدة

### طرق التواصل
- 📧 **البريد الإلكتروني**: raqmatc@gmail.com
- 🐛 **تقرير الأخطاء**: GitHub Issues
- 💬 **الدردشة**: GitHub Discussions
- 📱 **الدعم الفني**: متاح 24/7

### الأسئلة الشائعة

**س: كيف أحصل على مفاتيح Amadeus API؟**
ج: سجل في https://developers.amadeus.com وأنشئ تطبيق جديد.

**س: هل الخدمة مجانية؟**
ج: نعم، Amadeus يوفر طبقة مجانية للتطوير والاختبار.

**س: هل يمكن استخدام المشروع تجارياً؟**
ج: نعم، لكن تحتاج لترقية حساب Amadeus للإنتاج.

---

## 📈 خارطة الطريق

### الإصدار 1.1 (قريباً)
- [ ] دعم حجز الطيران
- [ ] نظام المراجعات والتقييمات
- [ ] تطبيق الهاتف المحمول
- [ ] دعم العملات المتعددة

### الإصدار 1.2 (المستقبل)
- [ ] الذكاء الاصطناعي للاقتراحات
- [ ] نظام النقاط والمكافآت
- [ ] تكامل مع وسائل التواصل
- [ ] دعم اللغات المتعددة

---

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

---

## 🙏 شكر وتقدير

- **Amadeus** - لتوفير APIs الفنادق المتقدمة
- **Font Awesome** - للأيقونات الجميلة
- **Google Fonts** - لخط Cairo العربي
- **Swiper.js** - لمعرض الصور التفاعلي
- **المجتمع العربي** - للدعم والتشجيع

---

## 📊 إحصائيات المشروع

![GitHub stars](https://img.shields.io/github/stars/raqmatc/paygo-amadeus-hotel-booking?style=social)
![GitHub forks](https://img.shields.io/github/forks/raqmatc/paygo-amadeus-hotel-booking?style=social)
![GitHub issues](https://img.shields.io/github/issues/raqmatc/paygo-amadeus-hotel-booking)
![GitHub license](https://img.shields.io/github/license/raqmatc/paygo-amadeus-hotel-booking)

---

<div align="center">

**🎉 مبروك! مشروعك جاهز للانطلاق! 🎉**

**صنع بـ ❤️ في المملكة العربية السعودية**

[⭐ ضع نجمة للمشروع](https://github.com/raqmatc/paygo-amadeus-hotel-booking) | [🐛 بلّغ عن خطأ](https://github.com/raqmatc/paygo-amadeus-hotel-booking/issues) | [💬 شارك رأيك](https://github.com/raqmatc/paygo-amadeus-hotel-booking/discussions)

</div>
