import tkinter as tk
from tkinter import ttk, messagebox
from NewSeedType import NewSeedType
from NewBed import NewBed
from NewSeedling import NewSeedling

print("userinterface.py loaded")
#class for the basic window layout that will be consistent across all windows and providing db access via UI
class FullApp(tk.Tk):
    def __init__(self, db):
        super().__init__()
        print("fullall started")
        self.db = db

        self.title("LeafLog_V1")
        self.geometry("800x600")
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        #fill the full window container
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames={}

#after Home below, include ,AddNewSeedling, AddProgress to parentheses as pages added
        for Pages in (Home, AddNewSeed, AddNewBed, AddNewSeedling):
            frame = Pages(container, self)
            self.frames[Pages] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Home)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

class Home(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="YellowGreen")

        title = tk.Label(
            self,
            text="Welcome to LeafLog!",
            font = ("Calibri", 24),
            bg="YellowGreen"
        )
        title.pack(pady=10)

        direction = tk.Label(
            self,
            text="What do you want to do today?",
            font = ("Calibri", 18, "italic"),
            bg="YellowGreen"
        )
        direction.pack(pady=10)

        ttk.Button(
            self,
            text="Add a New Seed Type",
            width=25,
            padding=12,
            command=lambda: controller.show_frame(AddNewSeed)
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Add a New Garden Bed",
            width=25,
            padding=12,
            command=lambda: controller.show_frame(AddNewBed)
         ).pack(pady=10)

        ttk.Button(
            self,
            text="Add a New Seedling",
            width=25,
            padding=12,
            command=lambda: controller.show_frame(AddNewSeedling)
        ).pack(pady=10)

class AddNewSeed(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="LightBlue")
        self.controller = controller
        self.seed_handler = NewSeedType(controller.db)

        tk.Label(
            self,
            text="Add a New Seed Type",
            font=("Calibri", 24),
            bg="LightBlue"
        ).pack(pady=10)

        newSeed_FormFrame = tk.Frame(self, bg="LightBlue")
        newSeed_FormFrame.pack(pady=10)

        #box for seed_variety
        tk.Label(
            newSeed_FormFrame,
            text="Seed Variety:",
            font=("Comfortaa", 12),
            bg="LightBlue"
        ).grid(row=0, column=0,padx=5, pady=5, sticky="e")
        self.seed_variety_entry = ttk.Entry(newSeed_FormFrame, width=40)
        self.seed_variety_entry.grid(row=0, column=1, padx=5, pady=5)
        #gray_placeholder(self.seed_variety_entry, "example: Kentucky Blue Green Beans")

        #box for days_to_germinate
        tk.Label(
            newSeed_FormFrame,
            text="Package Stated Days to Germinate:",
            font=("Comfortaa", 12),
            bg="LightBlue"
        ).grid(row=1, column=0,padx=5, pady=5, sticky="e")
        self.days_to_germinate_entry = ttk.Entry(newSeed_FormFrame, width=40)
        self.days_to_germinate_entry.grid(row=1, column=1, padx=5, pady=5)

        #box for days_to_harvest
        tk.Label(
            newSeed_FormFrame,
            text="Package Stated Days to Harvest:",
            font=("Comfortaa", 12),
            bg="LightBlue"
        ).grid(row=2, column=0,padx=5, pady=5, sticky="e")
        self.days_to_harvest_entry = ttk.Entry(newSeed_FormFrame, width=40)
        self.days_to_harvest_entry.grid(row=2, column=1, padx=5, pady=5)

        #box for seed_depth
        tk.Label(
            newSeed_FormFrame,
            text="Planting Depth:",
            font=("Comfortaa", 12),
            bg="LightBlue"
        ).grid(row=3, column=0,padx=5, pady=5, sticky="e")
        self.seed_depth_entry = ttk.Entry(newSeed_FormFrame, width=40)
        self.seed_depth_entry.grid(row=3, column=1, padx=5, pady=5)

        #box for support_type
        tk.Label(
            newSeed_FormFrame,
            text="Support Type (if applicable):",
            font=("Comfortaa", 12),
            bg="LightBlue"
        ).grid(row=4, column=0,padx=5, pady=5, sticky="e")
        self.support_type_entry = ttk.Entry(newSeed_FormFrame, width=40)
        self.support_type_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(
            self,
            text="Save",
            command=self.save_seed_type
        ).pack(pady=30)

        ttk.Button(
            self,
            text="Back to Homepage",
            command=lambda: controller.show_frame(Home)
        ).pack(side="bottom", pady = 30)

