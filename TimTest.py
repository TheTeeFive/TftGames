import random
import customtkinter as ctk

# --- Tema ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- Spillvariabler ---
hemmelig_tall = 0
maks = 10
forsok = 0


def start_spill(valgt_maks):
    global hemmelig_tall, maks, forsok
    maks = valgt_maks
    hemmelig_tall = random.randint(1, maks)
    forsok = 0
    resultat_label.configure(text=f"Gjett et tall mellom 1 og {maks}")


def gi_hint(forskjell):
    if forskjell <= maks * 0.05:
        return "🔥 Veldig nærme!"
    elif forskjell <= maks * 0.1:
        return "🙂 Ganske nærme!"
    else:
        return "❄️ Langt unna!"


def sjekk_gjett():
    global forsok

    try:
        gjett = int(input_felt.get())
    except ValueError:
        resultat_label.configure(text="Skriv et tall!")
        return

    if not (1 <= gjett <= maks):
        resultat_label.configure(text=f"1 - {maks}!")
        return

    forsok += 1
    forskjell = abs(gjett - hemmelig_tall)

    if gjett == hemmelig_tall:
        resultat_label.configure(text=f"🎉 Riktig! {forsok} forsøk")
        return

    if gjett < hemmelig_tall:
        tekst = "For lavt!"
    else:
        tekst = "For høyt!"

    resultat_label.configure(text=tekst + "  " + gi_hint(forskjell))


# --- GUI ---
app = ctk.CTk()
app.title("Gjett tallet 🎯")
app.geometry("420x350")

# Tittel
tittel = ctk.CTkLabel(app, text="🎯 Gjett tallet", font=ctk.CTkFont(size=20, weight="bold"))
tittel.pack(pady=15)

# Knapp-ramme
knapp_frame = ctk.CTkFrame(app)
knapp_frame.pack(pady=10)

ctk.CTkButton(knapp_frame, text="Lett", width=100, command=lambda: start_spill(10)).grid(row=0, column=0, padx=5)
ctk.CTkButton(knapp_frame, text="Medium", width=100, command=lambda: start_spill(50)).grid(row=0, column=1, padx=5)
ctk.CTkButton(knapp_frame, text="Vanskelig", width=100, command=lambda: start_spill(100)).grid(row=0, column=2, padx=5)

# Input
input_felt = ctk.CTkEntry(app, placeholder_text="Skriv tallet ditt...", width=200)
input_felt.pack(pady=15)

# Gjett-knapp
ctk.CTkButton(app, text="Gjett!", command=sjekk_gjett).pack(pady=5)

# Resultat
resultat_label = ctk.CTkLabel(app, text="")
resultat_label.pack(pady=20)

app.mainloop()