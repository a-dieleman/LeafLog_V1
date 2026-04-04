#This file is for the New Seedling screen where users will enter a new Seedling to be tracked.

###outline screen visualization
    #a light blue screen background with the title in the top left.
    #users will have areas to enter information about the seed variety, the bed it is planted in,
    #the planting date and the expected days to harvest.
    #the options to cancel or save the action is centered at the bottom of the screen.
###variable list
    #plant_type_id - from the PlantType table
    #bed_info_id - from the BedInfo table
    #seedling_nickname - str
    #date_planted - str (text date type for sqlite)
    #days_to_harvest - from the PlantType table
    #expected_harvest_date = date_planted + days_to_harvest

import sqlite3
from datetime import datetime, timedelta

class NewSeedling:
    def __init__(self, db):
        self.db = db
####                                                     ####
#### BELOW COMMENTED OUT - WAS USED FOR TERMINAL TESTING ####
####  showed options from db - UI now handles dropdown   ####
    # def show_plant_options(self):
    #     cur = self.db.conn.execute("""
    #         SELECT id, seed_variety, days_to_harvest
    #         FROM PlantType
    #         ORDER BY id ASC
    #         """)
    #     rows = cur.fetchall()
    #
    #     if not rows:
    #         print("No Plant Types found in the database. Please navigate to the 'Add New Seed Type' screen to begin.")
    #         return []
    #
    #     print("Available Varieties:")
    #     for row in rows:
    #         print(f" ID {row['id']}: {row['seed_variety']} (Days to Harvest: {row['days_to_harvest']})")
    #     return rows
    #
    # def show_bed_options(self):
    #     cur = self.db.conn.execute("""
    #         SELECT id, bed_name
    #         FROM BedInfo
    #         ORDER BY id ASC
    #         """)
    #     rows = cur.fetchall()
    #
    #     if not rows:
    #         print("No garden beds found in the database. Please navigate to the 'Add New Bed' screen to begin.")
    #         return[]
    #
    #     print("Available Beds:")
    #     for row in rows:
    #         print(f"ID {row['id']}: {row['bed_name']}")
    #     return rows
    #
    def populate_seedling(self, plant_type_id, bed_info_id, seedling_nickname, date_planted):
    # Remove trailing spaces from seedling_nickname and date_planted, ensure values are not empty, ensure date formatting
        seedling_nickname = seedling_nickname.strip()
        date_planted = date_planted.strip()

        if seedling_nickname == "":
            raise ValueError("Seedling Name cannot be empty!")
        if date_planted == "":
            raise ValueError("Planting date cannot be empty!")

        try:
            planting_date_check = datetime.strptime(date_planted, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Date Planted must be in YYYY-MM-DD format.")

        try:
            plant_type_id = int(str(plant_type_id).strip())
        except (ValueError, TypeError):
            raise ValueError("Plant Type ID must be a whole number.")

        try:
            bed_info_id = int(str(bed_info_id).strip())
        except (ValueError, TypeError):
            raise ValueError("Bed ID must be a whole number.")

        cur = self.db.conn.execute("""
            SELECT days_to_harvest
            FROM PlantType
            WHERE id = ?
            """, (plant_type_id,))
        plant_result = cur.fetchone()

        if plant_result is None:
            raise ValueError(f"Plant Type ID {plant_type_id} doesn't exist.")

        days_to_harvest = plant_result["days_to_harvest"]

        if days_to_harvest is None:
            raise ValueError(f"Plant Type ID {plant_type_id} has no value for 'Days to Harvest' recorded.")


        cur = self.db.conn.execute("""
                            SELECT id
                            FROM BedInfo
                            WHERE id = ?
                            """, (bed_info_id,))
        bed_result = cur.fetchone()

        if bed_result is None:
            raise ValueError(f"Bed Info ID {bed_info_id} does not exist.")

        expected_harvest_date = planting_date_check + timedelta(days=days_to_harvest)
        expected_harvest_date = expected_harvest_date.strftime("%Y-%m-%d")

        #if no errors set off in section above, enter the user data into the db. while db is open, check that the users nickname isn't a duplicate.
        try:
            cur = self.db.conn.execute("""
                    INSERT INTO Seedlings (plant_type_id, bed_info_id, seedling_nickname, date_planted, expected_harvest_date)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                   (plant_type_id, bed_info_id, seedling_nickname, date_planted, expected_harvest_date)
                   )
            self.db.conn.commit()
            return cur.lastrowid

        except sqlite3.IntegrityError:
            raise ValueError(f"{seedling_nickname} already exists. Please enter a different nickname.")

####                                                     ####
#### BELOW COMMENTED OUT - WAS USED FOR TERMINAL TESTING ####
####                                                     ####
#     def user_input_seedling(self):
#         print("Add a new Seedling:")
#
#         plant_list = self.show_plant_options()
#         if not plant_list:
#             raise ValueError("Cannot add a seedling because the specified plant type does not yet exist in database.")
#
#         bed_list = self.show_bed_options()
#         if not bed_list:
#             raise ValueError("Cannot add a seedling because the specified bed does not yet exist in database.")
#
#         plant_type_id = input("Enter the Plant Type ID (choose from list printed above):")
#         bed_info_id = input("Enter the Bed Info ID (choose from list printed above):")
#         seedling_nickname = input("Enter seedling nickname:")
#         date_planted = input("Date Planted (YYYY-MM-DD):")
#
#         new_seedling_id = self.populate_seedling(
#             plant_type_id,
#             bed_info_id,
#             seedling_nickname,
#             date_planted
#         )
#
#         print(f"Saved successfully! The Unique ID for {seedling_nickname} is {new_seedling_id}.")
#
# if __name__ == "__main__":
#     from main import LeafLogDB
#     db = LeafLogDB()
#
#     try:
#         seedling = NewSeedling(db)
#         seedling.user_input_seedling()
#     except Exception as e:
#         print(f"error {e}")
#     finally:
#         db.conn.close()