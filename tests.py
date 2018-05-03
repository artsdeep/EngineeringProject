import os
import unittest
import json
from app import db, app

TEST_DB = 'test.db'
class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        POSTGRES_DB = "test"
        DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=app.config['POSTGRES_USER'], pw=app.config['POSTGRES_PW'],
                                                                       url=app.config['POSTGRES_URL'], db=POSTGRES_DB)



        #app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        path_sql_script = os.path.abspath(os.path.dirname(__file__))
        from app.request.models import Client
        if db.session.query(Client).count() == 0:
            sql_command = ''
            sql_file = open(path_sql_script + "/db.sql", 'r')
            for line in sql_file:
                if not line.startswith('--') and line.strip('\n'):
                    sql_command += line.strip('\n')
                    if sql_command.endswith(';'):
                        try:
                            db.engine.execute(str(sql_command))
                            # Assert in case of error
                        except:
                            print('Ops')

                        finally:
                            sql_command = ''
    def tearDown(self):
        pass
        # delete test database, etc.
    def test_product_areas(self):
        json_test = self.app.post('/get_product_areas')
        productAreas = json.loads(json_test.get_data().decode()).get("productAreas")
        assert 2 == productAreas[0].get("id"), "Problem"
        assert "Billing" == productAreas[0].get("name")
        assert 4 == productAreas[len(productAreas)-1].get("id")
        assert "Reports" == productAreas[len(productAreas)-1].get("name")

    def test_get_clients(self):
        json_test = self.app.post('/get_clients')
        clients = json.loads(json_test.get_data().decode()).get("clients")
        assert 1 == clients[0].get("id")
        assert "Client A" == clients[0].get("name")
        assert 3 == clients[len(clients)-1].get("id")
        assert "Client C" == clients[len(clients)-1].get("name")

    def test_add_feature_request(self):
        json_add = '{"title":"test request","desc":"test request description","clients":[{"id":"","name":""}, {"date_created":null,"id":1,"name":"Client A"},{"date_created":null,"id":2,"name":"Client B"}, {"date_created":null,"id":3,"name":"Client C"}],"clientValue":1,"clientPriority":"2","targetDate":"2018-04-25T14:02:10.142Z", "dateFormat":"mm/dd/yyyy","productArea":[{"id":"","name":""},{"date_created":null,"id":2,"name":"Billing"}, {"date_created":null,"id":3,"name":"Claims"},{"date_created":null,"id":1,"name":"Policies"}, {"date_created":null,"id":4,"name":"Reports"}],"productAreaValue":3,"errors":[]}'
        json_test = self.app.post('/add_feature_request', data=json_add, content_type='application/json')
        status = json.loads(json_test.get_data().decode()).get("status")
        assert status == "good"
if __name__ == '__main__':
    unittest.main()