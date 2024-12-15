import matplotlib.pyplot as plt

# Eingaben
iterationen = 60
wahrscheinlichkeiten = [1/12, 1/24, 0] # letztes Nuklid muss stabil sein

def p(x): # Wahrscheinlichkeit das Nuklid x in der Iteration zerfällt
    return wahrscheinlichkeiten[x] if 0 <= x else 0

memo = {} # Zum Speichern von den Werten von N(x, t)

def N(x, t): # Bestand
    if x < 0: # Nuklid x = -1 existiert nicht, also N = 0
        return 0

     # Es macht keinen Sinn die Werte immer wieder neu zu berechnen, 
     # weshalb man sie aus memo abruft wenn sie bereits berechnet worden sind
    if (x, t) in memo:
        return memo[(x, t)]
    
    if t == 0: # Startwerte
        # Obwohl ein absoluter Wert angegeben wird sind Bruchteile möglich
        return 10_000 if x == 0 else 0
    
    # Aktueller Bestand = Vorheriger Bestand - vorheriger Zerfall + vorheriger Zerfall des Mutternuklids
    memo[x, t] = N(x, t - 1) * (1 - p(x)) + N(x - 1, t - 1) * p(x - 1)
    
    return memo[x, t]

def n(x, t): # Zerfall
    return N(x, t) * p(x)


# Darstellung mit Matplotlib
fig, (ax_bestände, ax_zerfälle) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

nuklid_namen = ["Mutter", "Tochter", "Enkel", "Urenkel"]
for (x, _), name in zip(enumerate(wahrscheinlichkeiten), nuklid_namen):
    ax_bestände.plot(range(iterationen), [N(x, t) for t in range(iterationen)], label=name)
    ax_zerfälle.plot(range(iterationen), [n(x, t) for t in range(iterationen)], label=name)

ax_zerfälle.plot(
    range(iterationen),
    [sum([n(x, t) for x in range(len(wahrscheinlichkeiten))]) for t in range(iterationen)], 
    label="Gesamt"
    )

# Achsenbeschriftungen
ax_bestände.set_xlabel("Iteration")
ax_zerfälle.set_xlabel("Iteration")

ax_bestände.set_ylabel("Bestand")
ax_zerfälle.set_ylabel("Zerfälle pro Iteration")

ax_zerfälle.legend()
plt.show()