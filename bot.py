import telebot
import parser
from telebot import types
import pandas as pd
from keras.models import load_model
import numpy as np
import tensorflow

data=pd.read_csv('noc_regions.csv')
data['NOC']=data['NOC'].replace('ANZ','AUS')
data['NOC']=data['NOC'].replace('NFL','CAN')
data['NOC']=data['NOC'].replace('HKG','CHN')
data['NOC']=data['NOC'].replace('UAR','SYR')
data['NOC']=data['NOC'].replace(['SCG','YUG'],'SRB')

data['NOC']=data['NOC'].replace(['MAS','NBO'],'MAL')
data['NOC']=data['NOC'].replace(['BOH','TCH'],'CZE')

data['NOC']=data['NOC'].replace('CRT','GRE')
data['NOC']=data['NOC'].replace(['FRG','GDR','SAA'],'GER')
data['NOC']=data['NOC'].replace('WIF','TTO')
data['NOC']=data['NOC'].replace('VNM','VIE')
data['NOC']=data['NOC'].replace(['YAR','YMD'],'YEM')
data['NOC']=data['NOC'].replace('SIN','SGP')
data['NOC']=data['NOC'].replace('RHO','ZIM')
data['NOC']=data['NOC'].replace(['ROT','TUV'],'UNK')



list_of_region_noc=list()
list_of_region_noc=data['NOC'].unique()
list_of_regions=list()
flag=0
for i in range(209):
    for k in range(230):
        if(list_of_region_noc[i]==data['NOC'][k] and flag==0):
            list_of_regions.append(data['region'][k])
            flag=1
    flag=0





list_of_regions_array=[0 for i in range(209)]
count=1
for i in range(209):
    list_of_regions_array[i]=count
    count=count+1

list_of_sports=['Basketball','Judo','Football','Tug-Of-War','Speed Skating','Cross Country Skiing','Athletics','Ice Hockey','Swimming','Badminton','Sailing','Biathlon','Gymnastics','Art Competitions','Alpine Skiing','Handball','Weightlifting',
'Wrestling','Luge','Water Polo','Hockey','Rowing','Bobsleigh','Fencing','Equestrianism','Shooting','Boxing','Taekwondo','Cycling','Diving','Canoeing','Tennis','Modern Pentathlon','Figure Skating','Golf','Softball','Archery','Volleyball','Synchronized Swimming',
'Table Tennis','Nordic Combined','Baseball','Rhythmic Gymnastics','Freestyle Skiing','Rugby Sevens','Trampolining','Beach Volleyball','Triathlon','Ski Jumping','Curling','Snowboarding','Rugby','Short Track Speed Skating','Skeleton',
'Lacrosse','Polo','Cricket','Racquets','Motorboating','Military Ski Patrol','Croquet','Jeu De Paume','Roque','Alpinism','Basque Pelota','Aeronautics']

l=list()


data_sports_array=[0 for i in range(66)]
count=1
for i in range(66):
    data_sports_array[i]=count
    count=count+1

list_of_sports.sort()

list_of_special=['/','!','@','#','$','%','^','&','*','(',')','{','}','[',']','?',':',';','>','<',',','.','+','=','_','-']

TOKEN='869534639:AAFoKe5FvlHRizj2jnaxGTPcc1jgfG_Xljw'
bot=telebot.TeleBot(TOKEN)


@ bot.message_handler(commands=['start','go'])
def start_handler(message):
    bot.send_message(message.chat.id,'hello i am an telegram chatbot')
    
@bot.message_handler(commands=['startprediction'])
def predictions(message):
    msg=bot.send_message(message.chat.id,'please the details of an athlete in order to predict ')
    msg=bot.send_message(message.chat.id,'please enter height')
    bot.register_next_step_handler(msg,height)

def height(message):
    chat_id=message.chat.id
    text=message.text
    if( not text.isdigit()):
        msg=bot.send_message(message.chat.id,'Height must be numeric')
        bot.register_next_step_handler(msg,height)
    else:
        if(int(text)<127 or int(text)>226):
            msg=bot.send_message(message.chat.id,'Invalid height!(not in range of 127-226 cm')
            bot.register_next_step_handler(msg,height)
        else:   
            l.append(int(text))
            msg=bot.send_message(message.chat.id,'Please enter weight')
            bot.register_next_step_handler(msg,weight)
        

def weight(message):
    chat_id=message.chat.id
    text=message.text
    if( not text.isdigit()):
        msg=bot.send_message(message.chat.id,'Weight must be numeric')
        bot.register_next_step_handler(msg,weight)
    else:
        if(int(text)>214 or int(text)<25):
             msg=bot.send_message(message.chat.id,'Invalid weight!(not in range of 25-214 kg)')
             bot.register_next_step_handler(msg,weight)
        else:   
            l.append(int(text))
            msg=bot.send_message(message.chat.id,'Please enter age')
            bot.register_next_step_handler(msg,age)

