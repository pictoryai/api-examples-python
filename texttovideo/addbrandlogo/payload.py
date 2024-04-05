class payloads:

  global TEXT_SCENES

  TEXT_SCENES=['Jacobin sympathisers viewed the Directory as a betrayal of the Revolution, while Bonapartists later justified.','With Royalists apparently on the verge of power, Republicans attempted a pre-emptive coup on 4 September.']
  LOGO_URL="https://i0.wp.com/www.amazingathome.com/wp-content/uploads/2023/04/pictoryai_logo_main.jpg?fit=1080%2C1080&ssl=1"

  def create_auth_token_payload(clientid,clientsecret):
    payload = {}
    payload['client_id']=clientid
    payload['client_secret']=clientsecret
    return payload
    
    

  #This function creates audio object used in storyboard payload
  def create_audio_object(aivoiceover,auto_background_music ='true',background_music_volume = 0.5):
    audio = {}
    audio['autoBackgroundMusic']= auto_background_music
    audio['backGroundMusicVolume']= background_music_volume
    audio['aiVoiceOver']=aivoiceover
    return audio

  #This function creates aivoiceover object used in audio object
  def create_aivoiceover_object(speaker='Jackson',speed=100,amplify_level=0):
    aivoiceOver = {}
    aivoiceOver['speaker']= speaker
    aivoiceOver['speed']= speed
    aivoiceOver['amplifyLevel']= amplify_level
    return aivoiceOver

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
  def create_scenes(text_list):
    scenes=[]
    for text in text_list:
      scene=payloads.create_scene_object(text)
      scenes.append(scene)
    return scenes

  #This function creates object of brand logo used in storyboard payload
  def create_brand_logo_object(url=LOGO_URL,vertical_alignment='top',horizontal_alignment='left'):
    brand_logo={}
    brand_logo['url']=url
    brand_logo['verticalAlignment']=vertical_alignment
    brand_logo['horizontalAlignment']=horizontal_alignment
    return brand_logo

  #This function creates storyboard payload
  def create_storyboard_payload():
      payload={}
      aivoiceover=payloads.create_aivoiceover_object()
      audio=payloads.create_audio_object(aivoiceover)
      scenes=payloads.create_scenes(TEXT_SCENES)
      brand_logo=payloads.create_brand_logo_object()
      payload['videoName']='Text_To_Video_English'
      payload['videoDescription']='Text_To_Video_English'
      payload['language']='en'
      payload['audio']=audio
      payload['brandLogo']=brand_logo
      payload['scenes']=scenes
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

  #This function creates render payload
  def create_render_payload(audio,output,scenes):
      payload={}
      payload['audio']=audio
      payload['output']=output
      payload['scenes']=scenes
      payload['next_generation_video']=True
      payload['containsTextToImage']=True 
      return payload
