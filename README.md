# ImageApi


**NOTE:** I had a lot of difficulty trying to display the ascii image correctly without characters looking skewed or wrapping to the next line, but in the end I wasn't quite able to figure it out. I believe the ascii image is still generated and can be seen if the window size shows exactly 100 characters. Just wanted to make a note of that before anything else

## Usage
I've made some minor changes to the usage of the api than what was given as example on the assignment sheet and I hope that's alright! Some of these changes include:
1. Sending an image in the body of a request with the format of form-data
2. Adding a trailing slash to each of the `image/` paths
3. Opted to use `pip` and `venv` rather than poetry to save time as I am not familiar with `poetry`

I've tried to document each of the endpoints and how they'll be used to the best of my ability, I hope this helps!

## Endpoints

## [GET] `localhost:8000/images/`

**Body**: None

**Description**:
This endpoint is used to retrieve a list of all image data entries

**Returns**:
List of `image_data` objects

**Output Format**:
```
[
    {
        "id": 1,
        "name": "Name",
        "path": "<absolute_path>/images/CA25E7.PNG",
        "desc": "desc",
        "created_at": "2022-08-02T22:17:48.329311Z"
    }
]
```

**Example cURL**: 
```
curl --location --request GET 'localhost:8000/images/'
```

## [POST] `localhost:8000/images/`

**Body**: 
Format: `form-data`

Fields:
- image: `<image file>`
- name: `<str> display name of image`  OPTIONAL
- desc: `<str> description of image`  OPTIONAL

**Description**:
This endpoint allows a user to save an image and returns an id associated with the newly saved image

**Returns**:
`<int> id associated to image being saved`

**Output Format**:
```
1
```

**Example cURL**:
```
curl --location --request POST 'localhost:8000/images/' \
--form 'image=@" <path_to_image>/<image_name>.png"' \
--form 'name="name"' \
--form 'desc="desc"'
```

## [GET] `localhost:8000/images/<int:id>/`

**Body**: None

**Description**:
This endpoint is used to retrieve the asciified version of an image with `id`

**Returns**:
Ascii text version of image

**Output Format(Only one line)**:
```
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP*********************************************PP++PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP\n ...
```

**Example cURL**:
```
curl --location --request GET 'localhost:8000/images/<int:id>'
```


## Design

### Requirements
The requirements that I indentified for the scope of this project are:
1. Be able to upload an image via http POST request to a /images endpoint and have it return a unique id corresponding to the uploaded image.
2. Be able to view the ascii version of an image via http GET request to a /images/id endpoint where id is the id of the image that will be asciified
3. Be able to view a list of all images uploaded via http GET to an images/ endpoint

### ORM
I chose to use Django Rest Framework to build this API solely because of my familiarity with it and to save time learning new libraries or frameworks.

### Database
I chose to use a relational database for this application because of my familiarity with relational databases and the support in the future to add users to this application and the possiblility to make relational queries linking users to images.

That being said and despite my decision to use a relational database, within the scope of the application as it's stated in the provided document, I think a no-sql database would fit really well for the following reasons:
1. In the event that we don't have users, we need to make no relational queries
2. There's really only one data entity we need to keep track of in the form of images (and corresponding meta data) and we know the primary key to the image we want to access
3. Would provide better scalability if we wanted to allow for a larger number of images to be stored in the future

### Schema
I chose to use a simple ImageData model that stores a path field pointing to the actual image in an images folder as well as meta data associated to an image. This decision was made mostly due to its ease of implementation and to save time, but for the purposes of storing hundreds (upper bound 999) of photos I believe it would suffice.

### Generating Ascii image
When deciding how to implement the get endpoint to retrieve an ascii image I thought of two solutions:
1. Store the original image AND store the asciified version of the image. The benifit of this approach is that we wouldn't have to run the ascii generation algorithm each time a request is made, but would also have to store an additional (albeit very small) text file in addition to the original image file.

2. Generate the ascii version of the image each time a GET request is made. The benefit of this approach is lack of additional storage required to store a text file as well as the ability to change the asciify algorithm in the future. If we choose to generate the ascii image each time, we can more easily implement changes to the asciify algorithm (e.g. different character mappings, different asciified image size) in the future without having to worry about stale ascii image data.

I opted for the second approach because in my development I had a few troubles implementing the actual asciify algorithm and realized that there's not a set way to asciify an image. As a result I figured it would be beneficial to leave room for updating/tweaking the algorithm especially if we want to output the ascii image in different sizes. If we chose to store the ascii files and changed the asciifying algorithm after the fact, then there would have to be a mass refactoring of the generated ascii files that could be a large undertaking depending on the number of files that need to be changed.

All of that being said, I think the option to generate the ascii image upon each request will work for the scope of this assignment but can potentially lead to scaling issues in the future. If we have to generate an ascii image each time a request is made, as the request load increases, this could put a strain on our service especially with many concurrent requests. For this reason, I think if we were to scale this service, we should opt to actually store the ascii images in their own files and link them to their images by adding something like a new field to the ImageData model. And in the event that the ascii algorithm needs to be changed, we can implement  versioning to keep track of which version each asciified image is at and re-asciify an image if it's not at the up to date version. 

### Changes/TODO
For the sake of time saving, a few features were omitted that I thought I would list here: 
1. When using the POST endpoint to store an image check that the image file is of certain max size to avoid storing very large image files, or at least downscaling the stored image file to a certain max size
2. Potentially add a thumbnail field to the ImageData model and when listing all images, show downscaled thumbnail of image

## Q: What would you change or enhance for a production rollout of this service?
1. I think the addition of users would be a benificial feature. That way a user of this service would be able to more easily see all the images they have uploaded rather than either seeing a list of all images or remembering the ids of the images they've uploaded. This would also entail setting some sort of auth, something like a 3rd party OAuth2 service provider so users can sign in using existing accounts.
2. I would host this service remotely on a hosting platform (something like ec2), as well as setup a remote file storage for the images (something like S3), and host the db in a similar remote service.
3. Continuous deployment pipeline: I think an established process for deploying to different environments (i.e. dev, stage, prod) would greatly benifit development efforts in the future and would create a more maintainable codebase. 
4. I would want to implement some form of logging for easier debugging if a bug showed up after deployment and we wanted to figure out what caused it.
5. I would add a performance monitoring tool for easier monitoring and metrics across all environments
6. Also I think incorporating some sort of user feedback tool such that users could make tickets with suggestions or bug reports for easier ingestion by product/development teams would be very helpful once this service is in production

## Q: What would you want to monitor during that rollout?
1. Measure the requests per minute of each endpoint to keep track of load during real use to determine if multiple instances of the service need to be deployed to improve performance
2. Measure latency of each endpoint and monitor if there are any drastic/unexpected changes with varying loads of requests
3. Check logs to monitor if any errors occur
4. Be on standby to fix any catastrophic bugs

## Q: What scaling bottlenecks would you anticipate?
With the current implementation of generating an ascii image upon each request, I can forsee a performance/latency related issue arising with an increase of users and, subsequently, request load. I touched upon the more scalable option in the the 'Generating Ascii Image' section, but essentially I believe that to implement a more scalable version of this service, we would store the generated ascii image and simply retrieve and display it when a user makes a request. This would eliminate a large amount of redundant asciify_image calls and would in theory improve latency.

Another scaling concern would possibly be the ever growing storage size of images, but I think remote file storage providers offer robust enough scaling options that it wouldn't be a major concern.
