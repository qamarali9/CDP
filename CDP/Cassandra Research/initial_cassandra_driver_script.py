"""
Command executed in cqlsh:
    
SELECT cluster_name, listen_address FROM system.local;

CREATE KEYSPACE excelsior WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};

CREATE KEYSPACE excalibur WITH replication = {'class': 'NetworkTopologyStrategy', 'DC1' : 1, 'DC2' : 3} AND durable_writes = false;

DESCRIBE keyspaces;

create keyspace dev with replication = {'class':'SimpleStrategy','replication_factor':1};

use dev;

create table emp (empid int primary key, emp_first varchar, emp_last varchar, emp_dept varchar);

DESCRIBE emp;

INSERT INTO emp (empid, emp_first, emp_last, emp_dept) values (1,'fred', 'smith', 'eng');

UPDATE emp SET emp_dept = 'fin' where empid = 1;

SELECT * FROM emp;

SELECT * FROM emp WHERE emp_dept='fin';

SELECT * FROM emp WHERE empid=1;

CREATE index idx_dept on emp(emp_dept);

SELECT * FROM emp WHERE emp_dept='fin';



Installing cassandra python driver : pip install cassandra-driver

"""

from cassandra.cluster import Cluster
cluster = Cluster()
session = cluster.connect('dev')
#session.execute("SELECT * FROM emp WHERE emp_dept='fin'")
rows = session.execute("SELECT * FROM emp WHERE emp_dept='fin'")
for row in rows:
    print(row)

rows = session.execute("SELECT cluster_name, listen_address FROM system.local;")
for row in rows:
    print(row)

