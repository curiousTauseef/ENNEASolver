import itertools
import sys
import string
import thread
from progressbar import ProgressBar

input = string.join(sys.argv[1:], "").lower()

def generate_words(input, length):
  return itertools.permutations(input, length)

print "Analyzing " + input

words = []

print "Generating internal wordlist..."
device = range(3, len(input) + 1)
for n in device:
  for i in generate_words(input, n):
    words.append(string.join(i, ""))

print "Internal Wordslist finished, putting stuff in the DB..."

import psycopg2

conn = psycopg2.connect("dbname=jhbruhn user=jhbruhn")

cur = conn.cursor()

results = []

cur.execute("DROP TABLE temp;")

cur.execute("CREATE TABLE temp (entry varchar(100)); CREATE INDEX entry ON temp (entry)")
conn.commit()

n = 0

progress = ProgressBar(maxval=len(words) + 1)

for word in words:
  n = n + 1
  cur.execute("INSERT INTO temp (entry) VALUES (%s)", (word,))
  progress.update(n)
  if n % 4999 == 0:
    conn.commit()
conn.commit()
progress.finish()

print "Executing Compare Statement..."

cur.execute("SELECT DISTINCT temp.entry FROM temp, dictionary WHERE lower(temp.entry) = lower(german_dictionary.entry)")

print "Results:"
results = []
res = cur.fetchall()
for e in res:
  results.append(e[0])


conn.commit()
cur.close()
conn.close()

results.sort(lambda x,y: cmp(len(x), len(y)))

prevLength = 0

for r in results:
  if(len(r) > prevLength):
    prevLength = len(r)
    print str(len(r)) + ":"
  print r
