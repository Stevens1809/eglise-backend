package cd.eglise.app.data.remote

import retrofit2.http.*

/**
 * Interface Retrofit correspondant aux endpoints du backend Django.
 * Base URL à configurer selon l'environnement (voir RetrofitClient.kt).
 */
interface EgliseApi {

    @POST("api/auth/token/")
    suspend fun login(@Body request: LoginRequest): LoginResponse

    @GET("api/accounts/me/")
    suspend fun getMe(): UserDto

    @POST("api/accounts/me/fcm-token/")
    suspend fun updateFcmToken(@Body body: Map<String, String>)

    @GET("api/core/rayons/")
    suspend fun getRayons(): PagedResponse<RayonDto>

    @GET("api/core/rayons/{id}/membres/")
    suspend fun getMembresRayon(@Path("id") rayonId: Int): List<UserDto>

    @POST("api/core/rayons/{id}/ajouter_membre/")
    suspend fun ajouterMembre(@Path("id") rayonId: Int, @Body body: Map<String, Int>): UserDto

    @GET("api/events/evenements/")
    suspend fun getEvenements(): PagedResponse<EventDto>

    @GET("api/events/annonces/")
    suspend fun getAnnonces(): PagedResponse<AnnouncementDto>

    @POST("api/events/annonces/")
    suspend fun creerAnnonce(@Body body: Map<String, String>): AnnouncementDto

    @GET("api/notifications/notifications/")
    suspend fun getNotifications(): PagedResponse<NotificationDto>

    @PATCH("api/notifications/notifications/{id}/")
    suspend fun marquerNotificationLue(@Path("id") id: Int, @Body body: Map<String, Boolean>)
}
