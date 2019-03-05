Pas à pas Github :

1. TOUJOURS travailler sur la branche de développement.
Pour afficher TOUTES les branches, effectuer la commande suivante :
git branch -a

2. Ensuite, faire un git checkout remotes/origin/dev

3. Faire un git pull origin dev pour récupérer les modifications des autres 

4. Créer une branche de développement local : git checkout -b LD_Architecture

5. Faire les modifications

6. Faire un git add -A et un git commit -m "Nom des modifs"

7. Se remettre sur la branche principale dev et refaire un git pull origin dev systématiquement

8. A partir de cette branche master, faire un git merge LD_Architecture

9. Refaire une branche de développement à partir de master : git checkout -b LD_Architecture2

10. A partir de cette branche de développement, faire un git push

11. Aller dans Github, aller chercher notre branche de développement dans "branches" (LD_Architecture2)

12. Normalement, la possibilité de créer une pull request est proposée à côté de cette branche.
Veiller à ce que la pull request se fasse vers "dev" et non vers "master".

13. Ajouter à cette petite pull request un label "enhancement" ou autre en fonction de l'objet de la pull request.

14. Théoriquement, une autre personne du groupe va valider et merger la pull request.

CROISONS LES DOIGTS POUR QU'IL N'Y AIT PAS DE CONFLIT !!!!
