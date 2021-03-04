#!/usr/bin/env python
# coding: utf-8

# In[ ]:


APIKEY = '<<yourkeyforCloudVideoIntelligenceAPI>>'


# In[ ]:


get_ipython().system('pip install --upgrade pip')
get_ipython().system('pip install --upgrade google-api-python-client')
get_ipython().system('pip install PyDrive')


# In[ ]:


from google.cloud import vision
import io
import os
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from google.cloud import storage
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
#from google.colab import auth, drive
from oauth2client.client import GoogleCredentials


# In[ ]:


import json
from google.protobuf.json_format import MessageToDict
from google.cloud import storage
from google.cloud import videointelligence


# In[ ]:


APIKEY = '<<yourkeyforCloudVideoIntelligenceAPI>>'
output_dir='gs://bucket/output_dir/'
VIDEO = 'gs://bucket/videos_dir/video.mp4'

## Analizing just one video and getting the response in the consol

def detect_logo_gcs(input_uri=VIDEO):

    client = videointelligence.VideoIntelligenceServiceClient()

    features = [videointelligence.enums.Feature.LOGO_RECOGNITION]
    
    operation = client.annotate_video(features=features, input_uri=input_uri)
    
    print(u"Waiting for operation to complete...")
    response = operation.result()

    # Get the first response, since we sent only one video.
    annotation_result = response.annotation_results[0]

    # Annotations for list of logos detected, tracked and recognized in video.
    for logo_recognition_annotation in annotation_result.logo_recognition_annotations:
        entity = logo_recognition_annotation.entity

        # Opaque entity ID. Some IDs may be available in [Google Knowledge Graph
        # Search API](https://developers.google.com/knowledge-graph/).
        print(u"Entity Id : {}".format(entity.entity_id))

        print(u"Description : {}".format(entity.description))

        # All logo tracks where the recognized logo appears. Each track corresponds
        # to one logo instance appearing in consecutive frames.
        for track in logo_recognition_annotation.tracks:

            # Video segment of a track.
            print(
                u"\n\tStart Time Offset : {}.{}".format(
                    track.segment.start_time_offset.seconds,
                    track.segment.start_time_offset.nanos * 1000,
                )
            )
            print(
                u"\tEnd Time Offset : {}.{}".format(
                    track.segment.end_time_offset.seconds,
                    track.segment.end_time_offset.nanos * 1000,
                )
            )
            print(u"\tConfidence : {}".format(track.confidence))

            # The object with timestamp and attributes per frame in the track.
            for timestamped_object in track.timestamped_objects:
                # Normalized Bounding box in a frame, where the object is located.
                normalized_bounding_box = timestamped_object.normalized_bounding_box
                print(u"\n\t\tLeft : {}".format(normalized_bounding_box.left))
                print(u"\t\tTop : {}".format(normalized_bounding_box.top))
                print(u"\t\tRight : {}".format(normalized_bounding_box.right))
                print(u"\t\tBottom : {}".format(normalized_bounding_box.bottom))

                # Optional. The attributes of the object in the bounding box.
                for attribute in timestamped_object.attributes:
                    print(u"\n\t\t\tName : {}".format(attribute.name))
                    print(u"\t\t\tConfidence : {}".format(attribute.confidence))
                    print(u"\t\t\tValue : {}".format(attribute.value))

            # Optional. Attributes in the track level.
            for track_attribute in track.attributes:
                print(u"\n\t\tName : {}".format(track_attribute.name))
                print(u"\t\tConfidence : {}".format(track_attribute.confidence))
                print(u"\t\tValue : {}".format(track_attribute.value))

        # All video segments where the recognized logo appears. There might be
        # multiple instances of the same logo class appearing in one VideoSegment.
        for segment in logo_recognition_annotation.segments:
            print(
                u"\n\tStart Time Offset : {}.{}".format(
                    segment.start_time_offset.seconds,
                    segment.start_time_offset.nanos * 1000,
                )
            )
            print(
                u"\tEnd Time Offset : {}.{}".format(
                    segment.end_time_offset.seconds,
                    segment.end_time_offset.nanos * 1000,
                )
            )


# In[ ]:


## Analyzing one video and send to store the results in gcs

APIKEY = '<<yourkeyforCloudVideoIntelligenceAPI>>'
output_dir='gs://bucket/output_dir/response-multiple-video-intelligence-single-request.json'
VIDEO = 'gs://bucket/videos_dir/video.mp4'
#VIDEO = 'gs://bucket/videos_dir/*.*'


