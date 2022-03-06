from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    student_number = models.CharField(max_length=15, null=True)
    name = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.email


class Room(models.Model):
    name = models.CharField('空間名稱', max_length=10)
    location = models.CharField(max_length=30, null=True)
    # image = models.ImageField(null=True)
    contain_num = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    url = models.URLField()
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class BorrowTime(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(blank=True)
    borrower = models.ForeignKey(Profile, on_delete=models.CASCADE)
    borrow_reason = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.room.name
