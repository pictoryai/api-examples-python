from texttovideo.basic.payload import BasicPayloads

class payloads:

  global TEXT_SCENES

  TEXT_SCENES=['Jacobin sympathisers viewed the Directory as a betrayal of the Revolution, while Bonapartists later justified.','With Royalists apparently on the verge of power, Republicans attempted a pre-emptive coup on 4 September.']

  #This function creates object of brand logo used in storyboard payload
  def create_text_styles_object(self,text_color='#FFFF00',font_family='Roboto',text_background_color='#FFFF00',font_name='Serif',font_size=20,vertical_alignment='top',horizontal_alignment='center'):
    text_style={}
    text_style['textColor']=text_color
    text_style['textBackgroundColor']=text_background_color
    text_style['fontFamily']= font_family
    text_style['fontName']=font_name
    text_style['fontSize']=font_size
    text_style['verticalAlignment']=vertical_alignment
    text_style['horizontalAlignment']=horizontal_alignment
    return text_style

  #This function creates storyboard payload
  def create_storyboard_payload(self):
    payload={}
    obj=BasicPayloads()
    ai_voice_over=obj.create_aivoiceover_object()
    audio=obj.create_audio_object(ai_voice_over)
    scenes=obj.create_scenes(TEXT_SCENES)
    text_style=self.create_text_styles_object()
    payload['videoName']='add_text_style'
    payload['videoDescription']='add_text_style'
    payload['language']='en'
    payload['audio']=audio
    payload['textStyles']=text_style
    payload['scenes']=scenes
    return payload
