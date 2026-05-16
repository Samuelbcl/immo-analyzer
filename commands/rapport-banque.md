---
description: Génère un dossier PDF formel pour rendez-vous bancaire (plan de financement, amortissement, projections)
allowed-tools: ["Read", "Write", "Edit", "Bash", "WebFetch", "WebSearch", "AskUserQuestion"]
argument-hint: "<url-immoweb>"
---

# /rapport-banque

Génère un **dossier PDF formel** prêt à présenter à un banquier ou courtier.

## Arguments

- `$1` : URL de l'annonce Immoweb

## Workflow

1. **Lance d'abord `/analyse-immo $1`** complet pour avoir toutes les données.

2. **Informations complémentaires pour le banquier** (AskUserQuestion) :
   - Nom complet de l'emprunteur (+ co-emprunteur éventuel)
   - Date de naissance
   - Statut professionnel (CDI / indépendant / autre)
   - Ancienneté
   - Charges actuelles (autres crédits, loyer actuel)
   - Banque privilégiée pour le dossier (Belfius / ING / KBC / BNP / autre)

3. **Générer le PDF formel** :
   ```bash
   python3 scripts/build_bank_pdf.py \
     --analyse /tmp/analyse.json \
     --listing /tmp/listing.json \
     --renderings ~/Documents/immo-analyzer/<ref>/renderings/ \
     --borrower-info /tmp/borrower.json \
     --output ~/Documents/immo-analyzer/<ref>/dossier-banque.pdf
   ```

4. **Contenu du PDF** (10-15 pages) :
   - **Page 1 — Garde** : Nom emprunteur, adresse bien, date, montant demandé, photo principale
   - **Page 2 — Synthèse exécutive** : Le projet en 6 chiffres clés
   - **Page 3 — Le bien** : Description, photos avant, plan, caractéristiques
   - **Page 4-5 — Les images "après rénovation"** : Visualisations IA des pièces rénovées
   - **Page 6 — Plan de financement** : Apport / emprunt / quotité, frais d'acquisition détaillés
   - **Page 7 — Budget travaux** : Détail TVAC poste par poste, primes Wallonie attendues
   - **Page 8 — Capacité de remboursement** : Mensualité vs revenu, ratio d'effort, stress test +1 %
   - **Page 9 — Tableau d'amortissement** : Sur 25 ans avec capital restant dû annuel
   - **Page 10-11 — Projections locatives 10 ans** : Loyer indexé 2 %/an, charges, cash-flow, retour sur fonds propres
   - **Page 12 — Ratios bancaires** : LTV, DSCR, taux d'effort, après mise en location
   - **Page 13 — Sécurités proposées** : Hypothèque en 1er rang, assurance vie, assurance solde restant dû
   - **Page 14 — Plan de sortie** : Scénario revente après 10 ans avec hypothèses
   - **Page 15 — Annexes** : Liste des documents fournis (PEB, élec, certif gaz, plans, devis)

5. **Présenter** :
   - Lien vers le PDF
   - Conseil sur les 2-3 banques à contacter selon le profil
   - Argumentaire pour la première phrase d'entrée chez le banquier

## Exemple

```
> /rapport-banque https://www.immoweb.be/fr/annonce/maison/a-vendre/verviers/4800/21538755
```

## Ton du PDF

**Sérieux, factuel, technique.** Le banquier doit voir un emprunteur qui maîtrise son projet. Pas d'émojis, pas d'effets de manche. Chiffres tabulaires, hypothèses claires, sources citées. Police serif (Georgia) pour le PDF.

## Stress tests inclus

- Hausse de taux variable de +1 % et +2 %
- Vacance locative à 15 % au lieu de 8 %
- Travaux dépassent budget de 20 %
- Hausse précompte immobilier +50 %

Chaque test doit montrer que le projet reste sain.
