package cd.eglise.app.data.repository

import android.content.Context
import androidx.work.*
import cd.eglise.app.data.local.AppDatabase
import cd.eglise.app.data.remote.RetrofitClient
import java.util.concurrent.TimeUnit

/**
 * Synchronise périodiquement (toutes les 15 min, ou dès que le réseau revient)
 * les événements/annonces/notifications en arrière-plan. WorkManager gère
 * lui-même les retries en cas de connexion instable -- c'est le mécanisme
 * recommandé par Google pour ce cas d'usage précis.
 */
class SyncWorker(context: Context, params: WorkerParameters) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        val db = AppDatabase.getInstance(applicationContext)
        val repository = EventsRepository(RetrofitClient.api, db)
        val resultat = repository.synchroniser()
        return if (resultat.isSuccess) Result.success() else Result.retry()
    }

    companion object {
        private const val WORK_NAME = "sync_eglise_periodique"

        fun planifier(context: Context) {
            val contraintes = Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)
                .build()

            val requete = PeriodicWorkRequestBuilder<SyncWorker>(15, TimeUnit.MINUTES)
                .setConstraints(contraintes)
                .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 30, TimeUnit.SECONDS)
                .build()

            WorkManager.getInstance(context).enqueueUniquePeriodicWork(
                WORK_NAME, ExistingPeriodicWorkPolicy.KEEP, requete
            )
        }
    }
}
