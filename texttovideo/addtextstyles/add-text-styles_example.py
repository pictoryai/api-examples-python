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
             
#Calls storyboard api with payload present in payload.py and returns jobid as output
def create_preview_storyboard(token):
    BASE_URL=os.getenv('BASE_URL')
    STORYBOARD_ROUTE=os.getenv('STORYBOARD_ROUTE')
    url=BASE_URL+STORYBOARD_ROUTE
    texttovideopayload=payloads.create_storyboard_payload()
    headers=payloads.set_headers(token,"PictoryCustomer")
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
    url=BASE_URL+GET_JOB_ROUTE+str(jobid)
    headers=payloads.set_headers(token,"PictoryCustomer")
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
    url=BASE_URL+RENDER_ROUTE
    renderequestpayload=payloads.create_render_payload(renderdata['audio_settings'],renderdata['output_settings'],renderdata['scenes_settings'])
    headers=payloads.set_headers(token,"PictoryCustomer")
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
    destination = 'texttovideo/texttovideo.mp4'
    response = requests.get(url, stream=True)
    with open(destination, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)

def main():
    load_dotenv()
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    token = get_token(CLIENT_ID, CLIENT_SECRET)
    jobid=create_preview_storyboard(token)
    renderdata=wait_for_storyboard_job_to_complete(token,jobid)
    jobid=create_video_render(token,renderdata)
    url=wait_for_render_job_to_complete(token,jobid)
    download_video(url)


if __name__ == "__main__":
    main()
