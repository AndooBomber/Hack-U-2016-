import cgi
form = cgi.FieldStorage()

print("Content-type: text/html\n")
print("<html><body>"
      "<h1>Computer Network</h1>")
print("Hello")
print(", ", form["first"].value)
print(" ", form["last"].value)
print("!")
print("</body></html>")
