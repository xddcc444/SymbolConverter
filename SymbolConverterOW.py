import random
import tkinter as tk
import sys
import os

MAX_LENGTH = 30  # Define the max length globally or at the top of your script
FORBIDDEN_CHARS = set(' .,;:`\'"[]{}()<>!?/\\|@#$%^&*~-_+=№')
bold18 = ('Century Gothic', 18, 'bold')
bold14 = ('Century Gothic', 14, 'bold')
btn10 = ('Century Gothic', 10, 'bold')
btn12 = ('Century Gothic', 12, 'bold')
symbolbtn14 = ('Arial', 14, 'bold')
symbolbtn20 = ('Arial', 20, 'bold')
subtxt10 = ('Century Gothic', 10)
# Define the special letter mapping
special_map = {
    'a': ['Ǎ', 'Ǻ', 'Ǟ', 'Ȁ', 'Ȃ', 'Ǡ', 'Ą'],
    'b': ['Ɓ', 'Ƃ', 'Ƅ', 'ƃ', 'ƅ'],
    'c': ['Ƈ', 'Ɔ', 'Ċ', 'Ĉ', 'Ç'],
    'd': ['D', 'Đ', 'Ď'],
    'e': ['Ȅ', 'Ȇ', 'Ĕ', 'Ē', 'Ė', 'Ę', 'Ě', 'È', 'É', 'Ê', 'Ë', 'Ɛ', 'ǝ'],
    'f': 'Ƒ',
    'g': ['Ǵ', 'Ǧ', 'Ĝ', 'Ġ', 'Ģ', 'Ɠ'],
    'h': ['Ĥ', 'Ħ', 'ƕ'],
    'i': ['Ȉ', 'Ȋ', 'Ĭ', 'Ǐ', 'Ɨ', 'Ĩ', 'Į', 'Ì', 'Í', 'Î', 'Ï', 'Ɩ'],
    'j': ['Ĵ', 'ǰ'],
    'k': ['Ƙ', 'Ǩ', 'Ķ', 'ĸ'],
    'l': ['Ŀ', 'Ļ', 'Ĺ', 'Ľ', 'Ł'],
    'm': 'M',
    'n': ['Ŋ', 'Ň', 'Ņ', 'Ń', 'Ñ', 'Ǹ'],
    'o': ['Ø', 'Ǿ', 'Ȍ', 'Ő', 'Ȏ', 'Ǒ', 'Ŏ', 'Ō', 'Ö', 'Ò', 'Ó', 'Ô', 'Õ', 'Ǫ', 'Ǭ'],
    'p': 'P',
    'q': 'Q',
    'r': ['Ȑ', 'Ȓ', 'Ŗ', 'Ŕ', 'Ř'],
    's': ['Ś', 'Ŝ', 'Š', 'Ş'],
    't': ['Ŧ', 'Ţ', 'Ť'],
    'u': ['Ŭ', 'Ȕ', 'Ű', 'Ȗ', 'Ǔ', 'Ǖ', 'Ǘ', 'Ǚ', 'Ǜ', 'Ũ', 'Ū', 'Ů', 'Ų', 'Ù', 'Ú', 'Û', 'Ü'],
    'v': 'Ɣ',
    'w': 'Ŵ',
    'x': 'X',
    'y': ['Ŷ', 'Ÿ', 'Ŷ', 'Ý'],
    'z': ['Ź', 'Ż', 'Ž'],

}


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller sets this
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def replace_with_special(word):
    if len(word) == 1 and word in special_map:
        # Return all possible variants for single character input
        return ''.join(special_map[word])
    result = ''
    for char in word:
        if char in special_map:
            replacement = (
                random.choice(special_map[char])
                if isinstance(special_map[char], list)
                else special_map[char]
            )
            result += replacement
        else:
            result += char
    return result


