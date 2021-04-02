from django.apps import AppConfig


class FillTheBlanksConfig(AppConfig):
    name = 'fill_the_blanks'

    def ready(self):
        import fill_the_blanks.signals
        