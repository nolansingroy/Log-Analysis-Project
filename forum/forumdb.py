# "Database code" for the DB Forum.
import time
import bleach
import psycopg2
DBNAME = "forum"


def get_posts():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("select content, time from posts order by time desc")
  posts = c.fetchall()
  db.close()
  return posts

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("insert into posts (content) values (%s) ", 
                   (bleach.clean(content),))
  db.commit()
  db.close()

