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


def create_index(conn, name, tblname, unique, extras):
  crtidx = "CREATE "
  if unique == True:
    crtidx += "UNIQUE "
  crtidx += "INDEX " + name + " ON " + tblname + " (" + extras + ");"
  runsql(conn, crtidx)


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
    name    varchar(24),
    PRIMARY KEY(id)
  """)
  insert(conn, "users", "DEFAULT, 'chris'")
  insert(conn, "users", "DEFAULT, 'bob'")
  insert(conn, "users", "DEFAULT, 'george'")
  insert(conn, "users", "DEFAULT, 'fred'")
  insert(conn, "users", "DEFAULT, 'brice'")
  create_index(conn, "users_idx", "users", True, "lower(name)")

  create_table(conn, "auth", """
    user_id integer references users(id) on delete cascade,
    ver     integer,
    hash    varchar(256),
    salt    varchar(40),
    PRIMARY KEY(user_id)
  """)
  insert(conn, "auth", "1, 1, 'chrispass', 'chrissalt'")
  insert(conn, "auth", "2, 1, 'bobpass', 'bobsalt'")
  insert(conn, "auth", "3, 1, 'georgepass', 'georgesalt'")
  insert(conn, "auth", "4, 1, 'fredpass', 'fredsalt'")
  insert(conn, "auth", "5, 1, 'bricepass', 'bricesalt'")

  create_table(conn, "groups", """
    id       serial,
    name     varchar(16),
    PRIMARY KEY(id)
  """)
  insert(conn, "groups", "DEFAULT, 'worldnews'")
  insert(conn, "groups", "DEFAULT, 'politics'")
  insert(conn, "groups", "DEFAULT, 'programming'")
  insert(conn, "groups", "DEFAULT, 'cpp'")
  insert(conn, "groups", "DEFAULT, 'python'")
  insert(conn, "groups", "DEFAULT, 'running'")
  insert(conn, "groups", "DEFAULT, 'funny'")
  insert(conn, "groups", "DEFAULT, 'science'")
  insert(conn, "groups", "DEFAULT, 'android'")
  insert(conn, "groups", "DEFAULT, 'technology'")
  insert(conn, "groups", "DEFAULT, 'wtf'")
  insert(conn, "groups", "DEFAULT, 'gonewild'")
  create_index(conn, "groups_idx", "groups", True, "lower(name)")

  create_table(conn, "topics", """
    id       serial,
    group_id integer references groups(id) on delete cascade,
    user_id  integer references users(id) on delete set null,
    text     varchar(128),
    PRIMARY KEY(id)
  """)

  create_table(conn, "posts", """
    id       serial,
    topic_id integer references topics(id) on delete cascade,
    user_id  integer references users(id) on delete set null,
    text     varchar(4000),
    PRIMARY KEY(id)
  """)


if __name__ == "__main__":
  main()
