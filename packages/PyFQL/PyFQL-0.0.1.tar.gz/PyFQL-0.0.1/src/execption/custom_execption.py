class InvalideQueryPattern(Exception):
    def __init__(self, message="Requête mal orthographiée ou pattern invalide.\nvérifier la liste des patterns autorisés.\nConsulter pattern_check.py pour plus d'informations."):
        self.message = message
        super().__init__(self.message)
    pass