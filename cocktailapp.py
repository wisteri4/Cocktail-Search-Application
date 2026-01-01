#Cocktail Application - Izabel Mabulay Javier 
from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
import requests
import io 
        
class CocktailAPI:
    #------------------------ Drink Format ----------------------------------
    def display_drink(self, parent, data): 
        #the default format of searched drinks
        drink_name = data["drinks"][0]['strDrink']
        drink_image_url = data["drinks"][0]['strDrinkThumb']
        drink_id = data["drinks"][0]['idDrink']
        instructions = data["drinks"][0]['strInstructions']
        category = data["drinks"][0]['strCategory']
        alc = data["drinks"][0]['strAlcoholic']
        
        img_response = requests.get(drink_image_url)
        img_data = img_response.content
    
        pil_image = Image.open(io.BytesIO(img_data))
        pil_image = pil_image.resize((250, 250))
    
        tk_image = ImageTk.PhotoImage(pil_image)
    
        parent.searchresults.drink_image = tk_image
    
        showthemdrink = f"""
        \nDrink name: {drink_name}
        \nDrink ID: {drink_id}
        \nCategory: {category}
        \nType of drink: {alc}\n"""

        for i in range(1,17): #for the amount of ingredients and measurements ranging from 1 - 17
            ingredient = data["drinks"][0].get(f"strIngredient{i}")
            measure = data["drinks"][0].get(f"strMeasure{i}") 
    
            if ingredient:
                showthemdrink += (f"\n- {ingredient}: {measure}") #Add the values in this format 
            
        showthemdrink += f"\n\nInstructions:\n{instructions}"  # Add the instructions in this format
    
        parent.cocktailoutput.insert("1.0", showthemdrink) 
    
        img_label = Label(parent.searchresults, image =tk_image, bg="#3A0519")
        img_label.grid(row=0, column=0, padx=10) 
        
        
    # ------------------------- Random Drink --------------------------------------
    def get_random_drink(self, parent): 
        parent.showresults()
        url ="https://www.thecocktaildb.com/api/json/v1/1/random.php" # Random is already in the link itself
        response = requests.get(url)
        data = response.json()
        self.display_drink(parent, data)
    
    # ---------------------------ID AND NAME FIND -----------------------------------------
    def searchby(self, parent):
        selected = parent.studentcombo.get() 
        lookitup = parent.cocktailentry.get()
        
        if selected == "ID":
            if not lookitup.isdigit(): 
                messagebox.showerror("Invalid ID", "Drink ID must be numeric")
                return
            searchby_combo = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={lookitup}" 
        elif selected == "Name": 
            
            accentwords = ["Frosé", "Frappé", "Autodafé"]
            if lookitup in accentwords:
                lookitup.replace("é", "e")
                 
            searchby_combo = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={lookitup}"
        else:
            messagebox.askretrycancel("Invalid Name", "Enter a valid Drink Name or ID")
            return
            
        response = requests.get(searchby_combo)
        data = response.json()
        
        if not data.get("drinks"):
            messagebox.askretrycancel("Nope", "Drink is non-existent")
            return
        
        parent.showresults()
        self.display_drink(parent, data) 
    
    # ----------------------------- Find Drink in Category ------------------------------------
    def categories(self, category, parent):
        parent.listofdrinks()

        categ_url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?c={category}"
        response = requests.get(categ_url)
        data = response.json()
        
        listofdrinks = data.get("drinks")
    
        if listofdrinks: 
            for num, drink in enumerate(listofdrinks): #This area is ai assisted with displaying the list of drinks
                parent.labelfordrink = Label(parent.frame2scroll, text= drink["strDrink"], 
                font=("Times New Roman", "15"), bg="#3A0519", 
                fg="white", cursor='hand1')
                parent.labelfordrink.bind('<Button-1>', lambda f, 
                                          drin = drink["strDrink"]: self.picked_drink(drin, parent))
                parent.labelfordrink.grid(row=num + 1, column=1, pady=10, sticky='nw')
    
    # -------------------------Display the clicked drink ------------------------------
    def picked_drink(self, inputdrink, parent): 
        
        accentwords = ["Frosé", "Frappé", "Autodafé"]
        
        if inputdrink in accentwords:
            inputdrink.replace("é", "e")
        
        url_drink = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={inputdrink}"
            
        response = requests.get(url_drink)
        data = response.json()
        
        if not data.get("drinks"):
            messagebox.showinfo("Sorry", "We do not have the drink at the moment")
            return
    
        parent.showresults()
        self.display_drink(parent, data) 
        
