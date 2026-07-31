# Holiday Compass — Public Holiday & Cultural Awareness Planner

A desktop app that lets you look up a country's public holidays for a given
year, compare two countries' holidays side by side, and generate a short
AI-written explanation of what any individual holiday means culturally.

Built with Python and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
for the GUI, the free [Nager.Date API](https://date.nager.at/) for holiday
data, and Google's Gemini API for the cultural explanations.

\*\*\*Steps

**1. Get the code and open a terminal in the project folder** (the one
containing `main.py` and `requirements.txt`).

**2. (Recommended) Create and activate a virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set your Gemini API key**

The app works without a key (holiday lookup and comparison still work),
but the "Search Holiday Meaning" button needs one to generate real AI
explanations. Get a free key from
[Google AI Studio](https://aistudio.google.com/app/apikey), then either:

- Create a file named `.env` in the project folder containing:
  ```
  GEMINI_API_KEY=your_key_here
  ```
- **or** set it as an environment variable directly:

  ```bash
  # Windows (PowerShell)
  $env:GEMINI_API_KEY="your_key_here"

  # macOS / Linux
  export GEMINI_API_KEY=your_key_here
  ```

**5. Run the app**

```bash
python main.py
```

**6. Using it**

- **View Holidays tab:** enter a 2-letter country code (e.g. `NG`, `US`,
  `GB` — see the reference list file for all valid codes) and a 4-digit
  year, then click **Get Holidays**. Click **Search Holiday Meaning** next
  to any holiday for its cultural explanation.
- **Compare Countries tab:** enter two country codes and a year, then click
  **Compare** to see shared holidays and holidays unique to each country.
- **Save Result to File:** saves whatever's currently showing (holiday list
  or comparison) as a `.txt` file.

---

## Notes for the presentation

- No internet access → holiday lookups will fail with a clear
  "Connection error" popup rather than crashing.
- No `GEMINI_API_KEY` set → the app still runs fully; the "meaning" text
  just falls back to a plain one-line description instead of an AI-written
  one.
- `requirements.txt` includes some packages (e.g. `streamlit`, `pandas`)
  that aren't actually used by this app — they can be trimmed down to just
  `customtkinter`, `requests`, `python-dotenv`, and `google-generativeai`
  if you want a leaner install.
