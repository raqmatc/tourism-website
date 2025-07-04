document.getElementById('searchButton').addEventListener('click', function() {
    // جمع البيانات من الحقول
    const city = document.getElementById('city').value;
    const checkIn = document.getElementById('checkIn').value;
    const checkOut = document.getElementById('checkOut').value;
    const rooms = document.getElementById('rooms').value;
    const guests = document.getElementById('guests').value;

    // التحقق من أن الحقول ليست فارغة
    if (!city || !checkIn || !checkOut) {
        alert('يرجى ملء جميع الحقول الأساسية!');
        return;
    }

    // إعداد الطلب
    const apiUrl = 'https://demandapi-sandbox.booking.com/3.1/accommodations/search'; // بيئة الاختبار
    const apiToken = 'UspRLCHI82AtaL2AsflFSLYxrRh0asMB'; // API Key الخاص بيك
    const affiliateId = '0'; // استبدل برقم Affiliate ID لو عندك

    const headers = {
        'Authorization': `Bearer ${apiToken}`, // استخدام API Key كـ Bearer Token
        'Content-Type': 'application/json',
        'X-Affiliate-Id': affiliateId
    };

    const data = {
        booker: {
            country: 'sa' // يمكنك تغييره حسب بلد المستخدم
        },
        currency: 'SAR', // يمكنك تغييره حسب العملة
        filters: {
            maximum_results: 10,
            language: 'ar'
        },
        route: {
            pickup: {
                datetime: checkIn + 'T12:00:00',
                location: {
                    city: city
                }
            },
            dropoff: {
                datetime: checkOut + 'T12:00:00',
                location: {
                    city: city
                }
            }
        }
    };

    // إرسال الطلب
    fetch(apiUrl, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('خطأ في الاتصال بالـ API: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        if (data.data && data.data.length > 0) {
            const queryString = `?city=${encodeURIComponent(city)}&checkIn=${checkIn}&checkOut=${checkOut}&rooms=${rooms}&guests=${guests}`;
            window.location.href = `results.html${queryString}`;
        } else {
            alert('لا توجد فنادق متاحة بناءً على بحثك!');
        }
    })
    .catch(error => {
        console.error('خطأ:', error);
        alert('حدث خطأ أثناء البحث. حاول مرة أخرى. التفاصيل: ' + error.message);
    });
});
