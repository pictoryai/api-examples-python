from texttovideo.basic.payload import  BasicPayloads
class payloads:

  global TEXT_SCENES
  TEXT_SCENES=['Jacobin sympathisers viewed the Directory as a betrayal of the Revolution, while Bonapartists later justified.','With Royalists apparently on the verge of power, Republicans attempted a pre-emptive coup on 4 September.']
  video_url="http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"

  #This function creates scenes object used in storyboard payload
  def create_scenes(self,text_list):
    scenes=[]
    i=0
    for text in text_list:
      scene=self.create_scene_object(text,i)
      scenes.append(scene)
      i=i+1
    return scenes

  def create_background_video_segments(self,start, end):
    background_video_segments = [{}]
    background_video_segments[0]['start']=start
    background_video_segments[0]['end']=end
    return background_video_segments

   #This function creates scene object used in scenes array
  def create_scene_object(self,text,counter,video_url=video_url,backgroundType="video",font_family='Roboto',text_color='#00FF00',fontsize=32,text_background_color='#000000',voice_over=True,split_text_on_new_line=False,split_text_on_period=True):
    scene={}
    start=counter*5
    end=counter*5+5
    background_video_segments=self.create_background_video_segments(start,end)
    scene['text']=text
    scene['backgroundUri']=video_url
    scene['backgroundType']=backgroundType
    scene['backgroundVideoSegments']=background_video_segments
    scene['fontFamily']= font_family
    scene['textColor']= text_color
    scene['fontSize']= fontsize
    scene['textBackgroundColor']= text_background_color
    scene['voiceOver']= voice_over
    scene['splitTextOnNewLine']= split_text_on_new_line
    scene['splitTextOnPeriod']= split_text_on_period
    return scene

  #This function creates storyboard payload
  def create_storyboard_payload(self):
    payload={}
    basic_payload_obj=BasicPayloads()
    ai_voice_over=basic_payload_obj.create_aivoiceover_object()
    audio=basic_payload_obj.create_audio_object(ai_voice_over)
    scenes=self.create_scenes(TEXT_SCENES)
    payload['videoName']='visual_to_video'
    payload['videoDescription']='visual_to_video'
    payload['language']='en'
    payload['audio']=audio
    payload['scenes']=scenes
    return payload
