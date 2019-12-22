class Carte:
    def __init__(self, val):
        # Associer .png a valeur
        self.val = val
        self.j = False  # jouée

        if val < 15:
            self.n = str(self.get_n(val)) + "T"
        if 14 < val < 28:
            val -= 13
            self.n = str(self.get_n(val)) + "K"
        if 27 < val < 41:
            val -= 26
            self.n = str(self.get_n(val)) + "C"
        if 40 < val:
            val -= 39
            self.n = str(self.get_n(val)) + "P"
        self.p = self.get_p(self.n)

    def __str__(self):
        return self.n if not self.j else ""

    def __repr__(self):
        return self.n if not self.j else ""

    @staticmethod
    def get_n(v):
        return {
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9,
            10: 10,
            11: 'J',
            12: 'Q',
            13: 'K',
            14: 'A'
        }[v]

    @staticmethod
    def get_p(n):
        return {
            'A': 4,
            'J': 1,
            'Q': 2,
            'K': 3
        }.get(n[0], 0)

    @staticmethod
    def get_couleurs(self):
        return self.couleurs

    @staticmethod
    def get_couleurs_nom(self):
        return self.couleurs_nom
