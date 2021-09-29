# Solar Potentialrechner 

## Allgemein
Kernfrage: Wie viel Strom kann durch den Solarausbau auf öffentlichen Dächern erzeugt werden? 

Unsere Webapp soll verdeutlichen, wie viel Potenzial in den zur Verfügung stehenden öffentlichen Dachflächen steckt und ein Gefühl vermittelen, 
mit wie wenig Aufwand eine beachtliche Veränderung hervorgerufen werden kann. 
Hierzu berechnen wir die gesamt nutzbare Dachfläche einer Stadt anhand von Geodaten und betonen mithilfe von Daten, wie dem Stromverbrauch der jeweiligen Stadt,
was für eine große Auswirkung die Aufrüstung eines vergleichsweise kleinen Anteils der Dächer auf das Klima haben kann. 
Zusätzlich lässt sich jedes infrage kommende Gebäude einzeln betrachten und dessen Anteil an möglicher Stromerzeugung abschätzen.
Die App soll jeder Gemeinde ermöglichen Abzuwägen, inwieweit sich ein Ausbau mit Solarenergie für sie lohnt. 

## Frontend:
Ein Suchfeld bietet die Möglichkeit die gewünschte Stadt auszuwählen. Nach Auswahl 
werden die Daten am Server angefragt und anschließend in From einer kurzen Auswertung dargstellt.
Im unteren Bereich befindet sich eine auflistung aller in Betracht kommenden Gebäude samt ihrer Eigenschaften.


## Backend: 
Es werden zwei Datensätze angefragt. Der OSM Datensatz um die in betracht kommenden Gebäude zu erhalten. 
Sowie den Datensatz von Opengeodata NRW , um die zur Verfügung stehenden Dachflächen und deren mögliche Solarerzeugung zu erhalten. 
Beide Datensätze werden auf Ihre benötigten Eigenschaften reduziert und anschließend zusammengeführt. 
Dieser gekürzte Datensatz wird nun dem Frontend zur Verfügung gestellt. 


## Datenquellen:

Solarkatster vom Landesamt für Natur, Umwelt und Verbraucherschutz NRW
https://www.opengeodata.nrw.de/produkte/umwelt_klima/klima/solarkataster/photovoltaik/

Overpass API für OSM
https://wiki.openstreetmap.org/wiki/Overpass_API
