import os
from datetime import datetime

RESULTS_FILE = "results.txt"

def save_result(day, score):
    with open(RESULTS_FILE, "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"{now} | Nap: {day} | Pont: {round(score)}\n")


def load_best_result():
    if not os.path.exists(RESULTS_FILE):
        return None

    best_score = 0
    best_line = ""
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")

            if len(parts) < 3:
                continue

            try:
                score_part = parts[2].strip()
                score_value = int(score_part.replace("Pont:", "").strip())

                if score_value > best_score:
                    best_score = score_value
                    best_line = line.strip()

            except ValueError:
                continue

    return best_line if best_line else None