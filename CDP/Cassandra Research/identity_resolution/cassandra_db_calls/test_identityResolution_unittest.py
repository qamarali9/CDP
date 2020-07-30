import unittest
import cassandra

import connection
import init_db
import identities
import config



class TestIdentityResolution(unittest.TestCase):

    def setUp(self):
        self.cluster = cassandra.cluster.Cluster()
        self.session = self.cluster.connect()
        self.session.execute("CREATE KEYSPACE testdb WITH REPLICATION = {};".format({'class' : 'SimpleStrategy',
            'replication_factor' : 1
            }))
        self.session.set_keyspace('testdb')
    
    def tearDown(self):
        self.session.execute("DROP KEYSPACE testdb;")

    def test_identityResolution_connection(self):
        session = connection.get_connection({},'testdb')
        self.assertEqual(type(session), cassandra.cluster.Session, "Should be cassandra.cluster.Session")

    def test_identityResolution_put(self):
        init_db.create_table(self.session)
        identities.put(self.session,"mark@gmail.com","mail",123,76)
        row = self.session.execute("SELECT * FROM identities;").one()
        self.assertEqual(row.identity,"mark@gmail.com","Identity should be 'mark@gmail.com'")
        self.assertEqual(row.type,"mail","Type should be 'mail'")
        self.assertEqual(row.cid, 123,"cid should be 123")
        self.assertEqual(row.uid, 76,"uid should be 76")
        self.session.execute("DROP TABLE identities;")

    def test_identityResolution_get(self):
        init_db.create_table(self.session)
        identities.put(self.session,"mark@gmail.com","mail",123,76)
        row = identities.get(self.session,"mark@gmail.com","mail",123)
        self.assertEqual(row.uid, 76,"uid should be 76")
        self.session.execute("DROP TABLE identities;")

    def test_identityResolution_update(self):
        init_db.create_table(self.session)
        identities.put(self.session,"mark@gmail.com","number",123,98)
        identities.update(self.session,"mark@gmail.com","mail",123,76)
        row = self.session.execute("SELECT * FROM identities;").one()
        self.assertEqual(row.identity,"mark@gmail.com","Identity should be 'mark@gmail.com'")
        self.assertEqual(row.type,"mail","Type should be 'mail'")
        self.assertEqual(row.cid, 123,"cid should be 123")
        self.assertEqual(row.uid, 76,"uid should be 76")
        self.session.execute("DROP TABLE identities;")

    def test_identityResolution_delete(self):
        init_db.create_table(self.session)
        identities.put(self.session,"mark@gmail.com","mail",123,76)
        identities.delete(self.session,"mark@gmail.com","mail",123)
        row = self.session.execute("SELECT * FROM identities;").one()
        self.assertEqual(row,None,"row should be None")
        self.session.execute("DROP TABLE identities;")
 
if __name__ == '__main__':
    unittest.main()


"""

'''
class TestDB(unittest.TestCase):
    scenarios = [
        ('mysql', dict(database_connection=os.getenv("MYSQL_TEST_URL")),
        ('postgresql', dict(database_connection=os.getenv("PGSQL_TEST_URL")),
    ]

    def setUp(self):
       if not self.database_connection:
           self.skipTest("No database URL set")
       self.engine = sqlalchemy.create_engine(self.database_connection)
       self.connection = self.engine.connect()
       self.connection.execute("CREATE DATABASE testdb")

    def tearDown(self):
        self.connection.execute("DROP DATABASE testdb")
'''

'''
from unittest.mock import patch, MagicMock

@patch('mypackage.mymodule.pymysql')
def test(self, mock_sql):
    self.assertIs(mypackage.mymodule.pymysql, mock_sql)

    conn = Mock()
    mock_sql.connect.return_value = conn

    cursor      = MagicMock()
    mock_result = MagicMock()

    cursor.__enter__.return_value = mock_result
    cursor.__exit___              = MagicMock()

    conn.cursor.return_value = cursor

    connectDB()

    mock_sql.connect.assert_called_with(host='localhost',
                                        user='user',
                                        password='passwd',
                                        db='db')

    mock_result.execute.assert_called_with("sql request", ("user", "pass"))
'''

"""
