import customtkinter as ctk
from tkinter import filedialog, messagebox

from country import Country
from holiday_api_client import HolidayAPIClient
from culture_guide_generator import CultureGuideGenerator
from file_helpers import save_favourite

#  Named colours and fonts (change once here, applies everywhere) 
BG_COLOR = "#1E2723"       
TEXT_COLOR = "#E8F0EC"     
STATUS_COLOR = "#A8C4B4"   # slightly lighter green, for the status line
BOX_FONT = ("Arial", 13)   # font used for holiday text and comparison results
TITLE_FONT = ("Arial", 16, "bold")

# --- Button styling ---
BTN_FILL = "#3F6B52"       # sage green button colour
BTN_HOVER = "#4F8265"      # darker green when hovered
BTN_TEXT_COLOR = "white"
BTN_FONT = ("Arial", 12, "bold")  # bold button text
BTN_RADIUS = 21 
# BTN is short form for Button 

ctk.set_appearance_mode("dark")

client = HolidayAPIClient()
generator = CultureGuideGenerator()  # reads GEMINI_API_KEY from the environment

last_result = {"text": ""}
current_holidays = []  # Holiday objects from the last "Get Holidays" searchm  


def rounded_button(parent, text, command, width=135, height=40):
    return ctk.CTkButton(
        parent, text=text, command=command,
        corner_radius=BTN_RADIUS, width=width, height=height,
        fg_color=BTN_FILL, hover_color=BTN_HOVER,
        text_color=BTN_TEXT_COLOR, font=BTN_FONT,
    )


def show_holidays():
    output_box.pack_forget()  
    list_container.pack(padx=14, pady=(0, 8), fill="both", expand=True)
    clear_holiday_rows()
    try:
        country = Country(code_entry.get())
        holidays = client.get_holidays(country, year_entry.get())

        if not holidays:
            status_label.configure(text=f"No public holidays found for {country.code} in {year_entry.get()}.")
            return

        save_favourite(country.code)
        current_holidays.clear()
        current_holidays.extend(holidays)

        for h in holidays:
            add_holiday_row(h, country.code)

        # Build the full holiday list text for saving - not just a count
        lines = [f"Holiday Guide - {country.code} - {year_entry.get()}", "=" * 40, ""]
        for h in holidays:
            lines.append(f"{h.date} | {h.name} ({h.holiday_type})")
        last_result["text"] = "\n".join(lines)

        status_label.configure(
            text=f"Loaded {len(holidays)} holidays for {country.code} - {year_entry.get()}."
            + "  Click 'Search Holiday Meaning' next to a holiday for its cultural meaning."
        )

    except ValueError as e:
        messagebox.showerror("Input error", str(e))
    except ConnectionError as e:
        messagebox.showerror("Connection error", str(e))

    except ValueError as e:
        messagebox.showerror("Input error", str(e))
    except ConnectionError as e:
        messagebox.showerror("Connection error", str(e))


def clear_holiday_rows():
    # removes all the holiday rows from the previous search before loading new ones
    for widget in holiday_frame.winfo_children():
        widget.destroy()


def add_holiday_row(holiday, country_code):
    # builds one row: the holiday info, a Generate button, and a spot for the explanation
    row = ctk.CTkFrame(holiday_frame, fg_color="#2A3530", corner_radius=10)
    row.pack(fill="x", padx=8, pady=8)

    info = ctk.CTkLabel(
        row,
        text=f"{holiday.date} | {holiday.name} ({holiday.holiday_type})",
        text_color=TEXT_COLOR, font=BOX_FONT, anchor="w", justify="left",
    )
    info.pack(side="top", fill="x", padx=10, pady=(8, 4))

    explanation_label = ctk.CTkLabel(
        row, text="", text_color=TEXT_COLOR, font=BOX_FONT,
        wraplength=620, justify="left", anchor="w",
    )
    explanation_label.pack(side="top", fill="x", padx=10, pady=(0, 6))

    def on_generate():
        # only this ONE holiday gets sent to the AI, not the whole list
        generate_btn.configure(state="disabled", text="Searching...")
        row.update()
        explanation = generator.generate(holiday, country_code)
        explanation_label.configure(text=explanation)
        generate_btn.configure(state="normal", text="Searching")

    generate_btn = rounded_button(row, "Search Holiday Meaning", on_generate, width=110, height=32)
    generate_btn.pack(side="top", anchor="w", padx=10, pady=(0, 10))


