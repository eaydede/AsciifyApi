# PlanetImageApi

## Design

### Requirements
The requirements that I indentified for the scope of this project are:
1. Be able to upload an image via http POST request to a /images endpoint and have it return a unique id corresponding to the uploaded image.
2. Be able to view the ascii version of images via http GET request to a /images/id endpoint where id is the id of the image that will be asciified
3. Be able to view a list of all images uploaded via http GET to an images/ endpoint

### ORM
I chose to use Django Rest Framework to build this API solely because of my familiarity with it and to save time learning new libraries or frameworks.

### Database
I chose to use a relational database for this application because of my familiarity with relational databases and the support in the future to add users to this application and the possiblility to make relational queries linking users to images.

That being said and despite my decision to use a relational database, within the scope of the application as it's stated in the provided document, I think a no-sql database would fit really well for the following reasons:
1. In the event that we don't have users and we need to make no relational queries
2. There's really only one data entity we need to keep track of in the form of images (and corresponding meta data) and we know the primary key to the image we want to access
3. Would provide better scalability if we wanted to allow for a larger number of images to be stored in the future

### Schema
I chose to use a simple ImageData model that stores a path field pointing to the actual image in an images folder as well as meta data associated to an image. This decision was made mostly due to its ease of implementation and to save time, but for the purposes of storing hundreds (upper bound 999) of photos I believe it would suffice.

### Generating Ascii image
When deciding how to implement the post endpoint I thought of two solutions:
1. Store the original image AND store the asciified version of the image. The benifit of this approach is that we wouldn't have to run the ascii generation algorithm each time a request is made, but would also have to store an additional (albeit very small) text file in addition to the original image file.

2. Generate the ascii version of the image each time a GET request is made. The benefit of this approach is lack of additional storage required to store a text file as well as the ability to change the asciify algorithm in the future. If we choose to generate the ascii image each time, we can more easily implement changes to the asciify algorithm (e.g. different character mappings, different asciified image size) in the future without having to worry about stale ascii image data.

I opted for the second approach because in my development I had a few troubles implementing the actual asciify algorithm and realized that there's not a set way to asciifyin an image. As a result I figured it would be beneficial to leave room for updating/tweaking the algorithm especially if we want to output the ascii image in different sizes.

### Known Issues

### Validation
1. Check that image file is of certain max size
2. 

## Q: What would you change or enhance for a production rollout of this service?
1. I think the addition of the concept of users would be a benificial feature. That way a user of this service would be able to more easily see all the images they have uploaded rather than either seeing a list of all images or remembering the ids of the images they've uploaded. This would also entail setting some sort of auth, something like a 3rd party OAuth2 service provider so users can sign in using existing accounts.
2. I would host this service remotely on a hosting platform (something like ec2) as well as setup a remote file storage for the images (something like S3)
3. Continuous deployment pipeline: I think an established process for deploying to different environments (i.e. dev, stage, prod) would greatly benifit development efforts in the future and would create a more maintainable codebase. 
4. I would want to implement some form of logging for easier debugging if a bug showed up after deployment and we wanted to figure out what caused it.

## Q: What would you want to monitor during that rollout?

## Q: What scaling bottlenecks would you anticipate?