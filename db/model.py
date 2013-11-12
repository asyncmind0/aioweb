class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        default_views = {
            'all': {
                "map": """
                function(doc){
                if(doc.doc_type == "%s")
                emit(doc._id, doc);
            }
                """ % name
            }
        }
        attrs['default_views'] = default_views
        return type.__new__(cls, name, bases, attrs)


class Model(metaclass=ModelMeta):
    views = {}
    data = {}
    _fields = []
    def __init__(self,  **kwargs):
        for field in self.fields:
            self.data[field] = kwargs[field]
        for field in self.required_fields:
            assert field in kwargs, "Required field missing: %s" % field
        self.data['doc_type'] = self.__class__.__name__

    @classmethod
    def all(cls, db):
        view_name = cls.__name__.lower()
        n = yield from db.view(view_name, 'all')
        return n

    @property
    def fields(self):
        return self.required_fields + self._fields

    def get_data(self):
        return self.data
        
    def __setattr__(self, name, value):
        if name in self.required_fields or name in self.fields:
            self.data[name] = value
            
    def __getattr__(self, name):
        if name in self.required_fields or name in self.fields:
            return self.data[name]
            

    @classmethod
    def sync_design(cls, db):
        assert cls.views is not None, NotImplemented("views")
        info = yield from db.info()
        if info.reason == 'no_db_file':
            r = yield from db.create_db()
            assert hasattr(r, 'ok') and r.ok == True, \
                "Failed to create database: %s" % str(r)
        view_name = cls.__name__.lower()
        r = yield from db.get_design_doc(view_name)
        if r and hasattr(r, 'views'):
            r = yield from db.delete_design_doc(view_name, rev=r._rev)
            assert hasattr(r, 'ok') and r.ok == True, \
                "Failed to delete design doc: %s" %  str(r)
        _views = {}
        _views.update(cls.default_views)
        _views.update(cls.views)
        r = yield from db.put_design_doc(view_name, dict(views=_views))
        assert hasattr(r, 'ok') and r.ok == True, \
            "Failed to put design doc: %s" % str(r)
        

