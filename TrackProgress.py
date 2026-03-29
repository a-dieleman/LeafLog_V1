#This file is for the Track Progress screen where users will record plant growth progress

###outline screen visualization
    #a light green screen background with the title in the top left.
    #users will choose a specific plant/seedling and then record information about height, signs of disease,
    #whether or not a sprout was observed, count of vegetables harvested, and a photo.
    #the options to cancel or save the action is centered at the bottom of the screen.
###variable list
    #seedlings_id -  from Seedlings table - user chooses from drop down
    #date_recorded - int (text date type for sqlite)
    #sprout_date - bool
    #harvest_quantity - int
    #disease_symptom - str
    #progress_photo - str (file location)
    #sprout_date_entry - used to populate sprout_date based on user input. Not a variable found in tables.

import sqlite3
from datetime import datetime, timedelta

class NewProgress:
    def __init__(self, db):
        self.db = db

    #give user a list of available seedlings from the db
    # def show_seedling_options(self):
    #     cur = self.db.conn.execute("""
    #         SELECT id, seedling_nickname
    #         FROM Seedlings
    #         ORDER BY seedling_nickname ASC
    #         """)
    #     rows = cur.fetchall()
    #
    #     if not rows:
    #         print("No seedlings found in the database. Please navigate to the 'Add New Seedling' screen to begin.")
    #
    #     print("Available seedlings:")
    #     for row in rows:
    #         print(f"ID {row['id']}:{row['seedling_nickname']}")
    #     return rows
    #how to handle user entered data
    def populate_progress(self, seedlings_id, date_recorded, sprout_date, harvest_quantity, disease_symptom, progress_photo):

        date_recorded = (date_recorded or "").strip()
        disease_symptom = (disease_symptom or "").strip()
        progress_photo = (progress_photo or "").strip()
        sprout_date = (sprout_date or "").strip().lower()

        # validate the date entry for date_recorded
        if date_recorded == "":
            raise ValueError("The date of recording cannot be blank.")

        try:
            check_date = datetime.strptime(date_recorded, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Date Recorded must be in YYYY-MM-DD format.")

        if sprout_date in ["yes", "y", "Yes"]:
            sprout_date = check_date.strftime("%Y-%m-%d")
        elif sprout_date in ["no", "n", "No", ""]:
            sprout_date = None
        else:
            raise ValueError("Input must be yes, no, or blank.")


        #validate the number for harvest_quantity
        if str(harvest_quantity).strip()=="":
            harvest_quantity = 0
        else:
            try:
                harvest_quantity = int(str(harvest_quantity).strip())
            except (ValueError, TypeError):
                raise ValueError("Harvest Quantity must be a whole number. Example, if your seedling is a greenbean plant, enter the number of pods harvested.")

        #validate seedlings_id choice from list
        try:
            seedlings_id = int(str(seedlings_id).strip())
        except (ValueError, TypeError):
            raise ValueError("Seedling ID must be a whole number.")

        cur = self.db.conn.execute("""
            SELECT id
            FROM Seedlings
            WHERE id = ?
            """, (seedlings_id,))
        seedling_result = cur.fetchone()

        if seedling_result is None:
            raise ValueError(f"Seedling ID {seedlings_id} doesn't exist.")

        try:
            cur = self.db.conn.execute("""
                INSERT INTO Progress (seedlings_id, date_recorded, sprout_date, harvest_quantity, disease_symptom, progress_photo)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (seedlings_id, date_recorded, sprout_date, harvest_quantity, disease_symptom, progress_photo)
                )
            self.db.conn.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Unable to save progress due to {e}")

#     #collect user generated information - this section for the terminal testing
#     def user_input_progress(self):
#         print("Choose a seedling to add progress info to:")
#
#         list_seedlings = self.show_seedling_options()
#         if not list_seedlings:
#             raise ValueError("No seedlings exist in database. Cannot add progress info.")
#         seedlings_id = input("Enter the ID for the desired seedling from the list above:")
#         date_recorded = input("What date did you record this information? Enter as YYYY-MM-DD")
#         sprout_date = input("When recording this data, was there a sprout?")
#         harvest_quantity = input("Number of vegetables harvested: (leave blank if none)")
#         disease_symptom = input("If present, record any symptoms of disease:")
#         progress_photo = input("Select a file to attach a progress photo:")
#
#         new_progress_id = self.populate_progress(seedlings_id, date_recorded, sprout_date, harvest_quantity, disease_symptom, progress_photo)
#
#         print(f"Progress has been recorded. The unique ID for this entry is {new_progress_id}.")
#
#
# #below for testing in console
# if __name__ == "__main__":
#     from main import LeafLogDB
#     db = LeafLogDB()
#
#     try:
#         progress = NewProgress(db)
#         progress.user_input_progress()
#     except Exception as e:
#         print(f"Error:{e}")
#     finally:
#         db.conn.close()
#
