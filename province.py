import os
from pathlib import Path

def create_province_summaries(base_dir='txt'):
    """
    Crée un fichier 0_Province_X.txt dans chaque sous-dossier
    qui récapitule le contenu de tous les fichiers du dossier.
    """
    base_path = Path(base_dir)
    
    if not base_path.exists():
        print(f"Erreur : le dossier '{base_dir}' n'existe pas")
        return
    
    # Parcourir tous les sous-dossiers
    for province_dir in sorted(base_path.iterdir()):
        if not province_dir.is_dir():
            continue
        
        # Extraire le nom de la province (ex: "I_Aix" -> "Aix")
        province_name = province_dir.name.split('_', 1)[-1]
        
        # Nom du fichier récapitulatif
        summary_file = province_dir / f"0_Province_{province_name}.txt"
        
        # Récupérer tous les fichiers .txt (sauf le récapitulatif lui-même)
        txt_files = sorted([
            f for f in province_dir.glob('*.txt')
            if not f.name.startswith('0_Province_')
        ])
        
        if not txt_files:
            print(f"⚠️  Aucun fichier .txt trouvé dans {province_dir.name}")
            continue
        
        # Créer le fichier récapitulatif
        with open(summary_file, 'w', encoding='utf-8') as summary:
            # En-tête
            summary.write(f"PROVINCE ECCLÉSIASTIQUE DE {province_name.upper()}\n")
            summary.write("=" * 60 + "\n\n")
            
            # Liste des diocèses
            summary.write(f"Diocèses de la province ({len(txt_files)}) :\n")
            for txt_file in txt_files:
                diocese_name = txt_file.stem.split('_', 1)[-1]
                summary.write(f"  - {diocese_name}\n")
            summary.write("\n" + "=" * 60 + "\n\n")
            
            # Contenu de chaque fichier
            for i, txt_file in enumerate(txt_files, 1):
                diocese_name = txt_file.stem.split('_', 1)[-1]
                
                summary.write(f"\n{'#' * 60}\n")
                summary.write(f"# {i}. DIOCÈSE DE {diocese_name.upper()}\n")
                summary.write(f"{'#' * 60}\n\n")
                
                # Lire et écrire le contenu
                try:
                    with open(txt_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        summary.write(content)
                        if not content.endswith('\n'):
                            summary.write('\n')
                except Exception as e:
                    summary.write(f"[Erreur lors de la lecture : {e}]\n")
                
                summary.write("\n")
        
        print(f"✓ Créé : {summary_file}")

if __name__ == "__main__":
    create_province_summaries()
    print("\n✓ Terminé !")