import random
from datetime import datetime, timedelta

from main import LeafLogDB

def empty_all_tables(conn):
    #empty table contents
    conn.execute("DELETE FROM Progress")
    conn.execute("DELETE FROM Seedlings")
    conn.execute("DELETE FROM BedInfo")
    conn.execute("DELETE FROM PlantType")
    #reset autoincrement counter
    conn.execute("""
        DELETE FROM sqlite_sequence
        WHERE name IN ('Progress', 'Seedlings', 'BedInfo', 'PlantType') 
    """)
    conn.commit()

def populate_plants(conn):
    list_of_plants = [
        ("Cherry Tomato", 7, 75, 1, "Cage"),
        ("Roma Tomato", 8, 80, 1, "Stake"),
        ("Beefsteak Tomato", 9, 85, 1, "Cage"),
        ("Bell Pepper", 10, 90, 1, "Stake"),
        ("Jalapeno Pepper", 9, 80, 1, None),
        ("Cucumber", 6, 60, 1, "Trellis"),
        ("Zucchini", 5, 55, 1, None),
        ("Carrot", 12, 70, 1, None),
        ("Lettuce", 4, 45, 2, None),
        ("Spinach", 5, 40, 1, None),
        ("Green Bean", 6, 55, 1, "Pole"),
        ("Pumpkin", 8, 100, 2, "Trellis"),
        ("Basil", 5, 30, 3, None),
        ("Parsley", 14, 75, 2, None),
        ("Radish", 3, 28, 1, None),
        ("Kale", 7, 60, 1, None),
        ("Broccoli", 7, 85, 1, None),
        ("Onion", 10, 95, 1, None),
    ]

    #enter all quickly
    conn.executemany("""
        INSERT INTO PlantType (seed_variety, days_to_germinate, days_to_harvest, seed_depth, support_type)
        VALUES (?, ?, ?, ?, ?)
    """, list_of_plants)
    conn.commit()

def populate_beds(conn):
    list_of_beds = [
        ("North Bed", 12, "Loam", "Full Sun", None),
        ("South Bed", 16, "Clay", "Partial Sun", "Shade Cloth"),
        ("East Bed", 12, "Loam", "Morning Sun", None),
        ("West Bed", 12, "Clay Loam", "Afternoon Sun", None),
        ("Raised Bed 1", 18, "Garden Mix", "Full Sun", None),
        ("Raised Bed 2", 24, "Compost Mix", "Partial Shade", None),
        ("Herb Box", 10, "Sandy Loam", "Full Sun", None),
        ("Fence Line", 36, "Loam", "Full Sun", None),
        ("Black Planter", 10, "Potting Mix", "Partial Sun", None),
        ("Herb Window", 8, "Garden Mix", "Full Sun", "Roof Overhang"),
    ]

    #enter all quickly
    conn.executemany("""
    INSERT INTO BedInfo (bed_name, soil_depth, soil_type, sun_exposure, shade_structure)
    VALUES (?, ?, ?, ?, ?)
    """, list_of_beds)
    conn.commit()

def random_nicknames(taken_names, index):
    prefix = [
        "Sunny", "Little", "Big", "Green", "Happy", "Tall", "Tiny",
        "Red", "Golden", "Sweet", "Early", "Late", "Strong", "Wild",
        "Bright", "Lucky", "Quiet", "Brave", "Shady", "Fresh"
    ]

    suffix = [
        "Sprout", "Leaf", "Bloom", "Buddy", "Star", "Root",
        "Grower", "Patch", "Gem", "Trail", "Stem", "Bean",
        "Petal", "Vine", "Shooter", "Garden", "Branch", "Breeze"
    ]

    while True:
        nickname = f"{random.choice(prefix)} {random.choice(suffix)} {index}"
        if nickname not in taken_names:
            taken_names.add(nickname)
            return nickname

