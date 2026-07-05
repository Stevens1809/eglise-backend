package cd.eglise.app.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Cache local des événements. L'app affiche TOUJOURS ces données en premier
 * (lecture instantanée, même hors-ligne), puis les rafraîchit en arrière-plan
 * dès que le réseau est disponible (voir SyncWorker.kt).
 */
@Entity(tableName = "events_cache")
data class EventEntity(
    @PrimaryKey val id: Int,
    val titre: String,
    val description: String,
    val dateDebut: String,
    val lieu: String,
    val departementNom: String?,
    val visibilite: String,
    val derniereSynchro: Long = System.currentTimeMillis()
)

@Entity(tableName = "announcements_cache")
data class AnnouncementEntity(
    @PrimaryKey val id: Int,
    val titre: String,
    val contenu: String,
    val auteurNom: String?,
    val datePublication: String,
    val cible: String,
    val derniereSynchro: Long = System.currentTimeMillis()
)

@Entity(tableName = "notifications_cache")
data class NotificationEntity(
    @PrimaryKey val id: Int,
    val titre: String,
    val message: String,
    val type: String,
    val lu: Boolean,
    val dateEnvoi: String
)

/**
 * File d'attente des actions faites hors-ligne (ex: marquer une notif comme lue)
 * en attendant de pouvoir les rejouer vers le serveur au retour du réseau.
 */
@Entity(tableName = "pending_actions")
data class PendingActionEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val type: String,       // ex: "MARQUER_NOTIF_LUE"
    val payloadJson: String,
    val dateCreation: Long = System.currentTimeMillis()
)