def age(message):
    chat_id=message.chat.id
    text=message.text
    if( not text.isdigit()):
        msg=bot.send_message(message.chat.id,'Age must be numeric')
        bot.register_next_step_handler(msg,age)
    else:
        if(int(text)>97 or int(text)<10):
            msg=bot.send_message(message.chat.id,'Invalid Age(not in range of 10-97 years')
            bot.register_next_step_handler(msg,age)
        else:    
            l.append(int(text))
            msg=bot.send_message(message.chat.id,'Please enter sport')
            bot.register_next_step_handler(msg,sport)

def sport(message):
    chat_id=message.chat.id
    text=message.text
    if(text.isdigit()):
        msg=bot.send_message(message.chat.id,'Sport cannot be numeric')
        bot.register_next_step_handler(msg,sport)
    else:
        flag=0
        for k in list_of_special:
            if(k in text and flag==0):
                flag=1
        if(flag==1):
            msg=bot.send_message(message.chat.id,'Sport cannot have special characters')
            bot.register_next_step_handler(msg,sport)
        else:
            flag=0
            count=0
            for i in list_of_sports:
                if(i.upper()==text.upper()):
                    flag=1;
                    l.append(data_sports_array[count])
                count=count+1
            if(flag==0):
                msg=bot.send_message(message.chat.id,'Invalid Sport')
                bot.register_next_step_handler(msg,sport)
            else:                
                msg=bot.send_message(message.chat.id,'Please enter region')
                bot.register_next_step_handler(msg,region)
    
def region(message):
    chat_id=message.chat.id
    text=message.text
    if(text.isdigit()):
        msg=bot.send_message(message.chat.id,'Region cannot be numeric')
        bot.register_next_step_handler(msg,region)
    else:
        flag=0
        count=0
        for i in range (209):
            if(text == (list_of_regions[i]) and flag==0):
                flag=1
                l.append(list_of_regions_array[i])
            count=count+1
        if(flag==0):
            msg=bot.send_message(message.chat.id,'Region not found')
            bot.register_next_step_handler(msg,region)
        else:
            msg=bot.send_message(message.chat.id,'Please enter season')
            bot.register_next_step_handler(msg,season)

def season(message):
    chat_id=message.chat.id
    text=message.text
    if(text.isdigit()):
        msg=bot.send_message(message.chat.id,'Season cannot be numeric')
        bot.register_next_step_handler(msg,season)
    else:
        if(text.upper()!='WINTER' and text.upper()!='SUMMER'):
            msg=bot.send_message(message.chat.id,'Invalid Season(Season can be either Winter or Summer')
            bot.register_next_step_handler(msg,season)
        else:
            if(text.upper()=='WINTER'):
                l.append(1)
            elif(text.upper()=='SUMMER'):
                l.append(0)
            msg=bot.send_message(message.chat.id,'Please enter the gender of the athelete')
            bot.register_next_step_handler(msg,sex)
            
def sex(message):
    chat_id=message.chat.id
    text=message.text
    if(text.isdigit()):
        msg=bot.send_message(message.chat.id,'Gender cannot be numeric')
        bot.register_next_step_handler(msg,sex)
    else:
        if(text.upper()!='MALE' and text.upper()!='FEMALE'):
            msg=bot.send_message(message.chat.id,'Invalid Season(Gender can be either male or female')
            bot.register_next_step_handler(msg,sex)
        else:
            if(text.upper()=='MALE'):
                l.append(1)
            else:
                l.append(0)
            print(l)
            msg=bot.send_message(message.chat.id,'Thanks for the details, please allow me to process the information')
            model=load_model('simple.h5')
            l2=list()
            l2.append(l)
            labels=['Height','Weight','Age','Sport','Region','Season','Sex']
            l2=pd.DataFrame(l2,columns=labels)
            print(l2)
            pr=model.predict_proba(l2)
            print(pr)
            max_of_list=max(max(pr))
            min_of_list=min(min(pr))
            l3=list()
            for i in range(4):
                l3.append((pr[0][i]-min_of_list)/(max_of_list-min_of_list))

            sum_of_list3=sum(l3)
            for i in range(4):
                l3[i]=l3[i]/sum_of_list3
            
            
            print(l3)
            index=0
            if(l3[1]>l3[2] and l3[1]>l3[3]):
                index=1
            if( l3[2]>l3[1] and l3[2]>l3[3]):
                index=2
            if( l3[3]>l3[2] and l3[3]>l3[1]):
                index=3
            if(l3[1]==0 and l3[2]==0 and l3[3]==0):
                index=0

            if(index==0):
                st="Sorry the player has zero probability of winning a medal in the upcoming olympics"
            elif(index==1):
                st="The athlete has the greatest probability of winning a gold medal at "+((str)(round(l3[1],2)))
            elif(index==2):
                st="The athlete has the greatest probability of winning a silver medal at "+((str)(round(l3[2],2)))
            elif(index==3):
                st="The athlete has the greatest probability of winning a bronze medal at "+((str)(round(l3[3],2)))
            
            msg=bot.send_message(message.chat.id,st)

    

@ bot.message_handler(content_types=['text'])
def text_handler(message):
    text=message.text.lower()
    chat_id=message.chat.id
    if text == 'hello':
        bot.send_message(chat_id,'Hello i am a bot')
    elif text == "how are you":
        bot.send_message(chat_id,'mind your own business lol')
    else:
        bot.send_message(chat_id,'Sorry i did not understand')




bot.polling()


