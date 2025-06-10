Die Scripts zum Senden von Packeten müssen als Module aufgerufen werden:
```
PYTHON_PATH/python.exe -m DIR.SCRIPT
```
Z.B
```
PATH/CC_BA2/.venv/Scripts/python.exe -m MQTT.mqtt -t 192.168.10.2 -l 5 -s
```
Die Empfänger-Scripte können ganz normal (mit Parametern) aufgerufen werden.

Parameter werden mit ```-h``` oder ```--help``` oder im Code erklärt.
