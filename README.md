# Pipeline-as-code

Nous n'avons pas pu effectuer les requêtes impliquant les deux tables en 
correspondance, car les données récupérées ne couvrent pas la même période. 
L’API que nous utilisons collecte des données en temps réel, ce qui signifie qu’il n’est 
pas possible de récupérer des données antérieures. En revanche, les données des 
"Yellow Taxis" (issues du fichier TLC Trip Record Data) sont figées dans un fichier 
Parquet, limité à un seul mois d’historique.
De ce fait, les requêtes nécessitant la jonction ou la comparaison des deux sources de 
données ne sont pas réalisables. Nous avons préparé un document Word afin d’y 
intégrer des captures d’écran illustrant ces limitations
