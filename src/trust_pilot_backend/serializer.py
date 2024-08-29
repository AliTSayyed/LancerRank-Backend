from rest_framework import serializers
from .models import Reviews, Freelancers, Users

# create serializer of the models to process the incoming json data. 

class ReviewsSearializer(serializers.ModelSerializer):
 # These fields will accept user_name and freelancer_name in the POST request
  user_name = serializers.CharField(write_only=True) 
  freelancer_name = serializers.CharField(write_only=True)

  # These fields are only sent in a GET request. 
  user = serializers.PrimaryKeyRelatedField(read_only=True)
  freelancer = serializers.PrimaryKeyRelatedField(read_only=True) 

  class Meta:
    model = Reviews
    fields = ['id', 'user', 'freelancer', 'rating', 'review_text', 'date', 'user_name', 'freelancer_name'] # even though the Review model does not have a user_name or freelancer_name, these fields must be included for POST and PUT requests.

  # Must edit the Post data to exclude the user and freelancer fields but obtain the id's of those users from the user's and freelancer's table
  def validate(self, attrs):
    # get the user name and freelaner name from the incoming json 
    user_name = attrs.get("user_name")
    freelancer_name = attrs.get("freelancer_name")
    if not user_name or not freelancer_name:
        raise serializers.ValidationError("user_name and freelancer_name are required fields.") # in case no name was sent.  
    
    # create or get a user from the User's table by finding a mathcing name or making a new user. 
    user, created = Users.objects.get_or_create(user_name=user_name) 
    freelancer, created = Freelancers.objects.get_or_create(freelancer_name=freelancer_name)
    # add the username/freelancername to the data under their respective feilds. Do not need to send the id, Django will take care of that. 
    attrs['user'] = user
    attrs['freelancer'] = freelancer
    
    # update the post data to now include a user and freelancer object (name and id), not just a name. 
    return super().validate(attrs) 
  
  # After modifying the post data, return the correct fields to the serializer. Now usernames and freelancer names have been corretly converted to their respective ids. Ensures unique users and freelancers. 
  def create(self, validated_data):
    # remove the user_name and freelancer_name fields from the data so no error occurs. Those feilds are only allowed for write only not read only (GET)
    validated_data.pop("user_name", None)
    validated_data.pop("freelancer_name", None)
    
    # send the update data with correct user and freelancer objects.
    return Reviews.objects.create(**validated_data)

# This serializer will accept freelancer data with that only contain fields 'id' and 'freelancer_name'
class FreelancersSearializer(serializers.ModelSerializer):
  class Meta:
    model = Freelancers
    fields = ['id', 'freelancer_name']

# This serializer will accept user data with that only contain fields 'id' and 'user_name'
class UsersSearializer(serializers.ModelSerializer):
  class Meta:
    model = Users
    fields = ['id', 'user_name']
 
