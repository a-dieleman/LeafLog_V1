#file made to handle validation in order to simplify other methods and support future scalability

from datetime import datetime
import tkinter as tk
from tkinter import ttk

#method to check TEXT fields that are required
def text_is_required(value, field_name):
    value = str(value).strip()
    if not value:
        raise ValueError(f"The {field_name} box cannot be empty.")
    return value

#method to format optional text fields
def text_is_optional(value):
    if value is None:
        return None
    value = str(value).strip()
    return value if value else None

#method to make sure integers are >0
def num_is_positive(value, field_name):
    try:
        number = int(str(value).strip())
        if number < 0:
            raise ValueError
        return number
    except (ValueError, TypeError):
        raise ValueError(f"The {field_name} box cannot contain a negative number.")

#method to check NUMBER fields that are required
def num_is_required(value, field_name):
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        raise ValueError(f"The {field_name} box cannot be empty.")

#method to handle optional integers (default if empty)
def num_is_optional(value, field_name="Value", default=0):
    if str(value).strip() == "":
        return default

    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        raise ValueError(f"The {field_name} box cannot be blank.")

#method to make sure date is in YYYY-MM-DD format
def require_date(value, field_name, date_format="%Y-%m-%d"):
    value = text_is_required(value, field_name)
    try:
        entered_date = datetime.strptime(value, date_format).date()
        return value, entered_date
    except ValueError:
        raise ValueError(f"{field_name} must be in YYYY-MM-DD format.")

#method to handle Y/N variations
def handle_yn(value, field_name="Input"):
    value = str(value).strip().lower()
    if value in ("yes", "y", "yeah"):
        return "yes"
    if value in ("no", "n", ""):
        return "no"
    raise ValueError(f"The {field_name} must be yes, no, or blank.")

#method to help handle dropdown validation
def dropdown_required(chosen_value, results, field_name):
    chosen_value = str(chosen_value).strip()
    if not chosen_value:
        raise ValueError(f"The {field_name} dropdown must be selected.")
    if chosen_value not in results:
        raise ValueError(f"Entry in {field_name} is invalid. Please select option from provided dropdown.")
    return results[chosen_value]

def clear_text(widgets):
    for widget in widgets:
        if isinstance(widget, ttk.Combobox):
            widget.set("----Select from Dropdown----")
        elif isinstance(widget, tk.Entry):
            widget.delete(0, tk.END)

