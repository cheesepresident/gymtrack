from flask_login import current_user, UserMixin
import sirope
import werkzeug.security as safe
from datetime import datetime

monthsdict = {	'01':'January',
		'02':'February',
		'03':'March',
		'04':'April',
		'05':'May',
		'06':'June',
		'07':'July',
		'08':'August',
		'09':'September',
		'10':'October',
		'11':'November',
		'12':'December'		}

class User(UserMixin):
    def __init__(self, username, password):
        self._username = username
        self._password = safe.generate_password_hash(password)

    @property
    def username(self):
        return self._username
    
    def get_id(self):
        return self._username
    
    
    def chk_password(self, pswd):
        return safe.check_password_hash(self._password, pswd)
    
    @staticmethod
    def find(s: sirope.Sirope, username: str) -> "User":
        return s.find_first(User, lambda u: u.username == username)
    
class Workout():
    def __init__(self, exercise, amount=None, unit=None, weight=None, notes=None):
        self._user = current_user.get_id()
        self._exercise = exercise
        self._amount = amount
        self._unit = unit
        self._weight = weight
        self._notes = notes
        date = datetime.now() 
        self._year = date.year
        self._month = monthsdict[f"{date.month:02d}"]
        self._day = date.day

    @property
    def username(self):
        return getattr(self, "_user", None)
    @property
    def exercise(self):
        return self._exercise
    @property
    def amount(self):
        return getattr(self, "_amount", None)
    @property
    def unit(self):
        return getattr(self, "_unit", None)
    @property
    def weight(self):
        return getattr(self, "_weight", None)
    @property
    def notes(self):
        return getattr(self, "_notes", None)
    @property
    def year(self):
        return self._year
    @property
    def month(self):
        return self._month
    @property
    def day(self):
        return self._day
    