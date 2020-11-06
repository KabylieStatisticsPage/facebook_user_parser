import os
import requests
from bs4 import BeautifulSoup as bs
from fake_headers import Headers
from time import sleep
import sys


url='https://upload.facebook.com'
headers={'User-Agent':'Mozilla/5.0'}

r = requests.get(url)
sleep(10)
soup = bs(r.text,'lxml')
form = soup.find('form',{'id':'login_form'})
inputs = form.find_all('input')
load={}

for i in inputs:
    load[i.get('name')]=i.get('value')

#FB login
v_email = 'timunent.iteqvaylit@gmail.com'
v_password = 'TafSut?Taqvaylit80!'
load['email'] = v_email
load['pass'] = v_password
s=requests.session()
# retrieve the cookie of the user you are using. Cookie name: presence
v_cookies = {'presence': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxx'}
r=s.post(form.get('action'),data=load,headers=headers, cookies=v_cookies)

######
# def 
######

def parse_user_info(user_fb_id):
 ### name and town
 # sleep 30 seconds for each step to prevent getting blocked by FB
 sleep(30)
 URL = "https://upload.facebook.com/"+user_fb_id+"/about?section=living"
 headers = Headers().generate()
 respond = s.get(URL,headers = headers, cookies=v_cookies)
 soupt = str(respond.content.decode('utf-8')).replace("<!--", "").replace("-->", "")
 soup = bs(soupt,"lxml")


 if "Vous ne pouvez pas utiliser cette" not in soupt:
    print("not blocked yet :) ")
    nom_fb = ""
    spans = soup.find_all('span')

    for span in spans:
        for an in span.find_all('a'):
            clas = str(an.get ('class'))
            if clas == "['_2nlw', '_2nlv']":
                #print("content = " + clas) #print in terminal to verify results
                nom_fb = str(an.contents[0])
                print("nom_fb  " + nom_fb)
    #################### towns
    ville_actuel=""
    ville_origine=""
    dern_demenagement=""
    avant_dern_demenagement=""
    ville=""

    divs = soup.find_all('div')
    for div in divs:
        div_t = str(div.get ('class'))
        if div_t == "['_6a', '_6b']":
            for span in div.find_all('span'):
                span_t = str(span.get ('class'))
                if span_t == "['_2iel', '_50f7']":
                    for av in span.find_all('a'):
                        if (av.contents[0]) != 0:
                            ville = str(av.contents[0])
                        #print("ville  "+ ville)

            for divss in div.find_all('div'):
                div_tss = str(divss.get ('class'))
                if div_tss == "['fsm', 'fwn', 'fcg']":
                    ville_type = str(divss.contents).replace("'", "").replace("[", "").replace("]", "")
                    if "<div " not in ville_type:

                        if "ctuell" in ville_type and ville_actuel == "":
                            ville_actuel = ville
                            print("ville_actuel  " + ville)

                        elif "origine" in ville_type and ville_origine == "":
                            ville_origine = ville
                            print("ville_origine  " + ville)

                        elif "nagement" in ville_type and dern_demenagement == "" and avant_dern_demenagement =="":
                            dern_demenagement = ville
                            print("dern_demenagement  " + dern_demenagement)
                        elif "nagement" in ville_type and dern_demenagement != "" and avant_dern_demenagement =="":
                            avant_dern_demenagement = ville
                            print("avant_dern_demenagement " + avant_dern_demenagement)
    ###################
    ### employment and education
    # sleep 30 seconds for each step to prevent getting blocked by FB
    sleep(30)
    URL = "https://upload.facebook.com/"+user_fb_id+"?sk=about&section=education"
    headers = Headers().generate()
    respond = s.get(URL,headers = headers, cookies=v_cookies)
    #(soup.prettify())
    soup = str(respond.content.decode('utf-8')).replace("<!--", "").replace("-->", "")
    soup = bs(soup,"lxml")
    dern_emploi=""
    detail_dern_emploi=""
    avant_dern_emploi=""
    detail_avant_dern_emploi=""
    dern_scolarite=""
    detail_dern_scolarite=""
    avant_dern_scolarite=""
    detail_avant_dern_scolarite=""
    detail=""
    val_detail: str = ""
    #################### emploi_scol
    t_emp_scol: str = ""
    type_emp_scol=""
    divs = soup.find_all('div')
    for div in divs:
        div_t = str(div.get ('class'))
        if div_t == "['_4qm1']":
            for span_es in div.find_all('span'):
                if len(span_es) != 0:
                    type_emp_scol = str(span_es.contents[0])
                    if "Emplo" in type_emp_scol or "Scol" in type_emp_scol:
                        t_emp_scol= type_emp_scol
        elif div_t == "['_6a', '_6b']":
            for divs in div.find_all('div'):
                divs_t = str(divs.get ('class'))
                if divs_t == "['_2lzr', '_50f5', '_50f7']":
                    for ae in divs.find_all('a'):
                        emploi = str(ae.contents[0])
                    if "Emplo" in t_emp_scol and dern_emploi == "" and avant_dern_emploi =="":
                        dern_emploi = emploi.replace('<span dir="rtl">',"").replace("</span>","")
                        detail = "det_dern_emploi"
                        print("dern_emploi " + dern_emploi)
                    elif "Emplo" in t_emp_scol and dern_emploi != "" and avant_dern_emploi =="":
                        avant_dern_emploi = emploi.replace('<span dir="rtl">',"").replace("</span>","")
                        detail = "det_avant_dern_emploi"
                        print("avant_dern_emploi " + avant_dern_emploi)
                    elif "Scol" in t_emp_scol and avant_dern_scolarite == "" and dern_scolarite == "":
                        avant_dern_scolarite = emploi
                        detail = "det_avant_dern_scolarite"
                        print("avant_dern_scolarite " + avant_dern_scolarite)
                    elif "Scol" in t_emp_scol and dern_scolarite == "" and avant_dern_scolarite != "":
                        dern_scolarite = emploi
                        detail = "det_dern_scolarite"
                        print("dern_scolarite " + dern_scolarite)
                elif divs_t == "['_3-8w', '_50f8']":
                    val_detail = str(divs.contents[0])
                    print(detail +" "+ val_detail)
    ###################
    ### general info and address
    # sleep 30 seconds for each step to prevent getting blocked by FB
    sleep(30)
    URL = "https://upload.facebook.com/"+user_fb_id+"?sk=about&section=contact-info"
    headers = Headers().generate()
    respond = s.get(URL,headers = headers, cookies=v_cookies)
    #(soup.prettify())
    soup = str(respond.content.decode('utf-8')).replace("<!--", "").replace("-->", "")
    soup = bs(soup,"lxml")
    prem_langue=""
    deux_langue=""
    langue_t=""
    date_naiss=""
    lang=""
    #################### other info
    ### birth date
    lis = soup.find_all('li')
    for li in lis:
        li_t = str(li.get ('class'))
        if li_t == "['_3pw9', '_2pi4', '_2ge8', '_4vs2']":
            for span_dn in li.find_all('span'):
                span_dn_t = str(span_dn.get ('class'))
                if span_dn_t == "['_50f4', '_5kx5']":
                    if len(span_dn.contents[0]) !=0 :
                        dn_t = str(span_dn.contents[0])
                elif span_dn_t == "['_2iem']":
                    if len(span_dn.contents[0]) != 0:
                        dn = str(span_dn.contents[0])
                        if "Date de naissance" in dn_t:
                            date_naiss = dn
                            print("date naissance  "+ date_naiss)
    ###  gender
    for li in lis:
        li_t = str(li.get ('class'))
        if li_t == "['_3pw9', '_2pi4', '_2ge8', '_3ms8']":
            for span_ge in li.find_all('span'):
                span_ge_t = str(span_ge.get ('class'))
                if span_ge_t == "['_50f4', '_5kx5']":
                    if len(span_ge.contents[0]) != 0:
                        genre_t = str(span_ge.contents[0])
                elif span_ge_t == "['_2iem']":
                    genre = str(span_ge.contents[0])
                    if "Genre" in genre_t:
                        print("genre  " + genre)
    ### languages
    for li in lis:
        li_t = str(li.get ('class'))
        if li_t == "['_3pw9', '_2pi4', '_2ge8']":
            for span_lang in li.find_all('span'):
                span_lang_t = str(span_lang.get ('class'))
                if span_lang_t == "['_50f4', '_5kx5']" and "Langu" in str(span_lang.contents[0]):
                    if len(span_lang.contents[0]) != 0:
                        langue_t = str(span_lang.contents[0])
                elif span_lang_t == "['_2iem']":
                    for al in span_lang.find_all('a'):
                        if len(al.contents[0]) != 0:
                            lang = str(al.contents[0])
                            if "class=" not in lang:
                                if len(span_lang.contents[0]) != 0 and langue_t == "Langues":
                                    if prem_langue == "" and deux_langue == "":
                                        prem_langue = lang
                                        print("Langue 1  " + lang)
                                    elif prem_langue != "" and deux_langue == "":
                                        deux_langue = lang
                                        print("Langue 2  " + lang)
    csv = '"\'' + user_fb_id + '";"' + nom_fb + '";"' + ville_origine + '";"' + ville_actuel + '";"' + dern_demenagement + '";"' + avant_dern_demenagement + '";"' + dern_emploi + '";"' + detail_dern_emploi + '";"' + avant_dern_emploi + '";"' + detail_avant_dern_emploi + '";"' + dern_scolarite + '";"' + detail_dern_scolarite + '";"' + avant_dern_scolarite + '";"' + detail_avant_dern_scolarite + '";"' + prem_langue + '";"' + deux_langue + '";"' + date_naiss +'"'
    return csv
 else:
  csv = "error"
###################
path_in = 'input\\'
path_out = 'output\\'
header_f = '"user_fb_id";"nom_fb";"ville_origine";"ville_actuel";"dern_demenagement";"avant_dern_demenagement";"dern_emploi";"detail_dern_emploi";"avant_dern_emploi";"detail_avant_dern_emploi";"dern_scolarite";"detail_dern_scolarite";"avant_dern_scolarite";"detail_avant_dern_scolarite";"prem_langue";"deux_langue";"date_naiss"'
file_output = open(path_out + "\\input_file.csv","a",encoding="utf-8")
file_output.write(header_f + "\n")
file_output.close()
csv_w = ""
files = []
for r, d, f in os.walk(path_in):
 for file in f:
  if '.csv' in file:
   files.append(os.path.join(r, file))
file_input: str = ""
if csv_w != "error" and csv_w != "None" and csv_w is not None:
 for f in files:
  file_input = f
  print ("file input: " + file_input)
  file_output = open(path_out + "\\input_file.csv","a",encoding="utf-8")
  with open(file_input) as fp:
   for cnt, user_fb_id in enumerate(fp):
    try:
     user_fb_id = str(user_fb_id).rstrip("\r").rstrip("\n")
     csv_w = str(parse_user_info(user_fb_id))
     print("csv_w " + csv_w)
     if csv_w != "error" and csv_w is not None and csv_w != "None":
      file_output.write(csv_w + "\n")
     else:
      print ("Error parsing. File : " + file_input)
      sleep(5)
      sys.exit()
    except Exception as ex:
     print("failed adding: " + user_fb_id + "Exception: " + str(ex))
 print("End file: " + file_input)
 file_output.close()
 if csv_w != "error" and csv_w is not None and csv_w != "None":
  # sleep 15 minutes after each file to prevent getting blocked by FB
  sleep(900)
 else:
  print("Error parse")
  sys.exit()

else:
 print("Error parse")
 sys.exit()
print("End")


file_output.close()
s.close()


