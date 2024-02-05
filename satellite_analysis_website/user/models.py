from django.db import models


class User(models.Model):
    """
        This class represents an User. \n
        Attributes:
        -----------
        param username: Username of the user
        type username: str max_length=20
        param password: Password of the user
        type password: str
    """
    id = models.AutoField(primary_key=True)
    username = models.CharField(blank=True, max_length=20)
    password = models.CharField(default=None, max_length=255)

    @staticmethod
    def get_by_id(user_id):
        """
        :param user_id: SERIAL: the id of a user to be found in the DB
        :return: user object or None if a user with such ID does not exist
        """
        custom_user = User.objects.filter(id=user_id).first()
        return custom_user if custom_user else None

    @staticmethod
    def create_user(username, password):
        new_user = User(username=username, password=password)
        new_user.save()
        return new_user
