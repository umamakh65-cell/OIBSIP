import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip


class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("700x800")
        self.root.minsize(600, 650)

        self.history = []

        # Variables
        self.length = tk.IntVar(value=16)
        self.uppercase = tk.BooleanVar(value=True)
        self.lowercase = tk.BooleanVar(value=True)
        self.numbers = tk.BooleanVar(value=True)
        self.symbols = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)

        self.password = tk.StringVar()
        self.strength = tk.StringVar(value="Strength: Not generated")

        self.create_gui()

    def create_gui(self):

        # ==========================================
        # Scrollable Window
        # ==========================================

        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            container,
            highlightthickness=0
        )
        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview
        )
        scrollbar.pack(
            side="right",
            fill="y"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        # Main content frame
        main = tk.Frame(
            canvas,
            padx=25,
            pady=20
        )

        # Add main frame to canvas
        canvas_window = canvas.create_window(
            (0, 0),
            window=main,
            anchor="nw"
        )

        # Update scroll region whenever content changes
        def update_scroll_region(event=None):
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        main.bind(
            "<Configure>",
            update_scroll_region
        )

        # Make content width match window width
        def update_canvas_width(event):
            canvas.itemconfig(
                canvas_window,
                width=event.width
            )

        canvas.bind(
            "<Configure>",
            update_canvas_width
        )

        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        canvas.bind_all(
            "<MouseWheel>",
            on_mousewheel
        )

        # Configure main grid
        main.grid_columnconfigure(
            0,
            weight=1
        )

        # ==========================================
        # Title
        # ==========================================

        tk.Label(
            main,
            text="Random Password Generator",
            font=("Arial", 22, "bold")
        ).grid(
            row=0,
            column=0,
            pady=5
        )

        tk.Label(
            main,
            text="Create strong and secure passwords",
            font=("Arial", 10)
        ).grid(
            row=1,
            column=0,
            pady=(0, 15)
        )

        # ==========================================
        # Password Length
        # ==========================================

        length_frame = tk.LabelFrame(
            main,
            text="Password Length",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10
        )

        length_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=5
        )

        tk.Label(
            length_frame,
            text="Length:"
        ).pack(
            side="left"
        )

        tk.Spinbox(
            length_frame,
            from_=8,
            to=64,
            textvariable=self.length,
            width=6
        ).pack(
            side="left",
            padx=10
        )

        tk.Label(
            length_frame,
            text="Minimum 8 characters"
        ).pack(
            side="left"
        )

        # ==========================================
        # Character Types
        # ==========================================

        types_frame = tk.LabelFrame(
            main,
            text="Character Types",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=8
        )

        types_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=5
        )

        tk.Checkbutton(
            types_frame,
            text="Uppercase Letters (A-Z)",
            variable=self.uppercase
        ).pack(
            anchor="w"
        )

        tk.Checkbutton(
            types_frame,
            text="Lowercase Letters (a-z)",
            variable=self.lowercase
        ).pack(
            anchor="w"
        )

        tk.Checkbutton(
            types_frame,
            text="Numbers (0-9)",
            variable=self.numbers
        ).pack(
            anchor="w"
        )

        tk.Checkbutton(
            types_frame,
            text="Symbols (!@#$...)",
            variable=self.symbols
        ).pack(
            anchor="w"
        )

        # ==========================================
        # Security Options
        # ==========================================

        security_frame = tk.LabelFrame(
            main,
            text="Security Options",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=8
        )

        security_frame.grid(
            row=4,
            column=0,
            sticky="ew",
            pady=5
        )

        tk.Checkbutton(
            security_frame,
            text="Exclude ambiguous characters (0, O, l, 1, I)",
            variable=self.exclude_ambiguous
        ).pack(
            anchor="w"
        )

        # ==========================================
        # Generated Password
        # ==========================================

        password_frame = tk.LabelFrame(
            main,
            text="Generated Password",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10
        )

        password_frame.grid(
            row=5,
            column=0,
            sticky="ew",
            pady=5
        )

        self.password_entry = tk.Entry(
            password_frame,
            textvariable=self.password,
            state="readonly",
            readonlybackground="white",
            font=("Consolas", 15),
            justify="center"
        )

        self.password_entry.pack(
            fill="x",
            ipady=8
        )

        tk.Label(
            password_frame,
            textvariable=self.strength,
            font=("Arial", 11, "bold")
        ).pack(
            pady=8
        )

        # Visual strength bar
        self.strength_bar = tk.Canvas(
            password_frame,
            height=18,
            bg="lightgray",
            highlightthickness=0
        )

        self.strength_bar.pack(
            fill="x"
        )

        # ==========================================
        # Buttons
        # ==========================================

        button_frame = tk.Frame(
            main
        )

        button_frame.grid(
            row=6,
            column=0,
            sticky="ew",
            pady=15
        )

        button_frame.grid_columnconfigure(
            0,
            weight=1
        )

        button_frame.grid_columnconfigure(
            1,
            weight=1
        )

        # Generate Password button
        tk.Button(
            button_frame,
            text="GENERATE PASSWORD",
            command=self.generate_password,
            bg="#7B1FA2",
            fg="white",
            activebackground="#4A148C",
            activeforeground="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            cursor="hand2",
            relief="raised",
            bd=3
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5
        )

        # Copy to Clipboard button
        tk.Button(
            button_frame,
            text="COPY TO CLIPBOARD",
            command=self.copy_password,
            bg="#1565C0",
            fg="white",
            activebackground="#0D47A1",
            activeforeground="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            cursor="hand2",
            relief="raised",
            bd=3
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5
        )

        # ==========================================
        # Generation History
        # ==========================================

        history_frame = tk.LabelFrame(
            main,
            text="Generation History - Last 5",
            font=("Arial", 10, "bold"),
            fg="#7B1FA2",
            padx=10,
            pady=8,
            height=180
        )

        history_frame.grid(
            row=7,
            column=0,
            sticky="ew",
            pady=5
        )

        history_frame.grid_propagate(False)

        self.history_list = tk.Listbox(
            history_frame,
            font=("Consolas", 10),
            bg="#F3E5F5",
            fg="#212121",
            selectbackground="#7B1FA2",
            selectforeground="white",
            relief="solid",
            bd=1
        )

        self.history_list.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            history_frame,
            text="Passwords are kept only during this session.",
            font=("Arial", 9),
            fg="#555555"
        ).pack(
            pady=5
        )

    def get_character_sets(self):
        sets = []

        if self.uppercase.get():
            sets.append(string.ascii_uppercase)

        if self.lowercase.get():
            sets.append(string.ascii_lowercase)

        if self.numbers.get():
            sets.append(string.digits)

        if self.symbols.get():
            sets.append(string.punctuation)

        # Remove ambiguous characters
        if self.exclude_ambiguous.get():
            ambiguous = "0Ol1I"

            sets = [
                "".join(
                    char
                    for char in charset
                    if char not in ambiguous
                )
                for charset in sets
            ]

        return [
            charset
            for charset in sets
            if charset
        ]

    def generate_password(self):
        # Validate length
        try:
            length = int(self.length.get())

        except (ValueError, TypeError):
            messagebox.showerror(
                "Invalid Length",
                "Please enter a valid number."
            )
            return

        if length < 8:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be at least 8 characters."
            )
            return

        if length > 64:
            messagebox.showerror(
                "Invalid Length",
                "Password length cannot exceed 64 characters."
            )
            return

        # Count selected character types
        selected_count = sum([
            self.uppercase.get(),
            self.lowercase.get(),
            self.numbers.get(),
            self.symbols.get()
        ])

        # At least two types must be selected
        if selected_count < 2:
            messagebox.showerror(
                "Invalid Selection",
                "Please select at least 2 character types."
            )
            return

        character_sets = self.get_character_sets()

        if len(character_sets) < 2:
            messagebox.showerror(
                "Invalid Selection",
                "Please select at least 2 usable character types."
            )
            return

        # Guarantee one character from every selected type
        password_characters = []

        for charset in character_sets:
            password_characters.append(
                secrets.choice(charset)
            )

        # Combined character pool
        all_characters = "".join(character_sets)

        # Fill remaining characters
        while len(password_characters) < length:
            password_characters.append(
                secrets.choice(all_characters)
            )

        # Secure shuffle
        for i in range(
            len(password_characters) - 1,
            0,
            -1
        ):
            j = secrets.randbelow(i + 1)

            password_characters[i], password_characters[j] = (
                password_characters[j],
                password_characters[i]
            )

        generated = "".join(password_characters)

        # Display password
        self.password.set(generated)

        # Calculate strength
        strength, score = self.calculate_strength(
            generated,
            selected_count
        )

        self.strength.set(
            "Strength: " + strength
        )

        # Update strength bar
        self.update_strength_bar(score)

        # Automatically copy password
        self.copy_to_clipboard(generated)

        # Add to history
        self.add_history(generated)

    def calculate_strength(
        self,
        password,
        selected_count
    ):
        score = 0

        # Password length
        if len(password) >= 8:
            score += 1

        if len(password) >= 12:
            score += 2

        if len(password) >= 20:
            score += 2

        # Character diversity
        if any(
            char.islower()
            for char in password
        ):
            score += 1

        if any(
            char.isupper()
            for char in password
        ):
            score += 1

        if any(
            char.isdigit()
            for char in password
        ):
            score += 1

        if any(
            char in string.punctuation
            for char in password
        ):
            score += 1

        # Character type diversity
        if selected_count >= 3:
            score += 1

        if selected_count == 4:
            score += 1

        # Strength result
        if score <= 3:
            return "Weak", 30

        if score <= 6:
            return "Medium", 65

        return "Strong", 100

    def update_strength_bar(self, score):
        self.strength_bar.delete("all")

        width = self.strength_bar.winfo_width()

        if width < 10:
            width = 500

        if score <= 30:
            bar_color = "#E53935"

        elif score <= 65:
            bar_color = "#FB8C00"

        else:
            bar_color = "#43A047"

        self.strength_bar.create_rectangle(
            0,
            0,
            width * score / 100,
            18,
            fill=bar_color,
            outline=""
        )

    def copy_to_clipboard(self, password):
        try:
            pyperclip.copy(password)

        except Exception:
            # Password generation still succeeds
            # even if clipboard access fails.
            pass

    def copy_password(self):
        password = self.password.get()

        if not password:
            messagebox.showwarning(
                "No Password",
                "Please generate a password first."
            )
            return

        try:
            pyperclip.copy(password)

            messagebox.showinfo(
                "Copied",
                "Password copied to clipboard successfully."
            )

        except Exception as error:
            messagebox.showerror(
                "Clipboard Error",
                str(error)
            )

    def add_history(self, password):
        # Add newest password first
        self.history.insert(
            0,
            password
        )

        # Keep only the latest 5
        self.history = self.history[:5]

        # Clear history display
        self.history_list.delete(
            0,
            tk.END
        )

        # Display passwords
        for item in self.history:
            self.history_list.insert(
                tk.END,
                item
            )


# ==============================
# START APPLICATION
# ==============================

root = tk.Tk()

app = PasswordGenerator(root)

root.mainloop()
