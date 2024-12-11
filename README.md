# Tibia Items Editor

The **Tibia Items Editor** is a Python-based GUI application designed for managing items stored in an XML file. The application supports searching, editing, and saving XML data, with multi-language support.

---

## Features

- **Multi-language Support**: Available in Polish, English, and Portuguese.
- **Search Items**: Search for items by their name or partial name.
- **Edit Items**: Modify the attributes of selected items.
- **Save Changes**: Save the modified XML data to a file.
- **User-Friendly Interface**: Built using `Tkinter` for an intuitive GUI.

---

## Requirements

- Python 3.6+
- The following Python libraries:
  - `os`
  - `json`
  - `xml.etree.ElementTree`
  - `tkinter`

---

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/whitecrixu/tibia_items_editor.git
    cd tibia_items_editor
    ```

2. Install Python dependencies (if needed):

    ```bash
    pip install tk
    ```

3. Place your language files in the `lang` directory. The application supports:
    - `lang/lang_pl.json` (Polish)
    - `lang/lang_en.json` (English)
    - `lang/lang_pt.json` (Portuguese)

4. Prepare an XML file for testing or management.

---

## Usage

1. Run the application:

    ```bash
    python item_search_tool.py
    ```

2. Select a language from the prompt (e.g., `1` for Polish, `2` for English, `3` for Portuguese).

3. Use the buttons in the GUI to:
   - Load an XML file.
   - Search for items by name.
   - Edit attributes of selected items.
   - Save changes to a new XML file.
