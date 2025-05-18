import json

# Zielgröße in Bytes
target_size = 1024 * 1024  # 1 MB = 1,048,576 Bytes

# Struktur: {"data": "<string>"}
# Berechne die Anzahl Zeichen, die in den "data"-String passen
# {"data": ""} hat 10 Zeichen, also bleibt target_size - 10 für den Inhalt
payload_size = target_size - len(json.dumps({"data": ""}))

# Erzeuge einen Dummy-String genau dieser Länge
data = {"data": "A" * payload_size}

# Speichere die Datei
with open("./data/1mb.json", "w") as f:
    json.dump(data, f)

print("Datei '1mb.json' mit exakt 1 MB erzeugt.")