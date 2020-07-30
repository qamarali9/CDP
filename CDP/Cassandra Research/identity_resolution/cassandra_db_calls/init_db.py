from cassandra.cluster import Cluster
from config import *
import logging

# create logger with __name__
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('log_identityResolution.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

def create_db(session):
    logger.info("create_db() called")
    try:
        replication_dict = {
                'class' : 'SimpleStrategy',
                'replication_factor' : 1
                }
        create_keyspace_query = """
        CREATE KEYSPACE {}
        WITH REPLICATION = {};
        """.format(CASSANDRA_KEYSPACE,replication_dict)
        session.execute(create_keyspace_query)
        session.set_keyspace(CASSANDRA_KEYSPACE)
        logger.info("Created keyspace {}".format(CASSANDRA_KEYSPACE))
    except Exception as Exc:
        logger.error("(In create_db()) Could not create keyspace - {}".format(CASSANDRA_KEYSPACE))
        print(Exc)

def create_table(session):
    logger.info("create_table() called")
    try:
        # partition key is (identity,cid)
        create_table_query = """
        CREATE TABLE identities
        ( identity varchar,
        type varchar,
        cid int,
        uid int,
        createdtime timestamp,
        primary key ((identity,cid))
        );
        """
        session.execute(create_table_query)
        logging.info("Created identities")
    except Exception as Exc:
        logger.error("(In create_table()) Could not create table - identities")
        print(Exc)

if __name__ == "__main__":
    cluster = Cluster()
    session = cluster.connect()
    create_db(session)
    create_table(session)
