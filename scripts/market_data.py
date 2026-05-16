"""
market_data.py — Données de référence du marché immobilier belge 2026.

Toutes les valeurs sont indicatives et issues de moyennes 2025-2026 (Realo,
Immoweb, notaire.be, énergie.wallonie.be). À ajuster annuellement.
"""

# Prix moyens vente (€/m²) — sources : Realo, price.immoweb.be, mars 2026
PRIX_M2_VENTE = {
    "verviers": {"maison": 1600, "appartement": 1800},
    "liege": {"maison": 2100, "appartement": 2400},
    "seraing": {"maison": 1350, "appartement": 1500},
    "herstal": {"maison": 1450, "appartement": 1600},
    "namur": {"maison": 2300, "appartement": 2600},
    "charleroi": {"maison": 1200, "appartement": 1400},
    "mons": {"maison": 1400, "appartement": 1700},
    "bruxelles": {"maison": 3200, "appartement": 3500},
    "default": {"maison": 1800, "appartement": 2100},
}

# Loyer moyen (€/mois) — par typologie et ville
LOYER_MOYEN = {
    "verviers": {
        "studio": 460,
        "1ch": 580,
        "2ch": 720,
        "3ch": 850,
        "4ch": 950,
    },
    "liege": {
        "studio": 540,
        "1ch": 680,
        "2ch": 830,
        "3ch": 980,
        "4ch": 1150,
    },
    "namur": {
        "studio": 570,
        "1ch": 720,
        "2ch": 880,
        "3ch": 1050,
        "4ch": 1250,
    },
    "default": {
        "studio": 520,
        "1ch": 650,
        "2ch": 790,
        "3ch": 940,
        "4ch": 1080,
    },
}

# Coûts travaux indicatifs (€ TVAC, TVA 6% logement >10 ans)
# Sources : Bobex, Habitat Presto, WeBuild 2026
COUTS_TRAVAUX = {
    # Énergétique
    "isolation_toiture_par_m2": 45,         # soufflé ou sarking
    "isolation_facade_int_par_m2": 80,      # par l'intérieur
    "isolation_facade_ext_par_m2": 180,     # par l'extérieur ITE
    "isolation_sol_par_m2": 35,
    "chassis_pvc_par_m2": 450,
    "chassis_alu_par_m2": 700,
    "vmc_simple_flux_forfait": 2500,
    "vmc_double_flux_forfait": 7500,

    # Chauffage
    "chaudiere_condensation_gaz": 5500,
    "pompe_a_chaleur_air_eau": 14000,

    # Conformité
    "mise_conformite_elec_par_m2": 75,      # full rewire
    "compteur_gaz_supplementaire": 1500,
    "compteur_elec_supplementaire": 1500,

    # Pièces humides
    "sdb_rafraichissement_forfait": 3500,
    "sdb_complete_par_m2": 1500,
    "kitchenette_forfait": 2500,
    "cuisine_economique_par_m2": 1100,
    "cuisine_moyen_de_gamme_par_m2": 1800,

    # Finitions
    "peinture_par_m2": 25,
    "sol_stratifie_par_m2": 35,
    "sol_parquet_par_m2": 75,
    "sol_carrelage_par_m2": 80,

    # Plomberie / sanitaire
    "plomberie_divers_forfait": 3000,

    # Toiture
    "refection_toiture_par_m2": 180,         # tuiles + voligeage
    "zinguerie_corniche_par_ml": 45,

    # Division en logements
    "permis_urbanisme_architecte": 3500,
    "separation_porte_paliere": 3500,
    "isolation_phonique_plancher_par_m2": 35,

    # Audit + PEB
    "audit_logement_certinergie": 600,
    "certificat_peb_apres_travaux": 250,

    # Toujours appliquer
    "reserve_imprevus_pct": 0.15,
}

# Primes Wallonie 2026 (catégorie de revenus)
# R3 = revenus moyens (la plupart des cas)
PRIMES_WALLONIE = {
    "isolation_toiture_par_m2_max": 35,
    "isolation_facade_par_m2_max": 45,
    "vmc_forfait_max": 800,
    "audit_logement_max": 460,
    "chaudiere_pac_forfait_max": 1500,
}

# Droits enregistrement Wallonie (depuis 01/01/2025)
DROITS_ENREGISTREMENT = {
    "habitation_propre_unique": 0.03,
    "investissement_locatif": 0.125,
    "residence_secondaire": 0.125,
    "donation_etc": 0.05,  # cas particuliers
}

# Frais notaire — barème national (honoraires + droits d'écriture + recherches)
# Approximation moyenne : ~3-4 % du prix pour un achat < 100k€
def frais_notaire_estimes(prix_achat: float) -> float:
    """Estimation des honoraires + frais notaire (hors droits d'enregistrement)."""
    # Barème dégressif : ~4% jusqu'à 50k, 3.3% jusqu'à 100k, 2.5% jusqu'à 150k, etc.
    if prix_achat <= 50_000:
        return prix_achat * 0.04 + 600
    elif prix_achat <= 100_000:
        return 2_000 + (prix_achat - 50_000) * 0.033
    elif prix_achat <= 200_000:
        return 3_650 + (prix_achat - 100_000) * 0.025
    else:
        return 6_150 + (prix_achat - 200_000) * 0.018

# Frais hypothèque (~1.5% du capital emprunté)
def frais_hypotheque(montant_emprunte: float) -> float:
    return montant_emprunte * 0.015 + 800

# Quotités max BNB
QUOTITE_MAX = {
    "habitation_propre_premier": 1.05,    # jusqu'à 105% (rare, dossier solide)
    "habitation_propre": 0.95,
    "investissement_locatif": 0.80,
    "residence_secondaire": 0.80,
}

# Taux hypothécaires fixes 2026 (DirectFin baromètre avril)
TAUX_HYPOTHECAIRE = {
    "fixe_20_ans": 0.0372,
    "fixe_25_ans": 0.0377,
    "fixe_25_ans_locatif": 0.0410,       # +0.3% locatif
    "fixe_25_ans_quotite_haute": 0.0450,  # quotité > 90%
}

# Précompte immobilier Wallonie — formule simplifiée
# PI annuel ≈ RC × indexation × (1.25% + additionnels communaux + provincial)
# Verviers : additionnels communaux ~2800%, provincial ~1500
PRECOMPTE_COMMUNES = {
    "verviers": {"add_communaux": 28.0, "add_prov": 15.0},
    "liege": {"add_communaux": 30.0, "add_prov": 15.0},
    "namur": {"add_communaux": 23.0, "add_prov": 12.5},
    "default": {"add_communaux": 27.0, "add_prov": 14.0},
}

# Coefficient d'indexation RC 2026 (publié au MB chaque année)
INDEXATION_RC_2026 = 2.18

def precompte_immobilier(rc: float, commune: str) -> float:
    """Calcule le précompte immobilier annuel Wallonie."""
    commune_low = commune.lower() if commune else "default"
    coeff = PRECOMPTE_COMMUNES.get(commune_low, PRECOMPTE_COMMUNES["default"])
    rc_indexe = rc * INDEXATION_RC_2026
    base = rc_indexe * 0.0125  # 1.25% région
    total = base * (1 + coeff["add_communaux"] + coeff["add_prov"] / 10)
    return round(total, 2)
