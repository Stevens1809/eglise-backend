package cd.eglise.app.data.local

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Dao
interface EventDao {
    @Query("SELECT * FROM events_cache ORDER BY dateDebut ASC")
    fun observerTous(): Flow<List<EventEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun remplacerTous(events: List<EventEntity>)

    @Query("DELETE FROM events_cache")
    suspend fun viderCache()
}

@Dao
interface AnnouncementDao {
    @Query("SELECT * FROM announcements_cache ORDER BY datePublication DESC")
    fun observerToutes(): Flow<List<AnnouncementEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun remplacerToutes(announcements: List<AnnouncementEntity>)
}

@Dao
interface NotificationDao {
    @Query("SELECT * FROM notifications_cache ORDER BY dateEnvoi DESC")
    fun observerToutes(): Flow<List<NotificationEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun remplacerToutes(notifications: List<NotificationEntity>)

    @Query("UPDATE notifications_cache SET lu = 1 WHERE id = :id")
    suspend fun marquerLue(id: Int)

    @Query("SELECT COUNT(*) FROM notifications_cache WHERE lu = 0")
    fun observerNombreNonLues(): Flow<Int>
}

@Dao
interface PendingActionDao {
    @Insert
    suspend fun ajouter(action: PendingActionEntity)

    @Query("SELECT * FROM pending_actions ORDER BY dateCreation ASC")
    suspend fun listerEnAttente(): List<PendingActionEntity>

    @Delete
    suspend fun supprimer(action: PendingActionEntity)
}

@Database(
    entities = [
        EventEntity::class, AnnouncementEntity::class,
        NotificationEntity::class, PendingActionEntity::class,
    ],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun eventDao(): EventDao
    abstract fun announcementDao(): AnnouncementDao
    abstract fun notificationDao(): NotificationDao
    abstract fun pendingActionDao(): PendingActionDao

    companion object {
        @Volatile private var INSTANCE: AppDatabase? = null

        fun getInstance(context: android.content.Context): AppDatabase =
            INSTANCE ?: synchronized(this) {
                INSTANCE ?: Room.databaseBuilder(
                    context.applicationContext, AppDatabase::class.java, "eglise_db"
                ).build().also { INSTANCE = it }
            }
    }
}
