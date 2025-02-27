from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String , Float , Column
from sqlalchemy import func

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET']="87327y@shbfjhsd"

db=SQLAlchemy(app)
app.secret_key = "super secret key"

# with app.app_context():
#         db.create_all()

class Depense(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  titre=db.Column(db.String(100))
  montant=db.Column(db.Integer)
  def __repr__(self):
    return f"budget {self.titre} {self.montant}"

class Revenu(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  titre=db.Column(db.String(100))
  montant=db.Column(db.Integer)
  def __repr__(self):
    return f"budget {self.titre} {self.montant}"



@app.route("/")
def index():
  revenu = Revenu.query.all()
  depense =Depense.query.all()
  total_revenu = db.session.query(func.sum(Revenu.montant)).scalar()
  total_depense = db.session.query(func.sum(Depense.montant)).scalar()
  solde = total_revenu - total_depense

  return render_template("index.html", revenu=revenu, depense=depense,total_depense=total_depense,total_revenu=total_revenu,solde=solde)

@app.route('/add_depense', methods=['GET', 'POST'])
def add_depense():
    if request.method == 'POST':
      montant = request.form['montant']
      total_revenu = db.session.query(func.sum(Revenu.montant)).scalar()
      if int(montant) > total_revenu:
        flash("Le montant de la dépense ne doit pas être supérieur au total des revenus")
        return redirect(url_for('add_depense'))
      titre = request.form['titre']

      new_depense=Depense(titre=titre, montant=montant)
      db.session.add(new_depense)
      db.session.commit()
      return redirect(url_for('index'))  # Redirige vers la page d'accueil
    return render_template('add_depense.html')

@app.route('/add_revenu', methods=['GET', 'POST'])
def add_revenu():
   if request.method == 'POST':
     titre = request.form['titre']
     montant = request.form['montant']
     new_revenu=Revenu(titre=titre, montant=montant)
     db.session.add(new_revenu)
     db.session.commit()
     return redirect(url_for('index'))
   return render_template("add_revenu.html")


@app.route("/Depense/<int:id>/delete")
def delete_Depense(id):
  depense = Depense.query.get_or_404(id)
  try:
      db.session.delete(depense)
      db.session.commit()
      return redirect(url_for("index"))
  except Exception:
      return "Une erreur s'est produite"


@app.route("/Revenu/<int:id>/delete")
def delete_Revenu(id):
  revenu = Revenu.query.get_or_404(id)
  try:
      db.session.delete(revenu)
      db.session.commit()
      return redirect(url_for("index"))
  except Exception:
      return "Une erreur s'est produite"
    

@app.route("/update_depense/<int:id>/", methods=["GET" , "POST"])
def update_depense(id):
  depense=Depense.query.get_or_404(id)
  if request.method=="POST":
    depense.titre=request.form["titre"]
    depense.montant=request.form["montant"]
    try:
      db.session.commit()
      return redirect(url_for("index"))
    except Exception:
      return "Nous ne pouvons pas modifier"
  return render_template("update_depense.html", depense=depense)



@app.route("/update_revenu/<int:id>/", methods=["GET" , "POST"])
def update_revenu(id):
  revenu=Revenu.query.get_or_404(id)
  if request.method=="POST":
    revenu.titre=request.form["titre"]
    revenu.montant=float(request.form["montant"])
    try:
      db.session.commit()
      return redirect(url_for("index"))
    except Exception:
      return "Nous ne pouvons pas modifier"
  return render_template("update_revenu.html", revenu=revenu)

if __name__ == '__main__':
 app.run(debug=True)


