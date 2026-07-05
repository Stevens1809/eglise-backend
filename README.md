# Backend — Application de gestion d'église (Butembo)

Backend Django REST fonctionnel, testé de bout en bout (auth JWT, inscription,
rayons, événements, annonces, notifications). Prêt à lancer en local en 5 minutes.

## Installation

```bash
cd eglise_backend
python3 -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_data      # crée les 9 rayons + 7 départements
python manage.py createsuperuser
python manage.py runserver
```

L'API tourne sur `http://localhost:8000/`. L'admin Django (utilisable tout de
suite par le Consistoire) est sur `http://localhost:8000/admin/`.

En local, aucune variable d'environnement n'est nécessaire (valeurs par
défaut sûres pour le développement). Pour la production, voir la section
*Déploiement sur Railway* plus bas et le fichier `.env.example`.

## Structure du projet

- **accounts/** — Utilisateur custom (rôle, rayon, token FCM), inscription, permissions par rôle.
- **core/** — Départements, Rayons, réunions de prière (lundi/mercredi/samedi), pointage de présence.
- **events/** — Événements du calendrier + annonces, avec filtrage automatique par visibilité (global / rayon / département).
- **notifications/** — Historique des notifications + service d'envoi (squelette FCM prêt à activer).
- **prayerrequests/** — Demandes de prière / signalements de cas sociaux.

## Les 4 niveaux d'autorisation

| Rôle | Ce qu'il peut faire |
|---|---|
| **Fidèle** | Voir calendrier/annonces filtrés selon son rayon et ses départements, recevoir des notifications, soumettre une demande de prière. |
| **Chef de rayon** | Tout ce que fait un fidèle + gérer les membres de SON rayon, modifier/annuler les réunions de SON rayon, pointer les présences, publier des annonces ciblées à son rayon. |
| **Responsable de département** | Voir/gérer les demandes adressées à SON département, créer des événements pour son département. |
| **Admin / Consistoire** | Accès total : gestion des utilisateurs, rôles, rayons, départements, tout événement/annonce. |

La logique de filtrage est dans `get_queryset()` de chaque ViewSet (voir
`core/views.py` et `events/views.py`) — c'est le cœur du système de permissions.

## Endpoints principaux

```
POST   /api/auth/token/                    -> login (username + password) -> access + refresh
POST   /api/auth/token/refresh/            -> renouveler le token
POST   /api/accounts/register/             -> inscription fidèle
GET    /api/accounts/me/                   -> profil connecté
POST   /api/accounts/me/fcm-token/         -> enregistrer le token push de l'app mobile

GET    /api/core/rayons/                   -> liste des rayons
GET    /api/core/rayons/{id}/membres/      -> membres d'un rayon (chef de rayon / admin / membre lui-même)
POST   /api/core/rayons/{id}/ajouter_membre/
POST   /api/core/rayons/{id}/retirer_membre/
GET    /api/core/reunions-priere/          -> réunions filtrées selon le rôle
GET    /api/core/presences/
GET    /api/core/departements/

GET    /api/events/evenements/             -> calendrier filtré automatiquement
GET    /api/events/annonces/               -> annonces filtrées automatiquement
POST   /api/events/annonces/               -> créer une annonce (déclenche les notifications)

GET    /api/notifications/notifications/   -> notifications de l'utilisateur connecté
GET    /api/prayerrequests/demandes-priere/
```

## Notifications push (FCM)

Le squelette est dans `notifications/services.py`. Pour l'activer réellement :

1. `pip install firebase-admin`
2. Créer un projet Firebase, télécharger `serviceAccountKey.json`
3. Renseigner `FCM_CREDENTIALS_PATH` dans `config/settings.py`
4. Décommenter le code Firebase dans `notifications/services.py`

**Important** : même sans FCM configuré, chaque notification est déjà enregistrée
en base de données. C'est ce qui permet le fonctionnement "hors-ligne d'abord" :
l'app mobile peut toujours récupérer les notifications via
`GET /api/notifications/notifications/` au prochain sync, même si le push
en direct a échoué à cause d'une connexion instable.

## Déploiement sur Railway (guide pas à pas)

Le projet est déjà prêt pour Railway (Procfile, gestion des variables
d'environnement, PostgreSQL, fichiers statiques via Whitenoise). Voici la marche à suivre :

### 1. Mettre le projet sur GitHub

```bash
cd eglise_backend
git init
git add .
git commit -m "Backend initial - application église"
```

Crée un dépôt vide sur GitHub (bouton "New repository"), puis :

```bash
git remote add origin https://github.com/TON_COMPTE/eglise-backend.git
git branch -M main
git push -u origin main
```

### 2. Créer le projet sur Railway

1. Va sur [railway.app](https://railway.app), connecte-toi avec GitHub.
2. **New Project** → **Deploy from GitHub repo** → sélectionne ton dépôt `eglise-backend`.
3. Railway détecte automatiquement le `Procfile` et va essayer de builder avec Nixpacks (Python) — rien à faire de spécial.

### 3. Ajouter une base de données PostgreSQL

Dans le même projet Railway : **+ New** → **Database** → **Add PostgreSQL**.
Railway crée automatiquement une variable `DATABASE_URL` que ton `settings.py`
sait déjà lire (grâce à `dj-database-url`) — tu n'as rien à configurer ici.

### 4. Configurer les variables d'environnement

Sur le service de ton backend (pas la base de données) → onglet **Variables** → ajoute :

| Variable | Valeur |
|---|---|
| `SECRET_KEY` | une longue chaîne aléatoire (génère-en une avec `python -c "import secrets; print(secrets.token_urlsafe(50))"`) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | l'URL Railway de ton service, ex: `eglise-backend-production.up.railway.app` (Railway te la donne dans l'onglet **Settings** → **Domains**) |
| `CORS_ALLOW_ALL_ORIGINS` | `False` |
| `CORS_ALLOWED_ORIGINS` | l'URL depuis laquelle ton app mobile/web appellera l'API |

### 5. Générer un domaine public

Onglet **Settings** → **Networking** → **Generate Domain**. Tu obtiens une URL du style
`https://eglise-backend-production.up.railway.app`.

### 6. Vérifier que tout tourne

Railway exécute automatiquement, à chaque déploiement :
- `release: python manage.py migrate && python manage.py seed_data` (ligne du Procfile) — donc tes rayons/départements sont recréés automatiquement au premier déploiement.
- `web: gunicorn config.wsgi` — le serveur de production.

Ouvre `https://ton-url.up.railway.app/admin/` — tu dois voir la page de connexion Django.

**Important** : crée ton superuser en production via l'onglet **Shell** de Railway (dans le service backend) :
```bash
python manage.py createsuperuser
```

### 7. Mettre à jour ton app Android

Dans `RetrofitClient.kt`, remplace `BASE_URL_DEV` par ta vraie URL Railway pour la version release de l'app.

## Prochaines étapes suggérées

1. Brancher Firebase Cloud Messaging pour de vrais push.
2. Ajouter une commande planifiée (cron / Celery beat) qui génère
   automatiquement les `PrayerMeeting` du lundi/mercredi/samedi suivant pour
   chaque rayon, pour éviter la saisie manuelle.
3. Ajouter les permissions DRF plus fines par action (actuellement certains
   contrôles sont faits manuellement dans les vues plutôt que via des classes
   de permission dédiées à 100% — fonctionnel mais à raffiner si l'équipe grandit).
4. Câbler l'app Android (voir dossier `android_scaffold/`).
