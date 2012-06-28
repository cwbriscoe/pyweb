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


def insert(conn, name, values):
    sql = "INSERT INTO " + name + " VALUES(" + values + ");"
    runsql(conn, sql)


def main():
  try:
    conn = dbase.connect("host='localhost' dbname='testdb' user='chris' password='commode'")
  except:
    print "unable to connect to the database"
    raise

  create_table(conn, "users", """
    id      serial,
    name    varchar(40),
    PRIMARY KEY(id)
  """)
  insert(conn, "users", "DEFAULT, 'chris'")
  insert(conn, "users", "DEFAULT, 'bob'")
  insert(conn, "users", "DEFAULT, 'george'")
  insert(conn, "users", "DEFAULT, 'fred'")
  insert(conn, "users", "DEFAULT, 'brice'")

  create_table(conn, "auth", """
    user_id integer references users(id) on delete cascade,
    version integer,
    hash    varchar(256),
    salt    varchar(40),
    PRIMARY KEY(user_id)
  """)
  insert(conn, "auth", "1, 1, 'chrispass', 'chrissalt'")
  insert(conn, "auth", "2, 1, 'bobpass', 'bobsalt'")
  insert(conn, "auth", "3, 1, 'georgepass', 'georgesalt'")
  insert(conn, "auth", "4, 1, 'fredpass', 'fredsalt'")
  insert(conn, "auth", "5, 1, 'bricepass', 'bricesalt'")


if __name__ == "__main__":
  main()
