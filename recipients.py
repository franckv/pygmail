def recipient_id(db, display, mail):
    cur = db.cursor()
    cur.execute('SELECT id from recipient WHERE email=?', (mail,))
    row = cur.fetchone()
    if not row:
	cur.execute('INSERT INTO recipient (display, email) VALUES (?, ?);',
		(display.encode('utf8'), mail.encode('utf8')))
	id = db.insert_id()
    else:
	id = row[0]
    cur.close()
    return id

def get_display_name(db, id):
    cur = db.cursor()
    cur.execute('SELECT display, email from recipient WHERE id=%i' % id)
    row = cur.fetchone()
    cur.close()
    if not row:
	return None
    else:
	if row[0] == '':
	    return row[1]
	else:
	    return row[0]


