from App import db, bcrypt
from App.models import Admin

username = 'admin'
email = 'g.gyanankit@gmail.com'
password = bcrypt.generate_password_hash(username).decode('utf-8')

admin = Admin(username=username, email=email, password=password, role='admin')

db.session.add(admin)
db.session.commit()