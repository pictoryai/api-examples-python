import json
#Payload for storyboard api
texttovideopayload=payload = json.dumps({
  "videoName": "Text_To_Video_English",
  "videoDescription": "Text_To_Video_English",
  "language": "en",
  "audio": {
    "autoBackgroundMusic": True,
    "backGroundMusicVolume": 0.5,
    "aiVoiceOver": {
      "speaker": "Jackson",
      "speed": 100,
      "amplifyLevel": 0
    }
  },
  "scenes": [
    {
      "text": "Jacobin sympathisers viewed the Directory as a betrayal of the Revolution, while Bonapartists later justified.",
      "fontFamily": "Roboto",
      "textColor": "#00FF00",
      "fontSize": 32,
      "textBackgroundColor": "#000000",
      "voiceOver": True,
      "splitTextOnNewLine": False,
      "splitTextOnPeriod": True
    },
    {
      "text": "With Royalists apparently on the verge of power, Republicans attempted a pre-emptive coup on 4 September.",
      "fontFamily": "Roboto",
      "textColor": "#00FF00",
      "fontSize": 32,
      "textBackgroundColor": "#000000",
      "voiceOver": True,
      "splitTextOnNewLine": False,
      "splitTextOnPeriod": True
    }
  ]
})