# Femme Santé — Backend

API de **Femme Santé**, une application mobile de suivi de la santé féminine : cycles menstruels, journal quotidien, suivi médical et rappels.

- Application mobile : [femme_sante_frontend](https://github.com/Ndeye-Fatou-SOW/femme_sante_frontend)

## Fonctionnalités

- **Comptes** : inscription, connexion, profil, suppression du compte ; authentification par JWT avec renouvellement et révocation des jetons.
- **Cycle** : enregistrement des cycles et des symptômes.
- **Journal quotidien** : saisie des observations du jour.
- **Suivi médical** : consultations et rappels.
- **Prévision** : estimation du prochain cycle et détection d'anomalies (`/api/ml/predict/`, `/api/ml/anomalies/`).

## Technologies

Python · Django · Django REST Framework · Simple JWT · PostgreSQL · CORS

## Lancer le projet

Prérequis : Python 3 et PostgreSQL.

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers psycopg2-binary

# Définir les variables d'environnement : SECRET_KEY, DB_PASSWORD
# et les autres paramètres de base de données lus dans core/settings.py

python manage.py migrate
python manage.py runserver
```

Aucun secret n'est stocké dans le dépôt : la clé Django et le mot de passe de la base passent par des variables d'environnement.

## Routes

| Route | Rôle |
|---|---|
| `/api/auth/` | inscription, connexion, profil |
| `/api/cycle/` | cycles et symptômes |
| `/api/logs/` | journal quotidien |
| `/api/medical/` | consultations et rappels |
| `/api/ml/` | prévision et anomalies |

## Auteure

Ndéye Fatou SOW — Master 2 Systèmes d'Information Répartis, Université Cheikh Anta Diop de Dakar
Portfolio : https://ndeye-fatou-sow.github.io/ndeyefatousow.github.io/