#save data on button press
    def save_seed_type(self):
        seed_variety = self.seed_variety_entry.get()
        days_to_germinate = self.days_to_germinate_entry.get()
        days_to_harvest = self.days_to_harvest_entry.get()
        seed_depth = self.seed_depth_entry.get()
        support_type = self.support_type_entry.get()

        try:
            new_seed_id = self.seed_handler.populate_seed_type(
                seed_variety,
                days_to_germinate,
                days_to_harvest,
                seed_depth,
                support_type
            )

            messagebox.showinfo(
                "Success",
                f"Saved successfully! The unique ID for {seed_variety.strip()} is {new_seed_id}."
            )

            #self.clear_entries()
            self.controller.show_frame(Home)

        except ValueError as e:
            messagebox.showerror("input Error", str(e))

    # def clear_entries(self):
    #     self.seed_variety_entry.delete(0, tk.END)
    #     self.days_to_germinate_entry.delete(0, tk.END)
    #     self.days_to_harvest_entry.delete(0, tk.END)
    #     self.seed_depth_entry.delete(0, tk.END)
    #     self.support_type_entry.delete(0, tk.END)

    #def gray_placeholder(value, placeholder):
     #   return "" if value == placeholder else value

class AddNewBed(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="Sienna")
        self.controller = controller
        self.bed_handler = NewBed(controller.db)

        tk.Label(
            self,
            text="Add a New Garden Bed",
            font=("Calibri", 24),
            bg="Sienna"
        ).pack(pady=10)

        newBed_FormFrame = tk.Frame(self,bg="Sienna")
        newBed_FormFrame.pack(pady=10)

        #box for bed_name
        tk.Label(
            newBed_FormFrame,
            text="Garden Bed Name:",
            font=("Comfortaa",12),
            bg="Sienna"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.bed_name_entry = ttk.Entry(newBed_FormFrame, width=40)
        self.bed_name_entry.grid(row=0, column=1, padx=5, pady=5)

        #box for soil_depth
        tk.Label(
            newBed_FormFrame,
            text="Soil Depth in Bed:",
            font=("Comfortaa",12),
            bg="Sienna"
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.soil_depth_entry = ttk.Entry(newBed_FormFrame, width=40)
        self.soil_depth_entry.grid(row=1, column=1, padx=5, pady=5)

        #box for soil_type
        tk.Label(
            newBed_FormFrame,
            text="Briefly Describe the Soil Mix:",
            font=("Comfortaa",12),
            bg="Sienna"
        ).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.soil_type_entry = ttk.Entry(newBed_FormFrame, width=40)
        self.soil_type_entry.grid(row=2, column=1, padx=5, pady=5)

        #box for sun_exposure
        tk.Label(
            newBed_FormFrame,
            text="Describe the Sun Exposure This Bed will Receive:",
            font=("Comfortaa",12),
            bg="Sienna"
        ).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.sun_exposure_entry = ttk.Entry(newBed_FormFrame, width=40)
        self.sun_exposure_entry.grid(row=3, column=1, padx=5, pady=5)

        #box for shade_structure
        tk.Label(
            newBed_FormFrame,
            text="Describe the Shade Structure, if any:",
            font=("Comfortaa",12),
            bg="Sienna"
        ).grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.shade_structure_entry = ttk.Entry(newBed_FormFrame, width=40)
        self.shade_structure_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(
            self,
            text="Save",
            command=self.save_new_bed
        ).pack(pady=30)

        ttk.Button(
            self,
            text="Back to Homepage",
            command=lambda: controller.show_frame(Home)
        ).pack(side="bottom", pady=30)

    # save data on button press
    def save_new_bed(self):
        bed_name = self.bed_name_entry.get()
        soil_depth = self.soil_depth_entry.get()
        soil_type = self.soil_type_entry.get()
        sun_exposure = self.sun_exposure_entry.get()
        shade_structure = self.shade_structure_entry.get()

        try:
            new_bed_id = self.bed_handler.populate_bed(
                bed_name,
                soil_depth,
                soil_type,
                sun_exposure,
                shade_structure
            )

            messagebox.showinfo(
                "Success",
                f"Saved successfully! The unique ID for {bed_name.strip()} is {new_bed_id}."
            )

            #self.clear_entries()
            self.controller.show_frame(Home)

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    # def clear_entries(self):
    #     self.bed_name_entry.delete(0, tk.END)
    #     self.soil_depth_entry.delete(0, tk.END)
    #     self.soil_type_entry.delete(0, tk.END)
    #     self.sun_exposure_entry.delete(0, tk.END)
    #     self.shade_structure_entry.delete(0, tk.END)

class AddNewSeedling(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="khaki1")
        self.controller = controller
        self.seedling_handler = NewSeedling(controller.db)

        self.plant_type_dropdown_format = {}
        self.bed_info_dropdown_format = {}

        tk.Label(
            self,
            text="Add a New Seedling",
            font=("Calibri", 24),
            bg="khaki1"
        ).pack(pady=10)

        newSeedling_FormFrame = tk.Frame(self,bg="khaki1")
        newSeedling_FormFrame.pack(pady=10)

        #box for plant_type_id (dropdown needed)
        tk.Label(
            newSeedling_FormFrame,
            text="Choose a Seed Variety from the dropdown:",
            font=("Comfortaa",12),
            bg="khaki1"
        ).grid(row=0,column=0, padx=5,pady=5, sticky="e")
        self.plant_type_dropdown = ttk.Combobox(newSeedling_FormFrame, width=37, state="readonly")
        self.plant_type_dropdown.grid(row=0,column=1,padx=5, pady=5)

        #box for bed_info_id (dropdown needed)
        tk.Label(
            newSeedling_FormFrame,
            text="From the dropdown, choose the bed this seed was planted in:",
            font=("Comfortaa",12),
            bg = "khaki1"
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.garden_bed_dropdown = ttk.Combobox(newSeedling_FormFrame, width=37, state="readonly")
        self.garden_bed_dropdown.grid(row=1,column=1,padx=5,pady=5)

        #box for seedling_nickname
        tk.Label(
            newSeedling_FormFrame,
            text="Seedling Nickname (example: Tomato - Row 1, Seed 1):",
            font=("Comfortaa", 12),
            bg="khaki1"
        ).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.seedling_nickname_entry = ttk.Entry(newSeedling_FormFrame, width=40)
        self.seedling_nickname_entry.grid(row=2, column=1, padx=5, pady=5)

        #box for date_planted
        tk.Label(
            newSeedling_FormFrame,
            text="Enter the date planted as YYYY-MM-DD:",
            font=("Comfortaa",12),
            bg="khaki1"
        ).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.date_planted_entry = ttk.Entry(newSeedling_FormFrame, width=40)
        self.date_planted_entry.grid(row=3, column=1, padx=5, pady=5)

        #save button
        ttk.Button(
            self,
            text="Save",
            command=self.save_seedling
        ).pack(pady=10)

        #back button
        ttk.Button(
            self,
            text="Back to Homepage",
            command=lambda: controller.show_frame(Home)
        ).pack(side="bottom", pady = 30)

        self.display_dropdown_options()

    def display_dropdown_options(self):
        cur = self.controller.db.conn.execute("""
            SELECT id, seed_variety
            FROM PlantType
            ORDER BY seed_variety ASC
        """)
        plant_rows = cur.fetchall()

        plant_list_display = ["---- Select from Dropdown ----"]
        self.plant_type_dropdown_format = {"---- Select from Dropdown ----": None}

        for row in plant_rows:
            list_display = f"{row['seed_variety']}"
            plant_list_display.append(list_display)
            self.plant_type_dropdown_format[list_display] = row["id"]

        self.plant_type_dropdown["values"] = plant_list_display
        if plant_list_display:
            self.plant_type_dropdown.current(0)
        else:
            self.plant_type_dropdown.set("")

        cur = self.controller.db.conn.execute("""
            SELECT id, bed_name
            FROM BedInfo
            ORDER BY bed_name ASC
        """)
        bed_rows = cur.fetchall()

        bed_list_display = ["---- Select from Dropdown ----"]
        self.bed_info_dropdown_format = {"---- Select from Dropdown ----": None}

        for row in bed_rows:
            list_display = f"{row['bed_name']}"
            bed_list_display.append(list_display)
            self.bed_info_dropdown_format[list_display] = row["id"]

        self.garden_bed_dropdown["values"] = bed_list_display
        if bed_list_display:
            self.garden_bed_dropdown.current(0)
        else:
            self.garden_bed_dropdown.set("")

    #save info below -  needs updated - current is copy from new bed section
    def save_seedling(self):
        chosen_seed_type = self.plant_type_dropdown.get()
        chosen_bed_type = self.garden_bed_dropdown.get()
        seedling_nickname = self.seedling_nickname_entry.get()
        date_planted = self.date_planted_entry.get()

        try:
            plant_type_id = self.plant_type_dropdown_format[chosen_seed_type]
            bed_info_id = self.bed_info_dropdown_format[chosen_bed_type]

            new_seedling_id = self.seedling_handler.populate_seedling(
                plant_type_id,
                bed_info_id,
                seedling_nickname,
                date_planted
            )

            messagebox.showinfo(
                "Success",
                f"Saved successfully! The unique ID for {seedling_nickname.strip()} is {new_seedling_id}."
            )

            #self.clear_entries()
            self.controller.show_frame(Home)

        except ValueError as e:
            messagebox.showerror("input Error", str(e))