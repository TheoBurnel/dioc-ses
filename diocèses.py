from svgpathtools import parse_path
import json
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
    
    # --- chercher uniquement le fichier 0_Province_*.txt ---
    province_files = [f for f in os.listdir(input_folder) if f.startswith("0_Province_") and f.endswith(".txt")]
    
    if not province_files:
        print(f"⚠️  Aucun fichier 0_Province_*.txt trouvé dans {folder_name}")
        continue
    
    province_file = os.path.join(input_folder, province_files[0])
    
    with open(province_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # --- identifier les sections de diocèses ---
    # On cherche les sections qui commencent par "# X. DIOCÈSE DE ..."
    diocese_pattern = r'#{60}\n# \d+\. DIOCÈSE DE ([^\n]+)\n#{60}\n\n(.*?)(?=\n#{60}|\Z)'
    matches = re.findall(diocese_pattern, content, re.DOTALL)
    
    if not matches:
        print(f"⚠️  Aucun diocèse trouvé dans {province_files[0]}")
        continue
    
    features = []
    
    for diocese_name, diocese_content in matches:
        diocese_name = diocese_name.strip()
        print(f"  📍 Traitement du diocèse : {diocese_name}")
        
        # --- extraire les chemins SVG du contenu ---
        # On suppose que le contenu SVG est tout ce qui ressemble à des commandes SVG
        svg_lines = [line.strip() for line in diocese_content.split('\n') if line.strip()]
        
        # --- séparer en polygones à chaque M ou m ---
        path_blocks = re.split(r'(?=[Mm])', " ".join(svg_lines))
        
        for block in path_blocks:
            block = block.strip()
            if not block:
                continue
            
            try:
                path = parse_path(block)
            except Exception as e:
                print(f"    ⚠️ Erreur parsing SVG pour {diocese_name}: {e}")
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
                        "province": folder_name
                    },
                    "geometry": {"type": "Polygon", "coordinates": [coords]}
                })
    
    # --- enregistrer le GeoJSON de la province ---
    fc = {"type": "FeatureCollection", "features": features}
    
    province_name = folder_name.split('_', 1)[-1]
    output_file = os.path.join(output_folder, f"Province_{province_name}.geojson")
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(fc, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(features)} polygones créés dans {output_file}")

print("\n🌍 Conversion complète terminée !")