def compare_countries():
    list_container.pack_forget()  # hide the empty holiday list so it doesn't block this box
    output_box.pack(padx=14, pady=14, fill="both", expand=True)  # show the big box, same size as the holiday list
    output_box.delete("1.0", "end") # delete from the frist text to the last in d box dat 
    clear_holiday_rows()
    status_label.configure(text="")
    try:
        country_a = Country(cmp_code_a.get())
        country_b = Country(cmp_code_b.get())
        year = cmp_year.get()

        holidays_a = {h.date: h for h in client.get_holidays(country_a, year)}
        holidays_b = {h.date: h for h in client.get_holidays(country_b, year)}

        shared = sorted(set(holidays_a) & set(holidays_b))
        only_a = sorted(set(holidays_a) - set(holidays_b))
        only_b = sorted(set(holidays_b) - set(holidays_a))

        lines = [f"Comparison - {country_a.code} vs {country_b.code} - {year}", "=" * 40, "", "Shared dates:"]
        for d in shared:
            lines.append(f"  {d}: {holidays_a[d].name} (A) / {holidays_b[d].name} (B)")

        lines.append(f"\nOnly in {country_a.code}:")
        for d in only_a:
            lines.append(f"  {d}: {holidays_a[d].name}")

        lines.append(f"\nOnly in {country_b.code}:")
        for d in only_b:
            lines.append(f"  {d}: {holidays_b[d].name}")

        last_result["text"] = "\n".join(lines)
        output_box.insert("end", last_result["text"])

    except ValueError as e:
        messagebox.showerror("Input error", str(e))
    except ConnectionError as e:
        messagebox.showerror("Connection error", str(e))


def save_result():
    if not last_result["text"]:
        messagebox.showinfo("Nothing to save", "Get some holidays or a comparison first.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", "*.txt")])
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(last_result["text"])
        messagebox.showinfo("Saved", f"Saved to {path}")


window = ctk.CTk()
window.title("Public Holiday & Cultural Awareness Planner")
window.geometry("750x650")
window.configure(fg_color=BG_COLOR)

ctk.CTkLabel(window, text="HOLIDAY COMPASS", text_color=TEXT_COLOR,
             font=TITLE_FONT, fg_color=BG_COLOR).pack(pady=(16, 10))

# --- Tabs: single country lookup vs comparison ---
tabs = ctk.CTkTabview(window, fg_color=BG_COLOR, segmented_button_fg_color=BTN_FILL,
                       segmented_button_selected_color=BTN_HOVER,
                       segmented_button_selected_hover_color=BTN_HOVER,
                       segmented_button_unselected_color=BTN_FILL, text_color="white",
                       height=90)
tabs.pack(pady=12, padx=14, fill="x")
tabs.add("View Holidays")
tabs.add("Compare Countries")

# Tab 1: single country
single_tab = tabs.tab("View Holidays")

ctk.CTkLabel(single_tab, text="Country code:", text_color=TEXT_COLOR, fg_color=BG_COLOR).grid(row=0, column=0, padx=8, pady=10)
code_entry = ctk.CTkEntry(single_tab, width=80, corner_radius=10)
code_entry.grid(row=0, column=1, padx=8, pady=10)

ctk.CTkLabel(single_tab, text="Year:", text_color=TEXT_COLOR, fg_color=BG_COLOR).grid(row=0, column=2, padx=8, pady=10)
year_entry = ctk.CTkEntry(single_tab, width=80, corner_radius=10)
year_entry.grid(row=0, column=3, padx=8, pady=10)

rounded_button(single_tab, "Get Holidays", show_holidays, width=140, height=38).grid(row=0, column=4, padx=12, pady=10)

# Tab 2: compare
compare_tab = tabs.tab("Compare Countries")

ctk.CTkLabel(compare_tab, text="Country A:", text_color=TEXT_COLOR, fg_color=BG_COLOR).grid(row=0, column=0, padx=8, pady=10)
cmp_code_a = ctk.CTkEntry(compare_tab, width=80, corner_radius=10)
cmp_code_a.grid(row=0, column=1, padx=8, pady=10)

ctk.CTkLabel(compare_tab, text="Country B:", text_color=TEXT_COLOR, fg_color=BG_COLOR).grid(row=0, column=2, padx=8, pady=10)
cmp_code_b = ctk.CTkEntry(compare_tab, width=80, corner_radius=10)
cmp_code_b.grid(row=0, column=3, padx=8, pady=10)

ctk.CTkLabel(compare_tab, text="Year:", text_color=TEXT_COLOR, fg_color=BG_COLOR).grid(row=0, column=4, padx=8, pady=10)
cmp_year = ctk.CTkEntry(compare_tab, width=80, corner_radius=10)
cmp_year.grid(row=0, column=5, padx=8, pady=10)

rounded_button(compare_tab, "Compare", compare_countries, width=120, height=38).grid(row=0, column=6, padx=12, pady=10)

# --- Status line (plain text, no box, sits directly on the window background) ---
status_label = ctk.CTkLabel(window, text="", text_color=STATUS_COLOR, fg_color=BG_COLOR,
                             font=("Arial", 11, "italic"), anchor="w", justify="left")
status_label.pack(padx=14, pady=(0, 6), fill="x")

# --- Scrollable holiday list (each row has its own Generate button) ---
list_container = ctk.CTkFrame(window, fg_color=BG_COLOR)
list_container.pack(padx=14, pady=(0, 8), fill="both", expand=True)

holiday_frame = ctk.CTkScrollableFrame(list_container, fg_color="#2A3530", height=250, corner_radius=12)
holiday_frame.pack(fill="both", expand=True)

# --- Output box (used for comparison results only - stays hidden until Compare is clicked) ---
output_box = ctk.CTkTextbox(window, width=680, height=280, wrap="word", font=BOX_FONT,
                             text_color=TEXT_COLOR, fg_color="#2A3530", corner_radius=12)

rounded_button(window, "Save Result to File", save_result, width=200, height=40).pack(pady=(4, 16))

window.mainloop()