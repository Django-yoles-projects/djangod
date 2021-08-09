from django.apps import AppConfig


class RegisterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.register'

    # def ready(self) -> None:    
    #     from django.db.models.signals import post_save
    #     Profile = self.get_model('Profile')
    #     post_save.connect(receiver, sender='app_label.MyModel')
