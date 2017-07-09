import locale
import datetime
import pprint
import os
import sys

import mistune
import jinja2

POSTS_FOLDER = "posts"
MDS_FOLDER = "md-files"
THEME_FOLDER = "theme"

# Display date in YOUR_LANGUAGE by setting up locale (ex. below for Russian)
#locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

def translit(s):
	"""
	Transliterates the input string. The result is URL-compatible string,
	with all spaces converted to '-'
	"""
	repls = {
		"а" :"a" ,
		"б" :"b" ,
		"в" :"v" ,
		"г" :"g" ,
		"д" :"d" ,
		"е" :"e" ,
		"ё" : "e",
		"ж" : "zh",
		"з" : "z",
		"и" : "i",
		"й" : "iy",
		"к" : "k",
		"л" : "l",
		"м" : "m",
		"н" : "n",
		"о" : "o",
		"п" : "p",
		"р" : "r",
		"с" : "s",
		"т" : "t",
		"у" : "u",
		"ф" : "f",
		"х" : "h",
		"ц" : "ts",
		"ч" : "ch",
		"ш" : "sh",
		"щ" : "sch",
		"ь" : "",
		"Ъ" : "",
		"Ы" : "y",
		"э" : "e",
		"ю" : "u",
		"я" : "ya",
		" " : "-"
	}
	s = s.strip()
	s = s.lower()

	sr = ""
	for ch in s:
		if ch in repls:
			sr += repls[ch]
		elif ch.isalnum():
			sr += ch
	while sr.find("--") > -1:
		sr = sr.replace("--", "-")

	if len(sr) > 0 and sr[-1] == "-":
		sr = sr[:-1]

	return sr

def rm_all_files_in_dir(path):
	""" Emptyes the folder, specifyed in path """
	os.system("rm -r " + path + "/*")

def load_post_structure(filepath):
	"""
	Load .md file of the post, specifyed in filepath, into internal strcuture
	"""
	post = {
		"date" : None,
		"title" : "",
		"meta_keywords":"",
		"meta_description":"",
		"url" : "",
		"intro" : "",
		"content" : ""
	}

	try:
		f = open(filepath, "r")
	except IOError:
		sys.exit("No such .md file: {}".format(filepath))

	# Date
	f.readline() # hint line
	sd = f.readline()
	if len(sd) > 1:
		sd = sd[:-1] # remove \n
		post["date"] = datetime.datetime.strptime(sd, "%d.%m.%Y")
	else:
		sys.exit("Date Line shouldn't be empty in " + filepath)

	#Title
	f.readline() # hint line
	post["title"] = f.readline()
	if len( post["title"] ) > 1:
		post["title"] = post["title"][:-1] # remove \n
	else:
		sys.exit("Title Line shouldn't be empty in " + filepath)

	#Meta-keywords
	f.readline() # hint line
	post["meta_keywords"] = f.readline()[:-1]

	#Meta-description
	f.readline() # hint line
	post["meta_description"] = f.readline()[:-1]

	#Introduction
	f.readline() # hint line
	line = ""
	while line != "\n":
		post["intro"] += line
		line = f.readline()

	#Content
	f.readline() # hint line
	for line in f:
		post["content"] += line

	f.close()

	post["url"] = os.path.join("/", POSTS_FOLDER, translit(post["title"]) )
	convert_in_markdown(post)

	return post

def convert_in_markdown(post):
	"""
	Converts all markdown-fields of the posts into their HTML repr.
	"""
	md2html = mistune.Markdown()
	post["intro"] = md2html(post["intro"])
	post["content"] = md2html(post["content"])
	return

def build_posts_index_in_dir(pub_dir):
	"""
	Load all .md posts into the list, sorted by date
	"""
	files = ( f for f in os.listdir(pub_dir) if os.path.isfile( os.path.join(pub_dir, f) ) )
	index = ( load_post_structure( os.path.join(pub_dir, f) ) for f in files )

	# newest posts are displayed first
	index = sorted( index, key=lambda post: post["date"], reverse=True )
	return index

def make_index_and_posts_pages(posts_tuple):
	"""
	The argument is inner representation of all posts
	Creates HTML file of index page. Creates folders for posts and their HTML files.
	Uses Jinja2 as template engine
	"""
	jenv = jinja2.Environment(
	    loader=jinja2.FileSystemLoader( os.path.join( os.path.dirname(__file__), THEME_FOLDER ) )
	)

	index_page = jenv.get_template('index.html')
	index_page_code = index_page.render(posts=posts_tuple)
	with open("index.html", "w") as fh:
	    fh.write(index_page_code)

	for post in posts_tuple:
		post_page = jenv.get_template('post.html')
		post_page_code = post_page.render(post=post)

		post_dir = "." + post["url"] 
		os.mkdir( post_dir )
		with open( os.path.join(post_dir, "index.html"), "w") as fh:
			fh.write(post_page_code)


if __name__ == "__main__":
	posts_tuple = build_posts_index_in_dir( MDS_FOLDER )
	rm_all_files_in_dir( POSTS_FOLDER )
	make_index_and_posts_pages( posts_tuple )
