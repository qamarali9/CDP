from cassandra.cluster import Cluster
import random

# Connecting to cassandra, entering into keyspace 'dev' and creating test_table
cluster = Cluster()
session = cluster.connect('dev')
session.execute("CREATE TABLE test_table (rowid int primary key, first_string varchar, random_string varchar);")

# Suffixes for strings to insert in test_table
first_string_suffix = "first_string_"
random_string_suffix = "random_string_"

# Getting the local cluster name and network info
rows = session.execute("SELECT cluster_name, listen_address FROM system.local;")
for row in rows:
    print(row)
    
# Inserting 10,000 records
for i in range(0,10000):
    #print("INSERT INTO test_table (rowid, first_string, random_string) values ("+ str(i) + ", " + first_string_suffix + str(i) + ", " + random_string_suffix + str(random.randint(0,10000)) + ");")
    session.execute("INSERT INTO test_table (rowid, first_string, random_string) values ("+ str(i) + ", '" + first_string_suffix + str(i) + "', '" + random_string_suffix + str(random.randint(0,10000)) + "');")

# Printing 100 rows
rows = session.execute("SELECT * FROM test_table;")
for row in rows[0:100]:
    print(row)

# Printing row with rowid=5678
rows = session.execute("SELECT * FROM test_table where rowid=5678;")
for row in rows[0:100]:
    print(row)

# Printing number of rows
rows = session.execute("SELECT COUNT(*) FROM test_table;")
for row in rows:
    print(row)

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
