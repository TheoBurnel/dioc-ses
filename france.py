import json
import os
from glob import glob

# --- répertoire des GeoJSON ---
geojson_root = "geojson"
output_file = "dioceses-france.geojson"

print("🇫🇷 Compilation de tous les diocèses de France...\n")

all_features = []

# --- parcourir tous les sous-dossiers ---
for folder_name in sorted(os.listdir(geojson_root)):
    folder_path = os.path.join(geojson_root, folder_name)
    
    if not os.path.isdir(folder_path):
        continue
    
    # --- chercher les fichiers Province_*.geojson ---
    province_files = glob(os.path.join(folder_path, "Province_*.geojson"))
    
    if not province_files:
        print(f"⚠️  Aucun fichier Province_*.geojson trouvé dans {folder_name}")
        continue
    
    for province_file in province_files:
        province_name = os.path.basename(province_file).replace("Province_", "").replace(".geojson", "")
        print(f"📍 Ajout de la province : {province_name} ({folder_name})")
        
        try:
            with open(province_file, "r", encoding="utf-8") as f:
                geojson_data = json.load(f)
            
            # Ajouter toutes les features de ce fichier
            if "features" in geojson_data:
                features_count = len(geojson_data["features"])
                all_features.extend(geojson_data["features"])
                print(f"   ✅ {features_count} diocèses ajoutés")
            
        except Exception as e:
            print(f"   ⚠️ Erreur lors de la lecture de {province_file}: {e}")

# --- créer le GeoJSON final ---
france_geojson = {
    "type": "FeatureCollection",
    "features": all_features
}

# --- sauvegarder ---
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(france_geojson, f, ensure_ascii=False, indent=2)

print(f"\n✅ Fichier créé : {output_file}")
print(f"📊 Total : {len(all_features)} diocèses compilés")
print("🌍 Compilation terminée !")