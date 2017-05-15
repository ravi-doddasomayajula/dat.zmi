#!/usr/bin/env python

import cgi,os
import cgitb

pth = "/home/jcebral/public_html/zmi"

#enable cgi debugging
cgitb.enable()

#create instance of FieldStorage 
form = cgi.FieldStorage()

#set user
if "REMOTE_USER" in os.environ:
  user=os.environ["REMOTE_USER"]
else:
  user="anon"

#save voting for this pair
sel = False
but = form.getvalue('select')
if but=='left': sel=1
if but=='right': sel=2
if sel:
  aid,a1,a2=form.getvalue("args").split(",")
  f = open("{:s}/votes_{:s}.csv".format(pth,user),"a")
  f.write("{:s},{:s},{:s},{:d}\n".format(aid,a1,a2,sel))

#read votes
ldone = []
try:
  f = open("{:s}/votes_{:s}.csv".format(pth,user),"r")
except:
  pass
else:
  for line in f:
    lid,a1,a2,r = line.strip().split(",")
    ldone += [lid]
ldone = set(ldone)

#find next
f = open("{:s}/pairs.csv".format(pth),"r")
for line in f.readlines()[1:]:
  aid,a1,a2 = line.strip().split(",")
  if aid not in ldone: break
  aid = None

if not aid:
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


#gather images of next pair
i1 = "https://cfd.gmu.edu/~jcebral/zmi/gifs/{0:s}.gif".format(a1)
i2 = "https://cfd.gmu.edu/~jcebral/zmi/gifs/{0:s}.gif".format(a2)

#generate form
print "Content-Type: text/html"
print
print "<!DOCTYPE html>"
print "<html>"
print "<head>"
print "<title>Shape Compare</title>"
print "</head>"
print "<body>"
print "<h2>Pair {}: select most complex shape</h2><br>".format(aid)
print "<form enctype=\"multipart/form-data\" action='shape_compare.cgi' method=\"post\">"
print "<table><tr>"
print "<td><image src=\"{}\" height=\"400\"></td>".format(i1)
print "<td><image src=\"{}\" height=\"400\"></td>".format(i2)
print "</tr>"
print "<td align=\"middle\"><input name=\"select\" type=\"submit\" value=\"left\"></td>"
print "<td align=\"middle\"><input name=\"select\" type=\"submit\" value=\"right\"></td>"
print "</tr></table>"
print "<input name=\"args\" type=\"hidden\" value=\"{:s},{:s},{:s}\">".format(aid,a1,a2)
print "</body>"
print "</html>"
