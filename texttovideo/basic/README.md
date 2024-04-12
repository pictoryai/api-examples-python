# Text to Video Generation

Pictory's Text-to-Video APIs offer a dynamic way to transform the text into engaging videos.

These APIs allow for the creation and editing of videos based on various text inputs. For instance, if you have a blog or an article, you can easily convert it into a captivating video by simply providing the webpage URL. Text-to-Video APIs open up various possibilities, including:

1. Generating new videos directly from existing text content.
2. Converting your published blogs or articles into videos using their URLs.

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

# Customization
You can customize the video output settings and audio settings by modifying the payload functions in payloads.py. Adjust the parameters according to your preferences.

# Example
python text_to_video.py

# Output
The final video will be saved as texttovideo/texttovideo.mp4 in the project directory.