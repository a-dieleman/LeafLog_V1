##This file is for the Query/Reports screen where users will be able to generate various reports from the database

###outline screen visualization
    #a violet screen background with the title in the top center.
    #users will have options for various reports to run as buttons on the screen.
    #the option to return to the home page will be at the bottom of the screen
###query options
    #list of seedlings by bed
    #list of diseases
    #count of planted seeds per variety
    #


import sqlite3
from datetime import datetime, timedelta
from main import LeafLogDB

class GardenQueries:
    def __init__(self, db):
        self.db = db

    def seedlings_by_bed_background(self):
        cursor = self.db.conn.execute("""
            SELECT BedInfo.bed_name, Seedlings.seedling_nickname, PlantType.seed_variety
            FROM Seedlings
            JOIN BedInfo
            ON Seedlings.bed_info_id = BedInfo.id
            JOIN PlantType
            ON Seedlings.plant_type_id = PlantType.id
            ORDER BY BedInfo.bed_name ASC, Seedlings.seedling_nickname ASC
        """)
        return cursor.fetchall()

    def seedlings_by_bed_output(self, rows):
        current_bed = None

        for row in rows:
            if row ["bed_name"] != current_bed:
                current_bed = row["bed_name"]
                print(f"\n----{current_bed}---")
            print(f"{row['seedling_nickname']}"
                  f" {row['seed_variety']}")

    def diseases_background(self):
        cursor = self.db.conn.execute("""
            SELECT PlantType.seed_variety, Progress.disease_symptom,
            COUNT(DISTINCT Seedlings.id) AS symptom_count
            FROM Progress
            JOIN Seedlings
            ON Progress.seedlings_id = Seedlings.id
            JOIN PlantType
            ON Seedlings.plant_type_id = PlantType.id
            WHERE Progress.disease_symptom IS NOT NULL
            GROUP BY PlantType.seed_variety, Progress.disease_symptom
            ORDER BY PlantType.seed_variety ASC, symptom_count DESC, Progress.disease_symptom ASC
        """)
        return cursor.fetchall()

    def diseases_output(self, rows):
        current_type = None
        for row in rows:
            if row["seed_variety"] != current_type:
                current_type = row["seed_variety"]
                print(f"\n----{current_type}----")
            print(f"{row['disease_symptom']} found on {row['symptom_count']} plants.")

    def seedlings_per_type_background(self):
        cursor = self.db.conn.execute("""
            SELECT PlantType.seed_variety,
            COUNT (*) AS type_count
            FROM Seedlings
            JOIN PlantType
            ON Seedlings.plant_type_id = PlantType.id
            GROUP BY PlantType.seed_variety
            ORDER BY type_count DESC
        """)
        return cursor.fetchall()


    def seedlings_per_type_output(self, rows):
        current_type = None
        for row in rows:
            if row["seed_variety"] != current_type:
                current_type = row["seed_variety"]
                print(f"\n----{current_type}----")
            print(f"{row['type_count']} planted seeds.")


    def upcoming_harvest_background(self):
        cursor = self.db.conn.execute("""
            SELECT BedInfo.bed_name, Seedlings.seedling_nickname, PlantType.seed_variety, Seedlings.expected_harvest_date
            FROM Seedlings
            JOIN BedInfo
            ON Seedlings.bed_info_id = BedInfo.id
            JOIN PlantType 
            ON Seedlings.plant_type_id = PlantType.id
            ORDER BY BedInfo.bed_name ASC, Seedlings.expected_harvest_date ASC
        """)
        return cursor.fetchall()

    def upcoming_harvest_output(self, rows):
        current_bed = None
        for row in rows:
            if row["bed_name"] != current_bed:
                current_bed = row["bed_name"]
                print(f"\n----{current_bed}----")
            print(f"{row['seedling_nickname']} ({row['seed_variety']}) projected harvest on {row['expected_harvest_date']}")


db = LeafLogDB("test_db_V1.db")
queries = GardenQueries(db)

#rows = queries.seedlings_by_bed_background()
#queries.seedlings_by_bed_output(rows)

rows = queries.diseases_background()
queries.diseases_output(rows)

#rows = queries.seedlings_per_type_background()
#queries.seedlings_per_type_output(rows)

#rows = queries.upcoming_harvest_background()
#queries.upcoming_harvest_output(rows)