def populate_seedlings(conn, count=75):
    cursor = conn.cursor()
    cursor.execute("SELECT id, days_to_harvest FROM PlantType")
    list_of_plants = cursor.fetchall()

    cursor.execute("SELECT id FROM BedInfo")
    list_of_beds = cursor.fetchall()
    taken_names = set()
    today = datetime.today()

    seedling_rows = []

    for i in range(1, count+1):
        plant = random.choice(list_of_plants)
        bed = random.choice(list_of_beds)

        plant_type_id = plant["id"]
        days_to_harvest = plant["days_to_harvest"]
        bed_info_id = bed["id"]

        nickname = random_nicknames(taken_names, i)

        how_long_ago_planted = random.randint(1,60)
        planting_date = today - timedelta(days=how_long_ago_planted)
        expected_harvest_date = planting_date + timedelta(days=days_to_harvest)

        seedling_rows.append((
            plant_type_id,
            bed_info_id,
            nickname,
            planting_date.strftime("%Y-%m-%d"),
            expected_harvest_date.strftime("%Y-%m-%d")
        ))

    conn.executemany("""
        INSERT INTO Seedlings (plant_type_id, bed_info_id, seedling_nickname, date_planted, expected_harvest_date) VALUES (?, ?, ?, ?, ?)
    """, seedling_rows)
    conn.commit()

def populate_progress(conn, entries_per_seedling=4):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
        s.id AS seedling_id,
        s.date_planted, 
        p.days_to_germinate, 
        p.days_to_harvest
        FROM Seedlings s
        JOIN PlantType p
        ON s.plant_type_id = p.id 
    """)
    seedlings = cursor.fetchall()

    disease_options = [
        None,
        None,
        None,
        "Yellowing leaves",
        "Wilt symptoms",
        "Spotted leaves",
        "Minor pest damage",
        "Powdery mildew signs"
    ]

    progress_rows = []

    for seedling in seedlings:
        seedlings_id = seedling["seedling_id"]
        date_planted_dt = datetime.strptime(seedling["date_planted"], "%Y-%m-%d")
        sprout_dt = date_planted_dt + timedelta(days=seedling["days_to_germinate"])
        harvest_dt = date_planted_dt + timedelta(days=seedling["days_to_harvest"])

        for step in range(1, entries_per_seedling + 1):
            recorded_dt = date_planted_dt + timedelta(days=step * 7)

            sprout_date = None
            if recorded_dt >= sprout_dt:
                sprout_date = sprout_dt.strftime("%Y-%m-%d")

            harvest_quantity = 0
            if recorded_dt >= harvest_dt:
                harvest_quantity = random.choice([1, 2, 3, 5, 8, 10])

            disease_symptom = random.choice(disease_options)

            progress_photo = None
            if random.choice([False, False, True]):
                progress_photo = f"photos/seedling_{seedlings_id}_{step}.jpg"

            progress_rows.append((
                seedlings_id,
                recorded_dt.strftime("%Y-%m-%d"),
                sprout_date,
                harvest_quantity,
                disease_symptom,
                progress_photo
            ))

    conn.executemany("""
            INSERT INTO Progress (
                seedlings_id,
                date_recorded,
                sprout_date,
                harvest_quantity,
                disease_symptom,
                progress_photo
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, progress_rows)

    conn.commit()


def print_counts(conn):
    for table_name in ["PlantType", "BedInfo", "Seedlings", "Progress"]:
        cursor = conn.execute(f"SELECT COUNT(*) AS count FROM {table_name}")
        row = cursor.fetchone()
        print(f"{table_name}: {row['count']}")


def main():
    db = LeafLogDB("test_db_V1.db")
    conn = db.conn

    empty_all_tables(conn)
    populate_plants(conn)
    populate_beds(conn)
    populate_seedlings(conn, count=75)
    populate_progress(conn, entries_per_seedling=4)

    print("Dummy test data loaded successfully.")
    print_counts(conn)

    conn.close()


if __name__ == "__main__":
    main()