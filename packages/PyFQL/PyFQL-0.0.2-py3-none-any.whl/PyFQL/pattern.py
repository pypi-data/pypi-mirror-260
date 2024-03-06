import unicodedata

class Pattern:
    def __init__(self):
        self.pattern_allowed = {
            "RESERVER": "ALLOWED",
            "ACTION": "ALLOWED",
            "ACTION IGNORE RESERVER VARIABLE": "ALLOWED",
            "ACTION IGNORE RESERVER VARIABLE IGNORE VARIABLE": "ALLOWED",
            "ACTION IGNORE RESERVER IGNORE IGNORE RESERVER VARIABLE": "ALLOWED",
            "ACTION IGNORE RESERVER VARIABLE IGNORE RESERVER VARIABLE": "ALLOWED",
            "ACTION IGNORE RESERVER VARIABLE IGNORE IGNORE RESERVER VARIABLE": "ALLOWED",
            "ACTION IGNORE RESERVER VARIABLE IGNORE ACTION IGNORE RESERVER VARIABLE": "ALLOWED",
            "ACTION IGNORE RESERVER IGNORE RESERVER VARIABLE IGNORE RESERVER IGNORE RESERVER VARIABLE IGNORE VARIABLE": "ALLOWED",
            "ACTION IGNORE RESERVER VARIABLE IGNORE ACTION IGNORE RESERVER VARIABLE IGNORE IGNORE IGNORE VARIABLE": "ALLOWED"
        }

        self.formes_conjuguees_lemmes = {
            "crées": "creer",
            "crée": "creer",
            "créez": "creer",
            "créé": "creer",
            "créée": "creer",
            "créées": "creer",
            "créés": "creer",
            "utilises": "utiliser",
            "utilisez": "utiliser",
            "utilise": "utiliser",
            "utilisé": "utiliser",
            "utilisée": "utiliser",
            "utilisées": "utiliser",
            "utilisés": "utiliser",
            "supprimes": "supprimer",
            "supprimez": "supprimer",
            "supprime": "supprimer",
            "supprimé": "supprimer",
            "supprimée": "supprimer",
            "supprimées": "supprimer",
            "supprimés": "supprimer",
            "ajoutes": "ajouter",
            "ajoutez": "ajouter",
            "ajoute": "ajouter",
            "ajouté": "ajouter",
            "ajoutée": "ajouter",
            "ajoutées": "ajouter",
            "ajoutés": "ajouter",
            "modifies": "modifier",
            "modifiez": "modifier",
            "modifie": "modifier",
            "modifié": "modifier",
            "modifiée": "modifier",
            "modifiées": "modifier",
            "modifiés": "modifier",
            "renommes": "renommer",
            "renommez": "renommer",
            "renomme": "renommer",
            "renommé": "renommer",
            "renommée": "renommer",
            "renommées": "renommer",
            "renommés": "renommer",
            "quit": "quitter",
            "exit": "quitter",
            "quitter": "quitter",
            "bye": "quitter",
        }

        self.lemme_to_english = {
            "creer": "create",
            "utiliser": "use",
            "supprimer": "delete",
            "ajouter": "insert",
            "modifier": "update",
            "renommer": "rename",
            "quitter": "quit",
            "bdd": "db",
        }

        self.correspondances = {
            "creer": "ACTION",
            "utiliser": "ACTION",
            "table": "RESERVER",
            "bdd": "RESERVER",
            "supprimer": "ACTION",
            "ajouter": "ACTION",
            "modifier": "ACTION",
            "renommer": "ACTION",
            "champ": "RESERVER",
            "ligne": "RESERVER",
            "lignes": "RESERVER",
            "quitter": "RESERVER",
            "test": "RESERVER",
            "debug": "RESERVER",

            "le": "IGNORE",
            "la": "IGNORE",
            "les": "IGNORE",
            "des": "IGNORE",
            "a": "IGNORE",
            "de": "IGNORE",
            "position": "IGNORE",
            "et": "IGNORE",
            "tous": "IGNORE",
            "toutes": "IGNORE",
            "toute": "IGNORE",
            "avec": "IGNORE",
            "du": "IGNORE",
            "dans": "IGNORE",
            "l'": "IGNORE",
            "l": "IGNORE",
            "'": "IGNORE",
            "un": "IGNORE",
            "une": "IGNORE",
            "au": "IGNORE",
            "aux": "IGNORE",
            "en": "IGNORE",
            "par": "IGNORE",
            "pour": "IGNORE",
            "sur": "IGNORE",
        }

    def remove_accents(self, input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

    def identify_mot(self, mot):
        mot = mot.lower()
        if mot in self.formes_conjuguees_lemmes:
            mot = self.formes_conjuguees_lemmes[mot]
        categorie = self.correspondances.get(mot, "VARIABLE")
        return categorie

    def is_allowed(self, mots_et_categories):
        pattern_generer = ' '.join([categorie for mot, categorie in mots_et_categories])
        return pattern_generer in self.pattern_allowed