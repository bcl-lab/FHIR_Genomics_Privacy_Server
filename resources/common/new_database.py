import json
import mymerge as merge
import psycopg2
import psycopg2.extras
import bcrypt
from config_db import dbuser, dbname

# TO DO: extend the policy_data to a more appropriate structure

ok                  =  1
type_error          = -1
already_existed     =  0
not_existed         = -2

db = "dbname=%s user=%s" % (dbname, dbuser)

INSERT_PRIVACY = "INSERT INTO privacy (patient_id, policy, last_modified) VALUES (%s, %s, %s)"
DELETE_PRIVACY = "DELETE FROM privacy WHERE patient_id = %s"
SELECT_PRIVACY = "SELECT * FROM privacy WHERE patient_id = %s"
UPDATE_PRIVACY = "UPDATE privacy set policy=%s, last_modified=%s WHERE patient_id=%s"

INSERT_USER = "INSERT INTO user (user_id, password, email) VALUES (%s, %s, %s)"
DELETE_USER = "DELETE FROM user WHERE user_id = %s"
SELECT_USER = "SELECT * FROM user WHERE user_id = %s"

def search_policy(patient_id):
    """
    This function search for the record of the given patient.
    :param patient_id:  the patient's id
    :return:            return 'ok'             : the record exists
                        return 'not_existed'    : the record doesn't exist
    """
    conn = psycopg2.connect(db)

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        with curs:
            curs.execute(SELECT_PRIVACY, (patient_id,))
            result = curs.fetchone()

    if result is not None:
        return ok
    else:
        return not_existed


def insert_policy(patient_id, policy, time):
    """
    :param patient_id:  patient id that identifies the patient
    :param policy:      patient's privacy policy
    :param time:        time that the policy is inserted
    :return:            return 'ok'                 : inserted successfully
                        return 'already_existed'    : the patient's policy already exists
                        return 'type_error'         : the type of parameter is wrong
    """
    conn = psycopg2.connect(db)

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        with curs:
            curs.execute(SELECT_PRIVACY, (patient_id,))
            result = curs.fetchone()

    if result is None:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            with curs:
                if type(policy) in [dict, list]:
                    dumped_policy = json.dumps(policy, sort_keys=True)
                elif type(policy) is str:
                    dumped_policy = json.dumps(json.loads(policy))
                else:
                    conn.close()
                    return type_error
                curs.execute(INSERT_PRIVACY, (patient_id, dumped_policy, time))
    else:
        return already_existed

    conn.commit()
    conn.close()
    return ok


def delete_policy(patient_id):
    """
    :delete the record of the patient identified by the given id

    :param patient_id: the patient's id whose record will be deleted
    """
    conn = psycopg2.connect(db)

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        with curs:
            curs.execute(DELETE_PRIVACY, (patient_id,))

    conn.commit()
    conn.close()


def merge_policy(patient_id, added_policy, time):
    """
    This function add added_policy into a patient existing privacy policy.
    If the patient is not in the database, then create a new record with added_policy.
    :param patient_id:      the patient id
    :param added_policy:    the additional privacy policy that will be added
    :param time:            the time that the record is modified
    :return:                return 'ok'         : policy added successfully
                            return 'type_error' : type of added_policy is incorrect
    """

    if type(added_policy) is str:
        added_policy = json.loads(added_policy)
    elif type(added_policy) not in [list, dict]:
        return type_error

    conn = psycopg2.connect(db)

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        with curs:
            curs.execute(SELECT_PRIVACY, (patient_id,))
            result = curs.fetchone()
    if result is not None:
        merged_policy = merge.merger(result[1], added_policy)

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            with curs:
                curs.execute(UPDATE_PRIVACY, (json.dumps(merged_policy), time, patient_id))
    else:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            with curs:
                curs.execute(INSERT_PRIVACY, (patient_id, added_policy, time))

    conn.commit()
    conn.close()
    return ok


def select_policy(patient_id):
    """
    This function select the record of the assumed patient and return the patient's privacy record
    :param patient_id:  the patient id
    :return:            return the privacy policy if select successfully
                        return 'not_existed' if the patient is not in the database
    """
    conn = psycopg2.connect(db)

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        with curs:
            curs.execute(SELECT_PRIVACY, (patient_id,))
            result = curs.fetchone()

    if result is not None:
        return result[1]
    else:
        return not_existed


def add_user(user_id, password, email=""):
    """
    Function Description:
        add_user(user_id, password, email) add a new user in the db user.
        add_user will first examine whether the user already existed.
        If existed, return "User Already Existed".
        If not, return "OK".
    Parameters:
        user_id   : the identifier of users.
        password  : the plain text form of the password
        email     : the user's email
    """
    conn = psycopg2.connect(db)

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        with curs:
            curs.execute(SELECT_USER, (user_id,))
            result = curs.fetchone()

    if result is not None:
        return "User Already Existed"
    else:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            with curs:
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
                curs.execute(INSERT_USER, (user_id, hashed_password, email,))

    conn.commit()
    conn.close()
    return "OK"


def select_user(user_id):
    """
    Function Description:
        select_user_by_id(user_id) selects the user's record in user table
        with the given user_id. This method returns exactly what the selection
        operation returns.
    Parameters:
        user_id           : the identifier of users.
        entered_password  : the plain text form of the password
    """
    conn = psycopg2.connect(db)

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        with curs:
            curs.execute(SELECT_USER, (user_id,))
            result = curs.fetchone()

    conn.close()
    return result


def verify(user_id, entered_password):
    """
    Function Description:
        verify_by_id(user_id, entered_password) verifies a user's sign in
        request.
        If the user is not in the db, return "User Not Found".
        If match, return "Matched", else "Not Matched".
    Parameters:
        user_id           : the identifier of users.
        entered_password  : the plain text form of the password
    """
    select_result = select_user_by_id(user_id)
    if result is None:
        return "User Not Found"
    else:
        hashed_password = result[1]
        if bcrypt.hashpw(entered_password, hashed_password) == hashed_password:
            return "Matched"
        else:
            return "Not Matched"