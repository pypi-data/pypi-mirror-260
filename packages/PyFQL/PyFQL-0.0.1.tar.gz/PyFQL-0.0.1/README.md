# Guide d'utilisation du script `query.py`

/!\ Modification régulière peut ne pas marcher ou etre à jour /!\

Ce guide explique comment utiliser le script `query.py` pour interagir avec ma base de données simplifiée via des commandes en ligne de commande. Le script permet de créer des tables, d'ajouter des enregistrements, de les afficher et de les supprimer de différentes manières.

## Prérequis

Assurez-vous d'avoir Python installé sur votre système pour exécuter le script.

## Exécution du script

Pour lancer le script, ouvrez un terminal ou une invite de commandes, accédez au répertoire contenant le fichier `query.py` et exécutez la commande suivante :

```bash
python query.py
```

## Commandes disponibles

Le script prend en charge les commandes suivantes :

- `creer table [nom_table]`: Crée une nouvelle table dans la base de données.
- `ajoute [nom_table] [attributs]`: Ajoute un enregistrement à une table existante.
- `supprime [nom_table] [options]`: Supprime des enregistrements ou une table entière de la base de données.
- `affiche [nom_table]`: Affiche le contenu d'une table.
- `exit` ou `quit`: Quitte le programme.

## Exemples de requêtes

Voici des exemples de requêtes que vous pouvez exécuter dans le script :

1. **Création d'une table** :
   ```bash
   creer table voiture
   ```

2. **Ajout d'un enregistrement** :
   ```bash
   ajoute voiture marque=Toyota modele=Corolla annee=2020 couleur=bleu
   ```

3. **Affichage du contenu d'une table** :
   ```bash
   affiche voiture
   ```

4. **Suppression d'un enregistrement par index** :
   ```bash
   supprime voiture 0
   ```

5. **Suppression d'un champ spécifique d'un enregistrement** :
   ```bash
   supprime voiture 0 couleur
   ```

6. **Suppression de tous les enregistrements d'une table** :
   ```bash
   supprime voiture tous
   ```

7. **Suppression d'une table entière** :
   ```bash
   supprime voiture
   ```

## Fonctionnement du script

Le script utilise une classe `Database` pour gérer la base de données. Voici un aperçu de ses principales méthodes :

- `create_table`: Crée une nouvelle table dans la base de données.
- `insert`: Insère un nouvel enregistrement dans une table existante.
- `delete`: Supprime des enregistrements ou une table entière de la base de données.
- `display_table`: Affiche le contenu d'une table.
- `execute_query`: Analyse et exécute les commandes fournies par l'utilisateur.

## Phrase type traiter en language naturel sans library externe
- [creer] la [table]/[bdd] [VARIABLE]       
  RESERVER IGNORE RESERVER VARIABLE
--
- [utilise] la [bdd] [VARIABLE]
  RESERVER IGNORE RESERVER VARIABLE
--
- [supprime] la [table]/[bdd] [VARIABLE]
  RESERVER IGNORE RESERVER VARIABLE
--
- [supprime] le [champ]/ [VARIABLE] de la [table] [VARIABLE]
  RESERVER IGNORE RESERVER VARIABLE IGNORE IGNORE RESERVER VARIABLE
--
- [supprime] les [enregistrements] de la [table] [VARIABLE]
  RESERVER IGNORE RESERVER IGNORE IGNORE RESERVER VARIABLE
--
-[modifie] la [table] [VARIABLE] et [renome] le [champ] [VARIABLE] par [VARIABLE]
RESERVER IGNORE RESERVER RESERVER IGNORE RESERVER IGNORE RESERVER RESERVER IGNORE VARIABLE
--
-[modifie] la [table] [VARIABLE] et [ajoute] le [champ] [VARIABLE]
RESERVER IGNORE RESERVER VARIABLE IGNORE RESERVER IGNORE RESERVER VARIABLE
--
- [modifie] la     [table] [VARIABLE] et    [ajoute]   le [champ] [VARIABLE]  a la position [VARIABLE]
  RESERVER IGNORE RESERVER VARIABLE  IGNORE RESERVER IGNORE RESERVER VARIABLE IGNORE IGNORE IGNORE VARIABLE
--
## Conclusion

Ce guide devrait vous aider à comprendre comment utiliser le script `query.py` pour interagir avec une base de données simple via des commandes en ligne de commande. Si vous avez des questions ou des problèmes, n'hésitez pas à demander de l'aide à ce mail yannbanas@gmail.com.
