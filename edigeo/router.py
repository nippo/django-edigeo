class EdigeoRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'edigeo':
            return 'edigeo'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'edigeo':
            return 'edigeo'
        return None
