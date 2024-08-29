from .models import Reviews, Freelancers, Users
from .serializer import ReviewsSearializer, FreelancersSearializer, UsersSearializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# create views for CRUD operations and logic for backend
# the name of each function will be specfied with a url path in urls.py 

@api_view(['GET', 'POST']) # retrieve all the reviews and post a review 
def review_list(request): 
  if request.method == 'GET':
    # need to handle pagination to display reviews 
    # front end will send the paramater of how many items per page and what page the user is on
    # store those query params as values to send back the right selection of reveiws from the database. 
    page = request.query_params.get('page', 1)
    per_page = request.query_params.get('perPage', 10)

    # create a reviews object that will have all the database entries in it 
    reviews = Reviews.objects.all()
    # organize the reviews by date so it looks normal for users. 
    reviews = reviews.order_by('-date')
    
    # this is a django paginator, it takes all the reviews (data), and te amount of reviews to display.
    paginator = Paginator(reviews, per_page)

    # create variable reviews_page which will store the exact reviews to be displayed based on the page we are on. 
    try:
        reviews_page = paginator.page(page)
    except PageNotAnInteger:
        # go back to page 1 if a wrong page is input 
        reviews_page = paginator.page(1)
    except EmptyPage:
        # if there is no page, go to the last page. 
        reviews_page = paginator.page(paginator.num_pages)

    # Serialize the reviews on the current page
    serializer = ReviewsSearializer(reviews_page, many=True)

    # Return the paginated response. The data includes the specific range of reviews from the database we wanted plus data that will be used for the paginator component in the front end. 
    return Response({
        'reviews': serializer.data,
        'total': paginator.count,
        'page': reviews_page.number,
        'perPage': per_page,
        'totalPages': paginator.num_pages,
    }, status=status.HTTP_200_OK)

  # if a post request is sent to this api, then serialize the data and then store it in the database. Serializer will take care of processing data to ensure correctness before adding it to the database. 
  elif request.method == 'POST':
    serializer = ReviewsSearializer(data=request.data) # take the request data, and pass it into the serailzer
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status = status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST) # error if incorrect data sent 
    
@api_view(['GET', 'PUT', 'DELETE']) # retrieve 1 review, update it, and delete it 
def review_details(request, id):
  try:
    review = Reviews.objects.get(pk=id) # find the correct review if it exists
  except Reviews.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  if request.method == 'GET':
    serializer = ReviewsSearializer(review) # serialize that review
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = ReviewsSearializer(review, data=request.data)
    if serializer.is_valid():
      serializer.save() # save the updated review if it is in a valid format
      return Response(serializer.data, status = status.HTTP_201_CREATED)
    else:
       return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST) # error if incorrect data sent 
  elif request.method == 'DELETE':
    review.delete()
    return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST']) # get all the freelancers and create freelancers
def freelancer_list(request):
  if request.method == 'GET':
    freelancers = Freelancers.objects.all()
    serializer = FreelancersSearializer(freelancers, many=True)
    return Response(serializer.data)
  if request.method == 'POST':
    serializer = FreelancersSearializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status = status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE']) # get, update, and delete a specific freelancer
def freelancer_details(request, id):
  try:
    freelancer = Freelancers.objects.get(pk=id)
  except Freelancers.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  if request.method == 'GET':
    serializer = FreelancersSearializer(freelancer)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = FreelancersSearializer(freelancer, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status= status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    freelancer.delete()
    return Response(status = status.HTTP_204_NO_CONTENT)
  
@api_view(['GET', 'POST']) # get and create a user
def user_list(request):
  if request.method == 'GET':
    users = Users.objects.all()
    serializer = UsersSearializer(users, many=True)
    return Response(serializer.data)
  elif request.method == 'POST':
    serializer = UsersSearializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
@api_view(['GET', 'PUT', 'DELETE']) # get, update and delete a specific user
def user_details(request, id):
  try:
    user = Users.objects.get(pk=id)
  except Users.DoesNotExist:
    return Response(status=status.HTTP_400_BAD_REQUEST)
  if request.method == 'GET':
    serializer = UsersSearializer(user)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = UsersSearializer(user, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET']) # get all the reviews for a specific freelancer 
def freelancer_reviews(request, id):
  try: # check if freelancer exists
    freelancer = Freelancers.objects.get(pk=id) 
  except Freelancers.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  reviews_of_freelancer = Reviews.objects.filter(freelancer=id)
  reviews_of_freelancer = reviews_of_freelancer.order_by('-date') # give the reviews back with the newest first. 
  serializer = ReviewsSearializer(reviews_of_freelancer, many=True)
  return Response(serializer.data)

@api_view(['GET']) # get all the reviews for a specific freelancer 
def user_reviews(request, id):
  try: # check if freelancer exists
    user = Users.objects.get(pk=id) 
  except Users.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  reviews_of_user = Reviews.objects.filter(user=id)
  reviews_of_user = reviews_of_user.order_by('-date') # give the reviews back with the newest first. 
  serializer = ReviewsSearializer(reviews_of_user, many=True)
  return Response(serializer.data)


@api_view(['GET']) # end point for sorting and filtering reviews
def sort_and_filter_reviews(request):
  if request.method == 'GET':
    # Because sorted and filtered reviews are its own path, need to again set up pagination so reviews are displayed in the exact same way non sorted/filtered reviews are. 
    page = request.query_params.get('page', 1)
    per_page = request.query_params.get('perPage', 10)

    reviews = Reviews.objects.all()

    paginator = Paginator(reviews, per_page)

    try:
        reviews_page = paginator.page(page)
    except PageNotAnInteger:
        reviews_page = paginator.page(1)
    except EmptyPage:
        reviews_page = paginator.page(paginator.num_pages)

    reviews = Reviews.objects.all()

    # Apply query paramters
    freelancer_id_param = request.GET.get('freelancer', None)

    # if the query paramater exists, filter by the query paramater
    if freelancer_id_param:
      reviews = reviews.filter(freelancer=freelancer_id_param)
    
   # Apply sorting based on sort_by
    sort_by = request.GET.getlist('sort_by', None)
    if sort_by:
        sort_fields = []
        if 'rating_high_to_low' in sort_by:
            sort_fields.append('-rating')
        elif 'rating_low_to_high' in sort_by:
            sort_fields.append('rating')
        if 'date_newest_first' in sort_by:
            sort_fields.append('-date')
        elif 'date_oldest_first' in sort_by:
            sort_fields.append('date')

        # Apply the sorting based on the accumulated sort fields
        if sort_fields:
            reviews = reviews.order_by(*sort_fields)

    # send the filtered reviews 
    serializer = ReviewsSearializer(reviews, many=True)
    return  Response({
        'reviews': serializer.data,
        'total': paginator.count,
        'page': reviews_page.number,
        'perPage': per_page,
        'totalPages': paginator.num_pages,
    }, status=status.HTTP_200_OK)
