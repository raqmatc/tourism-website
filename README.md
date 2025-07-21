# Paygo.com - موقع حجز الفنادق مع تكامل RateHawk

موقع حجز فنادق عربي متطور مع تكامل كامل مع شبكة RateHawk العالمية التي تضم أكثر من 2.7 مليون فندق حول العالم.

## 🌟 الميزات الرئيسية

### 🏨 حجز الفنادق
- **شبكة عالمية واسعة**: أكثر من 2.7 مليون فندق في 200+ دولة
- **أفضل الأسعار المضمونة**: تكامل مباشر مع RateHawk للحصول على أسعار تنافسية
- **بحث ذكي**: نظام بحث متقدم مع اقتراحات المدن
- **واجهة عربية**: تصميم متجاوب باللغة العربية

### 🔗 تكامل RateHawk
- **معرف الشريك**: `282088.affiliate.dd55`
- **تتبع النقرات**: نظام تتبع متقدم للنقرات والتحويلات
- **عمولات مضمونة**: 5%+ عمولة على كل حجز مكتمل
- **دعم 24/7**: دعم فني متواصل من RateHawk

### 🎨 التصميم والتجربة
- **تصميم متجاوب**: يعمل بشكل مثالي على جميع الأجهزة
- **واجهة حديثة**: تصميم عصري مشابه لـ Booking.com
- **تجربة مستخدم سلسة**: تنقل سهل وبديهي
- **تحميل سريع**: محسن للأداء والسرعة

## 🚀 التقنيات المستخدمة

- **HTML5**: بنية حديثة ومتوافقة
- **CSS3**: تصميم متجاوب مع animations
- **JavaScript ES6+**: وظائف تفاعلية متقدمة
- **Font Awesome**: أيقونات احترافية
- **Google Fonts**: خط Cairo العربي

## 📁 بنية المشروع

```
tourism-website/
├── index.html                 # الصفحة الرئيسية المحسنة
├── ratehawk-integration.js    # مكتبة التكامل مع RateHawk
├── README.md                  # وثائق المشروع
├── images/                    # الصور والأيقونات
├── hotels.html               # صفحة الفنادق
├── hotel-details.html        # تفاصيل الفندق
└── results.html              # صفحة النتائج
```

## ⚙️ إعداد المشروع

### 1. استنساخ المشروع
```bash
git clone https://github.com/raqmatc/tourism-website.git
cd tourism-website
```

### 2. تشغيل الموقع محلياً
```bash
# باستخدام Python
python -m http.server 8000

# أو باستخدام Node.js
npx serve .

# ثم افتح http://localhost:8000
```

### 3. رفع على GitHub Pages
الموقع مُعد للعمل مع GitHub Pages تلقائياً. سيكون متاحاً على:
`https://raqmatc.github.io/tourism-website/`

## 🔧 تكوين RateHawk

### معلومات الحساب
- **البريد الإلكتروني**: 55114sa@gmail.com
- **معرف الشريك**: 282088.affiliate.dd55
- **رابط الشراكة**: https://www.zenhotels.com

### الروابط التابعة
```javascript
// رابط البحث العام
https://www.zenhotels.com/search?partner_id=282088.affiliate.dd55

// رابط مدينة محددة (مثال: الرياض)
https://www.zenhotels.com/search?destination=Riyadh&partner_id=282088.affiliate.dd55
```

## 📊 تتبع الأداء

### Google Analytics
```javascript
gtag('event', 'hotel_search', {
  'destination': destination,
  'checkin': checkin,
  'checkout': checkout,
  'partner': 'ratehawk'
});
```

### تتبع مخصص
```javascript
// إرسال بيانات التتبع لخادم مخصص
fetch('/api/analytics', {
  method: 'POST',
  body: JSON.stringify({
    event: 'hotel_search',
    data: searchData,
    partner: 'ratehawk'
  })
});
```

## 💰 إمكانيات الربح

### العمولات من RateHawk
- **معدل العمولة**: 5% - 8% حسب الحجم
- **الحد الأدنى للدفع**: $100
- **دورة الدفع**: شهرية
- **طرق الدفع**: تحويل بنكي، PayPal

