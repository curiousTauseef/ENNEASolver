import psycopg2

conn = psycopg2.connect("dbname=jhbruhn user=jhbruhn")

cur = conn.cursor()

with open("german.dic") as f:
  dic = f.readlines()
  n = 0
  for entry in dic:
    n = n + 1
    try:
      cur.execute("INSERT INTO dictionary (entry) VALUES (%s)", (entry.strip(),))
    except psycopg2.IntegrityError:
      print "pscht"
    except psycopg2.InternalError:
      print "peda"

    if n % 500 == 499:
      conn.commit()
      print float(n) / len(dic) * 100

  cur.commit()

  cur.close()
