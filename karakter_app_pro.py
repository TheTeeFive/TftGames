import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- DATA ----------------
klasser = {}
aktiv_klasse = "Standard"
vurderinger = {}

fag_liste = ["Norsk", "Samfunnsfag", "KRLE"]

sort_reverse = False

# ---------------- LAGRING ----------------
def lagre_klasser():
    klasser[aktiv_klasse] = vurderinger
    with open("klasser.json", "w", encoding="utf-8") as f:
        json.dump(klasser, f, indent=4)

def last_klasser():
    global klasser
    if os.path.exists("klasser.json"):
        with open("klasser.json", encoding="utf-8") as f:
            klasser = json.load(f)
    else:
        klasser = {"Standard": {}}

# ---------------- HELPERS ----------------
def snitt(liste):
    return round(sum(liste) / len(liste), 2) if liste else "-"

def hent_fag(fagdata, fag):
    if fag not in fagdata:
        return []
    return [v["karakter"] for v in fagdata[fag]][-5:]

# ---------------- SORTERING ----------------
def sorter_elever():
    global sort_reverse, vurderinger

    sort_reverse = not sort_reverse

    data = list(vurderinger.items())
    data.sort(key=lambda x: x[0].lower(), reverse=sort_reverse)

    vurderinger = {k: v for k, v in data}
    oppdater_tabell()

# ---------------- KLASSE ----------------
def oppdater_klasse_dropdown():
    klasse_dropdown.configure(values=list(klasser.keys()))

def legg_til_klasse():
    global aktiv_klasse, vurderinger

    navn = ny_klasse_input.get().strip()
    if not navn:
        return

    if navn not in klasser:
        klasser[navn] = {}

    aktiv_klasse = navn
    vurderinger = klasser[navn]

    lagre_klasser()
    oppdater_klasse_dropdown()

    klasse_dropdown.set(navn)
    elev_valg.configure(values=list(vurderinger.keys()))
    oppdater_tabell()

def bytt_klasse(val=None):
    global aktiv_klasse, vurderinger

    lagre_klasser()

    aktiv_klasse = klasse_dropdown.get()

    if aktiv_klasse not in klasser:
        klasser[aktiv_klasse] = {}

    vurderinger = klasser[aktiv_klasse]

    elev_valg.configure(values=list(vurderinger.keys()))
    oppdater_tabell()

def slett_klasse():
    global klasser, aktiv_klasse, vurderinger

    navn = klasse_dropdown.get()

    if navn in klasser:
        del klasser[navn]

    if klasser:
        aktiv_klasse = list(klasser.keys())[0]
    else:
        klasser["Standard"] = {}
        aktiv_klasse = "Standard"

    vurderinger = klasser[aktiv_klasse]

    oppdater_klasse_dropdown()
    klasse_dropdown.set(aktiv_klasse)

    elev_valg.configure(values=list(vurderinger.keys()))
    oppdater_tabell()

    lagre_klasser()

# ---------------- ELEV ----------------
def legg_til_elev():
    navn = elev_input.get().strip()

    if navn and navn not in vurderinger:
        vurderinger[navn] = {}
        elev_valg.configure(values=list(vurderinger.keys()))
        elev_valg.set(navn)
        elev_input.delete(0, "end")
        oppdater_tabell()

def slett_elev():
    elev = elev_valg.get()

    if elev in vurderinger:
        del vurderinger[elev]

    elev_valg.configure(values=list(vurderinger.keys()))
    elev_valg.set("")
    oppdater_tabell()
    lagre_klasser()

# ---------------- KARAKTER ----------------
def lagre_vurdering():
    elev = elev_valg.get()
    fag = fag_valg.get()

    if not karakter_valg.get():
        return

    karakter = int(karakter_valg.get())

    if elev not in vurderinger:
        return

    if fag not in vurderinger[elev]:
        vurderinger[elev][fag] = []

    vurderinger[elev][fag].append({"karakter": karakter})
    vurderinger[elev][fag] = vurderinger[elev][fag][-5:]

    lagre_klasser()
    oppdater_tabell()

