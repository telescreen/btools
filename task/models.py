from rest_framework import serializers
from django.db import models


class Project(models.Model):
    PLANNING = 1
    ON_GOING = 2
    FINISHED = 3

    STATUS = (
        (PLANNING, 'Planning'),
        (ON_GOING, 'On Going'),
        (FINISHED, 'Finished')
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.IntegerField(choices=STATUS, default=PLANNING)
    session_time = models.IntegerField(default=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    NEW = 1
    DOING = 2
    DONE = 3

    STATUS = (
        (NEW, 'New'),
        (DOING, 'Doing'),
        (DONE, 'Done')
    )

    LOW = 1
    MIDDLE = 2
    HIGH = 3

    PRIORITY = (
        (LOW, 'Low'),
        (MIDDLE, 'Middle'),
        (HIGH, 'High')
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    status = models.IntegerField(choices=STATUS, default=NEW)
    estimated_time = models.IntegerField(blank=True)
    total_time = models.IntegerField(blank=True)
    priority = models.IntegerField(choices=PRIORITY, default=MIDDLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Checklist(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
