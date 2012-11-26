#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__= 'Frederic Laurent'
__version__= '1.0'
__license__ = "LGPL"
__email__ = "fl@opikanoba.org"


from bottle import route, run, request, response, error

#https://github.com/martinblech/mimerender
import mimerender
mimerender = mimerender.BottleMimeRender()

# My little data
mydata={ "0836221362" : { "title":"The Days Are Just Packed", 
				"author":"Bill Watterson", 
				"img":"http://isbn.abebooks.com/mz/57/83/0836217357.jpg"}
	}

def html_repr(data):
	"""
	HTML Representation of my data
	data : my data in a dictionary
	"""
	html="""
	<html>
		<head><title>Book ISBN %s</title></head>
		<body><h1>%s</h1>
		 <h2>%s</h2><img src="%s"/>
		</body>
	</html>"""%(data["isbn"], data["title"], 
				data["author"], data["img"])
	return html

def json_repr(data):
	"""
	JSON Representation of my data
	data : my data in a dictionary
	"""
	return data

def txt_repr(data):
	"""
	TEXT Representation of my data
	data : my data in a dictionary
	"""
	return "[%s] %s - %s\n"%(data["isbn"], data["title"], data["author"])


# Define the route (URL) of my resource
@route('/book/:isbn')

# Define wich representation will be used according to the MIME type asked
@mimerender(
    default = 'txt',
    html = lambda **args: html_repr(args),
    json = lambda **args: json_repr(args),
    txt  = lambda **args: txt_repr(args)
)
# Method that gets the ressource 
def book_ressource(isbn):
	dumpHeaders()
	book={'isbn':isbn}
	book.update(mydata[isbn])
	return book

# log the headers
def dumpHeaders():
	print('---- HEADERS ----')
	for k in request.headers.keys():
		print("%15s : %s"%(k, request.headers.get(k)))
	print('\n')


@error(404)
@error(500)
def notFound(code):
	return "ISBN Not Found"

# MAIN : start a local http server
run(host='localhost', port=8080)