def slett_siste_karakter():
    elev = elev_valg.get()
    fag = fag_valg.get()

    if elev in vurderinger and fag in vurderinger[elev]:
        if vurderinger[elev][fag]:
            vurderinger[elev][fag].pop()

    lagre_klasser()
    oppdater_tabell()

# ---------------- TABELL ----------------
def oppdater_tabell():
    for row in tree.get_children():
        tree.delete(row)

    for elev, fagdata in vurderinger.items():

        norsk = hent_fag(fagdata, "Norsk")
        samf = hent_fag(fagdata, "Samfunnsfag")
        krle = hent_fag(fagdata, "KRLE")

        tree.insert(
            "",
            "end",
            values=(
                elev,
                " | ".join(map(str, norsk)),
                snitt(norsk),
                " | ".join(map(str, samf)),
                snitt(samf),
                " | ".join(map(str, krle)),
                snitt(krle),
            )
        )

# ---------------- GUI ----------------
app = ctk.CTk()
app.title("Karakter System")
app.geometry("1200x750")
app.minsize(1000, 650)

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# ---------------- SIDEBAR ----------------
sidebar = ctk.CTkFrame(app, width=250)
sidebar.grid(row=0, column=0, sticky="ns")
sidebar.grid_propagate(False)

klasse_dropdown = ctk.CTkComboBox(sidebar, values=[], command=bytt_klasse)
klasse_dropdown.pack(pady=10)

ny_klasse_input = ctk.CTkEntry(sidebar, placeholder_text="Ny klasse")
ny_klasse_input.pack(pady=5)

ctk.CTkButton(sidebar, text="➕ Lag klasse", command=legg_til_klasse).pack(pady=5)
ctk.CTkButton(sidebar, text="🗑 Slett klasse", command=slett_klasse).pack(pady=5)

elev_input = ctk.CTkEntry(sidebar, placeholder_text="Elevnavn")
elev_input.pack(pady=15)

ctk.CTkButton(sidebar, text="➕ Legg til elev", command=legg_til_elev).pack(pady=5)
ctk.CTkButton(sidebar, text="🗑 Slett elev", command=slett_elev).pack(pady=5)

# ---------------- MAIN ----------------
main = ctk.CTkFrame(app)
main.grid(row=0, column=1, sticky="nsew")

elev_valg = ctk.CTkComboBox(main, values=[], state="readonly")
elev_valg.pack(pady=5)

fag_valg = ctk.CTkComboBox(main, values=fag_liste)
fag_valg.pack(pady=5)

karakter_valg = ctk.CTkComboBox(main, values=["1","2","3","4","5","6"])
karakter_valg.pack(pady=5)

ctk.CTkButton(main, text="Lagre karakter", command=lagre_vurdering).pack(pady=5)
ctk.CTkButton(main, text="🗑 Slett siste karakter", command=slett_siste_karakter).pack(pady=5)

# ---------------- TABLE ----------------
tree = ttk.Treeview(
    main,
    columns=("Elev","Norsk","Norsk snitt","Samf","Samf snitt","KRLE","KRLE snitt"),
    show="headings"
)

tree.heading("Elev", text="Elev", command=sorter_elever)

tree.heading("Norsk", text="Norsk")
tree.heading("Norsk snitt", text="Snitt")
tree.heading("Samf", text="Samf")
tree.heading("Samf snitt", text="Snitt")
tree.heading("KRLE", text="KRLE")
tree.heading("KRLE snitt", text="Snitt")

tree.pack(fill="both", expand=True)

# ---------------- START ----------------
last_klasser()

if "Standard" not in klasser:
    klasser["Standard"] = {}

vurderinger = klasser[aktiv_klasse]

klasse_dropdown.configure(values=list(klasser.keys()))
klasse_dropdown.set(aktiv_klasse)

oppdater_tabell()

app.mainloop()