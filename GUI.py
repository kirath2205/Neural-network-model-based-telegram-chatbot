
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #to display plots in tkinter
from matplotlib.figure import Figure
import webbrowser #to open dash
sb.set()
from tkinter import * #tkinter is a standard GUI library
import tkinter
##first clean the data

data=pd.read_csv('athlete_events.csv')
j=pd.read_csv('athlete_events.csv')

data_NOC_unique=data['NOC'].unique()

data_countries=pd.DataFrame(data['Team'])

data['NOC']=data['NOC'].replace(['RUS','URS'],'EUN')

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




data=data.drop(columns="Games")

#replacing Male with 1 and female 0

data['Sex'] = data['Sex'].replace('M',1)
data['Sex'] = data['Sex'].replace('F',0)

#replacing summer with 1 and winter with 0

data['Season']=data['Season'].replace('Summer',1)
data['Season']=data['Season'].replace('Winter',0)

#replacing gold with 1, silver with 2 , bronze with 3 , NaN with 0
data['Medal']=data['Medal'].replace('Gold',1)    
data['Medal']=data['Medal'].replace('Silver',2)
data['Medal']=data['Medal'].replace('Bronze',3)

data['Medal'] = data.Medal.fillna(0).astype(int)
data['Age']=data.Age.fillna(24).astype(float)
data['Height']=data.Height.fillna(150).astype(int)
data['Weight']=data.Weight.fillna(70).astype(int)
data.describe()
data=data.drop(columns=['City','Event','Team'])

data['Season']=data['Season'].astype('category')
data['Sex']=data['Sex'].astype('category')
data['Year']=data['Year'].astype('category')
data['Sport']=data['Sport'].astype('category')
data['Sex']=data['Sex'].astype('category')
data_NOC=pd.read_csv('noc_regions.csv')
data_NOC_unique=data['NOC'].unique()

data['Height'][(data['Height']==0)&(data['Weight']==0)&(data['Sex']==1)]=179
data['Height'][(data['Height']==0)&(data['Weight']==0)&(data['Sex']==0)]=168
data['Height'][(data['Weight']>=83)&(data['Height']==0)&(data['Sex']==1)]=185
data['Height'][(data['Weight']>=65)&(data['Height']==0)&(data['Sex']==0)]=173
data['Height'][(data['Weight']<=67)&(data['Height']==0)&(data['Sex']==1)]=172
data['Height'][(data['Weight']<=54)&(data['Height']==0)&(data['Sex']==0)]=162
data['Height'][(data['Weight']<83)&(data['Weight']>67)&(data['Height']==0)&(data['Sex']==1)]=179
data['Height'][(data['Weight']<65)&(data['Weight']>54)&(data['Height']==0)&(data['Sex']==0)]=168


data['Weight'][(data['Height']==0)&(data['Weight']==0)&(data['Sex']==1)]=74
data['Weight'][(data['Height']==0)&(data['Weight']==0)&(data['Sex']==0)]=59
data['Weight'][(data['Height']>=185)&(data['Weight']==0)&(data['Sex']==1)]=83
data['Weight'][(data['Height']>=173)&(data['Weight']==0)&(data['Sex']==0)]=65
data['Weight'][(data['Height']<=172)&(data['Weight']==0)&(data['Sex']==1)]=67
data['Weight'][(data['Height']<=162)&(data['Weight']==0)&(data['Sex']==0)]=54
data['Weight'][(data['Height']<185)&(data['Height']>172)&(data['Weight']==0)&(data['Sex']==1)]=74
data['Weight'][(data['Height']<173)&(data['Height']>162)&(data['Weight']==0)&(data['Sex']==0)]=59

#######################################################################
##Data Cleaning done
##Data Cleaning will result in a few warnings, GUI will still work the same

