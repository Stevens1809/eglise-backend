# Scaffold Android — App fidèles/chefs de rayon

Ce dossier n'est **pas** un projet Android buildable tel quel (pas de Gradle
wrapper complet, pas d'Android Studio dans cet environnement pour le tester).
C'est un **point de départ concret** : les fichiers Kotlin clés, dans le même
style que ton projet AquaFlow, à copier-coller dans un nouveau projet Android
Studio (ou dans ton projet existant si tu préfères réutiliser AquaFlow comme base).

## Ce qui est fourni

- **data/remote/ApiModels.kt** — DTOs correspondant exactement aux réponses JSON du backend.
- **data/remote/EgliseApi.kt** — Interface Retrofit avec tous les endpoints principaux.
- **data/remote/RetrofitClient.kt** — Client HTTP avec injection automatique du token JWT.
- **data/local/Entities.kt** + **AppDatabase.kt** — Cache Room (événements, annonces, notifications, actions en attente).
- **data/repository/EventsRepository.kt** — Pattern offline-first : l'UI observe toujours le cache local, la synchro réseau met à jour ce cache en arrière-plan.
- **data/repository/SyncWorker.kt** — Synchro périodique fiable via WorkManager (gère lui-même les retries en cas de réseau instable).
- **app/build.gradle.kts.snippet** — Dépendances à ajouter.

## Étapes pour démarrer

1. Crée un nouveau projet Android Studio (ou réutilise la structure d'AquaFlow).
2. Copie le dossier `data/` dans `app/src/main/java/<ton_package>/`.
3. Ajoute les dépendances du fichier `.snippet` dans `app/build.gradle.kts`.
4. Configure Firebase (comme pour AquaFlow) : télécharge `google-services.json`,
   crée un `FirebaseMessagingService` qui récupère le token et l'envoie au
   backend via `updateFcmToken()`.
5. Dans ton `Application` ou `MainActivity`, appelle :
   ```kotlin
   RetrofitClient.init(applicationContext)
   SyncWorker.planifier(applicationContext)
   ```
6. Construis les écrans (Compose ou XML, selon ce que tu utilises déjà) en
   observant les `Flow` exposés par `EventsRepository` — l'UI se met à jour
   automatiquement dès que le cache change, que ce soit via le réseau ou hors-ligne.

## Ce qu'il reste à toi de construire

- Écrans de connexion / inscription
- Écran calendrier (liste des `EventEntity` observés)
- Dashboard "Chef de rayon" : liste des membres du rayon, pointage de présence,
  publication d'annonce ciblée (utilise les endpoints `ajouter_membre`,
  `retirer_membre`, `membres`, déjà exposés côté API)
- Écran notifications avec badge de compteur non lues (`observerNombreNotifsNonLues()`)

Le gros du travail structurant (auth, cache offline, sync fiable) est déjà posé.
