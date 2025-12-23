from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

# Define models for each collection
class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=50)
    class Meta:
        app_label = 'octofit_tracker'
        db_table = 'users'

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        app_label = 'octofit_tracker'
        db_table = 'teams'

class Activity(models.Model):
    user_email = models.EmailField()
    activity_type = models.CharField(max_length=50)
    duration = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'
        db_table = 'activities'

class Leaderboard(models.Model):
    user_email = models.EmailField()
    points = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'
        db_table = 'leaderboard'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    class Meta:
        app_label = 'octofit_tracker'
        db_table = 'workouts'

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB directly for index creation
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()
        db.users.create_index('email', unique=True)

        # Teams
        marvel = {'name': 'Marvel'}
        dc = {'name': 'DC'}
        db.teams.insert_many([marvel, dc])

        # Users
        users = [
            {'email': 'ironman@marvel.com', 'name': 'Iron Man', 'team': 'Marvel'},
            {'email': 'captainamerica@marvel.com', 'name': 'Captain America', 'team': 'Marvel'},
            {'email': 'batman@dc.com', 'name': 'Batman', 'team': 'DC'},
            {'email': 'superman@dc.com', 'name': 'Superman', 'team': 'DC'},
        ]
        db.users.insert_many(users)

        # Activities
        activities = [
            {'user_email': 'ironman@marvel.com', 'activity_type': 'Running', 'duration': 30},
            {'user_email': 'captainamerica@marvel.com', 'activity_type': 'Cycling', 'duration': 45},
            {'user_email': 'batman@dc.com', 'activity_type': 'Swimming', 'duration': 60},
            {'user_email': 'superman@dc.com', 'activity_type': 'Flying', 'duration': 120},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'user_email': 'ironman@marvel.com', 'points': 100},
            {'user_email': 'captainamerica@marvel.com', 'points': 90},
            {'user_email': 'batman@dc.com', 'points': 110},
            {'user_email': 'superman@dc.com', 'points': 120},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'name': 'Super Strength', 'description': 'Lift heavy objects'},
            {'name': 'Flight Training', 'description': 'Practice flying'},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
