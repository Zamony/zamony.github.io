#NEXT LINE GOES YOUR POST'S DATE:
09.07.2017
#NEXT LINE GOES YOUR POST'S TITLE: 
How To Use DSSG && Custom Themes
#NEXT LINE GO YOUR META-KEYWORDS
dsssg, static site generator
#NEXT LINE GOES YOUR META-DESCRIPTION
You will know how to setup your own DSSSG blog
#PUT YOUR POST INTRODUCTION BELOW (OPTIONAL, BLANK IF YOU USE DEFAULT THEME). MAKE SURE YOU HAVE ONE EMPTY LINE AFTER IT
Example text goes
here

#PUT YOUR POST'S CONTENT BELOW
## How to create a post?
Go to the *md-file* folder. Then create a .md file of your post with the structure like this. Then open terminal in the base folder of DSSSG ( there should be publish.py ) and type in the terminal `python3 publish.py`
## Are custom themes supported?
Sure. DSSSG uses Jinja2 as a template engine, so just make sure you have two files in your theme: index.html and post.html for the index and post pages accordingly.
Then you should be able to access DSSSG variables `post` and `posts`.
Further reading on the [Jinja2 website](http://jinja.pocoo.org/docs/2.9/templates/ "Jinja2 website").
You can use default theme as an example.