##Defining a few functions
#this function is to plot the specific boxplots
def get_sport_dataset(i): ## Uses input "Sport" and get 4 jointDataFrame 
    dataset = data[(data.Sport == i)]
    dataset_male = dataset[(dataset.Sex == 1)]
    dataset_male_height = pd.DataFrame(dataset_male['Height'])
    dataset_male_weight = pd.DataFrame(dataset_male['Weight'])
    dataset_male_medal = pd.DataFrame(dataset_male['Medal'])
    male_weight_medalDF = pd.concat([dataset_male_weight, dataset_male_medal], axis = 1, join_axes = [dataset_male_weight.index])
    male_height_medalDF = pd.concat([dataset_male_height, dataset_male_medal], axis = 1, join_axes = [dataset_male_height.index])
    
    dataset_female = dataset[(dataset.Sex == 0)]
    dataset_female_height = pd.DataFrame(dataset_female['Height'])
    dataset_female_weight = pd.DataFrame(dataset_female['Weight'])
    dataset_female_medal = pd.DataFrame(dataset_female['Medal'])
    female_weight_medalDF = pd.concat([dataset_female_weight, dataset_female_medal], axis = 1, join_axes = [dataset_female_weight.index])
    female_height_medalDF = pd.concat([dataset_female_height, dataset_female_medal], axis = 1, join_axes = [dataset_female_height.index])
   #returns jointdataframe of medals and male_height male_weight female_height female_weight
    return male_weight_medalDF,male_height_medalDF,female_weight_medalDF,female_height_medalDF

#this function is to plot the specific pie chart
def get_dominant(sport):## uses input "Sport" and get the top 3 most dominant countries
    dom_dataset = data[(data.Sport == sport)]
    medalist = dom_dataset[(dom_dataset.Medal == 1)|(dom_dataset.Medal == 2)|(dom_dataset.Medal == 3)]
    country = pd.DataFrame(medalist['NOC'])
    most_dominant = country.mode()
    top3 = pd.value_counts(medalist['NOC'].values, sort=True).head(3)
    #returns top 3 most dominant countries and total no. of medals won
    return top3,medalist["ID"].nunique()

##From here down is for tkinter
#####################################################################################################################

