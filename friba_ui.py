import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as font
from PIL import ImageTk
import sqlite3

#constants
bgcolor = "#34495E"

#hae turnausten nimet
def hae_turnaus():
    connection = sqlite3.connect("friba.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT name FROM Events;")
    turnaus = cursor.fetchall()
    connection.close()
    return turnaus

#tulosta turnauksen osallistujat
def hae_turnaustiedot(nykyvalinta):
    tunnus = (nykyvalinta,)
    query = '''
        SELECT
            Events.ScheduleDate AS Pvm,
            Courses.Name AS Rata,
            Courses.Holecount,
            Players.FirstName AS Etunimi,
            Players.LastName AS Sukunimi,
            Scores.Score AS Pisteet
        FROM
            Events
        INNER JOIN Courses ON Courses.CourseID = Events.CourseID
        INNER JOIN Participants ON Participants.EventID = Events.EventID
        INNER JOIN Players ON Players.PlayerID = Participants.PlayerID
        INNER JOIN Scores ON Scores.PlayerID = Participants.PlayerID
        WHERE Events.Name = ?;
    '''
    connection = sqlite3.connect("friba.db")
    cursor = connection.cursor()
    cursor.execute(query, tunnus)
    osallistujat = cursor.fetchall()
    osallistujat.sort(key = lambda x: x[5], reverse=True)
    connection.close()
    return osallistujat

def hae_pelaajat():
    query = '''
        SELECT 
            *
        FROM
            Players;
    '''
    connection = sqlite3.connect("friba.db")
    cursor = connection.cursor()
    cursor.execute(query)
    osallistujat = cursor.fetchall()
    osallistujat.sort(key = lambda x: x[0])
    connection.close()
    return osallistujat

def hae_radat():
    query = '''
        SELECT 
            *
        FROM
            Courses;
    '''
    connection = sqlite3.connect("friba.db")
    cursor = connection.cursor()
    cursor.execute(query)
    radat = cursor.fetchall()
    radat.sort(key = lambda x: x[0])
    connection.close()
    return radat

def lisaa_pelaaja():
    
    def pelaajalisays():
        query = '''
            INSERT INTO Players
            (FirstName, LastName, Handicap)
            VALUES (?, ?, ?);
        '''
        tiedot = (fn_entry.get(), ln_entry.get(), int(hc_entry.get()),)
        print("lisäysvaluet", tiedot)
        connection = sqlite3.connect("friba.db")
        cursor = connection.cursor()
        cursor.execute(query, tiedot)
        connection.commit()
        connection.close()
        

    lisaa_otsikko = tk.Label(contentwindow, text="Uusi Pelaaja:", bg=bgcolor, fg="white")
    lisaa_otsikko.pack(side="top")

    fn_text = tk.Label(contentwindow, text="Etunimi", bg=bgcolor, fg="white")
    fn_entry = Entry(contentwindow, width=25)

    ln_text = tk.Label(contentwindow, text="Sukunimi", bg=bgcolor, fg="white")
    ln_entry = Entry(contentwindow, width=25)
    
    hc_text = tk.Label(contentwindow, text="Handicap", bg=bgcolor, fg="white")
    hc_entry = Entry(contentwindow, width=25)

    fn_text.pack(side="left")
    fn_entry.pack(side="left")

    ln_text.pack(side="left")
    ln_entry.pack(side="left")

    hc_text.pack(side="left")
    hc_entry.pack(side="left")
    

    vahvista = tk.Button(
        contentwindow,
        text="lisää Pelaaja",
        command=pelaajalisays,
    )
    vahvista.pack(side='top', padx=5)

    

#pääframe    
def lataa_mainwindow():

    #prevent child modifying parent
    mainwindow.pack_propagate(False)

    #logo
    logo_img = ImageTk.PhotoImage(file="logo.png")
    logo_widget = tk.Label(mainwindow, image=logo_img, bg=bgcolor)
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)

    #Otsikko
    tk.Label(
        mainwindow,
        text    = "Frisbeegolf Turnaukset",
        bg      = bgcolor,
        fg      = "white",
        font    = ("Consolas", 20)
        ).pack()

    #nappula1
    valikko_fontti = font.Font(family='Consolas', size=12)
    nykvalinta = StringVar()
    nykvalinta.set("Valitse turnaus")
    turnausvalinnat = OptionMenu(
        mainwindow,
        nykvalinta,
        *kaikki_turnaukset,
        command=lataa_contentwindow
        )
    turnausvalinnat['font'] = valikko_fontti
    turnausvalinnat.pack(pady=5)

    teksti = tk.Label(
        mainwindow,
        text="kaikki:",
        bg = bgcolor,
        fg = "white",
        font = ("Consolas", 15, 'bold')
    )
    teksti.place(x=50, y=140)

    nappi_fontti = font.Font(family='Consolas', size=10)
    #nappula2 
    pelaajat = Button(
        mainwindow,
        text = "Pelaajat",
        command=lataa_pelaajawindow
        )
    pelaajat['font'] = nappi_fontti
    pelaajat.place(x=55,y=165)

    #nappula3
    radat = Button(
        mainwindow,
        text = "Radat",
        command=lataa_ratawindow
        )
    radat['font'] = nappi_fontti
    radat.place(x=55,y=195)

def tyhjenna_tiedot(kentta):
    for data in kentta.winfo_children():
        data.destroy()

