import sys
sys.path.append("../util/*")
sys.path.append("../db/*")
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql


class Caregiver:
    def __init__(self, username, password=None, salt=None, hash=None):
        self.username = username
        self.password = password
        self.salt = salt
        self.hash = hash

    # getters
    def get(self):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor(as_dict=True)

        get_caregiver_details = "SELECT Salt, Hash FROM Caregivers WHERE Username = %s"
        try:
            cursor.execute(get_caregiver_details, self.username)
            for row in cursor:
                curr_salt = row['Salt']
                curr_hash = row['Hash']
                calculated_hash = Util.generate_hash(self.password, curr_salt)
                if not curr_hash == calculated_hash:
                    # print("Incorrect password")
                    cm.close_connection()
                    return None
                else:
                    self.salt = curr_salt
                    self.hash = calculated_hash
                    cm.close_connection()
                    return self
        except pymssql.Error as e:
            raise e
        finally:
            cm.close_connection()
        return None

    def get_username(self):
        return self.username

    def get_salt(self):
        return self.salt

    def get_hash(self):
        return self.hash

    def save_to_db(self):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        add_caregivers = "INSERT INTO Caregivers VALUES (%s, %s, %s)"
        try:
            cursor.execute(add_caregivers, (self.username, self.salt, self.hash))
            # you must call commit() to persist your data if you don't set autocommit to True
            conn.commit()
        except pymssql.Error:
            raise
        finally:
            cm.close_connection()

    # Insert availability with parameter date d
    def upload_availability(self, d):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        add_availability = "INSERT INTO Availabilities VALUES (%s , %s, 0)"
        try:
            cursor.execute(add_availability, (d, self.username))
            # you must call commit() to persist your data if you don't set autocommit to True
            conn.commit()
        except pymssql.Error:
            print("Error occurred when updating caregiver availability")
            raise
        finally:
            cm.close_connection()

    def get_availability(self, d):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()
        get_availability = "SELECT A.Username, V.Name, V.Doses FROM Availabilities A, Vaccines V WHERE A.Time = %s AND A.booked != 1 ORDER BY A.Username"
        try:
            cursor.execute(get_availability, (d))
            print("Caregiver | Vaccine | Doses")     
            print("-------------------------------------") 
            for row in cursor:
                print(row[0], row[1], row[2])
        except pymssql.Error:
            print("Error occured when obtaining caregiver availabilities")
            raise
        finally:
            cm.close_connection()
    
    def get_appointments(self, d):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        get_appointments = "SELECT A.AppointmentID, Vaccine, Time, Patient FROM Appointments A WHERE Caregiver = %s ORDER BY AppointmentID"
        try:
            cursor.execute(get_appointments, (d))
            print("AppointmentID | Vaccine | Date | Patient")     
            print("-------------------------------------")
            for row in cursor:
                print(row[0], row[1], row[2], row[3]) 
        except pymssql.Error:
            print("Error occured when obtaining Caregiver Appointments")
            raise
        finally:
            cm.close_connection()

    def cancel_appointment(self, id):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()
        cursor2 = conn.cursor()
        cursor3 = conn.cursor()
        cursor4 = conn.cursor()
        cancel_appointment = "SELECT * FROM Appointments A WHERE AppointmentID = %s"
        update1 = "UPDATE Vaccines SET Doses = Doses+1 WHERE Name = %s"
        update2 = "UPDATE Availabilities SET booked = 0 WHERE Time = %s AND Username = %s"
        update3 = "DELETE FROM Appointments WHERE AppointmentID = %s"
        try:
            cursor.execute(cancel_appointment, (id))
            vaccine = None
            date = None
            Caregiver = None
            for row in cursor:
                if row[0] is None:
                    print("This appointment does not exist! Cannot cancel appointment.")
                vaccine = row[1]
                date = row[2]
                Caregiver = row[3]
            cursor2.execute(update1, (vaccine))
            cursor3.execute(update2, (date, Caregiver))
            cursor4.execute(update3, (id))
            conn.commit()
        except pymssql.Error:
            print("Error occured when cancelling appointment")
            raise
        finally:
            cm.close_connection()