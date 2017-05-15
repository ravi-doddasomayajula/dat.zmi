#!/usr/bin/env python

# Import modules for CGI handling 
import cgi, os
import cgitb

pth = "/home/jcebral/public_html/zmi"

#enable cgi debugging
cgitb.enable()

# create instance of FieldStorage 
form = cgi.FieldStorage()

#set user
if "REMOTE_USER" in os.environ:
  user=os.environ["REMOTE_USER"]
else:
  user="anon"

#save voting for this pair
sel = False
but = form.getvalue('select')
if but=='simple': sel=1
if but=='complex': sel=2
if sel:
  num,aid=form.getvalue("args").split(",")
  f = open("{:s}/class_{:s}.csv".format(pth,user),"a")
  f.write("{:s},{:s},{:d}\n".format(num,aid,sel))

#read votes
ldone = []
try:
  f = open("{:s}/class_{:s}.csv".format(pth,user),"r")
except:
  pass
else:
  for line in f:
    lnu,aid,r = line.strip().split(",")
    ldone += [lnu]
ldone = set(ldone)

#find next
f = open("{:s}/idset.csv".format(pth),"r")
for line in f.readlines()[1:]:
  num,aid = line.strip().split(",")
  if num not in ldone: break
  num = None

if not num:
  print "Content-Type: text/html"
  print
  print "<!DOCTYPE html>"
  print "<html>"
  print "<head>"
  print "<title>Shape Classify</title>"
  print "</head>"
  print "<body>"
  print "<h2>DONE - THANK YOU !<br></h2>"
  print "</body>"
  print "</html>"
  exit(0)

# gather images of next pair
img = "https://cfd.gmu.edu/~jcebral/zmi/gifs/{0:s}.gif".format(aid)

# generate form
print "Content-Type: text/html"
print
print "<!DOCTYPE html>"
print "<html>"
print "<head>"
print "<title>Shape Classify</title>"
print "</head>"
print "<body>"
print "<h2>Case {}: classify shape</h2><br>".format(num)
print "<form enctype=\"multipart/form-data\" action='shape_classify.cgi' method=\"post\">"
print "<table><tr>"
print "<td colspan=\"2\"><image src=\"{}\" height=\"400\"></td>".format(img)
print "</tr>"
print "<td align=\"middle\"><input name=\"select\" type=\"submit\" value=\"simple\"></td>"
print "<td align=\"middle\"><input name=\"select\" type=\"submit\" value=\"complex\"></td>"
print "</tr></table>"
print "<input name=\"args\" type=\"hidden\" value=\"{:s},{:s}\">".format(num,aid)
print "</body>"
print "</html>"

