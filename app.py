from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String , Float , Column
from sqlalchemy import func

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class depense(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  titre=db.Column(db.String(100))
  montant=db.Column(db.Integer)
  def __repr__(self):
    return f"budget {self.titre} {self.montant}"
  
class revenu(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  titre=db.Column(db.String(100))
  montant=db.Column(db.Integer)
  def __repr__(self):
    return f"budget {self.titre} {self.montant}"



@app.route("/")
def index():
  revenus = revenu.query.all()
  depenses =depense.query.all()
  total_revenu = db.session.query(func.sum(revenu.montant)).scalar()
  total_depense = db.session.query(func.sum(depense.montant)).scalar()
  solde = total_revenu - total_depense

  return render_template("index.html", revenus=revenus, depenses=depenses,total_depense=total_depense,total_revenu=total_revenu,solde=solde)

@app.route('/add_depense', methods=['GET', 'POST'])
def add_depense():
    if request.method == 'POST':
      titre = request.form['titre']
      montant = request.form['montant'] 
      new_depense=depense(titre=titre, montant=montant)
      db.session.add(new_depense)
      db.session.commit()
      return redirect(url_for('index'))  # Redirige vers la page d'accueil
    return render_template('add_depense.html')
  
@app.route('/add_revenu', methods=['GET', 'POST'])
def add_revenu():
   if request.method == 'POST':
     titre = request.form['titre']
     montant = request.form['montant']
     new_revenu=revenu(titre=titre, montant=montant)
     db.session.add(new_revenu)
     db.session.commit()
     return redirect(url_for('index'))
   return render_template("add_revenu.html")
 
Depense=''
@app.route("/depense/<int:id>/delete")
def delete(id):
  depense = Depense.query.get_or_404(id)
  try:
      db.session.delete(depense)
      db.session.commit()
      return redirect(url_for("index"))
  except Exception:
      return "Une erreur s'est produite"


@app.route("/update/<int:id>/", methods=["GET" , "POST"])
def update(id):
  depense=Depense.query.get_or_404(id)
  if request.method=="POST":
    depense.titre=request.form["titre"]
    depense.montant=request.form["montant"]
    try:
      db.session.commit()
      return redirect(url_for(index))
    except Exception:
      return "Nous ne pouvons pas modifier"
  
  





if __name__ == '__main__':
 app.run(debug=True)
  
    
