from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.exc import UnmappedClassError


class NoLegacyQuerySQLAlchemy(SQLAlchemy):
    def init_app(self, app):
        super().init_app(app)
        
        @app.before_first_request
        def remove_query_property():
            self._remove_legacy_query_interface()
    
    def _remove_legacy_query_interface(self):
        try:
            for mapper in self.Model._sa_registry._class_registry.data.values():
                if hasattr(mapper, '__mro__') and self.Model in mapper.__mro__:
                    if hasattr(mapper, 'query'):
                        try:
                            delattr(mapper, 'query')
                        except (AttributeError, TypeError):
                            pass
        except (AttributeError, KeyError):
            pass


db = NoLegacyQuerySQLAlchemy()

