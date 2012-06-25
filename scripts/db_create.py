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


def create_table(conn, name, extras):
  drop = "DROP TABLE IF EXISTS " + name + " CASCADE;"
  runsql(conn, drop)

  create = "CREATE TABLE " + name + " (" + extras + ");"
  runsql(conn, create)


def main():
  try:
    conn = dbase.connect("host='localhost' dbname='testdb' user='chris' password='commode'")
  except:
    print "unable to connect to the database"
    raise

  create_table(conn, "users", """
    id      integer,
    name    varchar(40),
    pass    varchar(40),
    PRIMARY KEY(id)
  """)

  create_table(conn, "auth", """
    id      integer references users(id) on delete cascade,
    version integer,
    hash    varchar(256),
    salt    varchar(40),
    PRIMARY KEY(id)
  """)

if __name__ == "__main__":
  main()
