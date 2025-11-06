import tkinter as tk
from pet_SMM import PetSMM
from storage_SMM import save_result_SMM, load_best_result_SMM

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Pet")
        self.bg_color = "#ccfffa"
        self.root.configure(bg=self.bg_color)
        self.pet = PetSMM("Morzsi")
        self.show_main_menu()


    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(expand=True)

        tk.Label(frame, text="Virtual Pet", font=("Arial", 24, "bold"), bg=self.bg_color).pack(pady=20)

        tk.Button(frame, text="Új játék indítása", width=25, height=2, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=self.start_game).pack(pady=10)
        tk.Button(frame, text="Statisztikák megtekintése", width=25, height=2, font=("Arial", 12, "bold"), bg="#2196F3", fg="white", command=self.show_stats).pack(pady=10)
        tk.Button(frame, text="Kilépés", width=25, height=2, font=("Arial", 12, "bold"), bg="#f44336", fg="white", command=self.root.destroy).pack(pady=10)


    def start_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.pet = PetSMM("Morzsi")
        self.money = 1000
        self.food = 0
        self.toys = 0
        self.hour = 0
        self.day = 1
        self.score = 0
        self.multiplier = 1.0
        self.warning_active = False


        self.day_label = tk.Label(self.root, text=f"Nap: {self.day} | Óra: {self.hour}", font=("Arial", 14, "bold"), bg=self.bg_color)
        self.day_label.pack(pady=15)

        self.money_label = tk.Label(self.root, text=self.get_inventory(), font=("Arial", 11), bg=self.bg_color)
        self.money_label.pack(pady=5)

        tk.Label(self.root, text=f"{self.pet.name} állapota", font=("Arial", 16, "bold"), bg=self.bg_color).pack(pady=5)


        self.status_frame = tk.Frame(self.root, bg=self.bg_color)
        self.status_frame.pack(pady=10)

        self.create_status_row("Éhség", self.feed, "Etetés")
        self.create_status_row("Energia", self.sleep, "Alvás")
        self.create_status_row("Boldogság", self.play, "Játék")


        self.shop_frame = tk.Frame(self.root, bg=self.bg_color)
        self.shop_frame.pack(pady=15)

        tk.Button(self.shop_frame, text="Vesz tápot (20)", command=self.buy_food, width=20).grid(row=0, column=0, padx=10)
        tk.Button(self.shop_frame, text="Vesz játékszert (50)", command=self.buy_toy, width=20).grid(row=0, column=1, padx=10)


        self.status_label = tk.Label(self.root, text="Válassz tevékenységet!", font=("Arial", 11), bg=self.bg_color)
        self.status_label.pack(pady=10)


        self.bottom_frame = tk.Frame(self.root, bg=self.bg_color)
        self.bottom_frame.pack(side="bottom", anchor="se", pady=10, padx=10, fill="x")

        self.menu_button = tk.Button(self.bottom_frame, text="Vissza a főmenübe", width=20, fg="white", bg="#f44336", command=self.show_main_menu)
        self.menu_button.pack(anchor="se")

        self.update_bars()


    def show_stats(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Korábbi eredmények", font=("Arial", 20, "bold"), bg=self.bg_color).pack(pady=20)

        try:
            with open("results.txt", "r", encoding="utf-8") as f:
                results = f.readlines()

        except FileNotFoundError:
            results = []

        if results:
            text_box = tk.Text(frame, width=50, height=15, font=("Consolas", 11))
            text_box.pack(pady=10)
            for line in results:
                text_box.insert("end", line)
            text_box.config(state="disabled")
        else:
            tk.Label(frame, text="Még nincsenek mentett eredmények.", font="Arial 12", bg=self.bg_color).pack(pady=10)

        tk.Button(frame, text="Vissza a főmenübe", command=self.show_main_menu, width=20, fg="white", bg="#f44336").pack(pady=20)


    def create_bar(self, label_text):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        tk.Label(frame, text=label_text + ":", width=10, anchor="w").pack(side="left")
        canvas = tk.Canvas(frame, width=200, height=20, bg="#ddd", highlightthickness=1, highlightbackground="#aaa")
        canvas.pack(side="left", padx=5)

        return canvas


    def create_status_row(self, label_text, action_func, button_text):
        frame = tk.Frame(self.status_frame, bg=self.bg_color)
        frame.pack(pady=5)

        tk.Label(frame, text=label_text + ":", font="Arial 10 bold", width=10, anchor="w", bg=self.bg_color).pack(side="left")

        canvas = tk.Canvas(frame, width=200, height=20, bg="#ddd", highlightthickness=1, highlightbackground="#aaa")
        canvas.pack(side="left", padx=5)

        btn = tk.Button(frame, text=button_text, width=12, command=action_func)
        btn.pack(side="left", padx=5)

        if label_text == "Éhség":
            self.hunger_canvas = canvas
        elif label_text == "Energia":
            self.energy_canvas = canvas
        elif label_text == "Boldogság":
            self.happiness_canvas = canvas


    def draw_bar(self, canvas, value):
        canvas.delete("all")
        width = int(2 * value)

        if value > 85:
            color = "#006400"
        elif value > 60:
            color = "#00a000"
        elif value > 40:
            color = "#ffd700"
        elif value > 25:
            color = "#ff8c00"
        else:
            color = "#ff0000"

        canvas.create_rectangle(0, 0, width, 20, fill=color, outline="")


    def update_bars(self):
        self.draw_bar(self.hunger_canvas, self.pet.hunger)
        self.draw_bar(self.energy_canvas, self.pet.energy)
        self.draw_bar(self.happiness_canvas, self.pet.happiness)
        self.money_label.config(text=self.get_inventory())


    def advance_time_SMM(self, hours):
        prev_day = self.day
        self.hour += hours
        while self.hour >= 24:
            self.hour -= 24
            self.day += 1

        if self.day > prev_day:
            self.score += self.pet.hunger + self.pet.energy + self.pet.happiness

            if self.day % 2 == 0:
                self.multiplier += 0.1

        self.day_label.config(text=f"Nap: {self.day} | Óra: {self.hour}")


    def get_inventory(self):
        return f"Pénz: {self.money} | Táp: {self.food} | Játékszer: {self.toys}"


    def buy_food(self):
        if self.money >= 20:
            self.money -= 20
            self.food += 1
            self.status_label.config(text="Vettél 1 tápot.", fg="black")
        else:
            self.status_label.config(text="Nincs elég pénzed tápra!", fg="red")

        self.update_bars()


    def buy_toy(self):
        if self.money >= 50:
            self.money -= 50
            self.toys += 1
            self.status_label.config(text="Vettél 1 játékszert.", fg="black")
        else:
            self.status_label.config(text="Nincs elég pénzed játékszerre!", fg="red")

        self.update_bars()


    def feed(self):
        if self.food <= 0:
            self.status_label.config(text="Nincs tápod!", fg="red")
            return

        self.food -= 1
        self.pet.feed(self.multiplier)
        self.advance_time_SMM(1)
        self.status_label.config(text="Etettél (1 óra telt el).")
        self.update_bars()
        self.check_game_over()


    def play(self):
        if self.toys <= 0:
            self.status_label.config(text="Nincs játékszered!", fg="red")
            return

        broken = self.pet.play(self.multiplier)
        self.advance_time_SMM(2)
        if broken:
            self.toys -= 1
            self.status_label.config(text="Játszottál, de eltört a játékszer (2 óra telt el)!")
        else:
            self.status_label.config(text="Játszottál (2 óra telt el).", fg="black")
        self.update_bars()
        self.check_game_over()


    def sleep(self):
        self.pet.sleep(self.multiplier)
        self.advance_time_SMM(4)
        self.status_label.config(text="Aludt (4 óra telt el).")
        self.update_bars()
        self.check_game_over()


    def check_game_over(self):
        if self.pet.hunger <= 0 or self.pet.energy <= 0 or self.pet.happiness <= 0:
            if not self.warning_active:
                self.warning_active = True
                self.status_label.config(text=f"{self.pet.name} nagyon rossz állapotban van!", fg="red")
            else:
                self.end_game()
        else:
            self.warning_active = False


    def end_game(self):
        final_score = round(self.score)
        save_result_SMM(self.day, final_score)

        for widget in self.root.winfo_children():
            widget.destroy()

        end_frame = tk.Frame(self.root, bg=self.bg_color)
        end_frame.pack(expand=True)

        tk.Label(end_frame, text="Játék vége", font=("Arial", 24, "bold"), fg="red", bg=self.bg_color).pack(pady=20)
        tk.Label(end_frame, text=f"{self.pet.name} {self.day}. napig élt.\nÖsszpontszám: {final_score}", font=("Arial", 14), bg=self.bg_color).pack(pady=10)

        best = load_best_result_SMM()
        if best:
            tk.Label(end_frame, text=f"Eddigi legjobb: {best}", font=("Arial", 10, "bold"), fg="darkgreen", bg=self.bg_color).pack(pady=5)

        tk.Button(end_frame, text="Új játék", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=20, height=2, command=self.start_game).pack(pady=10)
        tk.Button(end_frame, text="Főmenü", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", width=20, height=2, command=self.show_main_menu).pack(pady=10)
