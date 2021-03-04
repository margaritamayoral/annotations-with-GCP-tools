!pip install PyDrive

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth, drive
from oauth2client.client import GoogleCredentials
# Use to import the file into google Colab drive
from google.colab import files
# Use to import io, which opens the file from the Colab drive
import io
import gspread

drive.mount('/content/drive')

auth.authenticate_user()

project_id = '<<your-project-name>>'
!gcloud config set project {project_id}
!gsutil ls

bucket_name1 = 'bucket_name/dir_images/'   ## this is the bucket/folder for the images
bucket_name2 = 'bucket_name/dir_videos/' ### this is the bucket/folder for the videos

!gsutil -m cp -r /content/drive/My\ Drive/Data/images_to_analyze/* gs://{bucket_name1}/   ### to send the images from google drive to the bucket "bucket_name/dir_images/"

!gsutil -m cp -r /content/drive/My\ Drive/Data/videos_to_analyze/* gs://{bucket_name2}/  ### to send the videos from google drive to the bucket "bucekt_name/dir_videos"
