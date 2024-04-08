class payloads:

  #This function creates payload for auth request
  def create_auth_token_payload(clientid,clientsecret):
    payload = {}
    payload['client_id']=clientid
    payload['client_secret']=clientsecret
    return payload

  #This function creates grenrate url payload
  def create_genrate_url_payload(filename):
    payload = {}
    payload['contentType']= 'video/mp4'
    payload['fileName']= filename
    return payload


  #This function creates transcription payload
  def create_transcription_payload(fileurl,language,webhook):
      payload={}
      payload['fileUrl']=fileurl
      payload['mediaType']="video"
      payload['language']=language
      payload['webhook']=webhook
      return payload

  #This function sets headers 
  def set_headers(token,userid):
    headers={}
    headers['Authorization']=token
    headers['X-Pictory-User-Id']=userid
    headers['Content-Type']='application/json'
    return headers  
  
  #This function sets headers for auth request
  def set_auth_headers():
    headers={}
    headers['Content-Type']='application/json'
    return headers  
  

  #This function creates audio object used in storyboard payload
  def create_audio_object(voice_over_uri,auto_background_music ='true',background_music_volume = 0.5):
    audio = {}
    audio['autoBackgroundMusic']= auto_background_music
    audio['backGroundMusicVolume']= background_music_volume
    audio['voiceOverUri']=voice_over_uri
    audio['autoSyncVoiceOver']=True
    return audio

  #This function creates scene object used in scenes array
  def create_scene_object(text,font_family='Roboto',text_color='#00FF00',fontsize=32,text_background_color='#000000',voice_over=True,split_text_on_new_line=False,split_text_on_period=True):
    scene={}
    scene['text']=text
    scene['fontFamily']= font_family
    scene['textColor']= text_color
    scene['fontSize']= fontsize
    scene['textBackgroundColor']= text_background_color
    scene['voiceOver']= voice_over
    scene['splitTextOnNewLine']= split_text_on_new_line
    scene['splitTextOnPeriod']= split_text_on_period
    return scene

  #This function creates scenes object used in storyboard payload
  def create_scenes(text):
    text=text.strip()
    scenes=[]
    text_list=text.split('.')
    for text in text_list:
      if(len(text)>0):
        scene=payloads.create_scene_object(text)
        scenes.append(scene)
    return scenes

  #This function creates storyboard payload
  def create_storyboard_payload(text,voice_over_uri):
      payload={}
      audio=payloads.create_audio_object(voice_over_uri)
      scenes=payloads.create_scenes(text)
      payload['videoName']='audio_to_video'
      payload['videoDescription']='audio_to_video'
      payload['language']='en'
      payload['audio']=audio
      payload['scenes']=scenes
      return payload

  #This function sets headers 
  def set_headers(token,userid):
    headers={}
    headers['Authorization']=token
    headers['X-Pictory-User-Id']=userid
    headers['Content-Type']='application/json'
    return headers  

  #This function creates render payload
  def create_render_payload(audio,output,scenes):
      payload={}
      payload['audio']=audio
      payload['output']=output
      payload['scenes']=scenes
      payload['next_generation_video']=True
      payload['containsTextToImage']=True 
      return payload

