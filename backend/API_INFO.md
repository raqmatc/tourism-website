# Booking.com API Information

## API Details
- **API Name**: Booking COM
- **Provider**: ntd119 on RapidAPI
- **Host**: booking-com18.p.rapidapi.com
- **Base URL**: https://booking-com18.p.rapidapi.com

## Endpoints

### 1. Search Locations (Auto-complete)
**Endpoint**: `GET /stays/auto-complete`

**Parameters**:
- `query` (required, string): Destination name (e.g., "New York", "Dubai")
- `languageCode` (optional, string): Language code (default: "en-us")

**Example**:
```
GET https://booking-com18.p.rapidapi.com/stays/auto-complete?query=Dubai&languageCode=ar
```

**Response**: Returns list of locations with:
- `dest_id`: Destination ID (used for hotel search)
- `dest_type`: Type (city, region, hotel, etc.)
- `name`: Location name
- Other location details

---

### 2. Search Hotels
**Endpoint**: `GET /stays/search`

**Parameters**:
- `dest_id` (required, string): Destination ID from auto-complete
- `arrival_date` (required, string): Check-in date (YYYY-MM-DD)
- `departure_date` (required, string): Check-out date (YYYY-MM-DD)
- `adults` (optional, number): Number of adults (default: 2)
- `room_qty` (optional, number): Number of rooms (default: 1)
- `units` (optional, string): Measurement units (metric/imperial)
- `temperature_unit` (optional, string): Temperature unit (c/f)
- `languagecode` (optional, string): Language code (default: en-us)
- `currency_code` (optional, string): Currency code (default: USD)

**Example**:
```
GET https://booking-com18.p.rapidapi.com/stays/search?dest_id=-782831&arrival_date=2025-12-09&departure_date=2025-12-10&adults=2&room_qty=1&languagecode=ar&currency_code=SAR
```

---

### 3. Get Hotel Details
**Endpoint**: `GET /stays/detail`

**Parameters**:
- `hotel_id` (required, string): Hotel ID from search results
- `arrival_date` (required, string): Check-in date
- `departure_date` (required, string): Check-out date
- `adults` (optional, number): Number of adults
- `room_qty` (optional, number): Number of rooms
- `languagecode` (optional, string): Language code
- `currency_code` (optional, string): Currency code

---

### 4. Get Hotel Reviews
**Endpoint**: `GET /stays/reviews`

**Parameters**:
- `hotel_id` (required, string): Hotel ID
- `languagecode` (optional, string): Language code

---

## Headers Required
```
x-rapidapi-host: booking-com18.p.rapidapi.com
x-rapidapi-key: YOUR_API_KEY
```

## Pricing Plans
- **BASIC**: $0.00/mo (limited requests)
- **PRO**: $15.00/mo
- **ULTRA**: $35.00/mo
- **MEGA**: $100.00/mo

## Notes
- All endpoints use GET method (not POST as currently implemented)
- The API returns real-time data from Booking.com
- Need to subscribe to a plan on RapidAPI to use the API
- The current API key needs to be verified and subscribed to the correct plan
