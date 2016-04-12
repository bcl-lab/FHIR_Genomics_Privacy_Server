"""
Script to prepare a local postgresql instance for the server,
for more advanced usage, well, this won't help
"""

import os
import subprocess
import psycopg2
from resources.common.config_db import dbname, dbuser, dbuserpassword



if __name__ == '__main__':
    os.environ['PGPASSWORD'] = dbuserpassword
    subprocess.call('sudo -u postgres createuser -d %s' % dbuser, shell=True)
    subprocess.call('createdb %s' % dbname, shell=True)

    # Create table "Privacy_Server" in database
    privacy_server = "dbname=%s user=%s" % (dbname, dbuser)
    conn = psycopg2.connect(privacy_server)
    with conn:
        with conn.cursor() as curs:
            curs.execute("CREATE TABLE privacy (patient_id varchar PRIMARY KEY, policy json, last_modified date)")
            curs.execute("CREATE TABLE user (user_id varchar PRIMARY KEY, password varchar, email varchar)")

    conn.close()