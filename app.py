import json
from pypresence import Presence
import time
import os

src = os.path.join(os.getenv("APPDATA"),"Activity-Condenser")
settingssrc = os.path.join(src,"settings.json")
datasrc = os.path.join(src,"data.json")

with open(settingssrc) as j:
    settings = json.load(j)
    print(settings)

client_id = settings['Client_ID']
RPC = Presence(client_id )
RPC.connect()

while 1 == 1:
   f = open(datasrc)

   data = json.load(f)

   Idfinal = []
   AppIDfinal = []
   Namefinal = []
   Urlfinal = []
   Detailsfinal = []
   Statefinal = []
   Timestampsfinal = []
   Assetsfinal = []
   Buttonsfinal = []
   Endfinal = []
   Partyfinal = []
   Startfinal = []
   Large_imagefinal = []
   Large_textfinal = []
   Small_imagefinal = []
   Small_textfinal = []
   Party_debug = {}
   buttons_tempfinal = []

   x = 0

   for i in data['Presence']:
      Id = data['Presence'][x]['ID']
      AppID = data['Presence'][x]['AppID']
      Name = data['Presence'][x]['Name']
      Url = data['Presence'][x]['URL']
      Details = data['Presence'][x]['Details']
      State = data['Presence'][x]['State']
      Timestamps = data['Presence'][x]['Timestamps']
      Large_image = data['Presence'][x]['large_image']
      Large_text = data['Presence'][x]['large_text']
      Small_image = data['Presence'][x]['small_image']
      Small_text = data['Presence'][x]['small_text']
      Buttons = data['Presence'][x]['Buttons']
      End = data['Presence'][x]['End']
      Party = data['Presence'][x]['Party']
      Start = data['Presence'][x]['Start']
      Idfinal.append(Id)
      AppIDfinal.append(AppID)
      Namefinal.append(Name)
      Urlfinal.append(Url)
      Detailsfinal.append(Details)
      Statefinal.append(State)
      Timestampsfinal.append(Timestamps)
      Large_imagefinal.append(Large_image)
      Large_textfinal.append(Large_text)
      Small_imagefinal.append(Small_image)
      Small_textfinal.append(Small_text)
      Buttonsfinal.append(Buttons)
      Endfinal.append(End)
      Partyfinal.append(Party)
      Startfinal.append(Start)
      Testdebug = int(settings['Client_ID'])
      x = x + 1
   z = 0
   while z < Idfinal[-1]:
      if Testdebug == AppIDfinal[z]:
         z = z + 1
         continue

      if "end" in Timestampsfinal[z]:
         if "start" in Timestampsfinal[z]:
            start_temp = Timestampsfinal[z]['start']
            end_temp = Timestampsfinal[z]['end']
         else :
            start_temp = None
            end_temp = Timestampsfinal[z]['end']
      else : 
         if "start" in Timestampsfinal[z]:
            start_temp = Timestampsfinal[z]['start']
            end_temp = None
         else :
            start_temp = None
            end_temp = None
      if Partyfinal[z] == Party_debug:
         party_id_temp = None
         party_size_temp = None
      else:
         party_id_temp = Partyfinal[z]['id']
         party_size_temp = Partyfinal[z]['size']
      if Buttonsfinal[z] == []:
         buttons_temp = None
         buttons_temp2 = None
         buttons_tempfinal = None
      else :
         w = len(Buttonsfinal[z])
         y = 0
         buttons_tempfinal = []
         while y < w:
            buttons_temp = Buttonsfinal[z][y]
            buttons_temp2 = {"label": buttons_temp, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
            buttons_tempfinal.append(buttons_temp2)
            print(buttons_tempfinal)
            y = y + 1
            
      print(RPC.update(buttons=buttons_tempfinal, party_id=party_id_temp, party_size=party_size_temp, details=Detailsfinal[z], state=Statefinal[z],start = start_temp,end = end_temp, large_image=Large_imagefinal[z], large_text=Large_textfinal[z], small_image=Small_imagefinal[z], small_text=Small_textfinal[z]))
      z = z + 1
      time.sleep(settings['refresh_time'])

   f.close()