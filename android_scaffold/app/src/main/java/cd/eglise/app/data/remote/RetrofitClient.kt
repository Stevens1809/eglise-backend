package cd.eglise.app.data.remote

import android.content.Context
import android.content.SharedPreferences
import okhttp3.Interceptor
import okhttp3.OkHttpClient
import okhttp3.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

/**
 * IMPORTANT : en dev, si tu testes sur un émulateur Android, utilise
 * "http://10.0.2.2:8000/" pour atteindre le "localhost" de ta machine.
 * En prod, remplace par l'URL de ton serveur déployé (Railway/Render).
 */
object RetrofitClient {

    private const val BASE_URL_DEV = "http://10.0.2.2:8000/"
    private const val BASE_URL_PROD = "https://ton-domaine-de-prod.com/"

    private lateinit var prefs: SharedPreferences

    fun init(context: Context) {
        prefs = context.getSharedPreferences("eglise_auth", Context.MODE_PRIVATE)
    }

    private val authInterceptor = Interceptor { chain ->
        val token = prefs.getString("access_token", null)
        val request = if (token != null) {
            chain.request().newBuilder()
                .addHeader("Authorization", "Bearer $token")
                .build()
        } else chain.request()
        chain.proceed(request)
    }

    private val client = OkHttpClient.Builder()
        .addInterceptor(authInterceptor)
        .build()

    val api: EgliseApi by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL_DEV) // change en BASE_URL_PROD pour la release
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(EgliseApi::class.java)
    }

    fun saveTokens(access: String, refresh: String) {
        prefs.edit().putString("access_token", access).putString("refresh_token", refresh).apply()
    }
}
