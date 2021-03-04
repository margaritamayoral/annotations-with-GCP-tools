#!/usr/bin/env python
# coding: utf-8

# In[1]:


APIKEY = "<<yourVisionAPIkey"


# In[2]:


get_ipython().system('pip install --upgrade pip')
get_ipython().system('pip install --upgrade google-api-python-client')
get_ipython().system('pip install PyDrive')


# In[4]:


from google.cloud import vision
import io
import os
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from google.cloud import storage
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import GoogleCredentials
import json
from google.cloud.vision import types
from google.protobuf.json_format import MessageToDict
from google.cloud.vision import ImageAnnotatorClient
from google.cloud import vision_v1


# In[6]:


from googleapiclient.discovery import build
import base64

## Detecting logos on just one image ###

IMAGE="gs://bucket/images/image_name1.jpg"
IMAGE2="gs://bucket/images/image_name2.jpg"
IMAGE3="gs://bucket/images/image_name3.jpg"
IMAGE4="gs://bucket/images/image_name4.jpg"
IMAGE5="gs://bucket/images/image_name5.jpg"
IMAGE6="gs://bucket/images/image_name6.jpg"
IMAGE7="gs://bucket/images/image_name7.jpg"
vservice = build('vision', 'v1', developerKey=APIKEY)
request = vservice.images().annotate(body={
    'requests': [{
       'image': {
          'source': {
              'imageUri': IMAGE7
          }
      },
      'features': [{
          'type': 'LOGO_DETECTION',
          'maxResults': 10
        },
      ]
     }],
  })
responses = request.execute(num_retries=1)
print('logo:', responses['responses'][0])


# In[ ]:




IMAGE7="gs://bucket/images/image_name7.jpg"
APIKEY = "<<yourVisionAPIkey"
output_dir='gs://bucket/output-dir/image_results'


def sample_async_batch_annotate_images_2(
    input_image_uri=IMAGE7,
    output_uri=output_dir,
):
    """Perform async batch image annotation. Here just one image is annotated and the output stored in gcs"""
    client = vision_v1.ImageAnnotatorClient()

    source = {"image_uri": input_image_uri}
    image = {"source": source}
    features = [
        {'type': 'LOGO_DETECTION'},
        {'type': 'LABEL_DETECTION'},
    ]

    # Each requests element corresponds to a single image.  To annotate more
    # images, create a request element for each image and add it to
    # the array of requests
    requests = [{"image": image, "features": features}]
    gcs_destination = {"uri": output_uri}

    # The max number of responses to output in each JSON file
    batch_size = 2
    output_config = {"gcs_destination": gcs_destination,
                     "batch_size": batch_size}

    operation = client.async_batch_annotate_images(requests=requests, output_config=output_config)

    print("Waiting for operation to complete...")
    response = operation.result(90)

    # The output is written to GCS with the provided output_uri as prefix
    gcs_output_uri = response.output_config.gcs_destination.uri
    print("Output written to GCS with prefix: {}".format(gcs_output_uri))


# In[ ]:


sample_async_batch_annotate_images_2() ## Sending just one image to annotate


# In[ ]:



IMAGE7="gs://bucket/images/image_name7.jpg"
APIKEY = "<<yourVisionAPIkey"
output_dir='gs://bucket/output-dir/image_results'


def sample_async_batch_annotate_images_3(
    input_image_uri,
    output_uri=output_dir,
):
    """Perform async batch image annotation. Taking more images and sending the result to store to gcs"""
    client = vision_v1.ImageAnnotatorClient()

    source = {"image_uri": input_image_uri}
    image = {"source": source}
    features = [
        {'type': 'LOGO_DETECTION'},
     #   {'type': 'LABEL_DETECTION'},
    ]

    # Each requests element corresponds to a single image.  To annotate more
    # images, create a request element for each image and add it to
    # the array of requests
    requests = [{"image": image, "features": features}]
    gcs_destination = {"uri": output_uri}

    # The max number of responses to output in each JSON file
    batch_size = 2
    output_config = {"gcs_destination": gcs_destination,
                     "batch_size": batch_size}

    operation = client.async_batch_annotate_images(requests=requests, output_config=output_config)

    print("Waiting for operation to complete...")
    response = operation.result(90)

    # The output is written to GCS with the provided output_uri as prefix
    gcs_output_uri = response.output_config.gcs_destination.uri
    print("Output written to GCS with prefix: {}".format(gcs_output_uri))


# In[ ]:


## taking as input all the images in the bucket "image-cv/CFM/" to logo detection and 
## sending the results to store to "image-cv/outputCFM/"

storage_client = storage.Client()
bucket1 = storage_client.bucket("image-cv")
bucket2 = storage_client.get_bucket("image-cv")
blobs = bucket.list_blobs(prefix="CFM")
images = []

blobs = bucket.list_blobs(prefix="CFM")
print(blobs)

blob_list = list(bucket.list_blobs(prefix="CFM"))
print('Output files:')
    
for idx, bl in enumerate(blob_list):
    if idx == 0:
        continue
    print(bl.name)
    sample_async_batch_annotate_images_3("gs://bucket/" + str(bl.name),'gs://bucket/output-dir/' + str(bl.name))

