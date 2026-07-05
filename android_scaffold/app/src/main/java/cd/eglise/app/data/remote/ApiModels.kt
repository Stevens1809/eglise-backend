package cd.eglise.app.data.remote

// Modèles de données correspondant aux serializers DRF du backend.
// (champs identiques aux réponses JSON de l'API)

data class UserDto(
    val id: Int,
    val username: String,
    val first_name: String,
    val last_name: String,
    val role: String,          // "fidele" | "chef_rayon" | "resp_departement" | "admin_consistoire"
    val rayon: Int?,
    val rayon_nom: String?
)

data class RayonDto(
    val id: Int,
    val nom: String,
    val chef_rayon: Int?,
    val chef_rayon_nom: String?,
    val nombre_membres: Int
)

data class EventDto(
    val id: Int,
    val titre: String,
    val description: String,
    val date_debut: String,   // ISO 8601 - à parser avec java.time
    val date_fin: String?,
    val lieu: String,
    val department: Int?,
    val department_nom: String?,
    val visibilite: String
)

data class AnnouncementDto(
    val id: Int,
    val titre: String,
    val contenu: String,
    val auteur_nom: String?,
    val date_publication: String,
    val cible: String,
    val rayon_nom: String?,
    val department_nom: String?
)

data class NotificationDto(
    val id: Int,
    val titre: String,
    val message: String,
    val type: String,
    val lu: Boolean,
    val date_envoi: String
)

data class LoginRequest(val username: String, val password: String)
data class LoginResponse(val access: String, val refresh: String)

data class PagedResponse<T>(
    val count: Int,
    val next: String?,
    val previous: String?,
    val results: List<T>
)
