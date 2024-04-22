from texttovideo.basic.payload import  BasicPayloads
class payloads:

  global TEXT_SCENES

  TEXT_SCENES=['Jacobin sympathisers viewed the Directory as a betrayal of the Revolution, while Bonapartists later justified.','With Royalists apparently on the verge of power, Republicans attempted a pre-emptive coup on 4 September.']
  LOGO_URL="https://i0.wp.com/www.amazingathome.com/wp-content/uploads/2023/04/pictoryai_logo_main.jpg?fit=1080%2C1080&ssl=1"


  #This function creates object of brand logo used in storyboard payload
  def create_brand_logo_object(self,url=LOGO_URL,vertical_alignment='top',horizontal_alignment='left'):
    brand_logo={}
    brand_logo['url']=url
    brand_logo['verticalAlignment']=vertical_alignment
    brand_logo['horizontalAlignment']=horizontal_alignment
    return brand_logo

  #This function creates storyboard payload
  def create_storyboard_payload(self):
    payload={}
    basic_payload_obj=BasicPayloads()
    ai_voice_over=basic_payload_obj.create_aivoiceover_object()
    audio=basic_payload_obj.create_audio_object(ai_voice_over)
    scenes=basic_payload_obj.create_scenes(TEXT_SCENES)
    brand_logo=self.create_brand_logo_object()
    payload['videoName']='Text_To_Video_English'
    payload['videoDescription']='Text_To_Video_English'
    payload['language']='en'
    payload['audio']=audio
    payload['brandLogo']=brand_logo
    payload['scenes']=scenes
    return payload
