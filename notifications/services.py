"""
Service d'envoi de notifications push via Firebase Cloud Messaging (FCM).

NOTE: ceci est un squelette prêt à brancher. Pour l'activer réellement :
1. pip install firebase-admin
2. Récupérer le fichier de credentials (serviceAccountKey.json) depuis
   la console Firebase de ton projet.
3. Décommenter le code firebase_admin ci-dessous et renseigner le chemin
   du fichier de credentials dans les settings (FCM_CREDENTIALS_PATH).

En attendant, la fonction crée toujours l'objet Notification en base
(historique consultable dans l'app même si le push échoue) -- c'est le
comportement "offline-first" recherché : l'utilisateur verra la notif
au prochain sync même si FCM n'a pas pu la pousser en direct.
"""
from .models import Notification

# import firebase_admin
# from firebase_admin import credentials, messaging
# from django.conf import settings
#
# if not firebase_admin._apps:
#     cred = credentials.Certificate(settings.FCM_CREDENTIALS_PATH)
#     firebase_admin.initialize_app(cred)


def envoyer_notification(user, titre, message, type_notif="autre"):
    """Crée l'entrée en base et tente l'envoi push si un token FCM existe."""
    notif = Notification.objects.create(
        user=user, titre=titre, message=message, type=type_notif
    )

    if user.fcm_token:
        try:
            # msg = messaging.Message(
            #     notification=messaging.Notification(title=titre, body=message),
            #     token=user.fcm_token,
            # )
            # messaging.send(msg)
            pass
        except Exception:
            # Ne jamais bloquer le flux applicatif si le push échoue :
            # la Notification reste en base, l'app la récupérera au sync.
            pass

    return notif


def envoyer_notification_masse(users_queryset, titre, message, type_notif="autre"):
    """Envoie la même notification à un ensemble d'utilisateurs (ex: tout un rayon)."""
    return [
        envoyer_notification(u, titre, message, type_notif) for u in users_queryset
    ]
