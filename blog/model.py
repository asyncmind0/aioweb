class Model():
    def __init__(self,  **kwargs):
        self.data = {}
        for field in self.required_fields:
            self.data[field] = kwargs[field]
        self.data['doc_type'] = self.__class__.__name__

    def get_data(self):
        return self.data
        
    def __setattr__(self, name, value):
        if name in required_fields or name in fields:
            self.data[name] = value
            
    def __getattr__(self, name):
        if name in required_fields or name in fields:
            return self.data[name]

    @classmethod
    def sync_design(cls, db):
        assert cls.design is not None, NotImplemented("design")
        view_name = cls.__name__.lower()
        r = yield from db.get_design_doc(view_name)
        if r and hasattr(r, 'views'):
            r = yield from db.delete_design_doc(view_name, rev=r._rev)
            assert hasattr(r, 'ok') and r.ok == True, \
                "Failed to delete design doc: %s" %  str(r)
        r = yield from db.put_design_doc(view_name, cls.design)
        assert hasattr(r, 'ok') and r.ok == True, \
            "Failed to put design doc: %s" % str(r)
        

class Post(Model):
    required_fields = ['title', 'body', 'date']
    design = {
        'views':{
            'all': {
                "map": """
                    function(doc){
                        if(doc.doc_type == "Post")
                        emit(doc._id, doc);
                    }
                    """
                    }
                }
            }