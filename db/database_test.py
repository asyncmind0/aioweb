from tulip import test_utils
from test import CouchDBTestCase


class CouchDBAdapterTest(CouchDBTestCase):
    def setUp(self):
        super(CouchDBAdapterTest, self).setUp()
        r = self.loop.run_until_complete(self.db.create_db())
        self.test_document = {'test': 'testdata'}
        r = self.loop.run_until_complete(self.db.put(self.test_document))
        assert r.ok is True
        self.test_document['id'] = r.id

    def tearDown(self):
        r = self.loop.run_until_complete(
            self.db.delete(self.test_document['id']))
        assert r.ok is True
        r = self.loop.run_until_complete(self.db.delete_db())
        self.assertEqual(r.ok, True)
        super(CouchDBAdapterTest, self).tearDown()

    def test_info(self):
        r = self.loop.run_until_complete(self.db.info())
        self.assertEqual(r.db_name, self.db._dbname)

    def test_put(self):
        document = {'test': 'testdata'}
        r = self.loop.run_until_complete(self.db.put(document))
        self.assertEqual(r.ok, True)

    def test_all(self):
        r = self.loop.run_until_complete(self.db.all())
        assert r.total_rows > 0

    def test_get(self):
        r = self.loop.run_until_complete(self.db.all())
        assert r.total_rows > 0
        one = r.rows[0]
        r = self.loop.run_until_complete(self.db.get(one['id']))
        assert r._id == one['id']

    def test_delete(self):
        document = {'test': 'testdelete'}
        document = self.loop.run_until_complete(self.db.put(document))
        r = self.loop.run_until_complete(self.db.delete(document.id))
        assert r.ok is True
        r = self.loop.run_until_complete(self.db.get(document.id))
        assert r.reason == 'deleted'

    def test_put_design_doc(self):
        document = {
            'views': {
                'all': {
                    "map": """
                            function(doc){
                                if(doc.doc_type == "User")
                                emit(doc._id, doc);
                            }
                        """
                    }
                }
            }

            r = self.loop.run_until_complete(
                self.db.put_design_doc('user', document))
            assert r.ok is True

    def test_view(self):
        self.test_put_design_doc()
        document = {'doc_type': 'User'}
        r1 = self.loop.run_until_complete(self.db.put(document))
        self.assertEqual(r1.ok, True)
        r = self.loop.run_until_complete(self.db.view("user", "all"))
        assert r.total_rows > 0
        assert r.rows[0]['id'] == r1.id
