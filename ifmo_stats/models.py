from django.db import models


class Grading(models.Model):
    course_id = models.CharField(max_length=255)
    problem_number = models.IntegerField()
    deadline = models.DateField(null=True)
    min_grade = models.FloatField(null=True)