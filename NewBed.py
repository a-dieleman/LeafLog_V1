#This file is for the New Bed screen where users will enter a new Bed to be tracked.

###outline screen visualization
    #a light brown screen background with the title in the top left.
    #users will have areas to enter the depth of the soil in the bed, a description of the soil type used,
    #a description of the sun exposure the bed receives, and if it has a shade structure.
    #the options to cancel or save the action is centered at the bottom of the screen
###variable list
    #bed_name - str
    #soil_depth - int
    #soil_type - str
    #sun_exposure - str
    #shade_structure - str

import sqlite3

class NewBed:
    def __init__(self, db):
        self.db = db

####                                                     ####
#### BELOW COMMENTED OUT - WAS USED FOR TERMINAL TESTING ####
####              accept user input                      ####
    # def user_input_bed(self):
    #     print("Add a new garden bed:")
    #
    #     bed_name = input("Choose a name for your garden bed:")
    #     soil_depth = input("In inches, how deep is the bed:")
    #     soil_type = input("Briefly describe the soil mixture:")
    #     sun_exposure = input("Briefly describe the sunlight exposure:")
    #     shade_structure = input("Describe the shade structure (optional):")
    #
    #     new_bed_id = self.populate_bed(
    #         bed_name, soil_depth, soil_type, sun_exposure, shade_structure
    #     )
    #     print(f"Saved successfully! The unique ID for {bed_name} is {new_bed_id}.")

    def populate_bed(self, bed_name, soil_depth, soil_type, sun_exposure, shade_structure=None):
    # cleanup the user input, validate entries for each type, enter into db, make sure the bed name is unique
        bed_name = bed_name.strip()
        soil_type = soil_type.strip()
        sun_exposure = sun_exposure.strip()
        shade_structure = shade_structure.strip() if shade_structure else None

        # make sure the required fields aren't empty
        for str_box_name, value in {
            "Bed Name": bed_name,
            "Soil Type": soil_type,
            "Sun Exposure": sun_exposure
        }.items():
            if not value.strip():
                raise ValueError(f"The {str_box_name} box cannot be empty!")

        # validate numeric fields (must be non-negative integers)
        try:
            soil_depth = int(soil_depth)
            if soil_depth < 0:
                raise ValueError("Soil Depth must be an integer.")
        except (ValueError, TypeError):
            raise ValueError("Soil Depth cannot be a negative number!")


        try:
            cur = self.db.conn.execute(
                """
                INSERT INTO BedInfo (bed_name, soil_depth, soil_type, sun_exposure, shade_structure)
                VALUES (?, ?, ?, ?, ?)
                """,
                (bed_name, soil_depth, soil_type, sun_exposure, shade_structure)
            )
            self.db.conn.commit()
            return cur.lastrowid

        except sqlite3.IntegrityError:
            raise ValueError(f"'{bed_name}' already exists. Please enter a different name for the garden bed.")