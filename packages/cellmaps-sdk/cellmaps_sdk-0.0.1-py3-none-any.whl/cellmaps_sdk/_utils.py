from minio import Minio # type: ignore
import os
import requests
import re
from pathlib import Path
import uuid
# Reads Environment Variables for Minio Credentials
# MINIO_ROOT_USERNAME
# MINIO_ROOT_PASSWORD
from ._config import Config as _Config #type: ignore

_valid_image_extension = ['.tiff', '.qtiff','.qptiff','.ome.tiff']
_valid_marker_extension = ['.txt']

def _minio_healthcheck():
    # Ping the minio server, if it returns a status code of 200
    # the server is functioning correctly
    res = requests.get(f"http://{_Config._MINIO_HOST}:{_Config._MINIO_PORT}/minio/health/live")
    if res.status_code == 200:
        return True
    else:
        return False 
     
def get_minio_client():
    if _minio_healthcheck():
        client = Minio(
        endpoint=f"http://{_Config._MINIO_HOST}:{_Config._MINIO_PORT}",
        access_key=_Config._MINIO_ACCESS_KEY,
        secret_key=_Config._MINIO_SECRET_KEY,
        secure=False)
        return client   


def read_minio(id: str = ""):
    client = get_minio_client()
    all_experiments = {} #type: ignore
    exclusions = []
    # Could populate file extensions from taxonomy
    tma_regex_file = re.compile(r'^[\w,\s-]+(?:\.tiff|\.tif|\.ome.tiff|\.qptiff)')
    # Read prefixes only (these are the experiment ids)
    for obj in client.list_objects("experiment-bucket",prefix=id):
        if obj.is_dir:
            # Remove slashed from prefix
            all_experiments[obj.object_name.replace("/","")] = {}

    # Read child objects and add them to their
    for obj in client.list_objects("experiment-bucket",recursive=True):
        if not obj.is_dir:
            prefix, file = obj.object_name.split("/")
            if re.match(r"\S*.txt", file) != None:
                # it must be a txt file then
                # Get data of an object.
                try:
                    response = client.get_object("experiment-bucket",object_name=obj.object_name)
                    data = [l.rstrip() for l in response.data.decode().split('\n') if l.rstrip() != '']
                    # Read data from response.
                finally:
                    response.close()
                    response.release_conn()

                all_experiments[prefix]['channel_markers'] = data
            else:
                # must be an image
                all_experiments[prefix]['tiff_name'] = file

                # Checks if the filename matches the regex, if it doesn't it's not a valid file so it's add to exclusion list
                if re.match(tma_regex_file,file) == None:
                    exclusions.append(prefix)

    correct_format = []
    for k,v in all_experiments.items():
        if k not in exclusions:
            correct_format.append({
                "experiment_name" : k,
                "tiff_name" : v['tiff_name'],
                "channel_markers" : v['channel_markers']
            })


    return correct_format

def download_stacked_tiff_locally(url,dest="temp-files"):
    file_from_presigned_url = re.compile('/([^/]*)\?')
    matches = re.findall(file_from_presigned_url,url)
    assert len(matches) == 1, f'Regex found {len(matches)} in URL {url}'
     # Prepend UUID, so two workflows working on the same experimental data won't encounter race conditions
    local_filename = f"{str(uuid.uuid4())}_{matches[0]}"
    dest = Path(dest)
    try:
        os.mkdir(dest)
    except:
        pass
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest / local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment ifD
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
                
   
    return dest / local_filename

def get_experiment_data_urls(bucket_name,prefix_name):
    client = get_minio_client()
    image_name, marker_name = None,None
    for obj in client.list_objects(bucket_name,prefix_name):
        fp = Path(obj.object_name)
        if  fp.suffix in _valid_image_extension:
            image_name = obj.object_name
        elif fp.suffix in _valid_marker_extension:
            marker_name = obj.object_name
              
    # Sanity Check to make sure the data exists
    if image_name != None and marker_name != None:
        # Files exist
        img_url = get_minio_client().get_presigned_url('GET', bucket_name=bucket_name,object_name=image_name)
        marker_url = get_minio_client().get_presigned_url('GET', bucket_name=bucket_name,object_name=marker_name)
        return img_url, marker_url
    else:
        raise 'Unable to find the experimental datacle'