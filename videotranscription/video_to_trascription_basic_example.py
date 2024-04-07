import requests
import json
import sys
from payload import payloads
from dotenv import load_dotenv
import os


#Genrates token with clientid and client secret
def get_token(CLIENT_ID,CLIENT_SECRET):
        BASE_URL=os.getenv('BASE_URL')
        AUTH_ROUTE=os.getenv('AUTH_ROUTE')
        url=BASE_URL+AUTH_ROUTE
        authpaylaod=payloads.create_auth_token_payload(CLIENT_ID,CLIENT_SECRET)
        payload = json.dumps(authpaylaod)
        headers=payloads.set_auth_headers()
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            token=response.json()['access_token']
            return token
        except requests.exceptions.RequestException as e:
            print(f"Error while fetching token: {e}")
            return None
             
def generate_upload_url(token):
    BASE_URL=os.getenv('BASE_URL')
    GENERATEURL_ROUTE=os.getenv('GENERATEURL_ROUTE')
    USER_ID = os.getenv('USER_ID')
    url=BASE_URL+GENERATEURL_ROUTE
    headers=payloads.set_headers(token,USER_ID)
    generateurl_payload=payloads.create_genrate_url_payload("testvideo.mp4")
    payload=json.dumps(generateurl_payload)
    try:
            response = requests.request("POST", url, headers=headers, data=payload)
            data=response.json()['data']
            return data
    except requests.exceptions.RequestException as e:
            print(f"Error while generate url: {e}")
            return None
    
def upload_video(url, video_path):
    headers = {"Content-Type": "video/mp4"}
    current_directory = os.getcwd()
    print("Current directory:", current_directory)
    with open(current_directory+'/'+video_path, "rb") as file:
        video_data = file.read()
    try:
        response = requests.put(url, headers=headers, data=video_data)
        response.raise_for_status()
        print("Video uploaded successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error uploading video: {e}")

#Calls storyboard api with payload present in payload.py and returns jobid as output
def create_trascription(token,fileurl,language):
    BASE_URL=os.getenv('BASE_URL')
    TRANSCRIPTION_ROUTE=os.getenv('TRANSCRIPTION_ROUTE')
    WEBHOOK_URL=os.getenv('WEBHOOK_URL')
    USER_ID = os.getenv('USER_ID')
    url=BASE_URL+TRANSCRIPTION_ROUTE
    transcriptionpayload=payloads.create_transcription_payload(fileurl,language,WEBHOOK_URL)
    headers=payloads.set_headers(token,USER_ID)
    payload=json.dumps(transcriptionpayload)
    try:
            response = requests.request("POST", url, headers=headers, data=payload)
            data=response.json()['data']
            jobid=data['jobId']
            return jobid
    except requests.exceptions.RequestException as e:
            print(f"Error while storyboard: {e}")
            return None

#Calls get jobs endpoind to get status of jobid
def get_jobid(token,jobid):
    BASE_URL=os.getenv('BASE_URL')
    GET_JOB_ROUTE=os.getenv('GET_JOB_ROUTE')
    USER_ID = os.getenv('USER_ID')
    url=BASE_URL+GET_JOB_ROUTE+str(jobid)
    headers=payloads.set_headers(token,USER_ID)
    try:
            response = requests.request("GET", url, headers=headers)
            data=response.json()
            return data
    except requests.exceptions.RequestException as e:
            print(f"Error while get jobid: {e}")
            return None
    
#Waits for storyboard job to get complete
def wait_for_transcription_job_to_complete(token,jobid):
    response=get_jobid(token,jobid)['data']
    while(str(response).__contains__("in-progress")):
        response=get_jobid(token,jobid)['data']
    return response

def main():
    load_dotenv()
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    token = get_token(CLIENT_ID, CLIENT_SECRET)
    data=generate_upload_url(token)
    VIDEO_PATH=os.getenv('VIDEO_PATH')
    upload_video(data['signedUrl'],VIDEO_PATH)
    jobid=create_trascription(token,data['url'],'en-US')
    transcriptiondata=wait_for_transcription_job_to_complete(token,jobid)
    print(transcriptiondata['txt'])
if __name__ == "__main__":
    main()
