#This file is for the New Seed Type screen where users will enter a new seed type to be tracked.

###outline screen visualization
    #a light green screen background with the title in the top left.
    #users will have areas to enter the seed variety, the expected days to germinate, expected days until harvest,
    #recommended planting depth, and if a support type is needed.
    #the options to cancel or save the action is centered at the bottom of the screen
###variable list
    #seed_variety - str
    #days_to_germinate - int
    #days_to_harvest - int
    #seed_depth - int
    #support_type - str (this variable must accept blanks that translate to NULL values)

import sqlite3
import Validation
from Validation import text_is_required, text_is_optional, num_is_positive


class NewSeedType:
    def __init__(self, db):
        self.db = db

    ####                                                     ####
    #### BELOW COMMENTED OUT - WAS USED FOR TERMINAL TESTING ####
    ####              accept user input                      ####
    # def user_input_seed_type(self):
    #     print("Add a new seed type:")
    #
    #     seed_variety = input("Seed Variety:")
    #     days_to_germinate = input("Days to Germinate according to package:")
    #     days_to_harvest = input("Days to Harvest according to package:")
    #     seed_depth = input("Seed Planting Depth according to package:")
    #     support_type = input("Support Type (optional):")
    #
    #     new_seed_id = self.populate_seed_type(
    #         seed_variety, days_to_germinate, days_to_harvest, seed_depth, support_type
    #     )
    #     print(f"Saved successfully! The unique ID for {seed_variety} is {new_seed_id}.")

    def populate_seed_type(self, seed_variety, days_to_germinate, days_to_harvest, seed_depth, support_type=None):
    # cleanup user input for white spaces, proper variables aren't empty, and that integers are correct
        seed_variety = text_is_required(seed_variety, "Seed Variety")
        support_type = text_is_optional(support_type)
        days_to_harvest = num_is_positive(days_to_harvest, "Days to Harvest")
        days_to_germinate = num_is_positive(days_to_germinate, "Days to Germinate")
        seed_depth = num_is_positive(seed_depth, "Planting Depth")
    ####                                                     ####
    ####   BELOW COMMENTED OUT - REPLACED BY VALIDATION.PY   ####
    ####                                                     ####
    #     seed_variety = seed_variety.strip()
    #     support_type = support_type.strip() if support_type else None
    #
    #     # make sure the seed variety isn't empty
    #     if not seed_variety:
    #         raise ValueError("The Seed Variety box cannot be empty!")
    #
    #     # validate numeric fields (must be non-negative integers)
    #     for name, value in {
    #         "Days to Germinate": days_to_germinate,
    #         "Days to Harvest": days_to_harvest,
    #         "Seed Depth": seed_depth
    #     }.items():
    #         try:
    #             number = int(value)
    #             if number < 0:
    #                 raise ValueError
    #         except (ValueError, TypeError):
    #             raise ValueError(f"{name} must be a non-negative integer.")
    #
    #         if name == "Days to Germinate":
    #             days_to_germinate = number
    #         elif name == "Days to Harvest":
    #             days_to_harvest = number
    #         else:
    #             seed_depth = number

        try:
            # insert into db, make sure the seed name is unique.
            cur = self.db.conn.execute(
                """
                INSERT INTO PlantType (seed_variety, days_to_germinate, days_to_harvest, seed_depth, support_type)
                VALUES (?, ?, ?, ?, ?)
                """,
                (seed_variety, days_to_germinate, days_to_harvest, seed_depth, support_type)
            )
            self.db.conn.commit()
            return cur.lastrowid

        except sqlite3.IntegrityError:
            raise ValueError(f"'{seed_variety}' already exists. Please enter a different seed type name.")

#print("NewSeedType module loaded")