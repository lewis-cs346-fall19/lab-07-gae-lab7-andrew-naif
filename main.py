import webapp2
import passwords
import MySQLdb
import random
import cgi
class MainPage(webapp2.RequestHandler): 
    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        self.response.write("Hello worlds")
        conn = MySQLdb.connect(unix_socket = passwords.UNIX_SOCKET,
                       user = passwords.SQL_USER,
                       passwd = passwords.SQL_PASSWD,
                       db = 'gae')
        cursor = conn.cursor()
	cursor1 = conn.cursor()
        cursor2 = conn.cursor()
	cursor3 = conn.cursor()
	cursor4 = conn.cursor()
	cookie = self.request.cookies.get("cookie_name")
	id = "%032x" % random.getrandbits(128)
	self.response.write(id)
	cursor2.execute("SELECT * FROM sessions WHERE id = %s;", [id])
	cursor3.execute("SELECT * FROM sessions;")
	ses = cursor2.fetchall()	
	stuff = cursor3.fetchall()
	self.response.write(stuff)
	self.response.write(ses)
	if cookie == None:
		self.response.set_cookie("cookie_name", id, max_age=1800)
		cursor1.execute("INSERT INTO sessions (id) VALUES (%s);", [id])
	elif len(ses) ==  1:
		self.response.write("""<html><body>
		<form action="/" method="get">
  		<input type=text name=username value="">
  		<input type=submit>
		</form></body></html>""")
		try:
			form = cgi.FieldStorage()
			cursor.execute("UPDATE sessions SET username = %s WHERE id = %s;", [form["username"].value, id])
			cursor3.execute("SELECT * FROM sessions;")
			stuff = cursor3.fetchall()
		        self.response.write(stuff)
		except:
			self.response.write("No form")	
	else:
		self.response.write("""<html><body>
                <p> Increment by 1? </p>
		<form action="/" method="get">
                <input type=submit>
                </form></body></html>""")
				
	conn.commit()

app = webapp2.WSGIApplication([
    ("/", MainPage),
], debug=True)
