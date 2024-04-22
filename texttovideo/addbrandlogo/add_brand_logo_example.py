import requests
import json
import sys
from texttovideo.basic.basic_example import basic
from texttovideo.basic.payload import BasicPayloads
from payload import payloads
from dotenv import load_dotenv
import os



#Calls storyboard api with payload present in payload.py and returns jobid as output
def create_preview_storyboard(token):
    BASE_URL=os.getenv('BASE_URL')
    STORYBOARD_ROUTE=os.getenv('STORYBOARD_ROUTE')
    USER_ID = os.getenv('USER_ID')
    url=BASE_URL+STORYBOARD_ROUTE
    payloads_obj=payloads()
    basic_payload_obj=BasicPayloads()
    text_to_video_payload=payloads_obj.create_storyboard_payload()
    headers=basic_payload_obj.set_headers(token,USER_ID)
    payload_storyboard=json.dumps(text_to_video_payload)
    try:
            response = requests.request("POST", url, headers=headers, data=payload_storyboard)
            data=response.json()
            jobid=data['jobId']
            return jobid
    except requests.exceptions.RequestException as e:
            print(f"Error while storyboard: {e}")
            return None

def main():
    load_dotenv()
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    obj=basic()
    token = obj.get_token(CLIENT_ID, CLIENT_SECRET)
    jobid=create_preview_storyboard(token)
    render_data=obj.wait_for_storyboard_job_to_complete(token,jobid)
    jobid=obj.create_video_render(token,render_data)
    url=obj.wait_for_render_job_to_complete(token,jobid)
    obj.download_video(url,"add_brand_logo.mp4")


if __name__ == "__main__":
    main()
