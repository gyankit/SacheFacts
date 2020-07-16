from App import db
from App.models import AccountSetting

account = AccountSetting(
    id=1, 
    site_title = 'Sache Fact', 
    site_logo = 'site/logo.jpg', 
    site_poster = 'site/poster.jpg', 
    admin_firstname = 'Himashu', 
    admin_lastname = 'Kumar', 
    admin_displayname = 'Himashu Kumar', 
    admin_contact = '+91 8002220258', 
    admin_email = 'sachefacts1526@gmail.com', 
    admin_address = '', 
    admin_photo = 'site/admin.jpg'
    )

print(account)
db.session.add(account)
#db.session.commit()