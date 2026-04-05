#Welcome to LeafLog
#A data storage application built for Windows 11 via Python, sqlite, and (matplotlib or pandas) for data visualization by ADieleman
    #LeafLog is a program to meet the needs of new gardeners in planning plantings, tracking growth,
    #recording harvest, and informing future decisions based on user gathered data. It will store
    #information about each seedling/vegetable. Including seed types, planting dates, expected harvest
    #dates, measurements over time, and other observations. A small database will track relationships
    #between logged information about multiple areas of garden conditions and growth, and users will be
    #able to identify patterns that can inform decision making. Users will be able to store photos as
    #reference and keep them organized by seedling and garden bed.
#Main.py will have the following functions:
    # - Connect to the .db file
    # - Call functions located in other .py files

#import sqlite and UI
import sqlite3
from UserInterface import FullApp


#build tables if they don't already exist
class LeafLogDB:
    def __init__(self, db_name="LeafLog_V1.db"):
    #def __init__(self, db_name="test_db_V1.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.create_tables()
#Table Names: PlantType, BedInfo, Seedlings, Progress
    def create_tables(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS PlantType (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            seed_variety TEXT NOT NULL UNIQUE,
            days_to_germinate INTEGER NOT NULL,
            days_to_harvest INTEGER NOT NULL,
            seed_depth INTEGER NOT NULL,
            support_type TEXT
            )
        """)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS BedInfo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bed_name TEXT NOT NULL UNIQUE, 
            soil_depth INTEGER NOT NULL,
            soil_type TEXT NOT NULL,
            sun_exposure TEXT NOT NULL,
            shade_structure TEXT 
            )
        """)
# date_planted and expected_harvest_date store as 'YYYY-MM-DD'
#foreign keys include plant_type_id and bed_info_id
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS Seedlings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_type_id INTEGER NOT NULL, 
            bed_info_id INTEGER NOT NULL,
            seedling_nickname TEXT NOT NULL UNIQUE, 
            date_planted TEXT NOT NULL, 
            expected_harvest_date TEXT NOT NULL,
            
            FOREIGN KEY (plant_type_id) REFERENCES PlantType (id),
            FOREIGN KEY (bed_info_id) REFERENCES BedInfo (id)
            )
        """)
# date_recorded and sprout_date store as 'YYYY-MM-DD'
# an ON DELETE CASCADE command has been built in - may reconsider this. would remove all progress data related to a specific seedling if deleted.
# may look into an ARCHIVE data function if on delete cascade stays
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS Progress(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            seedlings_id INTEGER NOT NULL, 
            date_recorded TEXT NOT NULL, 
            sprout_date TEXT, 
            harvest_quantity INTEGER NOT NULL DEFAULT 0, 
            disease_symptom TEXT, 
            progress_photo TEXT,
            
            FOREIGN KEY (seedlings_id) REFERENCES Seedlings (id) ON DELETE CASCADE
        )
        """)
        self.conn.commit()

#Menu for the terminal now commented out since UI - user presented with options for populating tables
# def main():
#     db = LeafLogDB()
#
#     try:
#         while True:
#             print("What would you like to do?")
#             print("1: Add a New Seed Type")
#             print("2: Add a New Garden Bed")
#             #print("3: Add a New Seedling to Track")
#             #print("4: Track Progress for a Specific Seedling")
#             #print("5: Run a Report")
#             print("5: Quit")
#
#             user_choice = input("Enter Your Choice:")
#
#             if user_choice == "1":
#                 NewSeedType.NewSeedType(db).user_input_seed_type()
#             elif user_choice == "2":
#                 NewBed.NewBed(db).user_input_bed()
#             elif user_choice == "5":
#                 break
#             else:
#                 print ("That is not a valid option.")
# #close db connection when user is done
#     finally:
#         db.conn.close()


if __name__ == "__main__":
    #print("main started")
    db = LeafLogDB()
    #print("db created")
    app = FullApp(db)
    #print("app created")
    app.mainloop()
    db.conn.close()

#see the below often recommended - not sure fully understand benefits. Further reading needed.
#if __name__ == "__main__":
#    main()