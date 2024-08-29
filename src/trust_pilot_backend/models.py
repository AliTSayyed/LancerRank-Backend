from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# create models

# freelancer table will keep track of all the freelancer's unique ids and their names. No name can be repeated twice so that each freelancer is unique. 
# important that freelancers are distingusihable since users do not want to accidently look at the reviews of a different freelancer that has the same name. 
class Freelancers(models.Model):
  freelancer_name = models.CharField(max_length=120, unique=True, default='')

# users table is the same. Keeps track of all the users' unique id's and their names. No name can be repeated twice so that each user is unique. 
# for the same reason, a random user should not mistake 2 differnet users's reviews (with the same name) as the same person.
class Users(models.Model):
   user_name = models.CharField(max_length=70, unique=True, default='')
 
# The reviews table will contain the id of users and freelancers along with a rating, date, and the review itself. The rating can only be an integer 1-5 no other values allowed. 
# Use a forign key to refrence a freelancer or user from their respective tables. 
class Reviews(models.Model):
  user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='reviews')
  rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
  review_text = models.TextField(blank=False, null=False)
  date = models.DateTimeField(auto_now_add=True)
  freelancer = models.ForeignKey(Freelancers, on_delete=models.CASCADE, related_name='reviews')


