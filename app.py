from flask import Flask, render_template, request, jsonify
from collections import defaultdict
import sqlite3
import re

app = Flask(__name__)

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ajax')
def ajax():
	return render_template('ajax.html')

@app.route('/words', methods=['POST'])
def words():
	word = request.form['text']

	words = get_anagrams(word)

	return render_template('words.html', words=words)

@app.route('/wordsjson')
def wordsjson():
	functions = {}
	functions['anagram'] = get_anagrams
	functions['containing'] = get_containing
	functions['regex'] = get_regex
	functions['starts'] = get_starts
	functions['ends'] = get_ends

	word = request.args.get('word', "", type=str).upper()
	giventype = request.args.get('type', "anagram", type=str)

	print word
	print giventype

	words = functions[giventype](word)

	#words = get_anagrams(word)

	if word in words:
		words.remove(word)

	if len(words) == 0:
		html = "<i>No words found</i>"
		return jsonify(result=html, css='bg-danger')

	else:
		html = "<ul>"
		html += "".join(["<li>%s</li>" % w for w in words])
		html += "</ul>"
		return jsonify(result=html, css='bg-success')




def get_anagrams(word):
	letters = defaultdict(lambda: 0)

	word = word.upper()

	for letter in word:
		letters[letter] += 1

	sql = "SELECT * FROM words WHERE "

	for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
		sql += "%s = %s" % (letter, letters[letter])
		if letter != "Z":
			sql += " AND "
		else:
			sql += ";"

	conn = sqlite3.connect('test.db')

	print sql
	results = conn.execute(sql)

	words = [res[1] for res in results.fetchall()]

	return words

def get_containing(word):
	letters = {}

	word = word.upper()


	print word
	for letter in word:
		try:
			letters[letter] += 1
		except:
			letters[letter] = 1

	sql = "SELECT * FROM words WHERE "

	print sql
	for letter, count in letters.iteritems():
		print letter, count
		sql += "%s = %s AND " % (letter, count)

	sql = sql[0:-4] + ";"

	conn = sqlite3.connect('test.db')

	print sql
	results = conn.execute(sql)

	words = [res[1] for res in results.fetchall()]

	return words
	#return []

def get_starts(word):
	with open("words.txt") as f:
		lines = map(str.strip, f.readlines())

	return filter(lambda x: x.startswith(word), lines)

def get_ends(word):
	with open("words.txt") as f:
		lines = map(str.strip, f.readlines())

	return filter(lambda x: x.endswith(word), lines)

def get_regex(regex):
	compiled_regex = re.compile(r"^" + regex + r"$")

	with open("words.txt") as f:
		lines = map(str.strip, f.readlines())

	return filter(compiled_regex.search, lines)

if __name__ == '__main__':
    app.run(debug=True)
