##This file is for the Query/Reports screen where users will be able to generate various reports from the database

###outline screen visualization
    #a violet screen background with the title in the top center.
    #users will have options for various reports to run as buttons on the screen.
    #the option to return to the home page will be at the bottom of the screen
###query options
    #list of seedlings by bed
    #list of diseases by plant variety
    #count of planted seeds per plant variety
    #upcoming harvest dates by garden bed

class GardenQueries:
    def __init__(self, db):
        self.db = db
    #query to return lists of seedlings found in each garden bed
    def query_seedlings_by_bed(self):
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

    #query to return list of diseases by plant type - to help user identify prominent illnesses among plant varieties
    def query_diseases(self):
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

    #query to output how many seedlings, and their nicknames, per plant type
    def query_seedlings_per_type(self):
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

    #query to show upcoming harvest days (in order of soonest date) for each garden bed
    def query_upcoming_harvest(self):
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

##Formatting output for queries below - originally used print for terminal testing, those lines have been commented out
    def format_seedlings_by_bed(self, rows):
        lines = []
        current_bed = None
        for row in rows:
            if row ["bed_name"] != current_bed:
                current_bed = row["bed_name"]
                lines.append(f"\n----{current_bed}----")
            lines.append(f"{row['seedling_nickname']} ({row['seed_variety']})")
        return"\n".join(lines)
                #print(f"\n----{current_bed}---")
            #print(f"{row['seedling_nickname']}"
                  #f" {row['seed_variety']}")

    # output for terminal testing
    def format_diseases(self, rows):
        lines = []
        current_type = None
        for row in rows:
            if row["seed_variety"] != current_type:
                current_type = row["seed_variety"]
                lines.append(f"\n----{current_type}----")
            lines.append(f"{row["disease_symptom"]} found on {row['symptom_count']} plants.")
        return "\n".join(lines)
                #print(f"\n----{current_type}----")
            #print(f"{row['disease_symptom']} found on {row['symptom_count']} plants.")

    # output for terminal testing
    def format_seedlings_per_type(self, rows):
        lines = []
        current_type = None
        for row in rows:
            if row["seed_variety"] != current_type:
                current_type = row["seed_variety"]
                lines.append(f"\n----{current_type}----")
            lines.append(f"{row['type_count']} planted seeds.")
        return "\n".join(lines)
                #print(f"\n----{current_type}----")
            #print(f"{row['type_count']} planted seeds.")

    # output for terminal testing
    def format_upcoming_harvest(self, rows):
        lines = []
        current_bed = None
        for row in rows:
            if row["bed_name"] != current_bed:
                current_bed = row["bed_name"]
                lines.append(f"\n----{current_bed}----")
            lines.append(f"{row['seedling_nickname']} ({row['seed_variety']}) projected harvest on {row['expected_harvest_date']}")
        return "\n".join(lines)
                #print(f"\n----{current_bed}----")
            #print(f"{row['seedling_nickname']} ({row['seed_variety']}) projected harvest on {row['expected_harvest_date']}")

####                                                     ####
#### BELOW COMMENTED OUT - WAS USED FOR TERMINAL TESTING ####
####                                                     ####
#db = LeafLogDB("test_db_V1.db")
#queries = GardenQueries(db)

#rows = queries.query_seedlings_by_bed()
#queries.format_seedlings_by_bed(rows)

#rows = queries.diseases_background()
#queries.diseases_output(rows)

#rows = queries.seedlings_per_type_background()
#queries.seedlings_per_type_output(rows)

#rows = queries.upcoming_harvest_background()
#queries.upcoming_harvest_output(rows)