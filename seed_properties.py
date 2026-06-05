from database.connection import get_connection, sql_placeholder

properties = [
    {
        "name": "Nongsa Village Private Villa",
        "type": "Villa",
        "location": "Nongsa, Batam",
        "weekday_price": 1800000,
        "weekend_price": 2800000,
        "status": "available",
        "rating": 4.8,
        "facilities": "Private Pool,WiFi,AC,Dapur,Parkir,Balkon,View Laut",
        "max_guests": 8,
        "image_url": "img/properties/Nongsa Village Private Villa.jpg"
    },
    {
        "name": "Montigo Style Seaview Villa Nongsa",
        "type": "Villa",
        "location": "Nongsa, Batam",
        "weekday_price": 2500000,
        "weekend_price": 3800000,
        "status": "available",
        "rating": 4.9,
        "facilities": "Seaview,Private Pool,WiFi,AC,Kitchen,Parkir",
        "max_guests": 10,
        "image_url": "img/properties/Montigo Style Seaview Villa Nongsa.jpg"
    },
    {
        "name": "Turi Beach Pool Villa",
        "type": "Villa",
        "location": "Batam Center, Batam",
        "weekday_price": 1500000,
        "weekend_price": 2500000,
        "status": "available",
        "rating": 4.7,
        "facilities": "Pool,WiFi,AC,Kitchen,Parkir,View Laut",
        "max_guests": 6,
        "image_url": "img/properties/Turi Beach Pool Villa.jpg"
    },
    {
        "name": "Nuvasa Bay Sea View Apartment",
        "type": "Apartment",
        "location": "Nongsa, Batam",
        "weekday_price": 900000,
        "weekend_price": 1200000,
        "status": "available",
        "rating": 4.6,
        "facilities": "WiFi,AC,Parkir,Balkon,View Laut",
        "max_guests": 4,
        "image_url": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2"
    },
    {
        "name": "Nagoya Mansion City Apartment",
        "type": "Apartment",
        "location": "Nagoya, Batam",
        "weekday_price": 700000,
        "weekend_price": 950000,
        "status": "available",
        "rating": 4.5,
        "facilities": "WiFi,AC,Gym,Parkir",
        "max_guests": 3,
        "image_url": "img/properties/Nagoya Mansion City Apartment.jpg"
    },
    {
        "name": "Meisterstadt Batam Center Apartment",
        "type": "Apartment",
        "location": "Batam Center, Batam",
        "weekday_price": 650000,
        "weekend_price": 900000,
        "status": "available",
        "rating": 4.4,
        "facilities": "WiFi,AC,Parkir,Security",
        "max_guests": 3,
        "image_url": "https://images.unsplash.com/photo-1494526585095-c41746248156"
    },
    {
        "name": "Aston Batam Deluxe Room",
        "type": "HotelRoom",
        "location": "Batam Center, Batam",
        "weekday_price": 550000,
        "weekend_price": 750000,
        "status": "available",
        "rating": 4.3,
        "facilities": "WiFi,AC,Breakfast,Parkir",
        "max_guests": 2,
        "image_url": "img/properties/Aston Batam Deluxe Room.jpg"
    },
    {
        "name": "HARRIS Batam Center Room",
        "type": "HotelRoom",
        "location": "Batam Center, Batam",
        "weekday_price": 480000,
        "weekend_price": 680000,
        "status": "available",
        "rating": 4.2,
        "facilities": "WiFi,AC,Breakfast,Parkir",
        "max_guests": 2,
        "image_url": "img/properties/HARRIS Batam Center Room.jpg"
    },
    {
        "name": "Swiss-Belhotel Harbour Bay Room",
        "type": "HotelRoom",
        "location": "Harbour Bay, Batam",
        "weekday_price": 750000,
        "weekend_price": 1100000,
        "status": "available",
        "rating": 4.5,
        "facilities": "WiFi,AC,Sea View,Breakfast,Parkir",
        "max_guests": 2,
        "image_url": "img/properties/Swiss-Belhotel Harbour Bay Room.jpg"
    }
]

def main():
    ph = sql_placeholder()

    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute("DELETE FROM payments")
        cur.execute("DELETE FROM bookings")
        cur.execute("DELETE FROM properties")

        stmt = f"""
        INSERT INTO properties
        (name, type, location, weekday_price, weekend_price, status, rating, facilities, max_guests, image_url)
        VALUES ({','.join([ph] * 10)})
        """

        data = [
            (
                p["name"], p["type"], p["location"], p["weekday_price"],
                p["weekend_price"], p["status"], p["rating"],
                p["facilities"], p["max_guests"], p["image_url"]
            )
            for p in properties
        ]

        cur.executemany(stmt, data)

    print("Seed property berhasil diperbarui.")

if __name__ == "__main__":
    main()