### توقعات الدخل
| الزوار الشهريون | معدل التحويل | متوسط قيمة الحجز | الدخل المتوقع |
|-----------------|--------------|------------------|---------------|
| 1,000           | 2%           | $300             | $300          |
| 5,000           | 2.5%         | $350             | $2,187        |
| 10,000          | 3%           | $400             | $6,000        |
| 50,000          | 3.5%         | $450             | $39,375       |

## 🛠️ التطوير والصيانة

### إضافة مدن جديدة
```javascript
// في ملف ratehawk-integration.js
const POPULAR_CITIES = [
    'مدينة جديدة، البلد',
    // ... باقي المدن
];
```

### تحديث معرف الشريك
```javascript
// في ملف ratehawk-integration.js
const RATEHAWK_CONFIG = {
    partnerId: 'معرف-الشريك-الجديد',
    // ... باقي الإعدادات
};
```

### إضافة تتبع جديد
```javascript
// تتبع حدث مخصص
rateHawkIntegration.trackEvent('custom_event', {
    data: 'قيمة مخصصة'
});
```

## 🔍 تحسين محركات البحث (SEO)

### الكلمات المفتاحية المستهدفة
- حجز فنادق
- حجز فنادق رخيصة
- فنادق [اسم المدينة]
- عروض فنادق
- حجز أونلاين

### Meta Tags محسنة
```html
<title>Paygo.com - احجز فندقك المثالي مع RateHawk</title>
<meta name="description" content="احجز من أكثر من 2.7 مليون فندق حول العالم بأفضل الأسعار المضمونة">
<meta name="keywords" content="حجز فنادق, فنادق رخيصة, حجز أونلاين">
```

## 📱 التوافق مع الأجهزة

- ✅ أجهزة سطح المكتب
- ✅ الأجهزة اللوحية
- ✅ الهواتف الذكية
- ✅ جميع المتصفحات الحديثة

## 🚀 النشر والإطلاق

### GitHub Pages
```bash
# تفعيل GitHub Pages من إعدادات المستودع
# اختر main branch كمصدر
# الموقع سيكون متاحاً على:
# https://raqmatc.github.io/tourism-website/
```

### خادم مخصص
```bash
# رفع الملفات إلى خادم ويب
# تأكد من تفعيل HTTPS
# إعداد domain مخصص
```

## 📞 الدعم والمساعدة

### RateHawk Support
- **البريد الإلكتروني**: support@ratehawk.com
- **الهاتف**: متاح في لوحة التحكم
- **الدردشة المباشرة**: متاحة 24/7

### الوثائق التقنية
- [RateHawk API Documentation](https://docs.emergingtravel.com/)
- [Affiliate Program Guide](https://www.ratehawk.com/affiliate/)

## 📈 خطة التطوير المستقبلية

### المرحلة الأولى (الشهر الأول)
- [x] إعداد التكامل الأساسي مع RateHawk
- [x] تصميم واجهة المستخدم
- [x] نظام البحث والتوجيه
- [ ] اختبار شامل للوظائف

### المرحلة الثانية (الشهر الثاني)
- [ ] إضافة نظام تقييمات المستخدمين
- [ ] تحسين محركات البحث (SEO)
- [ ] إضافة المزيد من المدن العربية
- [ ] تطوير صفحات هبوط مخصصة

### المرحلة الثالثة (الشهر الثالث)
- [ ] تطبيق الهاتف المحمول
- [ ] نظام الولاء والمكافآت
- [ ] تكامل مع وسائل التواصل الاجتماعي
- [ ] لوحة تحكم للإحصائيات

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

## 🤝 المساهمة

نرحب بالمساهمات! يرجى قراءة [دليل المساهمة](CONTRIBUTING.md) قبل تقديم pull request.

## 📧 التواصل

- **البريد الإلكتروني**: raqmatc@gmail.com
- **GitHub**: [@raqmatc](https://github.com/raqmatc)
- **الموقع**: [paygo.com](https://raqmatc.github.io/tourism-website/)

---

**تم تطوير هذا المشروع بواسطة Manus AI لتوفير أفضل تجربة حجز فنادق للمستخدمين العرب** 🚀

