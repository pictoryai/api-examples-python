from texttovideo.basic.payload import BasicPayloads

class payloads:
  global TEXT_SCENES
  INTRO="Welcome to Pictory club"
  OUTRO="Thank you"
  TEXT_SCENES=[INTRO,'Jacobin sympathisers viewed the Directory as a betrayal of the Revolution, while Bonapartists later justified.','With Royalists apparently on the verge of power, Republicans attempted a pre-emptive coup on 4 September.',OUTRO]

    #This function creates storyboard payload
  def create_storyboard_payload(self):
      payload={}
      basic_payload_obj=BasicPayloads()
      aivoiceover=basic_payload_obj.create_aivoiceover_object()
      audio=basic_payload_obj.create_audio_object(aivoiceover)
      scenes=basic_payload_obj.create_scenes(TEXT_SCENES)
      payload['videoName']='intro_outro'
      payload['videoDescription']='intro_outro'
      payload['language']='en'
      payload['audio']=audio
      payload['scenes']=scenes
      return payload