def lataa_contentwindow(valinta):
    tyhjenna_tiedot(contentwindow)
    tulostus_data = ttk.Treeview(contentwindow)
    #kentät
    tulostus_data['columns'] = ("pvm", "Etunimi", "Sukunimi", "Pisteet")
    #format columns, anchor=W(west,vasen reuna)
    tulostus_data.column("#0", width = 0, stretch=NO)
    tulostus_data.column("pvm", anchor=W, width = 120)
    tulostus_data.column("Etunimi", anchor=W, width = 120)
    tulostus_data.column("Sukunimi", anchor=W, width = 120)
    tulostus_data.column("Pisteet", anchor=CENTER, width = 120)
    #Otsikot
    tulostus_data.heading("#0", text="", anchor=W)
    tulostus_data.heading("pvm", text="Päivämäärä", anchor=W)
    tulostus_data.heading("Etunimi", text="Etunimi", anchor=W)
    tulostus_data.heading("Sukunimi", text="Sukunimi", anchor=W)
    tulostus_data.heading("Pisteet", text="Pisteet", anchor=CENTER)

    #lisää tiedot
    tiedot = hae_turnaustiedot(valinta)
    idx = 0
    for tieto in tiedot:  
        tulostus_data.insert(parent='', index='end', iid=idx, text="", values=(tieto[0], tieto[3], tieto[4], tieto[5]))
        idx += 1
    radan_fontti = font.Font(family='Consolas', size=15, weight='bold')
    radan_nimi = tk.Label(
        contentwindow,
        text = f"Rata: {str(tieto[1])}\n Väyliä: {tieto[2]}",
        bg = bgcolor,
        fg = "white"
        )
    radan_nimi['font'] = radan_fontti
    radan_nimi.pack()
    tulostus_data.pack()

def lataa_pelaajawindow():
    tyhjenna_tiedot(contentwindow)
    pelaajat_data = ttk.Treeview(contentwindow)
    #kentät
    pelaajat_data['columns'] = ("Playerid", "Etunimi", "Sukunimi", "Handicap")
    pelaajat_data.column("#0", width = 0, stretch=NO)
    pelaajat_data.column("Playerid", anchor=W, width = 120)
    pelaajat_data.column("Etunimi", anchor=W, width = 120)
    pelaajat_data.column("Sukunimi", anchor=W, width = 120)
    pelaajat_data.column("Handicap", anchor=W, width = 120)
    
    #Otsikot
    pelaajat_data.heading("#0", text="", anchor=W)
    pelaajat_data.heading("Playerid", text="Pelaajatunnus", anchor=W)
    pelaajat_data.heading("Etunimi", text="Etunimi", anchor=W)
    pelaajat_data.heading("Sukunimi", text="Sukunimi", anchor=W)
    pelaajat_data.heading("Handicap", text="Handicap", anchor=W)
    
    tiedot = hae_pelaajat()
    idx = 0
    for tieto in tiedot:  
        pelaajat_data.insert(parent='', index='end', iid=idx, text="", values=(tieto[0], tieto[1], tieto[2], tieto[3]))
        idx += 1
    pelaajat_data.pack(pady=5)

    lisaa_pelaaja()


def lataa_ratawindow():
    tyhjenna_tiedot(contentwindow)
    radat_data = ttk.Treeview(contentwindow)
    #kentät
    radat_data['columns'] = ("Ratatunnus", "Nimi", "HoleCount", "CoursePar", "CourseRating", "BogeyRating", "SlopeRating" )
    radat_data.column("#0", width = 0, stretch=NO)
    radat_data.column("Ratatunnus", anchor=W, width = 120)
    radat_data.column("Nimi", anchor=W, width = 120)
    radat_data.column("HoleCount", anchor=W, width = 120)
    radat_data.column("CoursePar", anchor=W, width = 120)
    radat_data.column("CourseRating", anchor=W, width = 120)
    radat_data.column("BogeyRating", anchor=W, width = 120)
    radat_data.column("SlopeRating", anchor=W, width = 120)

    radat_data.heading("#0", text="", anchor=W)
    radat_data.heading("Ratatunnus", text="Ratatunnus", anchor=W)
    radat_data.heading("Nimi", text="Nimi", anchor=W)
    radat_data.heading("HoleCount", text="Väyliä", anchor=W)
    radat_data.heading("CoursePar", text="Par",anchor=W)
    radat_data.heading("CourseRating", text="Rata-Rating", anchor=W)
    radat_data.heading("BogeyRating", text="Bogey-Rating", anchor=W)
    radat_data.heading("SlopeRating", text="Slope-Rating", anchor=W)

    radat = hae_radat()
    idx = 0
    for tieto in radat:  
        radat_data.insert(parent='', index='end', iid=idx, text="", values=(tieto[0],tieto[1],tieto[2],tieto[3],tieto[4],tieto[5],tieto[6]))
        idx += 1
    radat_data.pack()

    


#init app
app = tk.Tk()
#title
app.title("Turnaussovellus")
#center app window (tcl - tkinter :: windowmethod . top level, center)
app.eval("tk::PlaceWindow . center")
#deny resize
app.resizable(False,False)
#turnaukset
kaikki_turnaukset = hae_turnaus()
kaikki_turnaukset = ["".join(ele) for ele in kaikki_turnaukset]
#pelaajat
kaikki_pelaajat = hae_pelaajat()


#frames (appname,leveys,korkeus,tausta)
mainwindow = tk.Frame(app, width=900, height=700, bg=bgcolor)
contentwindow = tk.Frame(app, bg=bgcolor)
lisayswindow = tk.Frame(app, bg=bgcolor)

mainwindow.grid(row=0, column=0)
contentwindow.grid(row=0, column=0)
lisayswindow.grid(row=1,column=0)


#header content
lataa_mainwindow()
#mainloop
app.mainloop()