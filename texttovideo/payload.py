class payloads:

  global TEXT_SCENE_1
  global TEXT_SCENE_2

  TEXT_SCENE_1='Jacobin sympathisers viewed the Directory as a betrayal of the Revolution, while Bonapartists later justified.'
  TEXT_SCENE_2='With Royalists apparently on the verge of power, Republicans attempted a pre-emptive coup on 4 September.'

  def create_auth_token_payload(clientid,clientsecret):
    payload = {}
    payload['client_id']=clientid
    payload['client_secret']=clientsecret
    return payload
    
    

  #This function creates audio object used in storyboard payload
  def create_audio_object(aivoiceover):
    audio = {}
    audio['autoBackgroundMusic']= 'true'
    audio['backGroundMusicVolume']= 0.5
    audio['aiVoiceOver']=aivoiceover
    return audio

  #This function creates aivoiceover object used in audio object
  def create_aivoiceover_object():
    aivoiceOver = {}
    aivoiceOver['speaker']= 'Jackson'
    aivoiceOver['speed']= 100
    aivoiceOver['amplifyLevel']= 0
    return aivoiceOver

  #This function creates scene object used in scenes array
  def create_scene_object(text):
    scene={}
    scene['text']=text
    scene['fontFamily']= 'Roboto'
    scene['textColor']= '#00FF00'
    scene['fontSize']= 32
    scene['textBackgroundColor']= '#000000'
    scene['voiceOver']= True
    scene['splitTextOnNewLine']= False
    scene['splitTextOnPeriod']= True
    return scene

  #This function creates scenes object used in storyboard payload
  def create_scenes(*argv):
    scenes=[]
    for arg in argv:
      scenes.append(arg)
    return scenes

  #This function creates storyboard payload
  def create_storyboard_payload():
      payload={}
      aivoiceover=payloads.create_aivoiceover_object()
      audio=payloads.create_audio_object(aivoiceover)
      scene1=payloads.create_scene_object(TEXT_SCENE_1)
      scene2=payloads.create_scene_object(TEXT_SCENE_2)
      scenes=payloads.create_scenes(scene1,scene2)
      payload['videoName']='Text_To_Video_English'
      payload['videoDescription']='Text_To_Video_English'
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
