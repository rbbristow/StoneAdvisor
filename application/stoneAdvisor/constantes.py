from warnings import warn

# clé secrète pour les mots de passe utilisateur-ice-s
SECRET_KEY = "Les archéologues ne fouillent pas des dinosaures"

# avertissement pour la personne ne connaissant pas la clé secrète
if SECRET_KEY == "Les archéologues ne fouillent pas des dinosaures":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)
