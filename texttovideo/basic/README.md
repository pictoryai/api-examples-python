# Requirements
Ensure you have the following prerequisites installed:

1. Python 3.x
2. requests
3. Pictory API KEYS which include CLIENT_ID, CLIENT_SECRET and X-Pictory-User-Id.    

Note: If you don't have your CLIENT_ID, CLIENT_SECRET and X-Pictory-User-Id please contact us at *support@pictory.ai*.


# Usage
 1. Update USER_ID,CLIENT_ID and CLIENT_SECRET in .env file.

 2. Run the script text_to_video.py to initiate the text-to-video conversion process. This will perform the following steps:

     a. **Authentication**: Generate an access token using the provided client ID and client secret.
     b. **Storyboard Creation**: Call the storyboard API with predefined payloads to create a storyboard. Returns a job ID.
     c. **Waiting for Storyboard Job**: Monitor the status of the storyboard job until it completes.
     d. **Video Rendering**: Call the render endpoint with data obtained from the completed storyboard job. Returns a job ID for rendering.
     e. **Waiting for Render Job**: Monitor the status of the rendering job until it completes.
     f. **Download**: Once rendering is complete, download the final video.

```json
Sample Storyboard API
{
    "videoName": "Sino-Japanese-War", //Desired video file name
    "videoDescription": "Santa Claus is coming to town", //*optional*
    "language": "en", //Text language: English only
    "webhook": "https://webhook.site/f817c508-0cce-486c-a74d-4537759b077f",
    "brandLogo": {
    "url":"https://pictory.ai/wp-content/uploads/2022/03/logo-new-fon-2t.png", 
    "verticalAlignment": "top" , 
    "horizontalAlignment": "right"
    },
    "audio": {
        "autoBackgroundMusic": true, 
        "backGroundMusicVolume": 0.5, 
        "aiVoiceOver": {
            "speaker": "Adam", 
            "speed": 100, 
            "amplifyLevel": 0 
        }
    },
    "textStyles":{
    "fontFamily": "Roboto",
    "textColor": "#7000FD",
    "fontSize": 36,
    "textBackgroundColor": "#FFFFFF",
    "verticalAlignment": "bottom",
    "horizontalAlignment": "center"
    },
    "scenes": [
        {
            "backgroundUri": "https://dm0qx8t0i9gc9.cloudfront.net/watermarks/video/HVzxMQxkil73u47k1/videoblocks-retro-soldiers-troops53_hshdoehnt__6dfbfe0529e764e8f04bdf8e76ed41b3__P480.mp4?type=preview&origin=VIDEOBLOCKS&timestamp_ms=1712305921133&publicKey=NFKFzias7JkF35W3n9edUuQV1Rnn7udTDco3ZbvzlsXgiAzLXO0a15shkgbMNmXZ&organizationId=103776&apiVersion=2.0&stockItemId=348672814&resolution=480p&endUserId=718890439cf9899e412f4e3d6c8148c452fb5959&projectId=dev&searchId=9903f512-732f-4f3c-b474-bc0445fac778&searchPageId=55ea31e8-24a8-46d4-bf50-ee37a3926aae",
            "backgroundType": "video",
            "assetId": "1495121538",
            "library": "getty",
            "minSceneDuration":"6"
        }, 
        {
            "text": "The First Sino-Japanese War (25 July 1894 – 17 April 1895) or the First China–Japan War was a conflict between the Qing dynasty and Empire of Japan primarily over influence in Korea.",
            "voiceOver": true,
            "splitTextOnNewLine": false, 
            "splitTextOnPeriod": true 
        },
    ],
    "voiceOver": true, //AI voice reads the text
    "splitTextOnNewLine": false, //Split scenes on '\n' in text
    "splitTextOnPeriod": true //Split scenes at periods

}
```

# Customization
You can customize the video output settings and audio settings by modifying the payload functions in payloads.py. Adjust the parameters according to your preferences.

# Example
python text_to_video.py

# Output
The final video will be saved as texttovideo/texttovideo.mp4 in the project directory.


