from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    credit = models.CharField(max_length=100)
    price = models.BigIntegerField()
    summary = models.TextField()
    contents = models.TextField()
    link = models.URLField()
    site = models.CharField(max_length=100)
    img_idx = models.BigIntegerField()

    def __str__(self):
        return self.title


class CourseReview(models.Model):
    # owner = models.ManyToManyField(User)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rate = models.FloatField(validators=[MinValueValidator(0.5), MaxValueValidator(5)])
    comment = models.TextField()
