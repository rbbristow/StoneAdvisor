from flask import render_template, url_for, request, flash, redirect
from .app import app, login
from .modeles.donnees import Sites, Images
from .modeles.users import User
from flask_login import login_user, current_user, logout_user

# Accueil.
@app.route("/")
def accueil():
    sites = Sites.query.all()
    return render_template("pages/accueil.html", nom="Stone Advisor")

# Liste des sites archéologiques enregistrés.
@app.route("/sites")
def notices_sites():
    sites = Sites.query.all()
    return render_template("pages/notice_sites.html", nom="Stone Advisor", sites=sites)

# Sites individuels enregistrés.
@app.route("/sites/<int:Id>")
def site(Id):
    site = Sites.query.get(Id)
    image = site.Images
    return render_template("pages/sites.html", nom="Stone Advisor", site=site, image=image)

# Recherche.
@app.route("/recherche")
def recherche():
    motclef = request.args.get("keyword", None)
    #liste vide de résultats
    resultats = []
    #titre par défaut de la page
    titre = "Recherche"
    if motclef:
        resultats = Sites.query.filter(Sites.Nom.like("%{}%".format(motclef))).all()
        titre = 'Résultats pour la recherche "' + motclef + '"'
    return render_template("pages/recherche.html", resultats=resultats, titre=titre)

# Inscription.
@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )

        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("L'ajout de vos données a échoué pour les raisons suivantes : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")

# Connexion.
@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e.", "info")
        return redirect("/")
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        user = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if user:
            login_user(user)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus.", "error")

    return render_template("pages/connexion.html")

login.login_view = 'connexion'

from flask_login import logout_user, current_user

# Déconnexion.
@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e.", "info")
    return redirect("/")

# Ajouter un site archéologique dans la base de données.
@app.route("/participer", methods=["POST", "GET"])
def participer():
    if current_user.is_authenticated is False:
        flash("Pour ajouter des sites archéologiques dans la base de données, veuillez vous connecter.", "info")
        return redirect("/connexion")
    if request.method == "POST":
        statut, donnees = Sites.creer(
            nom=request.form.get("nom", None),
            adresse=request.form.get("adresse", None),
            latitude=request.form.get("latitude", None),
            longitude=request.form.get("longitude", None),
            description=request.form.get("description", None),
            periode=request.form.get("periode", None)
            #image=request.form.get("image", None)
        )

        if statut is True:
            flash("Les données ont été ajoutées à notre base, merci pour votre participation !", "success")
            return redirect("/participer")
        else:
            flash("L'ajout de vos données a échoué pour les raisons suivantes : " + ", ".join(donnees), "danger")
            return render_template("pages/participer.html")
    else:
        return render_template("pages/participer.html")

# Modifier un site archéologique de la base de données.
@app.route("/modifier/<int:id>", methods=["POST", "GET"])
def modification(id):
    # On renvoie sur la page html les éléments de l'objet site correspondant à l'identifiant de la route
    if request.method == "GET":
        site_a_modifier = Sites.query.get(id)
        return render_template("pages/modification_site.html", site_a_modifier=site_a_modifier)

    # on récupère les données du formulaire modifié
    else:
        statut, donnees= Sites.modifier(
            Id=id,
            Nom=request.form.get("nom", None),
            Adresse=request.form.get("adresse", None),
            Latitude=request.form.get("latitude", None),
            Longitude=request.form.get("longitude", None),
            Description=request.form.get("description", None),
            Periode=request.form.get("periode", None)
        )

        if statut is True:
            flash("Modification réussie !", "success")
            return render_template ("pages/notice_sites.html")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "danger")
            site_a_modifier = Sites.query.get(id)
            return render_template("pages/modification_site.html", site_a_modifier=site_a_modifier)
