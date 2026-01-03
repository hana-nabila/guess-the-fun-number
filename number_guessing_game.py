import customtkinter as ctk
import random
import json
import os
import winsound
from tkinter import messagebox

class GuessGameLogic:
    def __init__(self, min_num=1, max_num=100, attempts=10):
        self.best_score_file = "best_score.json"
        self.practice_mode = False
        self.load_best_score()
        self.configure(min_num, max_num, attempts)
        self.reset()

    def configure(self, min_n, max_n, att):
        self.min_num, self.max_num, self.max_attempts = min_n, max_n, att

    def reset(self):
        self.secret_number = random.randint(self.min_num, self.max_num)
        self.attempts_left = self.max_attempts

    def calculate_score(self):
        return self.attempts_left * 10 if not self.practice_mode else 0

    def load_best_score(self):
        if os.path.exists(self.best_score_file):
            try:
                with open(self.best_score_file, "r") as f:
                    self.best_score = json.load(f).get("score", 0)
            except: self.best_score = 0
        else: self.best_score = 0

    def save_best_score(self, current_score):
        if current_score > self.best_score:
            self.best_score = current_score
            with open(self.best_score_file, "w") as f:
                json.dump({"score": self.best_score}, f)
            return True
        return False

    def guess(self, value):
        if value == self.secret_number: return "correct"
        if not self.practice_mode:
            self.attempts_left -= 1
            if self.attempts_left <= 0: return "game_over"
        return "low" if value < self.secret_number else "high"

# UI CLASS
ctk.set_appearance_mode("light")

class GuessGameApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Guess The Fun Number")
        self.geometry("900x650")
        self.configure(fg_color="#F8FAFC")

        self.game = GuessGameLogic()
        self.colors = {
            "primary": "#3B82F6", "accent": "#10B981", 
            "error": "#EF4444", "text": "#1E293B", "reset": "#F59E0B"
        }

        self.difficulties = {
            "EASY":   {"min": 1, "max": 50,  "attempts": 12},
            "MEDIUM": {"min": 1, "max": 100, "attempts": 10},
            "HARD":   {"min": 1, "max": 200, "attempts": 8},
            "EXPERT": {"min": 1, "max": 500, "attempts": 6},
        }

        self.setup_ui()
        self.set_difficulty("MEDIUM")

    def play_sound(self, s_type):
        try:
            if s_type == "win": winsound.Beep(1000, 150); winsound.Beep(1500, 200)
            elif s_type == "lose": winsound.Beep(400, 400)
            elif s_type == "hint": winsound.Beep(800, 50)
        except: pass

    def setup_ui(self):
        # Header (Judul & Reset)
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(30, 10), fill="x", padx=50)

        self.title_label = ctk.CTkLabel(self.header_frame, text="GUESS THE FUN NUMBER!", 
                                        font=("Inter", 38, "bold"), text_color=self.colors["text"])
        self.title_label.pack(side="left")

        self.reset_btn = ctk.CTkButton(self.header_frame, text="RESET", width=100, height=40, 
                                       corner_radius=20, fg_color=self.colors["reset"], 
                                       font=("Inter", 14, "bold"), command=self.reset_game)
        self.reset_btn.pack(side="right")

        # Info Bar (Range & Best Score)
        self.info_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.info_bar.pack(fill="x", padx=50)

        self.range_label = ctk.CTkLabel(self.info_bar, text="ANTARA 1 - 100", 
                                        font=("Inter", 18, "bold"), text_color="#64748B")
        self.range_label.pack(side="left")

        self.best_label = ctk.CTkLabel(self.info_bar, text=f"🏆 Best Score: {self.game.best_score}", 
                                       font=("Inter", 16, "bold"), text_color="#F59E0B")
        self.best_label.pack(side="right")

        # Main Layout (Sidebar & Game Card)
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both", padx=50, pady=20)

        # Sidebar Difficulty
        self.sidebar = ctk.CTkFrame(self.container, fg_color="white", corner_radius=20, width=180)
        self.sidebar.pack(side="left", fill="y", padx=(0, 20))
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(self.sidebar, text="Difficulty", font=("Inter", 14, "bold")).pack(pady=20)

        self.level_buttons = {}
        for level in self.difficulties:
            btn = ctk.CTkButton(self.sidebar, text=level, corner_radius=12, height=45,
                                fg_color="#F1F5F9", text_color=self.colors["text"],
                                command=lambda l=level: self.set_difficulty(l))
            btn.pack(fill="x", padx=15, pady=5)
            self.level_buttons[level] = btn

        self.practice_switch = ctk.CTkSwitch(self.sidebar, text="Practice Mode", command=self.toggle_practice)
        self.practice_switch.pack(side="bottom", pady=30)

        # Game Card (Centered Content)
        self.card = ctk.CTkFrame(self.container, fg_color="white", corner_radius=30, border_width=1, border_color="#E2E8F0")
        self.card.pack(side="left", expand=True, fill="both")

        # Sun Icon / Mascot
        self.sun_icon = ctk.CTkLabel(self.card, text="☀️", font=("Arial", 80))
        self.sun_icon.pack(pady=(80, 10))

        # Pesan Petunjuk / Hint 
        self.hint_label = ctk.CTkLabel(self.card, text="AYO MULAI MENEBAK!", 
                                       font=("Inter", 22, "bold"), text_color=self.colors["primary"])
        self.hint_label.pack(pady=5)

        self.attempt_label = ctk.CTkLabel(self.card, text="10 KESEMPATAN LAGI", 
                                          font=("Inter", 14), text_color="#64748B")
        self.attempt_label.pack()

        # Input Section
        self.entry = ctk.CTkEntry(self.card, width=300, height=75, corner_radius=20,
                                  font=("Inter", 36, "bold"), justify="center",
                                  border_width=2, border_color="#E2E8F0", fg_color="#F8FAFC")
        self.entry.pack(pady=30)
        self.entry.bind("<Return>", lambda e: self.check_guess())

        self.guess_btn = ctk.CTkButton(self.card, text="TEBAK SEKARANG", width=300, height=60, 
                                       corner_radius=20, font=("Inter", 18, "bold"),
                                       fg_color=self.colors["accent"], command=self.check_guess)
        self.guess_btn.pack()

    def set_difficulty(self, level):
        conf = self.difficulties[level]
        self.game.configure(conf["min"], conf["max"], conf["attempts"])
        self.range_label.configure(text=f"ANTARA {conf['min']} - {conf['max']}")
        for l, btn in self.level_buttons.items():
            btn.configure(fg_color=self.colors["primary"] if l == level else "#F1F5F9",
                          text_color="white" if l == level else self.colors["text"])
        self.reset_game()

    def toggle_practice(self):
        self.game.practice_mode = self.practice_switch.get()
        self.reset_game()

    def check_guess(self):
        try:
            val = int(self.entry.get())
        except:
            return

        res = self.game.guess(val)
        self.entry.delete(0, 'end')

        if res == "correct":
            self.play_sound("win")
            score = self.game.calculate_score()
            self.game.save_best_score(score)
            self.hint_label.configure(text="TEPAT SEKALI! 🎉", text_color=self.colors["accent"])
            messagebox.showinfo("MENANG!", f"Hebat! Angka tersebut adalah {val}.\nSkor: {score}")
            self.reset_game()
        elif res == "game_over":
            self.play_sound("lose")
            self.hint_label.configure(text="KESEMPATAN HABIS!", text_color=self.colors["error"])
            messagebox.showerror("GAME OVER", f"Maaf, angkanya adalah {self.game.secret_number}")
            self.reset_game()
        else:
            self.play_sound("hint")
            if res == "low":
                self.hint_label.configure(text="TERLALU RENDAH! ↓", text_color=self.colors["error"])
            else:
                self.hint_label.configure(text="TERLALU TINGGI! ↑", text_color=self.colors["error"])
            
        self.update_status()

    def update_status(self):
        if self.game.practice_mode:
            self.attempt_label.configure(text="MODE LATIHAN (TANPA BATAS)")
        else:
            self.attempt_label.configure(text=f"{self.game.attempts_left} KESEMPATAN LAGI")

    def reset_game(self):
        self.game.reset()
        self.update_status()
        self.hint_label.configure(text="AYO MULAI MENEBAK!", text_color=self.colors["primary"])
        self.best_label.configure(text=f"🏆 Best Score: {self.game.best_score}")
        self.entry.focus()

if __name__ == "__main__":
    app = GuessGameApp()
    app.mainloop()