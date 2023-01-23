from tkinter.ttk import *
from tkinter import *
import tkinter.font as tkFont
from PIL import ImageTk, Image
from sqlite3 import *
from tkinter.messagebox import *

# ----------------------DataBase-------------------------------

conn = connect('Univs.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS universities(
                                                   univName TEXT NOT NULL ,
                                                   dept TEXT NOT NULL,
                                                   years INTEGER NOT NULL,
                                                   language text NOT NULL,
                                                   fees INTEGER NOT NULL,
                                                   langFees INTEGER NOT NULL,
                                                   PRIMARY KEY (univName, dept)
                                                   )""")

conn.commit()

# -----------------------------------------------------------------

root = Tk()
root.geometry('800x550')
root.title("Istanbul Foundation")
root.iconbitmap("devis/images/ist_found2.ico")

# ---------------Variables------------------------

fname = StringVar()
lname = StringVar()
passnumber = StringVar()
studFee = IntVar()
SelectedUniv = StringVar()
NameAgent = StringVar()

# ----------------------------Fonctions------------------------------
connection = connect('Univs.db')
cursor = connection.cursor()


def displayUniv(tab):
    data = cursor.execute("SELECT * FROM universities ")
    rows = data.fetchall()
    if len(rows) != 0:
        tab.delete(*tab.get_children())
        for row in rows:
            tab.insert('', 'end', values=row)
    else:
        tab.delete(*tab.get_children())
    connection.commit()


def insertUniv(Uname, Dname, yrs, lg, fee, lgfee):
    cursor.execute("INSERT INTO universities(UnivName, dept, years, language, fees, langFees) VALUES (?,?,?,?,?,?)",
                   (Uname, Dname, yrs, lg, fee, lgfee))


def SelectedRow(table):
    cursor = table.focus()
    content = table.item(cursor)
    row = content['values']
    return row


def getUniv():
    query = cursor.execute("SELECT univName, dept FROM universities").fetchall()
    li = []
    if len(query) != 0:
        for row in query:
            li.append(row[0] + " - " + row[1])
    return li


def araUniv(unidept):
    li = unidept.split(" - ")
    return li[0]


def araDept(unidept):
    li = unidept.split(" - ")
    return li[1]


def getFee(univ, dep):
    query = cursor.execute("SELECT fees FROM universities WHERE univname=? AND dept=?", (univ, dep,)).fetchone()
    return query[0]


def getLangFee(univ, dep):
    query = cursor.execute("SELECT langFees FROM universities WHERE univname=? AND dept=?", (univ, dep,)).fetchone()
    return query[0]


def univMan():
    new_window = Toplevel()
    new_window.title("Istanbul Foundation")
    new_window.geometry('1000x550')
    new_window.iconbitmap("devis/images/ist_found2.ico")

    # --------------------------------------------------------------------------
    newUniv = StringVar()
    newDept = StringVar()
    years = IntVar()
    SelectedLang = StringVar()
    fees = IntVar()
    lang_fees = IntVar()
    SelectedDept = StringVar()

    # ----------------------------------------------------------------------------

    def deptList():
        query = cursor.execute("SELECT upper(TRIM(dept)) FROM universities").fetchall()
        li = []
        if len(query) != 0:
            for row in query:
                li.append(row[0])
        return sorted(list(dict.fromkeys(li)))

    # -------------------------------------------------------------------------------
    frame1 = Frame(new_window, height=250, width=1000)
    frame1.grid(row=0, column=0)

    frame2 = Frame(new_window, height=300, width=1000)
    frame2.grid(row=1, column=0)

    # -------------------------------------------------------------------------------
    univName_lbl = Label(frame1, text="University :", font=label_font)
    univName_lbl.place(x=40, y=20)

    department_lbl = Label(frame1, text="Department :", font=label_font)
    department_lbl.place(x=530, y=20)

    yrs_lbl = Label(frame1, text="Years :", font=label_font)
    yrs_lbl.place(x=40, y=80)

    language_lbl = Label(frame1, text="Language :", font=label_font)
    language_lbl.place(x=530, y=80)

    fees_lbl = Label(frame1, text="Fees :", font=label_font)
    fees_lbl.place(x=40, y=140)

    languageFees_lbl = Label(frame1, text="Language Year  :\nFees ", font=label_font)
    languageFees_lbl.place(x=530, y=140)

    search_label = Label(frame1, text='Enter desired Departement :', font=label_font)
    search_label.place(x=100, y=200)

    # -------------------------------------------------------------------------------
    inputNewUniv = Entry(frame1, font=entrer_font, width=25, textvariable=newUniv)
    inputNewUniv.place(x=250, y=22)

    inputNewDept = Entry(frame1, font=entrer_font, width=25, textvariable=newDept)
    inputNewDept.place(x=720, y=22)

    inputYears = Entry(frame1, font=entrer_font, width=8, textvariable=years)
    inputYears.place(x=250, y=82)

    list_lang = ["EN", "TR", "(30%)EN"]
    inputLang = OptionMenu(frame1, SelectedLang, *list_lang)
    inputLang.place(x=720, y=82)

    inputFees = Entry(frame1, font=entrer_font, width=15, textvariable=fees)
    inputFees.place(x=250, y=142)

    inputLangFees = Entry(frame1, font=entrer_font, width=15, textvariable=lang_fees)
    inputLangFees.place(x=720, y=142)

    list_dept = deptList()
    search_input = OptionMenu(frame1, SelectedDept, *list_dept)
    search_input.place(x=400, y=200)

    def displayUnivSorted(tab):
        departement = SelectedDept.get()

        data = cursor.execute("SELECT * FROM universities WHERE upper(TRIM(dept)) = ?", (departement,))
        rows = data.fetchall()
        if len(rows) != 0:
            tab.delete(*tab.get_children())
            for row in rows:
                tab.insert('', 'end', values=row)
        else:
            tab.delete(*tab.get_children())
        connection.commit()

    def SortUniv():
        new_window1 = Toplevel()
        new_window1.title("Istanbul Foundation")
        new_window1.geometry('700x400')
        new_window1.iconbitmap("devis/images/ist_found2.ico")

        departement = SelectedDept.get()

        search_result_label = Label(new_window1, text="List of universities where you can study " + departement,
                                    font=label_font)
        search_result_label.place(x=30, y=30)

        tableUniv1 = Treeview(new_window1)
        tableUniv1['columns'] = ('univ', 'dept', 'yrs', 'lang', 'fees', 'langfees')
        tableUniv1.column('#0', width=0, stretch=NO)
        tableUniv1.column('univ', anchor=CENTER, width=200)
        tableUniv1.column('dept', anchor=CENTER, width=110)
        tableUniv1.column('yrs', anchor=CENTER, width=40)
        tableUniv1.column('lang', anchor=CENTER, width=60)
        tableUniv1.column('fees', anchor=CENTER, width=60)
        tableUniv1.column('langfees', anchor=CENTER, width=90)

        tableUniv1.heading('#0', text='', anchor=CENTER)
        tableUniv1.heading('univ', text='University', anchor=CENTER)
        tableUniv1.heading('dept', text='Department', anchor=CENTER)
        tableUniv1.heading('yrs', text='Years', anchor=CENTER)
        tableUniv1.heading('lang', text='Language', anchor=CENTER)
        tableUniv1.heading('fees', text='Fees', anchor=CENTER)
        tableUniv1.heading('langfees', text='Language Fees', anchor=CENTER)
        tableUniv1['show'] = 'headings'
        tableUniv1.place(x=90, y=90)

        displayUnivSorted(tableUniv1)
        return

    searchBtn = Button(frame1, text="Search", bg='goldenrod1', width=10, command=SortUniv)
    searchBtn.place(x=800, y=200)

    # -------------------------------------------------------------------------------
    def addUniv(table):
        UnivName = newUniv.get()
        DeptName = newDept.get()
        yrs = years.get()
        lang = SelectedLang.get()
        payement = fees.get()
        feeLang = lang_fees.get()

        if UnivName == '' or DeptName == '' or yrs == '' or payement == '' or feeLang == '':
            showerror('Error', 'Please Fill ALL the input fields !!')
        else:
            insertUniv(UnivName, DeptName, yrs, lang, payement, feeLang)
            displayUniv(table)
            showinfo('Message', 'New University added Successfully :D !!')

    def DeleteUniv(table):
        row = SelectedRow(table)
        cursor.execute("DELETE FROM universities WHERE univName = ? and dept = ?", (row[0], row[1],))
        displayUniv(table)
        showinfo('Message', 'University deleted Successfully :D !!')

    # -------------------------------------------------------------------------------
    tableUniv = Treeview(frame2)
    tableUniv['columns'] = ('univ', 'dept', 'yrs', 'lang', 'fees', 'langfees')
    tableUniv.column('#0', width=0, stretch=NO)
    tableUniv.column('univ', anchor=CENTER, width=150)
    tableUniv.column('dept', anchor=CENTER, width=150)
    tableUniv.column('yrs', anchor=CENTER, width=40)
    tableUniv.column('lang', anchor=CENTER, width=60)
    tableUniv.column('fees', anchor=CENTER, width=60)
    tableUniv.column('langfees', anchor=CENTER, width=90)

    tableUniv.heading('#0', text='', anchor=CENTER)
    tableUniv.heading('univ', text='University', anchor=CENTER)
    tableUniv.heading('dept', text='Department', anchor=CENTER)
    tableUniv.heading('yrs', text='Years', anchor=CENTER)
    tableUniv.heading('lang', text='Language', anchor=CENTER)
    tableUniv.heading('fees', text='Fees', anchor=CENTER)
    tableUniv.heading('langfees', text='Language Fees', anchor=CENTER)
    tableUniv['show'] = 'headings'
    tableUniv.place(x=20, y=20)

    displayUniv(tableUniv)

    # -------------------------------------------------------------------------------
    addBtn = Button(frame2, text="Add University", font=btn_font, bg='LightSkyBlue3', width=20,
                    command=lambda: addUniv(tableUniv))
    addBtn.place(x=650, y=40)

    dltBtn = Button(frame2, text="Delete University", font=btn_font, bg='LightSkyBlue3', width=20,
                    command=lambda: DeleteUniv(tableUniv))
    dltBtn.place(x=650, y=140)

    return


# -------------------Fonts--------------------------------

label_font = tkFont.Font(family="Bahnschrift Light", size=14, weight="bold")
entrer_font = tkFont.Font(family="Bahnschrift Light", size=12)
btn_font = tkFont.Font(family="Javanese Text", size=11, weight="bold")

# -------------------------------Frames-------------------------------

TopFrame = Frame(root, height=400, width=800)
TopFrame.grid(row=0, column=0)

BottomFrame = Frame(root, height=150, width=800)
BottomFrame.grid(row=1, column=0)

# -----------------------------Image------------------------------

myImage = Image.open("devis/images/ist_found1.png")
resized = myImage.resize((250, 180), Image.Resampling.LANCZOS)

newPic = ImageTk.PhotoImage(resized)
myLabel = Label(TopFrame, image=newPic)

myLabel.place(x=530, y=20)

# -------------------------------Labels--------------------------------
lblFname = Label(TopFrame, text="First Name :", font=label_font)
lblFname.place(x=40, y=20)

lblLname = Label(TopFrame, text="Last Name :", font=label_font)
lblLname.place(x=40, y=80)

lblpassport = Label(TopFrame, text="Passport Number :", font=label_font)
lblpassport.place(x=40, y=140)

lblfee = Label(TopFrame, text="Studying Fee :", font=label_font)
lblfee.place(x=40, y=200)

lblUniv = Label(TopFrame, text="University :", font=label_font)
lblUniv.place(x=40, y=260)

lblAgent = Label(TopFrame, text="Agent :", font=label_font)
lblAgent.place(x=40, y=320)

# --------------------Input Fields----------------------------

inputFname = Entry(TopFrame, font=entrer_font, width=25, textvariable=fname)
inputFname.place(x=260, y=23)

inputLname = Entry(TopFrame, font=entrer_font, width=25, textvariable=lname)
inputLname.place(x=260, y=83)

inputpassport = Entry(TopFrame, font=entrer_font, width=25, textvariable=passnumber)
inputpassport.place(x=260, y=143)

inputfee = Entry(TopFrame, font=entrer_font, width=25, textvariable=studFee)
inputfee.place(x=260, y=203)

list_univ = getUniv()
inputUniv = OptionMenu(TopFrame, SelectedUniv, *list_univ)
inputUniv.place(x=260, y=263)

inputAgent = Entry(TopFrame, font=entrer_font, width=25, textvariable=NameAgent)
inputAgent.place(x=260, y=323)


# ---------------------Buttons--------------------------------
def GenFile():
    nom = fname.get()
    prenom = lname.get()
    numero = passnumber.get()
    fee = studFee.get()
    univdept = SelectedUniv.get()
    agent = NameAgent.get()

    file_name = nom + "_" + prenom
    somme = int(getFee(araUniv(univdept), araDept(univdept))) + int(getLangFee(araUniv(univdept), araDept(univdept)))

    if nom == "" or prenom == "" or numero == "" or fee == "" or univdept == "":
        showerror('Error', 'Please Fill ALL the cases !!!')

    fichier = """<!DOCTYPE html>
                <html lang="fr">
                <head>
                  <meta http-equiv="Content-Type" content="text/html; charset=ISO 8859-1" />
                  <title>"""

    fichier += str(file_name) + """</title>
                  <style>
                    .corps{
                      margin: 5px;
                    }

                    img{
                      width: 250px;
                      height: 180px;
                    }

                    td, th, tr{
                      font-size: 18px;
                      font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
                      padding: 10px;
                    }

                    table {
                      border-collapse: collapse;
                      width: 100%;
                    }

                    .fees{
                      margin-left: auto;
                    }

                    .heading{
                      height: 20px;
                    }

                    h2{
                      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    }
                    .cachet{
                        width: 200px;
                        height: 180px;
                    }
                  </style>
                </head>
                <body>
                  <div class="corps">
                    <table>
                      <tr>
                        <td width="80%"><h2>Devis</h2></td>
                        <td><img src="images/ist_found1.png" alt="logo"></td>
                      </tr>
                    </table>
                    <br>
                    <hr>
                    <br>
                    <table>
                        <tr>
                            <td width="40%">Nom : </td>
                            <td>"""

    fichier += nom + """</td>
                          </tr>
                          <tr>
                            <td width="40%">Prénom : </td>
                            <td>"""
    fichier += prenom + """</td>
                              </tr>
                              <tr>
                                <td width="40%">Numéro de passport : </td>
                                <td>"""
    fichier += numero + """</td>
                          </tr>
                          <tr>
                            <td width="40%">Université et département : </td>
                            <td>"""
    fichier += univdept + """</td>
                          </tr>
                          <tr>
                            <td width="40%">Frais d'inscription et dossier : </td>
                            <td>"""
    fichier += str(fee) + """ $
                           </table>
                             <br><br><br><br>
                            <table border="1" class="fees">
                              <tr>
                                <th class="heading" width="80%">Description</th>
                                <th class="heading">Montant (TL)</th>
                              </tr>
                              <tr>
                                <td>Frais de scolarité annuelle </td>
                                <td>"""

    fichier += str(getFee(araUniv(univdept), araDept(univdept))) + """ </td>
                                                  </tr>
                                                  <tr>
                                                    <td>Frais de l'année d'apprentissage de la langue </td>
                                                    <td>"""
    fichier += str(getLangFee(araUniv(univdept), araDept(univdept))) + """ </td>
                                                              </tr>
                                                              <tr>
                                                                <td>Frais Total</td>
                                                                <td>
                                                              """
    fichier += str(somme) + """</td>
                      </tr>
                    </table>
                    <br><br>
                    <table>
                        <tr>
                            <td width="70%">Agent :\t<b>"""
    fichier += agent + """</b></td>
                            <td> Signature: </td>
                        </tr>
                        <tr>
                            <td width="70%"></td>
                            <td> <img src="images/cachet.png" alt="cachet" class="cachet"></td>
                        </tr>
                    </table>

                  </div>
                </body>
                </html>"""

    ourFile = open("devis/" + file_name + ".html", 'w')
    ourFile.write(fichier)


UnivMangementBtn = Button(BottomFrame, text="Manage Universities", bg="LightSkyBlue3", font=btn_font, width=25,
                          command=univMan)
UnivMangementBtn.place(x=80, y=40)

GenerateBtn = Button(BottomFrame, text="Generate", bg="LightSkyBlue3", font=btn_font, width=20, command=GenFile)
GenerateBtn.place(x=520, y=40)

root.mainloop()