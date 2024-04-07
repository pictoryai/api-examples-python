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
    
#Waits for transcription job to get complete
def wait_for_transcription_job_to_complete(token,jobid):
    response=get_jobid(token,jobid)['data']
    while(str(response).__contains__("in-progress")):
        response=get_jobid(token,jobid)['data']
    return response

#Calls storyboard api with payload present in payload.py and returns jobid as output
def create_preview_storyboard(token,text):
    BASE_URL=os.getenv('BASE_URL')
    STORYBOARD_ROUTE=os.getenv('STORYBOARD_ROUTE')
    USER_ID = os.getenv('USER_ID')
    url=BASE_URL+STORYBOARD_ROUTE
    texttovideopayload=payloads.create_storyboard_payload(text)
    headers=payloads.set_headers(token,USER_ID)
    payloadstoryboard=json.dumps(texttovideopayload)
    try:
            response = requests.request("POST", url, headers=headers, data=payloadstoryboard)
            data=response.json()
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
def wait_for_storyboard_job_to_complete(token,jobid):
    response=get_jobid(token,jobid)
    renderdata={}
    while(str(response).__contains__("in-progress")):
        response=get_jobid(token,jobid)
    renderdata['audio_settings']=response['data']['renderParams']['audio']
    renderdata['output_settings']=response['data']['renderParams']['output']
    renderdata['scenes_settings']=response['data']['renderParams']['scenes']
    return renderdata

#Calls render endpoint with payload came from storyboard and returns jobid as output
def create_video_render(token,renderdata):
    BASE_URL=os.getenv('BASE_URL')
    RENDER_ROUTE=os.getenv('RENDER_ROUTE')
    USER_ID = os.getenv('USER_ID')
    url=BASE_URL+RENDER_ROUTE
    renderequestpayload=payloads.create_render_payload(renderdata['audio_settings'],renderdata['output_settings'],renderdata['scenes_settings'])
    headers=payloads.set_headers(token,USER_ID)
    payload=json.dumps(renderequestpayload)
    try:
            response = requests.request("POST", url, headers=headers, data=payload)
            data=response.json()
            jobid=data['data']['job_id']
            return jobid
    except requests.exceptions.RequestException as e:
            print(f"Error while render: {e}")
            return None

#Waits for render job to get complete
def wait_for_render_job_to_complete(token,jobid):
    data=get_jobid(token,jobid)
    while(str(data).__contains__("in-progress")):
        data=get_jobid(token,jobid)
    url=data['data']['shareVideoURL']
    return url
     
#Download the final video genrated
def download_video(url):
    destination = 'audiotovideo/audiotovideo.mp4'
    response = requests.get(url, stream=True)
    with open(destination, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)


def main():
    load_dotenv()
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    token = get_token(CLIENT_ID, CLIENT_SECRET)
    data=generate_upload_url(token)
    AUDIO_PATH=os.getenv('AUDIO_PATH')
    upload_video(data['signedUrl'],AUDIO_PATH)
    jobid=create_trascription(token,data['url'],'en-US')
    transcriptiondata=wait_for_transcription_job_to_complete(token,jobid)
    text=transcriptiondata['txt']
    jobid=create_preview_storyboard(token,text)
    renderdata=wait_for_storyboard_job_to_complete(token,jobid)
    jobid=create_video_render(token,renderdata)
    url=wait_for_render_job_to_complete(token,jobid)
    download_video(url)
if __name__ == "__main__":
    main()
