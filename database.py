import couchdb

db = None

def get_db():
    global db
    dbname = 'blog'
    if not db:
        couch = couchdb.Server('http://localhost:5984/')
        try:
            db = couch[dbname]
        except couchdb.ResourceNotFound as e:
            cb = couch.create(dbname)
    return db
