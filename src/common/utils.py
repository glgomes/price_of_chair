from passlib.hash import pbkdf2_sha512
import re

__author__ = 'glgs'

class Utils(object):

    @staticmethod
    def hash_password(password):
        """
        Hashes password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks if the sent password matches that of the database.
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if they matche, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def email_is_valid(email):
        if len(email) < 5 or len(email) > 254:
            return False

        expression = "^[\w,_,-,\.]*@[\w,\.]+(\w)+$"
        if re.compile(expression).match(email) is not None:
            if ".." not in email:
                return True

        return False


