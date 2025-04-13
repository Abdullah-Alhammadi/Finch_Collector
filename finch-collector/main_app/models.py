from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)


class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('toy-detail', kwargs={'pk': self.id})


class Finch(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # Use the 'reverse' function to dynamically find the URL for viewing this cat's details
        return reverse('finch-detail', kwargs={'finch_id': self.id})
            

class Feeding(models.Model):
    date = models.DateField('Feeding date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
    )
    finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"

    class Meta:
        ordering = ['-date']  


class Photo(models.Model):
    url = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    # this will add a property with the date when created
    created_at = models.DateField(auto_now_add=True) 
    # below will add an update property that will update the date each time the object is updated.
    updated_at = models.DateField(auto_now=True)
    # like the feeding model - we will delete any related images if a Cat is deleted
    finch = models.OneToOneField(Finch, on_delete=models.CASCADE)


    def __str__(self):
        return f"Photo for finch_id: {self.finch.id} @{self.url}"