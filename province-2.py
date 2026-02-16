from svgpathtools import parse_path
import json
from glob import glob
import os
import re

# --- coefficients pour la transformation SVG → Geo ---
ax, bx, cx = 0.00786374579, 0.000107873306, -5.91550251
ay, by, cy = -0.0000547414942, -0.00541671605, 51.4850962

def svg_to_geo(x, y):
    lon = ax * x + bx * y + cx
    lat = ay * x + by * y + cy
    return [lon, lat]

# --- répertoires racine ---
input_root = "txt"
output_root = "geojson"
os.makedirs(output_root, exist_ok=True)

# --- parcourir tous les sous-dossiers ---
for folder_name in sorted(os.listdir(input_root)):
    input_folder = os.path.join(input_root, folder_name)
    
    if not os.path.isdir(input_folder):
        continue  # ignore les fichiers
    
    output_folder = os.path.join(output_root, folder_name)
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"\n📁 Traitement du dossier : {folder_name}")
    
    # --- récupérer tous les fichiers .txt SAUF les 0_Province_*.txt ---
    txt_files = [
        f for f in glob(os.path.join(input_folder, "*.txt"))
        if not os.path.basename(f).startswith("0_Province_")
    ]
    
    for txt_file in txt_files:
        # Extraire le nom du diocèse depuis le nom du fichier (ex: "1_Aix.txt" -> "Aix")
        diocese_name = os.path.basename(txt_file).replace(".txt", "").split("_", 1)[-1]
        
        print(f"  📍 Traitement du diocèse : {diocese_name}")
        
        with open(txt_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        
        # --- séparer en polygones à chaque M ou m ---
        path_blocks = re.split(r'(?=[Mm])', " ".join(lines))
        features = []
        
        for block in path_blocks:
            block = block.strip()
            if not block:
                continue
            
            try:
                path = parse_path(block)
            except Exception as e:
                print(f"    ⚠️ Erreur parsing SVG : {e}")
                continue
            
            coords = []
            for seg in path:
                for t in [i / 10 for i in range(11)]:
                    pt = seg.point(t)
                    x, y = pt.real, pt.imag
                    coords.append(svg_to_geo(x, y))
            
            # fermer le polygone si besoin
            if coords and coords[0] != coords[-1]:
                coords.append(coords[0])
            
            # ajouter le polygone
            if len(coords) >= 3:
                features.append({
                    "type": "Feature",
                    "properties": {
                        "diocese": diocese_name,
                        "province": folder_name,
                        "source": os.path.basename(txt_file)
                    },
                    "geometry": {"type": "Polygon", "coordinates": [coords]}
                })
        
        # --- enregistrer le GeoJSON ---
        fc = {"type": "FeatureCollection", "features": features}
        output_file = os.path.join(
            output_folder,
            os.path.basename(txt_file).replace(".txt", ".geojson")
        )
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(fc, f, ensure_ascii=False, indent=2)
        
        print(f"    ✅ {len(features)} polygones créés dans {output_file}")

print("\n🌍 Conversion complète terminée !")