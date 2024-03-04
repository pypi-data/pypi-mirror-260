from database_mysql_local.point import Point


# TOOO Person -> PersonLocal
class Person:
    "person details class"
    # TODO: is there a way to give a default values for Point?
    # Point(None, None) is not working
    # TODO We prefer not to use Point(0,0) and use NULL in the database
    def __init__(self, number: int = None, last_coordinate: Point = Point(0, 0),
                 birthday_date: str = None, day: int = None,
                 month: int = None, year: int = None, first_name: str = None,
                 last_name: str = None, location_id: int = None,
                 nickname: str = None, gender_id: int = None,
                 father_name: str = None, main_email_address: str = None,
                 birthday_original: str = None, is_approved: bool = False,
                 is_identity_confirmed: bool = False, birthday_timestamp: str = None,
                 year_cira: int = None, first_name_approved: bool = False,
                 last_name_approved: bool = False, nickname_approved: bool = False,
                 last_location_id: int = None, is_rip: bool = False, is_test_data: bool = False) -> None:
        self.number = number
        self.gender_id = gender_id
        self.last_coordinate = last_coordinate
        self.location_id = location_id
        self.birthday_date = birthday_date
        self.day = day
        self.month = month
        self.year = year
        self.first_name = first_name
        self.last_name = last_name
        self.nickname = nickname
        self.father_name = father_name
        self.main_email_address = main_email_address
        self.birthday_original = birthday_original
        self.is_approved = is_approved
        self.is_identity_confirmed = is_identity_confirmed
        self.birthday_timestamp = birthday_timestamp
        self.year_cira = year_cira
        self.first_name_approved = first_name_approved
        self.last_name_approved = last_name_approved
        self.nickname_approved = nickname_approved
        self.last_location_id = last_location_id
        self.is_rip = is_rip
        self.is_test_data = is_test_data
