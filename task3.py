
import sqlite3

conn = sqlite3.connect("bus_booking.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger TEXT NOT NULL,
    route TEXT NOT NULL,
    seat INTEGER NOT NULL,
    UNIQUE(route, seat)
)
""")
conn.commit()

buses = {
    "1": ("Bengaluru to Mysuru", 30),
    "2": ("Bengaluru to Mangaluru", 40),
    "3": ("Mysuru to Bengaluru", 30)
}

while True:
    print("\n=== BUS TICKET RESERVATION ===")
    print("1. Search bus routes")
    print("2. Book a seat")
    print("3. View bookings")
    print("4. Cancel booking")
    print("5. Exit")

    choice = input("Choose option: ")

    if choice == "1":
        for key, bus in buses.items():
            print(key, bus[0], "| Total seats:", bus[1])

    elif choice == "2":
        for key, bus in buses.items():
            print(key, bus[0])

        route_key = input("Enter route number: ")

        if route_key not in buses:
            print("Invalid route!")
            continue

        route = buses[route_key][0]
        passenger = input("Passenger name: ").strip()

        if not passenger:
            print("Name cannot be empty!")
            continue

        try:
            seat = int(input("Choose seat number: "))
        except ValueError:
            print("Enter a valid seat number!")
            continue

        if seat < 1 or seat > buses[route_key][1]:
            print("Invalid seat number!")
            continue

        try:
            cursor.execute(
                "INSERT INTO bookings (passenger, route, seat) VALUES (?, ?, ?)",
                (passenger, route, seat)
            )
            conn.commit()
            print("Booking successful!")
        except sqlite3.IntegrityError:
            print("Sorry, this seat is already booked!")

    elif choice == "3":
        cursor.execute("SELECT * FROM bookings")
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No bookings found.")

    elif choice == "4":
        try:
            booking_id = int(input("Enter booking ID to cancel: "))
            cursor.execute(
                "DELETE FROM bookings WHERE id = ?", (booking_id,)
            )
            conn.commit()

            if cursor.rowcount:
                print("Booking cancelled.")
            else:
                print("Booking ID not found.")
        except ValueError:
            print("Enter a valid booking ID!")

    elif choice == "5":
        break

    else:
        print("Invalid option!")

conn.close()
print("Thank you!")
