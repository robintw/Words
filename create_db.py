from collections import defaultdict 
import sqlite3

conn = sqlite3.connect('test.db')

filename = 'words.txt'
#filename = 'testwords'

conn.execute("""DROP TABLE words;""")
conn.execute("""CREATE TABLE words (
			id INTEGER PRIMARY KEY,
			word VARCHAR(255) NOT NULL,
			a INTEGER DEFAULT 0,
			b INTEGER DEFAULT 0,
			c INTEGER DEFAULT 0,
			d INTEGER DEFAULT 0,
			e INTEGER DEFAULT 0,
			f INTEGER DEFAULT 0,
			g INTEGER DEFAULT 0,
			h INTEGER DEFAULT 0,
			i INTEGER DEFAULT 0,
			j INTEGER DEFAULT 0,
			k INTEGER DEFAULT 0,
			l INTEGER DEFAULT 0,
			m INTEGER DEFAULT 0,
			n INTEGER DEFAULT 0,
			o INTEGER DEFAULT 0,
			p INTEGER DEFAULT 0,
			q INTEGER DEFAULT 0,
			r INTEGER DEFAULT 0,
			s INTEGER DEFAULT 0,
			t INTEGER DEFAULT 0,
			u INTEGER DEFAULT 0,
			v INTEGER DEFAULT 0,
			w INTEGER DEFAULT 0,
			x INTEGER DEFAULT 0,
			y INTEGER DEFAULT 0,
			z INTEGER DEFAULT 0
		);""")

conn.commit()


with open(filename) as f:
	for word in f.readlines():
		letters = defaultdict(lambda: 0)

		word = word.strip().upper()

		for letter in word:
			letters[letter] += 1

		sql = "INSERT INTO words (word, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z) VALUES ('%s'" % word

		for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
			sql += ",%s" % letters[letter]

		sql += ")"
		print sql

		conn.execute(sql)

	conn.commit()