from app import app, db, Revenu, Depense


def init_db():
    with app.app_context():
        # Création des tables
        db.create_all()
        revenus = Revenu(titre="Salaire", montant=3000)
        loyer = Depense(titre="Loyer", montant=800)
        edf = Depense(titre="EDF", montant=100)
        db.session.add(revenus)
        db.session.add(loyer)
        db.session.add(edf)
        db.session.commit()
        print("Tables créées avec succès")

if __name__ == "__main__":
    init_db()