#this code is basically for the main/menu window containing the buttons
#depending on what button you press, different windows will appear
class Window(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Data Visualisation Tool")
        self.pack(fill=BOTH, expand=1) #adjusting the window size so that the GUI will adjust to fit if expanded
        #command is if clicked do...  client_exit is defined by us
        #so if you click the Quit button, client_exit will run
        quitButton = Button(self, text="Quit", command=self.client_exit)#Button is imported from tkinter
        quitButton.place(x=0, y=0)

        main_heading = Label(self, text="Welcome to our Data Visualisation Tool",font = ("arial",20,"bold")).pack()
        #this 3 below use dash
        heading_scatter = Label(self, text="For the Height and Weight Scatterplot: ",font = ("arial",15,"bold")).place(x=100,y=80)
        scatterheightweightButton = Button(self, text="CLICK HERE", command = self.open_dash).place(x=470, y=83)

        header_top3barchart = Label(self, text="For the bar chart for the Top 3 Countries: ",font = ("arial",15,"bold")).place(x=100,y=120)
        topthreecountriesButton = Button(self, text="CLICK HERE", command = self.open_dash).place(x=500, y=123)

        heading_noofathletes = Label(self, text="For the bubble plot for the number of athletes: ",font = ("arial",15,"bold")).place(x=100,y=160)
        noofathletesButton = Button(self, text="CLICK HERE", command = self.open_dash).place(x=545, y=163)
        #basically above 3 buttons do the same function: open the dash webpage

        #this 2 below use tkinter do display the plots
        
        #first one for height/weight and medal boxplot
        heading_hwm = Label(self, text="For the Height and Weight Boxplot",font = ("arial",15,"bold")).place(x=100,y=200)
        sportinputlabel_hwm = Label(self, text='Enter the sport:', font=("arial",10)).place(x=110,y=225)
        name = StringVar()
        entry_box_hwm = Entry(self, textvariable = name, width=25).place(x=208,y=228)
        #this function will take in the sport user input and open up a window displaying the boxplot
        def display_boxplot():
            sportname = str(name.get())#sportname takes in the sport the user puts in
            malew,maleh,femalew,femaleh = get_sport_dataset(sportname)#getting the 4 joint dataframe
            ## get the dataset first then initialise a new window

            boxplot = Tk()
            boxplot.geometry("1280x960") #this is recommending resolution so that the titles won't overlap each other
            #basically like we learn in jupyter, plot 4 boxplots 2x2
            f, axes = plt.subplots(2, 2, figsize=(70, 70))
            sb.boxplot(x = "Weight", y = "Medal",data = malew, orient = "h",ax=axes[0,0]).set_title("Male Athletes")
            sb.boxplot(x = "Height", y = "Medal", data = maleh, orient = "h",ax=axes[0,1]).set_title("Male Athletes")
            sb.boxplot(x = "Weight", y = "Medal",data = femalew, orient = "h",ax=axes[1,0]).set_title("Female Athletes")
            sb.boxplot(x = "Height", y = "Medal", data = femaleh, orient = "h",ax=axes[1,1]).set_title("Female Athletes")
            #this is what tkinter use to display the plots
            canvas = FigureCanvasTkAgg(f, master=boxplot)  # A tk.DrawingArea.
            canvas.draw()
            canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
            boxplot.mainloop()
            
        #code for the button
        #if this button pressed, display_boxplot will run
        enter = Button(self, text="Enter", command=display_boxplot).place(x=365,y=227)

        #second one for most dominant country for a sport piechart
        heading_mostdom = Label(self, text="To see the most dominant countries for a sport",font = ("arial",15,"bold")).place(x=100,y=260)
        sportinputlabel_mostdom = Label(self, text='Enter the sport:', font=("arial",10)).place(x=110,y=285)
        secondname = StringVar()
        entry_box_mostdom = Entry(self, textvariable = secondname, width=25).place(x=208,y=288)
        def display_dominant():
            #calculating the pie slices
            sportname = str(secondname.get())
            top3,totalcount = get_dominant(sportname)
            
            countries = top3.index#countries[0] will be most dominant [1] 2nd most...
            count = top3 
            #code below is to calculate the percentage of medals that the individual countries won
            first = countries[0]
            firstpercentage = count[0]/totalcount*100
            
            second = countries[1]
            secondpercentage = count[1]/totalcount*100

            third = countries[2]
            thirdpercentage = count[2]/totalcount*100

            percentage = ((count[0] + count[1] + count[2])/totalcount) #top 3 countries slice
            counter = 1 - percentage #rest of countries slice
            
            slices = [percentage,counter] 
            countries = [first+" "+second+" "+third,"All other countries"]
            colors = ['r', 'b']

            #initialising the app
            dominant = Tk()
            dominant.geometry("1280x960")
            #plotting piechart
            f, axes = plt.subplots(1, 1, figsize=(70, 70))
            plt.pie(slices, labels=countries, colors=colors, startangle=90, autopct='%.1f%%')
            #displaying the piechart;
            canvas = FigureCanvasTkAgg(f, master=dominant)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
            firstlabel = Label(dominant, text="The most dominant country is "+str(first)+" winning "+str(round(firstpercentage, 2))+"% of the total medals").place(x=50,y=100)
            secondlabel = Label(dominant, text="The second most dominant country is "+str(second)+" winning "+str(round(secondpercentage, 2))+"% of the total medals").place(x=50,y=130)
            thirdlabel = Label(dominant, text="The third most dominant country is "+str(third)+" winning "+str(round(thirdpercentage, 2))+"% of the total medals").place(x=50,y=160)
            dominant.mainloop()
        #code for the button
        #if this button pressed display_dominant will run
        enter_second = Button(self, text="Enter", command=display_dominant).place(x=365,y=287)
        
    #if press exit then exit
    def client_exit(self):
        exit()
    #if press any of the top 3 buttons, open dash app. Make sure to run the dash code first
    def open_dash(self):
        webbrowser.open("http://localhost:9999") #once run the dash code, this will open up a browser with the dash visualisation
   

## main window/menu interface   
main = Tk()
main.geometry("800x400") #defining size for window
app = Window(main)

main.mainloop()
