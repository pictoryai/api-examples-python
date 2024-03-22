import requests
import requests
import json
import os
import sys
from Payload import texttovideopayload

#Params passed in headers while any call to pictory
headersPayload="""{"Authorization": "","X-Pictory-User-Id": "PictoryCustomer","Content-Type": "application/json"}"""

#Payload schema for render api
renderequestPayload="""{
    "audio": "",
    "output": "",
    "scenes": "",
    "next_generation_video": true,
    "containsTextToImage": true
}"""


#Genrates token with clientid and client secret
def gettoken(CLIENT_ID,CLIENT_SECRET):

        url="https://api.pictory.ai/pictoryapis/v1/oauth2/token"
        payload = json.dumps({
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        })
        headers = {
            'Content-Type': 'application/json'
        }
        print(payload)
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            token=response.json()['access_token']
            return token
        except requests.exceptions.RequestException as e:
            print(f"Error while fetching token: {e}")
            return None
             
#Calls storyboard api with payload present in payload.py and returns jobid as output
def CreatePreviewStoryboard(token):
    url="https://api.pictory.ai/pictoryapis/v1/video/storyboard"
    headers=json.loads(headersPayload)
    headers['Authorization']=token
    payloadstoryboard=texttovideopayload
    print(payloadstoryboard)
    try:
            response = requests.request("POST", url, headers=headers, data=payloadstoryboard)
            data=response.json()
            print(data)
            jobid=data['jobId']
            print(jobid)
            return jobid
    except requests.exceptions.RequestException as e:
            print(f"Error while storyboard: {e}")
            return None

#Calls get jobs endpoind to get status of jobid
def GetJobId(token,jobid):
    url="https://api.pictory.ai/pictoryapis/v1/jobs/"+jobid
    headers=json.loads(headersPayload)
    headers['Authorization']=token
    try:
            response = requests.request("GET", url, headers=headers)
            data=response.json()
            return data
    except requests.exceptions.RequestException as e:
            print(f"Error while get jobid: {e}")
            return None
    
#Waits for storyboard job to get complete
def WaitForStoryboardJobToComplete(token,jobid):
    response=GetJobId(token,jobid)
    renderdata={}
    while(str(response).__contains__("in-progress")):
        response=GetJobId(token,jobid)
    renderdata['audio_settings']=response['data']['renderParams']['audio']
    renderdata['output_settings']=response['data']['renderParams']['output']
    renderdata['scenes_settings']=response['data']['renderParams']['scenes']
    print(renderdata)
    return renderdata

#Calls render endpoint with payload came from storyboard and returns jobid as output
def CreateVideoRender(token,renderdata):
    url="https://api.pictory.ai/pictoryapis/v1/video/render"
    headers=json.loads(headersPayload)
    headers['Authorization']=token
    payloadRender=json.loads(renderequestPayload)
    payloadRender['audio']=renderdata['audio_settings']
    payloadRender['output']=renderdata['output_settings']
    payloadRender['scenes']=renderdata['scenes_settings']
    print(payloadRender)
    payload=json.dumps(payloadRender)
    print(payload)
    try:
            response = requests.request("POST", url, headers=headers, data=payload)
            data=response.json()
            print(data)
            jobid=data['data']['job_id']
            print(jobid)
            return jobid
    except requests.exceptions.RequestException as e:
            print(f"Error while render: {e}")
            return None

#Waits for render job to get complete
def WaitForRenderJobToComplete(token,jobid):
    data=GetJobId(token,jobid)
    while(str(data).__contains__("in-progress")):
        data=GetJobId(token,jobid)
    print(data)
    url=data['data']['shareVideoURL']
    return url
     
#Download the final video genrated
def DownloadVideo(url):
    destination = 'Text-To-Video/textToVideo.mp4'
    response = requests.get(url, stream=True)
    with open(destination, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)

def main():
    if len(sys.argv) != 3:
        print("Usage: python GenrateVideo.py <CLIENT_ID> <CLIENT_SECRET>")
        sys.exit(1)

    CLIENT_ID = sys.argv[1]
    CLIENT_SECRET = sys.argv[2]
    
    token = gettoken(CLIENT_ID, CLIENT_SECRET)
    print(token)
    jobid=CreatePreviewStoryboard(token)
    renderdata=WaitForStoryboardJobToComplete(token,jobid)
    jobid=CreateVideoRender(token,renderdata)
    url=WaitForRenderJobToComplete(token,jobid)
    DownloadVideo(url)


if __name__ == "__main__":
    main()