def detect_logo_gcs2(input_uri=VIDEO, output_uri=output_file):

    client = videointelligence.VideoIntelligenceServiceClient()

    features = [videointelligence.enums.Feature.LOGO_RECOGNITION]
    
    operation = client.annotate_video(features=features, input_uri=input_uri, output_uri=output_uri)
    print("\nProcessing video for object annotations.")

    print(u"Waiting for operation to complete...")
    response = operation.result()
    print("\nFinished processing.\n")

    # Get the first response, since we sent only one video.
    annotation_result = response.annotation_results[0]
    # The first result is retrieved because a single video was processed.
    #object_annotations = result.annotation_results[0].object_annotations

    # Annotations for list of logos detected, tracked and recognized in video.
    for logo_recognition_annotation in annotation_result.logo_recognition_annotations:
        entity = logo_recognition_annotation.entity

        # Opaque entity ID. Some IDs may be available in [Google Knowledge Graph
        # Search API](https://developers.google.com/knowledge-graph/).
        print(u"Entity Id : {}".format(entity.entity_id))

        print(u"Description : {}".format(entity.description))

        # All logo tracks where the recognized logo appears. Each track corresponds
        # to one logo instance appearing in consecutive frames.
        for track in logo_recognition_annotation.tracks:

            # Video segment of a track.
            print(
                u"\n\tStart Time Offset : {}.{}".format(
                    track.segment.start_time_offset.seconds,
                    track.segment.start_time_offset.nanos * 1000,
                )
            )
            print(
                u"\tEnd Time Offset : {}.{}".format(
                    track.segment.end_time_offset.seconds,
                    track.segment.end_time_offset.nanos * 1000,
                )
            )
            print(u"\tConfidence : {}".format(track.confidence))

            # The object with timestamp and attributes per frame in the track.
            for timestamped_object in track.timestamped_objects:
                # Normalized Bounding box in a frame, where the object is located.
                normalized_bounding_box = timestamped_object.normalized_bounding_box
                print(u"\n\t\tLeft : {}".format(normalized_bounding_box.left))
                print(u"\t\tTop : {}".format(normalized_bounding_box.top))
                print(u"\t\tRight : {}".format(normalized_bounding_box.right))
                print(u"\t\tBottom : {}".format(normalized_bounding_box.bottom))

                # Optional. The attributes of the object in the bounding box.
                for attribute in timestamped_object.attributes:
                    print(u"\n\t\t\tName : {}".format(attribute.name))
                    print(u"\t\t\tConfidence : {}".format(attribute.confidence))
                    print(u"\t\t\tValue : {}".format(attribute.value))

            # Optional. Attributes in the track level.
            for track_attribute in track.attributes:
                print(u"\n\t\tName : {}".format(track_attribute.name))
                print(u"\t\tConfidence : {}".format(track_attribute.confidence))
                print(u"\t\tValue : {}".format(track_attribute.value))

        # All video segments where the recognized logo appears. There might be
        # multiple instances of the same logo class appearing in one VideoSegment.
        for segment in logo_recognition_annotation.segments:
            print(
                u"\n\tStart Time Offset : {}.{}".format(
                    segment.start_time_offset.seconds,
                    segment.start_time_offset.nanos * 1000,
                )
            )
            print(
                u"\tEnd Time Offset : {}.{}".format(
                    segment.end_time_offset.seconds,
                    segment.end_time_offset.nanos * 1000,
                )
            )


# In[ ]:


## Analyzing all the videos in the gcs bucket directory and send to store all the results in just one json file

APIKEY = '<<yourkeyforCloudVideoIntelligenceAPI>>'
output_dir='gs://bucket/output_dir/response-multiple-video-intelligence-single-request.json'
#VIDEO = 'gs://bucket/videos_dir/video.mp4'
gcs_uri = 'gs://bucket/videos_dir/*.*'

video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.enums.Feature.LOGO_RECOGNITION]

operation = video_client.annotate_video(input_uri=gcs_uri, features=features, output_uri=output_uri)
print("\nProcessing video for object annotations.")

result = operation.result()
print("\nFinished processing.\n")

# The first result is retrieved because a single video was processed.
object_annotations = result.annotation_results[0].object_annotations

for object_annotation in object_annotations:
    print("Entity description: {}".format(object_annotation.entity.description))
    if object_annotation.entity.entity_id:
        print("Entity id: {}".format(object_annotation.entity.entity_id))

    print(
        "Segment: {}s to {}s".format(
            object_annotation.segment.start_time_offset.seconds
            + object_annotation.segment.start_time_offset.nanos / 1e9,
            object_annotation.segment.end_time_offset.seconds
            + object_annotation.segment.end_time_offset.nanos / 1e9,
        )
    )

    print("Confidence: {}".format(object_annotation.confidence))

    # Here we print only the bounding box of the first frame in the segment
    frame = object_annotation.frames[0]
    box = frame.normalized_bounding_box
    print(
        "Time offset of the first frame: {}s".format(
            frame.time_offset.seconds + frame.time_offset.nanos / 1e9
        )
    )
    print("Bounding box position:")
    print("\tleft  : {}".format(box.left))
    print("\ttop   : {}".format(box.top))
    print("\tright : {}".format(box.right))
    print("\tbottom: {}".format(box.bottom))
    print("\n")


# In[ ]:


from googleapiclient.discovery import build
import base64

## Analyzing all the videos in a gcs bucket directory and send to store the results in the same bucket in different json files.

def logo_detection_videos_to_gcs(input_uri, output_uri):

    client = videointelligence.VideoIntelligenceServiceClient()

    features = [videointelligence.enums.Feature.LOGO_RECOGNITION]
    
    operation = client.annotate_video(features=features, input_uri=input_uri, output_uri=output_uri)
    print("\nProcessing video for object annotations.")
    print(u"Waiting for operation to complete...")
    response = operation.result()
    print("\nFinished processing.\n")
    
storage_client = storage.Client()
bucket = storage_client.bucket('image-cv')
print(bucket)

blobs = bucket.list_blobs(prefix="CFM_videos")
print(blobs)
videos_paths = []
print(videos_paths)

blob_list = list(bucket.list_blobs(prefix="CFM_videos"))
print('Output files:')
for blob in blob_list:
    blob.name
    print(blob.name)

blob_list = list(bucket.list_blobs(prefix="CFM_videos"))
print('Output files:')
for idx, bl in enumerate(blob_list):
    if idx == 0:
        continue
    print("working on video:", bl.name)
    logo_detection_videos_to_gcs("gs://bucket/" + str(bl.name),'gs://bucket/output_dir/' + str(bl.name) + '.json')

