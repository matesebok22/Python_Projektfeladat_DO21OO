import random

class PetSMM:
    def __init__(self, name):
        self.name = name
        self.hunger = 80
        self.energy = 80
        self.happiness = 80


    def feed(self, multiplier):
        self.hunger = min(100, self.hunger + (20 / multiplier))
        self.energy = max(0, self.energy - (10 * multiplier))


    def play(self, multiplier):
        self.happiness = min(100, self.happiness + (15 / multiplier))
        self.energy = max(0, self.energy - (25 * multiplier))
        self.hunger = max(0, self.hunger - (5 * multiplier))

        broken = random.random() < 0.2
        return broken


    def sleep(self, multiplier):
        self.energy = min(100, self.energy + (30 / multiplier))
        self.hunger = max(0, self.hunger - (10 * multiplier))
        self.happiness = max(0, self.happiness - (5 * multiplier))