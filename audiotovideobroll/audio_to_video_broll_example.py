import requests
import json
import sys
from payload import payloads
import os
import math
import time

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
BASE_URL = os.environ.get('BASE_URL', "https://api.pictory.ai")
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
USER_ID = os.getenv('X_PICTORY_USER_ID')


def get_token(CLIENT_ID, CLIENT_SECRET):

    url = f"{BASE_URL}/pictoryapis/v1/oauth2/token"
    authpaylaod = payloads.create_auth_token_payload(CLIENT_ID, CLIENT_SECRET)
    payload = json.dumps(authpaylaod)
    headers = payloads.set_auth_headers()
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        token = response.json()['access_token']
        return token
    except requests.exceptions.RequestException as e:
        print(f"Error while fetching token: {e}")
        return None


def transcribe_audio(token, fileurl, language):
    url = f"{BASE_URL}/pictoryapis/v2/transcription"
    transcriptionpayload = payloads.create_transcription_payload(
        fileurl, language, WEBHOOK_URL)
    headers = payloads.set_headers(token, USER_ID)
    payload = json.dumps(transcriptionpayload)
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        data = response.json()['data']
        jobid = data['jobId']
        return jobid
    except requests.exceptions.RequestException as e:
        print(f"Error while storyboard: {e}")
        return None


def wait_for_transcription_job_to_complete(token, jobid):
    response = get_job(token, jobid)['data']
    while (str(response).__contains__("in-progress")):
        response = get_job(token, jobid)['data']
    return response


def create_broll_storyboard_from_audio_transcription(token, audio_uri, transcript):
    scene_images = [
        "https://images.unsplash.com/photo-1591696331111-ef9586a5b17a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wzODkzOTJ8MHwxfHNlYXJjaHw4fHxBcnRpZmljaWFsfGVufDB8fHx8MTc0MTIzNzExOHww&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1608512532288-8f985c15345d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wzODkzOTJ8MHwxfHNlYXJjaHw1fHxBcnRpZmljaWFsfGVufDB8fHx8MTc0MTIzNzExOHww&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1490093158370-1a6be674437b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wzODkzOTJ8MHwxfHNlYXJjaHwxMHx8QXJ0aWZpY2lhbHxlbnwwfHx8fDE3NDEyMzcxMTh8MA&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1516110833967-0b5716ca1387?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wzODkzOTJ8MHwxfHNlYXJjaHwxfHxBcnRpZmljaWFsfGVufDB8fHx8MTc0MTIzNzExOHww&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1580777361964-27e9cdd2f838?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wzODkzOTJ8MHwxfHNlYXJjaHw2fHxBcnRpZmljaWFsfGVufDB8fHx8MTc0MTIzNzExOHww&ixlib=rb-4.0.3&q=80&w=1080"
    ]

    total_words = 0
    for sentence in transcript:
        total_words += len(sentence['words'])

    max_words_per_scene = math.ceil(total_words / len(scene_images))

    scene_subtitle = ""
    scene_background_image_index = 0
    scenes = []
    current_word_count = 0
    start_word = transcript[0]['words'][0]
    for sentence in transcript:
        for word in sentence['words']:
            if current_word_count <= max_words_per_scene:
                scene_subtitle += " " + word['word']
                current_word_count += 1
            else:
                scenes.append({
                    'text': scene_subtitle.strip(),
                    'splitTextOnNewLine': False,
                    'splitTextOnPeriod': False,
                    'subtitle': True,
                    'backgroundUri': scene_images[scene_background_image_index],
                    'backgroundType': "image",
                    'minimumDuration': word['start_time'] - start_word["start_time"],
                    'voiceOver': True
                })
                scene_background_image_index += 1
                scene_subtitle = word['word']
                current_word_count = 1
                start_word = word

    if current_word_count > 1:
        scenes.append({
            'text': scene_subtitle.strip(),
            'splitTextOnNewLine': False,
            'splitTextOnPeriod': False,
            'subtitle': True,
            'backgroundUri': scene_images[scene_background_image_index],
            'backgroundType': "image",
            'minimumDuration': transcript[-1]["words"][-1]["end_time"] - start_word["start_time"],
            'voiceOver': True
        })
    else:
        scenes[-1]['text'] += " " + scene_subtitle.strip()
        scenes[-1]["minimumDuration"] = scenes[-1]["minimumDuration"] + \
            start_word["end_time"] - start_word["start_time"]

    story_board_payload = {
        "videoName": "audio_to_video",
        "videoDescription": "audio_to_video",
        "videoWidth": 1920,
        "videoHeight": 1080,
        "language": "en",
        "audio": {
            "voiceOverUri": audio_uri
        },
        "scenes": scenes
    }

    url = f"{BASE_URL}/pictoryapis/v1/video/storyboard"
    headers = payloads.set_headers(token, USER_ID)
    payloadstoryboard = json.dumps(story_board_payload)
    try:
        response = requests.request(
            "POST", url, headers=headers, data=payloadstoryboard)
        data = response.json()
        jobid = data['jobId']
        return jobid
    except requests.exceptions.RequestException as e:
        print(f"Error while storyboard: {e}")
        return None


def get_job(token, jobid):
    url = f"{BASE_URL}/pictoryapis/v1/jobs/{jobid}"
    headers = payloads.set_headers(token, USER_ID)
    try:
        time.sleep(5)
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error while get jobid: {e}")
        return None


def wait_for_storyboard_job_to_complete(token, jobid):
    response = get_job(token, jobid)
    renderdata = {}
    while (str(response).__contains__("in-progress")):
        response = get_job(token, jobid)
    return response["data"]["preview"]


def render_storyboard(token, story_board_jobid):
    url = f"{BASE_URL}/pictoryapis/v1/video/render/{story_board_jobid}"
    headers = payloads.set_headers(token, USER_ID)
    payload = json.dumps({})
    try:
        response = requests.request("PUT", url, headers=headers, data=payload)
        data = response.json()
        jobid = data['data']['job_id']
        return jobid
    except requests.exceptions.RequestException as e:
        print(f"Error while render: {e}")
        return None


def wait_for_render_job_to_complete(token, jobid):
    data = get_job(token, jobid)
    while (str(data).__contains__("in-progress")):
        data = get_job(token, jobid)
    video_output = data['data']
    return video_output


def download_video(url):
    destination = 'blogtovideo/blogtovideo.mp4'
    response = requests.get(url, stream=True)
    with open(destination, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)


def main():
    audio_uri = "https://audios-prod.pictorycontent.com/polly/production/projects/1741235626276/2b47b8638e834a1b9d03af59230bcf95.mp3"
    token = get_token(CLIENT_ID, CLIENT_SECRET)
    transcribe_job_id = transcribe_audio(
        token, audio_uri, 'en-US')
    transcription_result = wait_for_transcription_job_to_complete(
        token, transcribe_job_id)
    if transcription_result and transcription_result.get("transcript", None):
        transcript = transcription_result["transcript"]
        story_board_jobid = create_broll_storyboard_from_audio_transcription(
            token, audio_uri, transcript)
        if story_board_jobid:
            preview = wait_for_storyboard_job_to_complete(
                token, story_board_jobid)
            if preview:
                render_video_job_id = render_storyboard(
                    token, story_board_jobid)
                video_output = wait_for_render_job_to_complete(
                    token, render_video_job_id)
                print(video_output)


if __name__ == "__main__":
    main()