# ------------------- Display widgets and Parent Class ----------------------------
class design(Tk):
    #Object oriented programming reference from https://www.youtube.com/watch?v=zstcMt9_80w 
    def __init__(self):
        super().__init__()
        self.geometry("900x700")
        self.title('Drink Search')
        self.resizable(False,False)
        self.api = CocktailAPI() 
        #set instance of the api class to the parent class
        
        #Image Background for main 
        self.getimage = Image.open("swirlbg.jpg")
        self.pil_image = self.getimage.resize((900, 900))
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
        self.background_label = Label(self, image=self.tk_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        #------------------ Frame for search widgets ---------------------------
        self.frame1 = Frame(self, bg="#3A0519")
        self.frame1.pack(side="left", fill= "both", padx=60)
        self.titlelabel = Label(self.frame1, text="Search your Drink", 
                       font=("Times New Roman", "20", 'bold', 'italic'), bg="#3A0519", fg="white")
        self.titlelabel.pack(pady=30, padx= 30)
    
        self.randombutton = Button(self.frame1, text="Random drink", 
                          font=("Times New Roman", "12"), bg="#3A0519", fg="white", 
                          command= lambda: self.api.get_random_drink(self), cursor='hand1')
        self.randombutton.pack(pady=10)
    
        type = ["ID", "Name"]
        # stringredient1, idDrink, strDrink 
        self.studentcombo = ttk.Combobox(self.frame1, values=type, 
                            font=("Times New Roman", "12"), cursor='hand1')
        self.studentcombo.set("Search By")
        self.studentcombo.pack(pady=10)   
    
        self.cocktailentry = Entry(self.frame1, font=("Times New Roman", "12"), cursor='hand1')
        self.cocktailentry.pack(pady=10)
    
        self.submitbutton = Button(self.frame1, text="Submit",
                                   font=("Times New Roman", "12"), cursor='hand1', bg="#3A0519", fg="white", 
                                   command= lambda: self.api.searchby(self))
        self.submitbutton.pack(pady=10)
        
        #--------------------- Category Window -------------------------
        self.frame2 = Frame(self, bg="#3A0519")
        self.frame2.pack(side= "right", expand="y")
        self.alcoholcheck  = Checkbutton(self.frame2, text="Alcoholic", font=("Times New Roman", "12"), 
                        bg="#670D2F", fg="white")
        
        self.categorylabel = Label(self.frame2, text="Category", 
                       font=("Times New Roman", "20", 'bold', 'italic'), bg="#3A0519", fg="white")
        self.categorylabel.pack(pady=30)
        
        #list of categories
        listofcateg = ["Beer", "Cocktail", "Cocoa", "Coffee / Tea", "Homemade Liqueur", 
                       "Ordinary Drink", "Other / Unknown","Punch / Party Drink", "Shake", "Shot", "Soft Drink"]
        
        for categs in listofcateg:
            self.labelforcateg = Label(self.frame2, text=categs, 
                font=("Times New Roman", "15"), bg="#3A0519", 
                fg="white", cursor='hand1')
            self.labelforcateg.bind('<Button-1>', lambda f, cat=categs: self.api.categories(cat, self))
            #Use the category name to find the drink in function categories() in the COCKTAILAPI() class
            self.labelforcateg.pack(pady=10, padx=20, anchor='w')
        
    #-------- Window to display the results of search ------------------------------
    def showresults(self):
        self.searchresults = Toplevel(self)
        self.searchresults.title("Your Drink is served")
        self.searchresults.geometry("800x600")
        self.searchresults.resizable(False, False)
        self.searchresults['bg'] = '#3A0519'

        self.cocktailoutput = Text(self.searchresults,
                                   font=("Times New Roman", "12"),  bg="#670D2F", fg="white",
                                   width= 60, height= 28, wrap='word')
        self.cocktailoutput.grid(row=0, column=1)
        self.destorybutton = Button(self.searchresults, text="Back", font=("Times New Roman", "17"), 
                                    bg="#3A0519", fg="white", command=self.searchresults.destroy)
        self.destorybutton.grid(row=1, column=1)
    
    #----------------- Window to display List of drinks -------------------------------------------
    def listofdrinks(self):
        self.categors = Toplevel(self)
        self.categors.title("Category")
        self.categors.geometry("550x350")
        self.categors.resizable(False, False)
        self.categors['bg'] = '#670D2F'
        
        self.back = Button(self.categors, text="Back", font=("Times New Roman", "17"), 
                                    bg="#3A0519", fg="white", command=self.categors.destroy)
        self.back.grid(row=0, column=0) 
        
        #List of the drinks scroll bar reference https://youtu.be/0WafQCaok6g?si=BalV6JB7GEsbKOX3 
        self.canva = Canvas(self.categors, bg="#670D2F")
        self.canva['highlightbackground'] ='#670D2F'
        self.canva.grid(row=1, column=2, columnspan= 3, sticky="nsew")
        
        scrollon=Scrollbar(self.categors, orient='vertical', command=self.canva.yview) 
        scrollon.grid(row= 1, column=4, sticky ="ns")
        self.canva.config(yscrollcommand=scrollon.set)
        
        self.frame2scroll = Frame(self.canva, bg="#670D2F")
        
        self.canva.create_window((0,0), window = self.frame2scroll, anchor="nw")
        self.frame2scroll.bind('<Configure>', lambda e: self.canva.configure(scrollregion = self.canva.bbox("all")))
        
if __name__ == "__main__":
    mydrinkstore= design()
    mydrinkstore.mainloop()

