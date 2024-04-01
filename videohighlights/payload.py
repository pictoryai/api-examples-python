class payloads:

  #This function creates payload for auth request
  def create_auth_token_payload(clientid,clientsecret):
    payload = {}
    payload['client_id']=clientid
    payload['client_secret']=clientsecret
    return payload

  #This function creates genrate url payload
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
  
  #This function creates highlights payload 
  def create_highlights_payload(transcript,highlight_duration,webhook_url):
    payload={}
    payload['transcript']=transcript
    payload['highlight_duration']=highlight_duration
    payload['webhook']=webhook_url
    return payload 
