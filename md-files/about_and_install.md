#NEXT LINE GOES YOUR POST'S DATE:
08.07.2017
#NEXT LINE GOES YOUR POST'S TITLE: 
About && Installation Guide
#NEXT LINE GO YOUR META-KEYWORDS
dsssg, static site generator
#NEXT LINE GOES YOUR META-DESCRIPTION
You will know how to setup your own DSSSG blog
#PUT YOUR POST INTRODUCTION BELOW (OPTIONAL, BLANK IF YOU USE DEFAULT THEME). MAKE SURE YOU HAVE ONE EMPTY LINE AFTER IT
Example text goes
here

#PUT YOUR POST'S CONTENT BELOW
What is DSSSG? DSSSG is a dead-simple static site generator. You just create a .md file of your blog post, then type
`python3 publish.py`
and you are done.
## Installation
It works only on Python 3.3+ and you must install some dependencies. DSSSG uses mistune to convert Markdown into HTML, it also uses Jinja2 as a template engine.
    pip3 install mistune
    pip3 install jinja2
Then download DSSSG
