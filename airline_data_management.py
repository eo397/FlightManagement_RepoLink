import sqlite3

DB = "airline_database.db"

# =============================================
# DATABASE CLASS
# =============================================

class DBOperations:

    def __init__(self):
        try:
            # Establish initial connection to SQLite database
            self.conn = sqlite3.connect(DB)
            self.cur = self.conn.cursor()

            # Enable foreign key constraints
            self.conn.execute("PRAGMA foreign_keys = ON")

            # Create tables and insert sample data
            self._create_tables()
            self._insert_sample_data()
            self.conn.commit()
        except Exception as e:
            print("Initialization error:", e)
        finally:
            self.conn.close()

    def get_connection(self):
        # Opens a new connection whenever a method is called
        self.conn = sqlite3.connect(DB)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cur = self.conn.cursor()

    # -----------------------------------------------------
    # CREATING THE TABLES
    # -----------------------------------------------------
    def _create_tables(self):
        # Creates all required database tables if they do not exist
        # These create structure and define the relationships

        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS airports (
                airport_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                airport_name TEXT NOT NULL,
                iata_code    TEXT NOT NULL UNIQUE,
                city         TEXT NOT NULL,
                country      TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS aircraft (
                aircraft_id      INTEGER PRIMARY KEY AUTOINCREMENT,
                model            TEXT NOT NULL,
                total_seats      INTEGER,
                manufacture_year INTEGER
            );

            CREATE TABLE IF NOT EXISTS pilots (
                pilot_id        INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name      TEXT NOT NULL,
                last_name       TEXT NOT NULL,
                licence_number  TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS flights (
                flight_id          INTEGER PRIMARY KEY AUTOINCREMENT,
                aircraft_id        INTEGER,
                pilot_id           INTEGER,
                flight_number      TEXT NOT NULL,
                departure_airport  INTEGER NOT NULL,
                arrival_airport    INTEGER NOT NULL,
                departure_datetime TEXT NOT NULL,
                arrival_datetime   TEXT NOT NULL,
                status             TEXT NOT NULL DEFAULT 'scheduled',
                FOREIGN KEY (aircraft_id)       REFERENCES aircraft(aircraft_id),
                FOREIGN KEY (pilot_id)          REFERENCES pilots(pilot_id),
                FOREIGN KEY (departure_airport) REFERENCES airports(airport_id),
                FOREIGN KEY (arrival_airport)   REFERENCES airports(airport_id)
            );

            CREATE TABLE IF NOT EXISTS passengers (
                passenger_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name      TEXT NOT NULL,
                last_name       TEXT NOT NULL,
                passport_number TEXT UNIQUE,
                email           TEXT UNIQUE,
                contact         TEXT
            );

            CREATE TABLE IF NOT EXISTS bookings (
                booking_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_id    INTEGER NOT NULL,
                passenger_id INTEGER NOT NULL,
                booking_date TEXT NOT NULL,
                seat_number  TEXT,
                cabin_class  TEXT NOT NULL,
                FOREIGN KEY (flight_id)    REFERENCES flights(flight_id),
                FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id)
            );
        """)

    # -------------------------------------------------------------------
    # INSERTING DATA
    # The Data generated with the help of Claude Code AI (Anthropic,2026)
    # This data is only a simulation and not real data
    # -------------------------------------------------------------------
    def _insert_sample_data(self):
        # Inserts sample data into tables (only if empty)

        # airports
        # Checks if airports table already has data
        self.cur.execute("SELECT COUNT(*) FROM airports")
        if self.cur.fetchone()[0] == 0:
            airports = [
                ("Heathrow Airport",            "LHR", "London",       "United Kingdom"),
                ("Charles de Gaulle Airport",   "CDG", "Paris",        "France"),
                ("Dubai International Airport", "DXB", "Dubai",        "UAE"),
                ("JFK International Airport",   "JFK", "New York",     "USA"),
                ("OR Tambo International",      "JNB", "Johannesburg", "South Africa"),
                ("Jomo Kenyatta International", "NBO", "Nairobi",      "Kenya"),
                ("Murtala Mohammed Airport",    "LOS", "Lagos",        "Nigeria"),
                ("Frankfurt Airport",           "FRA", "Frankfurt",    "Germany"),
                ("Singapore Changi Airport",    "SIN", "Singapore",    "Singapore"),
                ("Tokyo Narita Airport",        "NRT", "Tokyo",        "Japan"),
                ("Sydney Airport",              "SYD", "Sydney",       "Australia"),
                ("Toronto Pearson Airport",     "YYZ", "Toronto",      "Canada"),
                ("Cairo International Airport", "CAI", "Cairo",        "Egypt"),
                ("King Khalid Airport",         "RUH", "Riyadh",       "Saudi Arabia"),
                ("Istanbul Airport",            "IST", "Istanbul",     "Turkey"),
            ]
            self.cur.executemany(
                # Insert airport data
                "INSERT INTO airports (airport_name, iata_code, city, country) VALUES (?,?,?,?)",
                airports
            )

        # aircraft
        self.cur.execute("SELECT COUNT(*) FROM aircraft")
        if self.cur.fetchone()[0] == 0:
            aircraft = [
                ("Boeing 777",   396, 2015),
                ("Airbus A380",  555, 2018),
                ("Boeing 737",   189, 2019),
                ("Airbus A320",  180, 2020),
                ("Boeing 787",   296, 2017),
                ("Airbus A350",  325, 2021),  
            ]
            self.cur.executemany(
                "INSERT INTO aircraft (model, total_seats, manufacture_year) VALUES (?,?,?)",
                aircraft
            )

        # pilots
        self.cur.execute("SELECT COUNT(*) FROM pilots")
        if self.cur.fetchone()[0] == 0:
            pilots = [
                ("James",   "Okoro",   "ATPL-001-NG"),
                ("Sarah",   "Mitchell","ATPL-002-UK"),
                ("Ahmed",   "Al-Farsi","ATPL-003-AE"),
                ("Priya",   "Sharma",  "ATPL-004-IN"),
                ("Carlos",  "Mendes",  "ATPL-005-BR"),
                ("Amara",   "Diallo",  "ATPL-006-GH"),
            ]
            self.cur.executemany(
                "INSERT INTO pilots (first_name, last_name, licence_number) VALUES (?,?,?)",
                pilots
            )

        # flights
        self.cur.execute("SELECT COUNT(*) FROM flights")
        if self.cur.fetchone()[0] == 0:
            flights = [
                (1, 1, "FM100", 1,  4,  "2025-06-01 06:00", "2025-06-01 15:00", "landed"),
                (2, 2, "FM101", 1,  3,  "2025-06-01 08:00", "2025-06-01 16:00", "landed"),
                (3, 3, "FM102", 2,  9,  "2025-06-02 10:00", "2025-06-02 20:00", "landed"),
                (4, 4, "FM103", 3,  6,  "2025-06-02 12:00", "2025-06-02 19:00", "landed"),
                (5, 5, "FM104", 4,  7,  "2025-06-03 06:00", "2025-06-03 14:00", "departed"),
                (6, 6, "FM105", 5,  1,  "2025-06-03 08:00", "2025-06-03 18:00", "departed"),
                (1, 1, "FM106", 6,  2,  "2025-06-04 10:00", "2025-06-04 21:00", "scheduled"),
                (2, 2, "FM107", 7,  10, "2025-06-04 14:00", "2025-06-05 02:00", "scheduled"),
                (3, 3, "FM108", 8,  11, "2025-06-05 06:00", "2025-06-05 22:00", "scheduled"),
                (4, 4, "FM109", 9,  12, "2025-06-05 08:00", "2025-06-05 18:00", "scheduled"),
                (5, 5, "FM110", 10, 13, "2025-06-06 10:00", "2025-06-06 17:00", "scheduled"),
                (6, 6, "FM111", 11, 14, "2025-06-06 12:00", "2025-06-06 20:00", "scheduled"),
                (1, 1, "FM112", 12, 15, "2025-06-07 06:00", "2025-06-07 14:00", "scheduled"),
                (2, 2, "FM113", 13, 16, "2025-06-07 08:00", "2025-06-07 18:00", "scheduled"),
                (3, 3, "FM114", 14, 17, "2025-06-08 10:00", "2025-06-08 22:00", "scheduled"),
                (4, 4, "FM115", 15, 18, "2025-06-08 14:00", "2025-06-09 02:00", "scheduled"),
                (5, 5, "FM116", 16, 19, "2025-06-09 06:00", "2025-06-09 18:00", "scheduled"),
                (6, 6, "FM117", 17, 20, "2025-06-09 08:00", "2025-06-09 20:00", "scheduled"),
                (1, 1, "FM118", 18, 1,  "2025-06-10 10:00", "2025-06-10 21:00", "scheduled"),
                (2, 2, "FM119", 19, 2,  "2025-06-10 12:00", "2025-06-10 20:00", "scheduled"),
                (3, 3, "FM120", 20, 3,  "2025-06-11 06:00", "2025-06-11 14:00", "scheduled"),
                (4, 4, "FM121", 1,  5,  "2025-06-11 08:00", "2025-06-11 18:00", "delayed"),
                (5, 5, "FM122", 2,  6,  "2025-06-11 10:00", "2025-06-11 20:00", "scheduled"),
                (6, 6, "FM123", 3,  7,  "2025-06-12 06:00", "2025-06-12 14:00", "scheduled"),
                (1, 1, "FM124", 4,  8,  "2025-06-12 08:00", "2025-06-12 16:00", "scheduled"),
                (2, 2, "FM125", 5,  9,  "2025-06-12 10:00", "2025-06-12 22:00", "scheduled"),
                (3, 3, "FM126", 6,  10, "2025-06-13 06:00", "2025-06-13 18:00", "scheduled"),
                (4, 4, "FM127", 7,  11, "2025-06-13 08:00", "2025-06-13 20:00", "scheduled"),
                (5, 5, "FM128", 8,  12, "2025-06-13 10:00", "2025-06-13 22:00", "scheduled"),
                (6, 6, "FM129", 9,  13, "2025-06-13 12:00", "2025-06-13 20:00", "delayed"),
                (1, 1, "FM130", 10, 14, "2025-06-14 06:00", "2025-06-14 18:00", "scheduled"),
                (2, 2, "FM131", 11, 15, "2025-06-14 08:00", "2025-06-14 16:00", "scheduled"),
                (3, 3, "FM132", 12, 16, "2025-06-14 10:00", "2025-06-14 20:00", "scheduled"),
            ]
            self.cur.executemany("""
                INSERT INTO flights (
                    aircraft_id, pilot_id, flight_number,
                    departure_airport, arrival_airport,
                    departure_datetime, arrival_datetime, status
                ) VALUES (?,?,?,?,?,?,?,?)
            """, flights)

        # passengers
        self.cur.execute("SELECT COUNT(*) FROM passengers")
        if self.cur.fetchone()[0] == 0:
            passengers = [
                ("John",    "Smith",    "PP100000", "john.smith0@email.com",     "+1-555-1000"),
                ("Mary",    "Johnson",  "PP100001", "mary.johnson1@email.com",   "+1-555-1001"),
                ("Ali",     "Khan",     "PP100002", "ali.khan2@email.com",       "+1-555-1002"),
                ("Fatima",  "Okafor",   "PP100003", "fatima.okafor3@email.com",  "+1-555-1003"),
                ("Chen",    "Wong",     "PP100004", "chen.wong4@email.com",      "+1-555-1004"),
                ("Yuki",    "Tanaka",   "PP100005", "yuki.tanaka5@email.com",    "+1-555-1005"),
                ("Carlos",  "Mendes",   "PP100006", "carlos.mendes6@email.com",  "+1-555-1006"),
                ("Amara",   "Diallo",   "PP100007", "amara.diallo7@email.com",   "+1-555-1007"),
                ("Sofia",   "Rossi",    "PP100008", "sofia.rossi8@email.com",    "+1-555-1008"),
                ("David",   "Brown",    "PP100009", "david.brown9@email.com",    "+1-555-1009"),
                ("Grace",   "Kimani",   "PP100010", "grace.kimani10@email.com",  "+1-555-1010"),
                ("Omar",    "Al-Said",  "PP100011", "omar.alsaid11@email.com",   "+1-555-1011"),
                ("Nina",    "Petrov",   "PP100012", "nina.petrov12@email.com",   "+1-555-1012"),
                ("Ravi",    "Patel",    "PP100013", "ravi.patel13@email.com",    "+1-555-1013"),
                ("Lucia",   "Garcia",   "PP100014", "lucia.garcia14@email.com",  "+1-555-1014"),
                ("Hassan",  "Muller",   "PP100015", "hassan.muller15@email.com", "+1-555-1015"),
                ("Emma",    "Dupont",   "PP100016", "emma.dupont16@email.com",   "+1-555-1016"),
                ("Kwame",   "Asante",   "PP100017", "kwame.asante17@email.com",  "+1-555-1017"),
                ("Aisha",   "Ibrahim",  "PP100018", "aisha.ibrahim18@email.com", "+1-555-1018"),
                ("James",   "Nkosi",    "PP100019", "james.nkosi19@email.com",   "+1-555-1019"),
                ("Lena",    "Schmidt",  "PP100020", "lena.schmidt20@email.com",  "+1-555-1020"),
                ("Pedro",   "Alvarez",  "PP100021", "pedro.alvarez21@email.com", "+1-555-1021"),
                ("Mei",     "Chen",     "PP100022", "mei.chen22@email.com",      "+1-555-1022"),
                ("Tariq",   "Hassan",   "PP100023", "tariq.hassan23@email.com",  "+1-555-1023"),
                ("Anna",    "Kowalski", "PP100024", "anna.kowalski24@email.com", "+1-555-1024"),
                ("Kofi",    "Mensah",   "PP100025", "kofi.mensah25@email.com",   "+1-555-1025"),
                ("Zara",    "Ahmed",    "PP100026", "zara.ahmed26@email.com",    "+1-555-1026"),
                ("Liam",    "Murphy",   "PP100027", "liam.murphy27@email.com",   "+1-555-1027"),
                ("Hana",    "Park",     "PP100028", "hana.park28@email.com",     "+1-555-1028"),
                ("Diego",   "Torres",   "PP100029", "diego.torres29@email.com",  "+1-555-1029"),
                ("Chioma",  "Eze",      "PP100030", "chioma.eze30@email.com",    "+1-555-1030"),
                ("Ivan",    "Volkov",   "PP100031", "ivan.volkov31@email.com",   "+1-555-1031"),
                ("Sakura",  "Yamamoto", "PP100032", "sakura.yamamoto32@email.com","+1-555-1032"),
                ("Khalid",  "Al-Rashid","PP100033", "khalid.alrashid33@email.com","+1-555-1033"),
                ("Claire",  "Dubois",   "PP100034", "claire.dubois34@email.com", "+1-555-1034"),
                ("Emeka",   "Obi",      "PP100035", "emeka.obi35@email.com",     "+1-555-1035"),
                ("Ingrid",  "Hansen",   "PP100036", "ingrid.hansen36@email.com", "+1-555-1036"),
                ("Wei",     "Zhang",    "PP100037", "wei.zhang37@email.com",     "+1-555-1037"),
                ("Fatou",   "Sow",      "PP100038", "fatou.sow38@email.com",     "+1-555-1038"),
                ("Marco",   "Bianchi",  "PP100039", "marco.bianchi39@email.com", "+1-555-1039"),
                ("Nia",     "Williams", "PP100040", "nia.williams40@email.com",  "+1-555-1040"),
                ("Arjun",   "Singh",    "PP100041", "arjun.singh41@email.com",   "+1-555-1041"),
                ("Leila",   "Nasser",   "PP100042", "leila.nasser42@email.com",  "+1-555-1042"),
                ("Bruno",   "Costa",    "PP100043", "bruno.costa43@email.com",   "+1-555-1043"),
                ("Akira",   "Sato",     "PP100044", "akira.sato44@email.com",    "+1-555-1044"),
                ("Nadia",   "Ivanova",  "PP100045", "nadia.ivanova45@email.com", "+1-555-1045"),
            ]
            self.cur.executemany(
                "INSERT INTO passengers (first_name, last_name, passport_number, email, contact) VALUES (?,?,?,?,?)",
                passengers
            )

        # bookings
        self.cur.execute("SELECT COUNT(*) FROM bookings")
        if self.cur.fetchone()[0] == 0:
            bookings = [
                (1,  1,  "2025-06-01", "12A", "economy"),
                (1,  2,  "2025-06-01", "14B", "economy"),
                (1,  3,  "2025-06-01", "16C", "business"),
                (2,  4,  "2025-06-01", "2A",  "first"),
                (2,  5,  "2025-06-01", "4B",  "economy"),
                (2,  6,  "2025-06-01", "6C",  "economy"),
                (3,  7,  "2025-06-02", "8A",  "business"),
                (3,  8,  "2025-06-02", "10B", "economy"),
                (3,  9,  "2025-06-02", "12C", "economy"),
                (4,  10, "2025-06-02", "1A",  "first"),
                (4,  11, "2025-06-02", "3B",  "economy"),
                (4,  12, "2025-06-02", "5C",  "economy"),
                (5,  13, "2025-06-03", "7A",  "business"),
                (5,  14, "2025-06-03", "9B",  "economy"),
                (5,  15, "2025-06-03", "11C", "economy"),
                (6,  16, "2025-06-03", "13A", "economy"),
                (6,  17, "2025-06-03", "15B", "first"),
                (6,  18, "2025-06-03", "17C", "economy"),
                (7,  19, "2025-06-04", "2A",  "economy"),
                (7,  20, "2025-06-04", "4B",  "business"),
                (7,  21, "2025-06-04", "6C",  "economy"),
                (8,  22, "2025-06-04", "8A",  "economy"),
                (8,  23, "2025-06-04", "10B", "economy"),
                (8,  24, "2025-06-04", "12C", "first"),
                (9,  25, "2025-06-05", "1A",  "economy"),
                (9,  26, "2025-06-05", "3B",  "economy"),
                (9,  27, "2025-06-05", "5C",  "business"),
                (10, 28, "2025-06-05", "7A",  "economy"),
                (10, 29, "2025-06-05", "9B",  "economy"),
                (10, 30, "2025-06-05", "11C", "economy"),
                (11, 31, "2025-06-06", "13A", "first"),
                (11, 32, "2025-06-06", "15B", "economy"),
                (11, 33, "2025-06-06", "17C", "economy"),
                (12, 34, "2025-06-06", "2A",  "business"),
                (12, 35, "2025-06-06", "4B",  "economy"),
                (12, 36, "2025-06-06", "6C",  "economy"),
                (13, 37, "2025-06-07", "8A",  "economy"),
                (13, 38, "2025-06-07", "10B", "economy"),
                (13, 39, "2025-06-07", "12C", "first"),
                (14, 40, "2025-06-07", "1A",  "economy"),
                (14, 41, "2025-06-07", "3B",  "business"),
                (14, 42, "2025-06-07", "5C",  "economy"),
                (15, 43, "2025-06-08", "7A",  "economy"),
                (15, 44, "2025-06-08", "9B",  "economy"),
                (15, 45, "2025-06-08", "11C", "economy"),
                (16, 46, "2025-06-08", "13A", "first"),
                (16, 47, "2025-06-08", "15B", "economy"),
                (16, 48, "2025-06-08", "17C", "business"),
                (17, 49, "2025-06-09", "2A",  "economy"),
                (17, 50, "2025-06-09", "4B",  "economy"),
                (17, 51, "2025-06-09", "6C",  "economy"),
                (18, 52, "2025-06-09", "8A",  "first"),
                (18, 53, "2025-06-09", "10B", "economy"),
                (18, 54, "2025-06-09", "12C", "economy"),
                (19, 55, "2025-06-10", "1A",  "business"),
                (19, 56, "2025-06-10", "3B",  "economy"),
                (19, 57, "2025-06-10", "5C",  "economy"),
                (20, 58, "2025-06-10", "7A",  "economy"),
                (20, 59, "2025-06-10", "9B",  "first"),
                (20, 60, "2025-06-10", "11C", "economy"),
                (21, 61, "2025-06-11", "13A", "economy"),
                (21, 62, "2025-06-11", "15B", "economy"),
                (21, 63, "2025-06-11", "17C", "business"),
                (22, 64, "2025-06-11", "2A",  "economy"),
                (22, 65, "2025-06-11", "4B",  "economy"),
                (22, 66, "2025-06-11", "6C",  "first"),
                (23, 67, "2025-06-12", "8A",  "economy"),
                (23, 68, "2025-06-12", "10B", "economy"),
                (23, 69, "2025-06-12", "12C", "economy"),
                (24, 70, "2025-06-12", "1A",  "business"),
                (24, 71, "2025-06-12", "3B",  "economy"),
                (24, 72, "2025-06-12", "5C",  "economy"),
                (25, 73, "2025-06-12", "7A",  "first"),
                (25, 74, "2025-06-12", "9B",  "economy"),
                (25, 75, "2025-06-12", "11C", "economy"),
                (26, 76, "2025-06-13", "13A", "economy"),
                (26, 77, "2025-06-13", "15B", "business"),
                (26, 78, "2025-06-13", "17C", "economy"),
                (27, 79, "2025-06-13", "2A",  "economy"),
                (27, 80, "2025-06-13", "4B",  "economy"),
                (27, 81, "2025-06-13", "6C",  "first"),
                (28, 82, "2025-06-13", "8A",  "economy"),
                (28, 83, "2025-06-13", "10B", "economy"),
                (28, 84, "2025-06-13", "12C", "business"),
                (29, 85, "2025-06-13", "1A",  "economy"),
                (29, 86, "2025-06-13", "3B",  "economy"),
                (29, 87, "2025-06-13", "5C",  "economy"),
                (30, 88, "2025-06-13", "7A",  "first"),
                (30, 89, "2025-06-13", "9B",  "economy"),
                (30, 90, "2025-06-13", "11C", "economy"),
                (31, 91, "2025-06-14", "13A", "economy"),
                (31, 92, "2025-06-14", "15B", "business"),
                (31, 93, "2025-06-14", "17C", "economy"),
                (32, 94, "2025-06-14", "2A",  "economy"),
                (32, 95, "2025-06-14", "4B",  "first"),
                (32, 96, "2025-06-14", "6C",  "economy"),
                (33, 97, "2025-06-14", "8A",  "economy"),
                (33, 98, "2025-06-14", "10B", "economy"),
                (33, 99, "2025-06-14", "12C", "business"),
                (34, 100, "2025-06-14", "1A",  "economy"),
                (34, 1,   "2025-06-14", "3B",  "economy"),
                (34, 2,   "2025-06-14", "5C",  "first"),
            ]
            self.cur.executemany(
                "INSERT INTO bookings (flight_id, passenger_id, booking_date, seat_number, cabin_class) VALUES (?,?,?,?,?)",
                bookings
            )


    # =============================================
    # FLIGHTS
    # =============================================

    def view_all_flights(self):
        try:
            self.get_connection()

            # SQL query to retrieve all flights with airport codes
            self.cur.execute("""
                SELECT f.flight_id, f.flight_number,
                       a1.iata_code, a2.iata_code,
                       f.departure_datetime, f.arrival_datetime, f.status
                FROM flights f
                JOIN airports a1 ON f.departure_airport = a1.airport_id 
                JOIN airports a2 ON f.arrival_airport   = a2.airport_id
                ORDER BY f.departure_datetime
            """)
            rows = self.cur.fetchall()

            if not rows:
                print("  No flights found.")
                return

            print("\n{:<5} {:<8} {:<6} {:<6} {:<18} {:<18} {:<12}".format(
                "ID", "Flight", "From", "To", "Departure", "Arrival", "Status"))
            print("-" * 80)
            for r in rows:
                print("{:<5} {:<8} {:<6} {:<6} {:<18} {:<18} {:<12}".format(*r))
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    def search_flight(self):
        try:
            self.get_connection()
            fid = int(input("  Flight ID: "))
            self.cur.execute("""
                SELECT f.flight_id, f.flight_number,
                       a1.iata_code, a2.iata_code,
                       f.departure_datetime, f.arrival_datetime, f.status
                FROM flights f
                JOIN airports a1 ON f.departure_airport = a1.airport_id
                JOIN airports a2 ON f.arrival_airport   = a2.airport_id
                WHERE f.flight_id = ?
            """, (fid,))
            r = self.cur.fetchone()
            if r:
                labels = ["Flight ID", "Flight No", "From", "To", "Departure", "Arrival", "Status"]
                for label, val in zip(labels, r):
                    print(f"  {label:<12}: {val}")
            else:
                print("  Flight not found.")
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    def add_flight(self):
        try:
            self.get_connection()

            # Takes user input and inserts a new flight into database
            self.cur.execute("SELECT aircraft_id, model FROM aircraft")
            print("\n  Aircraft:")
            for r in self.cur.fetchall():
                print(f"  {r[0]}. {r[1]}")

            self.cur.execute("SELECT pilot_id, first_name, last_name FROM pilots")
            print("\n  Pilots:")
            for r in self.cur.fetchall():
                print(f"  {r[0]}. {r[1]} {r[2]}")

            self.cur.execute("SELECT airport_id, iata_code, city FROM airports")
            print("\n  Airports:")
            for r in self.cur.fetchall():
                print(f"  {r[0]}. {r[1]} - {r[2]}")

            flight_number = input("\n  Flight number: ")
            aircraft_id   = int(input("  Aircraft ID: "))
            pilot_id      = int(input("  Pilot ID: "))
            dep_airport   = int(input("  Departure airport ID: "))
            arr_airport   = int(input("  Arrival airport ID: "))
            dep_dt        = input("  Departure (YYYY-MM-DD HH:MM): ")
            arr_dt        = input("  Arrival   (YYYY-MM-DD HH:MM): ")
            status        = input("  Status ") or "scheduled"

            self.cur.execute("""
                INSERT INTO flights
                (aircraft_id, pilot_id, flight_number,
                 departure_airport, arrival_airport,
                 departure_datetime, arrival_datetime, status)
                VALUES (?,?,?,?,?,?,?,?)
            """, (aircraft_id, pilot_id, flight_number,
                  dep_airport, arr_airport, dep_dt, arr_dt, status))
            self.conn.commit()
            print("  Flight added.")
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    def update_departure_time(self):
        try:
            self.get_connection()
            fid = int(input("  Flight ID: "))
            new_dt = input("  New departure (YYYY-MM-DD HH:MM): ")
            self.cur.execute(
                "UPDATE flights SET departure_datetime=? WHERE flight_id=?",
                (new_dt, fid))
            self.conn.commit()
            print(f"  {self.cur.rowcount} row(s) updated." if self.cur.rowcount else "  Not found.")
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    def update_flight_status(self):
        try:
            self.get_connection()
            fid = int(input("  Flight ID: "))
            status = input("  New status (scheduled/departed/landed/delayed/cancelled): ")

            # Updates flight status (e.g. scheduled, delayed, landed)
            self.cur.execute(
                "UPDATE flights SET status=? WHERE flight_id=?", (status, fid))
            self.conn.commit()
            print(f"  {self.cur.rowcount} row(s) updated." if self.cur.rowcount else "  Not found.")
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    def delete_flight(self):
        try:
            self.get_connection()
            fid = int(input("  Flight ID to delete: "))

            # Deletes a specific flight using its ID
            self.cur.execute("DELETE FROM flights WHERE flight_id=?", (fid,))
            self.conn.commit()
            print(f"  {self.cur.rowcount} row(s) deleted." if self.cur.rowcount else "  Not found.")
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    # =============================================
    # PILOTS
    # =============================================

    def view_all_pilots(self):
        try:
            self.get_connection()
            self.cur.execute(
                "SELECT pilot_id, first_name, last_name, licence_number FROM pilots")
            rows = self.cur.fetchall()

            if not rows:
                print("  No pilots found.")
                return

            print("\n{:<5} {:<12} {:<12} {:<15}".format("ID", "First", "Last", "Licence"))
            print("-" * 50)
            for r in rows:
                print("{:<5} {:<12} {:<12} {:<15}".format(*r))
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    def assign_pilot(self):
        try:
            self.get_connection()
            self.cur.execute("SELECT pilot_id, first_name, last_name FROM pilots")
            print("\n  Pilots:")
            for r in self.cur.fetchall():
                print(f"  {r[0]}. {r[1]} {r[2]}")

            fid = int(input("\n  Flight ID: "))
            pid = int(input("  Pilot ID: "))

            self.cur.execute(
                "UPDATE flights SET pilot_id=? WHERE flight_id=?", (pid, fid))
            self.conn.commit()
            print("  Pilot assigned." if self.cur.rowcount else "  Flight not found.")
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    def view_pilot_schedule(self):
        try:
            self.get_connection()
            self.cur.execute("SELECT pilot_id, first_name, last_name FROM pilots")
            print("\n  Pilots:")
            for r in self.cur.fetchall():
                print(f"  {r[0]}. {r[1]} {r[2]}")

            pid = int(input("\n  Pilot ID: "))
            self.cur.execute("""
                SELECT f.flight_id, f.flight_number,
                       a1.iata_code, a2.iata_code,
                       f.departure_datetime, f.status
                FROM flights f
                JOIN airports a1 ON f.departure_airport = a1.airport_id
                JOIN airports a2 ON f.arrival_airport   = a2.airport_id
                WHERE f.pilot_id = ?
                ORDER BY f.departure_datetime
            """, (pid,))
            rows = self.cur.fetchall()

            if rows:
                print("\n{:<5} {:<8} {:<6} {:<6} {:<18} {:<12}".format(
                    "ID", "Flight", "From", "To", "Departure", "Status"))
                print("-" * 62)
                for r in rows:
                    print("{:<5} {:<8} {:<6} {:<6} {:<18} {:<12}".format(*r))
            else:
                print("  No flights found for this pilot.")
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    # =============================================
    # BOOKINGS
    # =============================================

    def view_all_bookings(self):
        try:
            self.get_connection()
            self.cur.execute("""
                SELECT b.booking_id, f.flight_number,
                       p.first_name || ' ' || p.last_name,
                       b.seat_number, b.cabin_class, b.booking_date
                FROM bookings b
                JOIN flights    f ON b.flight_id    = f.flight_id
                JOIN passengers p ON b.passenger_id = p.passenger_id
                ORDER BY b.booking_id
            """)
            rows = self.cur.fetchall()

            if not rows:
                print("  No bookings found.")
                return

            print("\n{:<6} {:<8} {:<20} {:<6} {:<10} {:<12}".format(
                "ID", "Flight", "Passenger", "Seat", "Cabin", "Date"))
            print("-" * 70)
            for r in rows:
                print("{:<6} {:<8} {:<20} {:<6} {:<10} {:<12}".format(*r))
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    def add_booking(self):
        try:
            self.get_connection()
            self.cur.execute("""
                SELECT f.flight_id, f.flight_number, a1.iata_code, a2.iata_code
                FROM flights f
                JOIN airports a1 ON f.departure_airport = a1.airport_id
                JOIN airports a2 ON f.arrival_airport   = a2.airport_id
            """)
            print("\n  Flights:")
            for r in self.cur.fetchall():
                print(f"  {r[0]}. {r[1]} ({r[2]} -> {r[3]})")

            self.cur.execute(
                "SELECT passenger_id, first_name, last_name FROM passengers LIMIT 20")
            print("\n  Passengers (first 20):")
            for r in self.cur.fetchall():
                print(f"  {r[0]}. {r[1]} {r[2]}")

            flight_id    = int(input("\n  Flight ID: "))
            passenger_id = int(input("  Passenger ID: "))
            seat         = input("  Seat number: ")
            cabin        = input("  Cabin class (economy/business/first): ")
            date         = input("  Booking date (YYYY-MM-DD): ")

            self.cur.execute("""
                INSERT INTO bookings
                (flight_id, passenger_id, booking_date, seat_number, cabin_class)
                VALUES (?,?,?,?,?)
            """, (flight_id, passenger_id, date, seat, cabin))
            self.conn.commit()
            print("  Booking added.")
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    def delete_booking(self):
        try:
            self.get_connection()
            bid = int(input("  Booking ID to delete: "))
            self.cur.execute("DELETE FROM bookings WHERE booking_id=?", (bid,))
            self.conn.commit()
            print(f"  {self.cur.rowcount} row(s) deleted." if self.cur.rowcount else "  Not found.")
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    # =============================================
    # DESTINATIONS
    # =============================================

    def view_all_destinations(self):
        try:
            self.get_connection()
            self.cur.execute(
                "SELECT airport_id, iata_code, airport_name, city, country FROM airports")
            rows = self.cur.fetchall()

            if not rows:
                print("  No destinations found.")
                return

            print("\n{:<5} {:<6} {:<28} {:<16} {:<16}".format(
                "ID", "IATA", "Airport", "City", "Country"))
            print("-" * 78)
            for r in rows:
                print("{:<5} {:<6} {:<28} {:<16} {:<16}".format(*r))
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    def update_airport(self):
        try:
            self.get_connection()

            self.cur.execute(
                "SELECT airport_id, iata_code, airport_name, city, country FROM airports")
            rows = self.cur.fetchall()

            print("\n{:<5} {:<6} {:<28} {:<16} {:<16}".format(
                "ID", "IATA", "Airport", "City", "Country"))
            print("-" * 78)
            for r in rows:
                print("{:<5} {:<6} {:<28} {:<16} {:<16}".format(*r))

            aid     = int(input("\n  Airport ID to update: "))
            city    = input("  New city: ")
            country = input("  New country: ")

            self.cur.execute(
                "UPDATE airports SET city=?, country=? WHERE airport_id=?",
                (city, country, aid))
            self.conn.commit()
            print(f"  {self.cur.rowcount} row(s) updated." if self.cur.rowcount else "  Not found.")
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    # =============================================
    # SUMMARY REPORTS
    # =============================================

    def flights_per_destination(self):
        try:
            self.get_connection()

            # SQL query to count number of flights per destination
            self.cur.execute("""
                SELECT a.city, a.iata_code, COUNT(f.flight_id) AS total
                FROM flights f
                JOIN airports a ON f.arrival_airport = a.airport_id
                GROUP BY a.airport_id, a.city, a.iata_code
                ORDER BY total DESC
            """)
            rows = self.cur.fetchall()

            if not rows:
                print("  No data found.")
                return

            print("\n{:<20} {:<6} {:<8}".format("City", "IATA", "Flights"))
            print("-" * 38)
            for r in rows:
                print("{:<20} {:<6} {:<8}".format(*r))
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    def flights_per_pilot(self):
        try:
            self.get_connection()
            self.cur.execute("""
                SELECT p.first_name || ' ' || p.last_name, COUNT(f.flight_id)
                FROM pilots p
                LEFT JOIN flights f ON p.pilot_id = f.pilot_id
                GROUP BY p.pilot_id, p.first_name, p.last_name
                ORDER BY 2 DESC
            """)
            rows = self.cur.fetchall()

            if not rows:
                print("  No data found.")
                return

            print("\n{:<25} {:<8}".format("Pilot", "Flights"))
            print("-" * 36)
            for r in rows:
                print("{:<25} {:<8}".format(*r))
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    def passengers_per_destination(self):
        try:
            self.get_connection()
            self.cur.execute("""
                SELECT a.city, a.iata_code, COUNT(b.booking_id)
                FROM bookings b
                JOIN flights  f ON b.flight_id = f.flight_id
                JOIN airports a ON f.arrival_airport = a.airport_id
                GROUP BY a.airport_id, a.city, a.iata_code
                ORDER BY 3 DESC
            """)
            rows = self.cur.fetchall()

            if not rows:
                print("  No data found.")
                return

            print("\n{:<20} {:<6} {:<12}".format("City", "IATA", "Passengers"))
            print("-" * 42)
            for r in rows:
                print("{:<20} {:<6} {:<12}".format(*r))
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    def flight_duration_by_route(self):
        try:
            self.get_connection()
            self.cur.execute("""
                SELECT a1.iata_code || ' to ' || a2.iata_code,
                       ROUND(AVG((JULIANDAY(f.arrival_datetime) -
                                  JULIANDAY(f.departure_datetime)) * 24), 2),
                       COUNT(f.flight_id)
                FROM flights f
                JOIN airports a1 ON f.departure_airport = a1.airport_id
                JOIN airports a2 ON f.arrival_airport   = a2.airport_id
                GROUP BY a1.airport_id, a2.airport_id
                ORDER BY 2 DESC
            """)
            rows = self.cur.fetchall()

            if not rows:
                print("  No data found.")
                return

            print("\n{:<16} {:<12} {:<8}".format("Route", "Avg Hrs", "Flights"))
            print("-" * 40)
            for r in rows:
                print("{:<16} {:<12} {:<8}".format(*r))
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()

    def flights_by_departure_date(self):
        try:
            self.get_connection()
            self.cur.execute("""
                SELECT DATE(departure_datetime), COUNT(*)
                FROM flights
                GROUP BY DATE(departure_datetime)
                ORDER BY 1
            """)
            rows = self.cur.fetchall()

            if not rows:
                print("  No data found.")
                return

            print("\n{:<14} {:<8}".format("Date", "Flights"))
            print("-" * 26)
            for r in rows:
                print("{:<14} {:<8}".format(*r))
        except Exception as e:
            print("Error:", e)
        finally:
            self.conn.close()


# =============================================
# SUB MENUS
# =============================================

def flights_menu(db):
    # Displays menu options for flight operations

    while True:
        print("\n  --- Manage Flights ---")
         # Calls different DB methods based on user selected choice
        print("  1. View all flights")
        print("  2. Search flight by ID")
        print("  3. Add a new flight")
        print("  4. Update departure time")
        print("  5. Update flight status")
        print("  6. Delete a flight")
        print("  0. Back")
        choice = input("\n  Enter choice: ")

        if choice == "1":
            db.view_all_flights()
        elif choice == "2":
            db.search_flight()
        elif choice == "3":
            db.add_flight()
        elif choice == "4":
            db.update_departure_time()
        elif choice == "5":
            db.update_flight_status()
        elif choice == "6":
            db.delete_flight()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")


def pilots_menu(db):
    while True:
        print("\n  --- Manage Pilots ---")
        print("  1. View all pilots")
        print("  2. Assign pilot to flight")
        print("  3. View pilot schedule")
        print("  0. Back")
        choice = input("\n  Enter choice: ")

        if choice == "1":
            db.view_all_pilots()
        elif choice == "2":
            db.assign_pilot()
        elif choice == "3":
            db.view_pilot_schedule()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")


def bookings_menu(db):
    while True:
        print("\n  --- Manage Bookings ---")
        print("  1. View all bookings")
        print("  2. Add a new booking")
        print("  3. Delete a booking")
        print("  0. Back")
        choice = input("\n  Enter choice: ")

        if choice == "1":
            db.view_all_bookings()
        elif choice == "2":
            db.add_booking()
        elif choice == "3":
            db.delete_booking()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")


def destinations_menu(db):
    while True:
        print("\n  --- Manage Destinations ---")
        print("  1. View all destinations")
        print("  2. Update airport information")
        print("  0. Back")
        choice = input("\n  Enter choice: ")

        if choice == "1":
            db.view_all_destinations()
        elif choice == "2":
            db.update_airport()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")


def reports_menu(db):
    while True:
        print("\n  --- Summary Reports ---")
        print("  1. Flights per destination")
        print("  2. Flights per pilot")
        print("  3. Passengers per destination")
        print("  4. Flight duration by route")
        print("  5. Flights by departure date")
        print("  0. Back")
        choice = input("\n  Enter choice: ")

        if choice == "1":
            db.flights_per_destination()
        elif choice == "2":
            db.flights_per_pilot()
        elif choice == "3":
            db.passengers_per_destination()
        elif choice == "4":
            db.flight_duration_by_route()
        elif choice == "5":
            db.flights_by_departure_date()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")


# =============================================
# MAIN
# The main function parses arguments
# =============================================

db = DBOperations() # Initialize database

while True:
    # Displays main menu and handles user navigation
    print("\n========================================")
    print("      FLIGHT MANAGEMENT SYSTEM")
    print("========================================")
    print("  1. Manage Flights")
    print("  2. Manage Pilots")
    print("  3. Manage Bookings")
    print("  4. Manage Destinations")
    print("  5. Summary Reports")
    print("  0. Exit")

    choice = input("\n  Enter choice: ")

    if choice == "1":
        flights_menu(db)
    elif choice == "2":
        pilots_menu(db)
    elif choice == "3":
        bookings_menu(db)
    elif choice == "4":
        destinations_menu(db)
    elif choice == "5":
        reports_menu(db)
    elif choice == "0":
        print("\n You Have Exited the Application!!!!!!.\n")
        break
    else:
        print("  Invalid choice.")