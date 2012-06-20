#! /usr/bin/env python
import psycopg2 as dbase

def runsql(conn, sql):
  try:
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
  except Exception, err:
    conn.rollback()
    print err.pgerror


def main():
  try:
    conn = dbase.connect("host='localhost' dbname='testdb' user='chris' password='commode'")
  except:
    print "unable to connect to the database"
    raise

  runsql(conn, """DROP TABLE distributors;""")
  runsql(conn, """
    CREATE TABLE distributors (
      did     integer,
      name    varchar(40),
      PRIMARY KEY(did)
  );""")

if __name__ == "__main__":
  main()