def run_gui():
    def on_transform():
        input_text = input_entry.get()

        # Clear previous variants/buttons
        for widget in variants_frame.winfo_children():
            widget.destroy()

        if len(input_text) == 1 and input_text in special_map:
            # Clear transformed string
            result_label.config(text="")

            # Clear previous widgets
            for widget in variants_frame.winfo_children():
                widget.destroy()

            # Show label
            tk.Label(variants_frame, text=f"Variants of '{input_text}':", font=bold14, bg="lightblue").pack(pady=(0, 5))

            variants = special_map[input_text]
            total = len(variants)

            # Split dynamically into up to 2 rows
            if total <= 9:
                row1 = variants
                row2 = []
            else:
                split = total // 2 + total % 2  # Ensures first row has more if odd number
                row1 = variants[:split]
                row2 = variants[split:]

            row1_frame = tk.Frame(variants_frame, bg="lightblue")
            row1_frame.pack(anchor='center', pady=2)

            for variant in row1:
                btn = tk.Button(
                    row1_frame,
                    text=variant,
                    width=3,
                    bg="#ddeeff",
                    fg="#003366",
                    activebackground="#88bbff",
                    activeforeground="#001122",
                    font=symbolbtn20,
                    relief=tk.RAISED,
                    command=lambda v=variant: insert_variant(v)
                )
                btn.pack(side=tk.LEFT, padx=2)
                btn.bind("<Enter>", on_enter)
                btn.bind("<Leave>", on_leave)

            # If second row exists, do the same
            if row2:
                row2_frame = tk.Frame(variants_frame, bg="lightblue")
                row2_frame.pack(anchor='center', pady=2)

                for variant in row2:
                    btn = tk.Button(
                        row2_frame,
                        text=variant,
                        width=3,
                        bg="#ddeeff",
                        fg="#003366",
                        activebackground="#88bbff",
                        activeforeground="#001122",
                        font=symbolbtn20,
                        relief=tk.RAISED,
                        command=lambda v=variant: insert_variant(v)
                    )
                    btn.pack(side=tk.LEFT, padx=2)
                    btn.bind("<Enter>", on_enter)
                    btn.bind("<Leave>", on_leave)

            copy_button.pack_forget()

        else:
            # No variants, show spacer instead
            spacer = tk.Label(variants_frame, text="", height=2, bg="lightblue")
            spacer.pack()

            transformed = replace_with_special(input_text)
            result_label.config(text=transformed)

            copy_button.pack()

    def insert_symbol(symbol):
        pos = input_entry.index(tk.INSERT)  # Get current cursor position
        input_entry.insert(pos, symbol)
        update_length()  # Update the length label

    def on_copy():
        text_to_copy = result_label.cget("text")
        window.clipboard_clear()
        window.clipboard_append(text_to_copy)
        copy_status.config(text="Copied!", font=subtxt10)

    def on_validate(new_text):
        if len(new_text) > MAX_LENGTH:
            return False
        if any(c in FORBIDDEN_CHARS for c in new_text):
            return False
        if new_text and new_text[0].isdigit():
            return False
        window.after_idle(update_length)
        return True

    def update_length(event=None):
        current_length = len(input_entry.get())
        length_label.config(text=f"Length: {current_length}", font=subtxt10)
        length_label.config(fg="green" if current_length <= 12 else "red")
        copy_status.config(text="")  # Reset copy status

    def insert_variant(symbol):
        input_entry.insert(input_entry.index(tk.INSERT), symbol)
        update_length()

    def on_enter(e):
        e.widget['bg'] = '#aaddff'

    def on_leave(e):
        e.widget['bg'] = '#ddeeff'

    def show_help_window():
        help_win = tk.Toplevel(window)
        help_win.title("Help")
        help_win.geometry("512x288")
        help_win.configure(bg="lightblue")
        help_win.resizable(False, False)
        help_win.iconbitmap(resource_path("symbolconverter.ico"))

        tk.Label(help_win, text="How to Use", font=bold18, bg="lightblue").pack(pady=(10, 5))
        tk.Message(
            help_win,
            text="• You can enter up to 30 characters — spaces and most special symbols are not allowed.\n"
                 "• Input cannot start with a number.\n"
                 "• Type a single letter and click 'Transform' to view its symbol variants.\n"
                 "• Click any symbol in the Insert section to place it at your cursor.\n"
                 "• You can continue typing or transforming using inserted symbols.",
            font=("Century Gothic", 11),
            width=350,
            bg="lightblue"
        ).pack(pady=(0, 10))

        tk.Button(help_win,
                  text="Close",
                  bg="#ddeeff",
                  fg="#003366",
                  activebackground="#88bbff",
                  activeforeground="#001122",
                  font=btn10,
                  relief=tk.FLAT,
                  command=help_win.destroy).pack()

    # Create window
    window = tk.Tk()
    window.configure(bg="lightblue")
    window.title("Special Letter Converter")
    window.geometry("1024x576")
    window.resizable(False, False)
    window.iconbitmap(resource_path("symbolconverter.ico"))

    # Register the validation function
    vcmd = (window.register(on_validate), "%P")

    # Create a top-left floating frame for help button
    help_frame = tk.Frame(window)
    help_frame.place(x=10, y=10)  # Absolute position (10px from top and left)

    # Create the Help button
    help_button = tk.Button(help_frame,
                            text="Help",
                            bg="#ddeeff",
                            fg="#003366",
                            activebackground="#88bbff",
                            activeforeground="#001122",
                            font=btn10,
                            relief=tk.FLAT,
                            command=show_help_window)
    help_button.pack()
    # === Input ===
    tk.Label(window, text="Enter text:", font=bold18, bg="lightblue").pack(pady=(10, 0))
    entry_frame = tk.Frame(window, bg='lightgray', padx=5, pady=5)
    entry_frame.pack()
    input_entry = tk.Entry(window,
                           font=('Century Gothic', 14, 'italic'),
                           fg='darkblue',
                           bg='lightyellow',
                           width=40,
                           relief=tk.SUNKEN,
                           insertbackground='red',
                           validate="key",
                           validatecommand=vcmd)
    input_entry.pack(pady=5)
    input_entry.bind('<Return>', lambda event: on_transform())

    # === Length label ===
    length_label = tk.Label(window, text="Length: 0", font=subtxt10, bg="lightblue")
    length_label.pack()

    # === Symbol insert header ===
    symbol_frame = tk.Frame(window)
    symbol_frame.pack(pady=5)
    tk.Label(symbol_frame, text="Insert symbol:", font=bold18, bg="lightblue").pack(side=tk.LEFT)

    # === Symbol groups ===
    symbol_groups_frame = tk.Frame(window, bg="lightblue")
    symbol_groups_frame.pack(pady=10)

    def create_symbol_group(parent, title, color, symbols):
        box = tk.Frame(parent, highlightbackground=color, highlightthickness=2, padx=10, pady=10, bg="lightblue")
        box.pack(side=tk.LEFT, padx=10)
        tk.Label(box, text=title, font=bold14, bg="lightblue").pack(pady=(0, 5))

        for symbol in symbols:
            btn = tk.Button(
                box,
                text=symbol,
                width=3,
                bg="#ddeeff",
                fg="#003366",
                activebackground="#88bbff",
                activeforeground="#001122",
                font=symbolbtn14,
                relief=tk.RAISED,
                bd=3,
                command=lambda s=symbol: insert_symbol(s)
            )
            btn.pack(side=tk.LEFT, padx=3, pady=3)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

    create_symbol_group(symbol_groups_frame, "Special", "#3fa34d", ['ǂ', 'ǃ', 'ǀ', 'ǁ', 'Ǯ'])
    create_symbol_group(symbol_groups_frame, "Double", "#0077cc", ['Ǆ', 'Ǳ', 'Ǉ', 'Ǌ', 'Ĳ', 'Œ', 'Ǽ', 'Ǣ'])
    create_symbol_group(symbol_groups_frame, "Square", "#cc4444", ['Ƕ', 'Ƿ', 'Ǹ'])

    # === Transform button ===
    transform_button = tk.Button(
        window,
        text="Transform",
        bg="#ddeeff",
        fg="#003366",
        activebackground="#88bbff",
        activeforeground="#001122",
        font=btn12,
        relief=tk.RAISED,
        command=on_transform)
    transform_button.pack(pady=(0, 25))
    transform_button.bind("<Enter>", on_enter)
    transform_button.bind("<Leave>", on_leave)
    # === Result output ===
    result_label = tk.Label(window, text="", font=('Arial', 20, 'bold'), fg="#000000", wraplength=700, bg="lightblue")
    result_label.pack(pady=(5, 0))

    # === Variants frame (for single-letter transformation options) ===
    variants_frame = tk.Frame(window, bg="lightblue")
    variants_frame.pack(pady=(0, 5))
    #spacer = tk.Label(variants_frame, text="", height=2, bg="lightblue")
    #spacer.pack()

    # === Copy Output button inside a frame ===
    copy_frame = tk.Frame(window, bg="lightblue")
    copy_frame.pack(pady=5)  # Fixed vertical position

    copy_button = tk.Button(
        copy_frame,
        text="Copy Output",
        bg="#ddeeff",
        fg="#003366",
        activebackground="#88bbff",
        activeforeground="#001122",
        font=btn12,
        relief=tk.RAISED,
        command=on_copy)
    copy_button.pack()  # Pack once here
    copy_button.bind("<Enter>", on_enter)
    copy_button.bind("<Leave>", on_leave)

    # === FINAL copy status line ===
    copy_status = tk.Label(window, text="", fg="green", bg="lightblue")
    copy_status.pack()

    # === Keep references in global or outer scope if needed ===
    window.input_entry = input_entry
    window.length_label = length_label
    window.copy_button = copy_button
    window.result_label = result_label
    window.variants_frame = variants_frame
    window.copy_status = copy_status

    window.mainloop()


run_gui()
