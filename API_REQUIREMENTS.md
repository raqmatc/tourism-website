# متطلبات Booking.com API

## المشكلة الأساسية

**RapidAPI key يعمل لكن يجب الاشتراك في Booking.com API على RapidAPI**

## API Endpoint الصحيح

- **URL**: `https://booking-com18.p.rapidapi.com/stays/search`
- **Method**: GET
- **Headers**: 
  - `x-rapidapi-host`: `booking-com18.p.rapidapi.com`
  - `x-rapidapi-key`: `YOUR_RAPIDAPI_KEY`

## المعاملات المطلوبة

### معاملات أساسية (Required):
1. **locationId** (String): معرف الموقع من `/stays/auto-complete`
   - مثال: `eyJjaXR5X2...`
   - **ملاحظة مهمة**: يجب أن يكون من نتيجة auto-complete، وليس رقم عشوائي!

2. **checkIn** (Date): تاريخ الوصول بصيغة YYYY-MM-DD
   - مثال: `2024-01-21`

3. **checkOut** (Date): تاريخ المغادرة بصيغة YYYY-MM-DD
   - مثال: `2024-01-22`

### معاملات اختيارية:
- **page**: رقم الصفحة (افتراضي: 1)
- **sortBy**: طريقة الترتيب (افتراضي: popularity)
- **rooms**: عدد الغرف (افتراضي: 1)
- **adults**: عدد البالغين (افتراضي: 1)
- **children**: أعمار الأطفال (مثال: `0,11,17`)
- **minPrice**: السعر الأدنى
- **maxPrice**: السعر الأعلى
- **categoriesFilter**: فلاتر الفئات (مثال: `class::3,facility::107`)
- **units**: وحدات القياس (metric/imperial)
- **temperature**: وحدة الحرارة (c/f)
- **languageCode**: رمز اللغة (افتراضي: en-us)
- **currencyCode**: رمز العملة (مثال: USD)

## الخطوات المطلوبة لحل المشكلة

### 1. الاشتراك في API على RapidAPI
- الذهاب إلى: https://rapidapi.com/ntd119/api/booking-com18
- تسجيل الدخول أو إنشاء حساب
- اختيار خطة اشتراك (BASIC مجاني - 100 طلب/شهر)
- الاشتراك في API

### 2. الحصول على locationId الصحيح
المشكلة الحالية: نستخدم أرقام عشوائية مثل `-782831` لكن API يتطلب `locationId` من `/stays/auto-complete`

**الحل**:
- استخدام endpoint `/stays/auto-complete` للبحث عن المدينة
- الحصول على `data->id` من النتيجة
- استخدام هذا ID في `/stays/search`

مثال:
```
GET /stays/auto-complete?query=Dubai
Response: {
  "data": [
    {
      "id": "eyJjaXR5X2lkIjoxMjM0NTY3fQ==",  // هذا هو locationId الصحيح
      "name": "Dubai",
      "country": "United Arab Emirates"
    }
  ]
}
```

### 3. تحديث Backend
تم تحديث Backend ليستخدم:
- ✅ GET بدلاً من POST
- ✅ `/stays/search` بدلاً من `/hotels/search`
- ✅ `/stays/auto-complete` بدلاً من `/locations/auto-complete`

### 4. تحديث Frontend
تم تحديث Frontend ليستخدم:
- ✅ GET بدلاً من POST
- ⚠️ يجب استخدام `locationId` من auto-complete بدلاً من أرقام ثابتة

## الحالة الحالية

### ما يعمل:
- ✅ Backend منشور على Render
- ✅ Frontend منشور على GitHub Pages
- ✅ الاتصال بين Frontend و Backend يعمل
- ✅ طريقة الطلب صحيحة (GET)
- ✅ API endpoints صحيحة

### ما لا يعمل:
- ❌ RapidAPI يعيد خطأ 404 لأن:
  1. إما أن الاشتراك في API غير مفعّل
  2. أو أن `locationId` المستخدم غير صحيح (أرقام عشوائية بدلاً من IDs حقيقية)

## التوصيات

1. **فوري**: الاشتراك في Booking.com API على RapidAPI (مجاني للخطة الأساسية)
2. **مهم**: تحديث الكود ليستخدم `/stays/auto-complete` للحصول على `locationId` الصحيح
3. **اختياري**: إضافة معاملات إضافية مثل الفلاتر والترتيب
