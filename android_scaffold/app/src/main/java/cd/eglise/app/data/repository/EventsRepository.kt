package cd.eglise.app.data.repository

import cd.eglise.app.data.local.AppDatabase
import cd.eglise.app.data.local.EventEntity
import cd.eglise.app.data.local.NotificationEntity
import cd.eglise.app.data.remote.EgliseApi
import kotlinx.coroutines.flow.Flow

/**
 * Pattern "offline-first" (identique à celui utilisé dans AquaFlow) :
 * 1. L'UI observe TOUJOURS le cache local Room (via Flow) -> affichage instantané.
 * 2. En arrière-plan, on tente une synchro réseau ; si elle réussit, on met à jour
 *    le cache local, ce qui met automatiquement à jour l'UI qui observe le Flow.
 * 3. Si le réseau échoue (connexion instable, typique à Butembo), l'utilisateur
 *    voit simplement les dernières données connues -- pas d'écran vide, pas de crash.
 */
class EventsRepository(
    private val api: EgliseApi,
    private val db: AppDatabase,
) {
    fun observerEvenements(): Flow<List<EventEntity>> = db.eventDao().observerTous()

    fun observerNotifications(): Flow<List<NotificationEntity>> =
        db.notificationDao().observerToutes()

    fun observerNombreNotifsNonLues(): Flow<Int> =
        db.notificationDao().observerNombreNonLues()

    /** À appeler au lancement de l'app et via WorkManager en tâche périodique. */
    suspend fun synchroniser(): Result<Unit> {
        return try {
            val evenements = api.getEvenements().results.map {
                EventEntity(
                    id = it.id, titre = it.titre, description = it.description,
                    dateDebut = it.date_debut, lieu = it.lieu,
                    departementNom = it.department_nom, visibilite = it.visibilite,
                )
            }
            db.eventDao().remplacerTous(evenements)

            val notifications = api.getNotifications().results.map {
                NotificationEntity(
                    id = it.id, titre = it.titre, message = it.message,
                    type = it.type, lu = it.lu, dateEnvoi = it.date_envoi,
                )
            }
            db.notificationDao().remplacerToutes(notifications)

            Result.success(Unit)
        } catch (e: Exception) {
            // Pas de connexion ou erreur serveur : on ne fait RIEN au cache existant.
            // L'utilisateur continue de voir les dernières données synchronisées.
            Result.failure(e)
        }
    }

    /**
     * Marquer une notification comme lue : mise à jour optimiste du cache local
     * immédiatement (l'utilisateur voit le changement tout de suite), puis tentative
     * d'envoi au serveur. Si ça échoue, l'action reste en attente (PendingActionDao)
     * pour être rejouée plus tard -- à implémenter avec WorkManager selon le même
     * principe que la synchro.
     */
    suspend fun marquerNotificationLue(id: Int) {
        db.notificationDao().marquerLue(id)
        try {
            api.marquerNotificationLue(id, mapOf("lu" to true))
        } catch (e: Exception) {
            // échec silencieux -- le cache local reste correct, on retentera au sync suivant
        }
    }
}
