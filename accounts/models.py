
# Import Django's built-in AbstractUser model.
# It provides default user fields such as username, password,
# email, first name, last name, and authentication functionality.
from django.contrib.auth.models import AbstractUser

# Import Django's models module for defining database fields.
from django.db import models


# Create a custom User model that extends Django's AbstractUser.
# This allows us to keep Django's default authentication features
# while adding extra fields specific to the SchoolCore system.
class User(AbstractUser):

    # Define the roles available to users in the school management system.
    # Each tuple contains the database value and its display name.
    ROLE_CHOICES = [
        ("DIRECTOR", "Director"),
        ("HEAD", "Head Teacher"),
        ("ACCOUNTANT", "Accountant"),
        ("TEACHER", "Teacher"),
    ]

    # Store the user's role in the database.
    # max_length=20 sets the maximum number of characters allowed.
    # choices restricts the field to the roles defined above.
    # default="TEACHER" assigns the Teacher role if no role is specified.
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="TEACHER",
    )

    # Define the string representation of a user.
    # This makes the username appear when the user object is displayed
    # in places such as the Django admin panel.
    def __str__(self):
        return self.username
