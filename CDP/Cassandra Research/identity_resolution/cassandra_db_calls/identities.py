"""function put(session, identity, identity_type, cid, uid) returns status, throws Exception
function get(session, identity, identity_type, cid) returns uid, throws Exception
function update(session, identity, identity_type, cid, uid) returns status, throws Exception
function delete(session, identity, type, cid) returns status, throws Exception"""
from datetime import datetime
import logging
from id_generator import id_generator

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

def put(session, identity, identity_type, cid, uid):
    logger.info("put() called with parameters (identity:{},identity_type:{},cid:{},uid:{})".format(identity,identity_type,cid,uid))
    status = "SUCCESS"
    try:
        insert_query = """
        INSERT INTO identities
        (identity, type, cid, uid, createdtime)
        VALUES
        ('{}','{}', {}, {}, toTimeStamp(now()))
        IF NOT EXISTS
        ;
        """.format(identity,identity_type,cid,uid)
        row = session.execute(insert_query).one()
        logger.info("insert_query executed : {}".format(insert_query))
        if(row.applied == True):
            logger.info("Record inserted")
        else:
            logger.info("COULD NOT INSERT AS RECORD ALREADY EXISTS")
    except Exception as exc:
        logger.error("(In put()) Could not insert with parameters (identity:{},identity_type:{},cid:{},uid:{})".format(identity,identity_type,cid,uid))
        print(exc)
        status = "FAIL"
        raise
    return status


def get_uid(session, identity, identity_type, cid):
    row = get(session, identity, identity_type, cid)
    if(row == None):
        uid = id_generator.gen_id()
        put(session, identity, identity_type, cid, uid)
        return uid, False
    else:
        return row.uid, True

def get(session, identity, identity_type, cid):
    logger.info("get() called with parameters (identity:{},identity_type:{},cid:{})".format(identity,identity_type,cid))
    result = None
    try:
        select_query = """
        SELECT uid FROM identities
        WHERE identity = '{}' AND
        cid = {}
        ;
        """.format(identity,cid)
        results = session.execute(select_query)
        logger.info("select_query executed : {}".format(select_query))
    except Exception as exc:
        logger.error("(In get()) Could not select with parameters (identity:{},identity_type:{},cid:{})".format(identity,identity_type,cid))
        print(exc)
        raise
    return results.one()


def update(session, identity, identity_type, cid, uid):
    logger.info("update() called with parameters (identity:{},identity_type:{},cid:{},uid:{})".format(identity,identity_type,cid,uid))
    status = "SUCCESS"
    try:
        update_query = """
        UPDATE identities
        SET type = '{}',
        uid = {} 
        WHERE identity = '{}' AND
        cid = {}
        ;
        """.format(identity_type,uid,identity,cid)
        session.execute(update_query)
        logger.info("update_query executed : {}".format(update_query))
    except Exception as exc:
        logger.error("(In update()) Could not update with parameters (identity:{},identity_type:{},cid:{},uid:{})".format(identity,identity_type,cid,uid))
        print(exc)
        status = "FAIL"
        raise
    return status

def delete(session, identity, identity_type, cid):
    logger.info("delete() called with parameters (identity:{},identity_type:{},cid:{})".format(identity,identity_type,cid))
    status = "SUCCESS"
    try:
        delete_query = """
        DELETE FROM identities
        WHERE identity = '{}' AND
        cid = {}
        IF EXISTS
        ;
        """.format(identity,cid)
        session.execute(delete_query)
        logger.info("delete_query executed : {}".format(delete_query))
    except Exception as exc:
        logger.error("(In delete()) Could not select with parameters (identity:{},identity_type:{},cid:{})".format(identity,identity_type,cid))
        print(exc)
        status = "FAIL"
        raise
    return status
