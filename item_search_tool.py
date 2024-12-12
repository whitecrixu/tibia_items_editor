import json
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

def load_language_file():
    """Wyświetla okno wyboru języka i ładuje odpowiedni plik językowy."""
    lang_files = {
        "1": "lang/lang_pl.json",
        "2": "lang/lang_en.json",
        "3": "lang/lang_pt.json"
    }

    root = tk.Tk()
    root.withdraw()

    choice = simpledialog.askstring(
        "Language Selection", "Select language:\n1. Polski\n2. English\n3. Português"
    )
    lang_file = lang_files.get(choice, "lang/lang_en.json")

    try:
        with open(lang_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "Language file not found. Defaulting to English.")
        with open("lang/lang_en.json", "r", encoding="utf-8") as file:
            return json.load(file)

def load_items(file_path):
    """Wczytuje dane z pliku XML."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return tree, root
    except FileNotFoundError:
        messagebox.showerror("Error", "XML file not found.")
        exit()
    except ET.ParseError:
        messagebox.showerror("Error", "XML file contains errors.")
        exit()

def search_item_by_name(root, search_query):
    """Wyszukuje przedmioty zawierające frazę w nazwie."""
    results = []
    for item in root.findall('item'):
        name = item.get('name', '').lower()
        attributes = {
            attr.get('key'): attr.get('value')
            for attr in item.findall('attribute')
        }
        if search_query.lower() in name or search_query.lower() == name:
            results.append({
                'id': item.get('id'),
                'name': item.get('name'),
                'attributes': attributes
            })
    return results

def display_results(results, tree):
    """Wyświetla wyniki wyszukiwania w interfejsie GUI."""
    for item in tree.get_children():
        tree.delete(item)
    if results:
        for result in results:
            tree.insert('', 'end', values=(
                result['id'], result['name'], result['attributes']
            ))
    else:
        messagebox.showinfo("Info", "No items found.")

def search_callback(entry, root, tree):
    """Callback dla przycisku wyszukiwania."""
    if root is None:
        messagebox.showerror("Error", "No XML file loaded. Please load a file first.")
        return
    query = entry.get().strip()
    results = search_item_by_name(root, query)
    display_results(results, tree)

def edit_item_callback(tree, xml_tree, xml_root):
    """Edytuje wybrany przedmiot."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No item selected.")
        return

    item_id = tree.item(selected_item, "values")[0]
    item_element = xml_root.find(f".//item[@id='{item_id}']")

    if item_element is None:
        messagebox.showerror("Error", "Item not found in XML.")
        return

    edit_window = tk.Toplevel()
    edit_window.title("Edit Item")

    fields = {}
    row = 0
    for attribute in item_element.findall('attribute'):
        key = attribute.get('key')
        value = attribute.get('value')

        tk.Label(edit_window, text=key).grid(row=row, column=0, padx=5, pady=5)
        entry = tk.Entry(edit_window, width=30)
        entry.insert(0, value)
        entry.grid(row=row, column=1, padx=5, pady=5)
        fields[key] = entry
        row += 1

    def save_changes():
        for key, entry in fields.items():
            new_value = entry.get()
            attr = item_element.find(f".//attribute[@key='{key}']")
            if attr is not None:
                attr.set('value', new_value)
        messagebox.showinfo("Info", "Item updated.")
        edit_window.destroy()

    tk.Button(edit_window, text="Save", command=save_changes).grid(
        row=row, column=0, columnspan=2, pady=10
    )

def save_file_callback(xml_tree):
    """Zapisuje zmodyfikowany plik XML."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xml", filetypes=[("XML files", "*.xml")]
    )
    if file_path:
        xml_tree.write(file_path, encoding="utf-8", xml_declaration=True)
        messagebox.showinfo("Info", "File saved successfully.")

def load_file_callback():
    """Callback do załadowania pliku XML."""
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if not file_path:
        return None, None
    try:
        tree, root = load_items(file_path)
        messagebox.showinfo("Info", "XML file loaded successfully.")
        return tree, root
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None, None

def on_close(root):
    """Obsługuje zdarzenie zamknięcia okna."""
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

def create_gui():
    """Tworzy GUI aplikacji."""
    root = tk.Tk()
    root.title("Item Management Tool")

    # Obsługa zamknięcia aplikacji
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))

    # Zmienne globalne
    global xml_tree, xml_root, language
    xml_tree, xml_root = None, None

    # Ładowanie języka
    language = load_language_file()

    # Elementy GUI
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    label = tk.Label(frame, text=language["enter_item_name"])
    label.grid(row=0, column=0, padx=5, pady=5)

    entry = tk.Entry(frame, width=30)
    entry.grid(row=0, column=1, padx=5, pady=5)

    result_tree = ttk.Treeview(
        root, columns=("ID", "Name", "Attributes"), show="headings"
    )
    result_tree.heading("ID", text="ID")
    result_tree.heading("Name", text="Name")
    result_tree.heading("Attributes", text="Attributes")
    result_tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def load_file_and_update_globals():
        global xml_tree, xml_root
        xml_tree, xml_root = load_file_callback()

    search_button = tk.Button(
        frame,
        text=language["search"],
        command=lambda: search_callback(entry, xml_root, result_tree)
    )
    search_button.grid(row=0, column=2, padx=5, pady=5)

    edit_button = tk.Button(
        root,
        text=language["edit_item"],
        command=lambda: edit_item_callback(result_tree, xml_tree, xml_root)
    )
    edit_button.pack(pady=5)

    save_button = tk.Button(
        root,
        text=language["save_file"],
        command=lambda: save_file_callback(xml_tree)
    )
    save_button.pack(pady=5)

    file_button = tk.Button(
        root, text=language["load_file"], command=load_file_and_update_globals
    )
    file_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()