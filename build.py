import os
import json
import configparser

def generate_vmr_file():
    """
    Generate FSLTLCAV.vmr file from aircraft.cfg files in SimObjects/Airplanes
    """
    print("\n=== Generating FSLTLCAV.vmr ===")
    
    simobjects_path = "SimObjects/Airplanes"
    aircraft_data = []
    
    # Scan all aircraft folders
    if os.path.exists(simobjects_path):
        for aircraft_folder in sorted(os.listdir(simobjects_path)):
            aircraft_path = os.path.join(simobjects_path, aircraft_folder)
            
            # Only process CAN aircraft folders
            if os.path.isdir(aircraft_path) and aircraft_folder.endswith("_CAN"):
                aircraft_cfg_path = os.path.join(aircraft_path, "aircraft.cfg")
                
                if os.path.exists(aircraft_cfg_path):
                    try:
                        # Read aircraft.cfg
                        config = configparser.ConfigParser()
                        config.read(aircraft_cfg_path, encoding='utf-8')
                        
                        # Extract data
                        icao_type = config.get('GENERAL', 'icao_type_designator').strip('"')
                        title = config.get('FLTSIM.0', 'title').split(';')[0].strip().strip('"')
                        
                        aircraft_data.append({
                            'typecode': icao_type,
                            'model': title,
                            'folder': aircraft_folder
                        })
                        
                        print(f"  Found: {aircraft_folder} - {icao_type} - {title}")
                        
                    except Exception as e:
                        print(f"  Warning: Could not read {aircraft_cfg_path}: {e}")
    
    # Generate VMR XML content
    vmr_content = '<?xml version="1.0" encoding="utf-8"?> \n<ModelMatchRuleSet> \n'
    
    for aircraft in aircraft_data:
        vmr_content += f'<ModelMatchRule CallsignPrefix="CAN" TypeCode="{aircraft["typecode"]}" ModelName="{aircraft["model"]}" /> \n'
    
    vmr_content += '</ModelMatchRuleSet>\n'
    
    # Write to file
    vmr_file_path = "FSLTLCAV.vmr"
    with open(vmr_file_path, 'w', encoding='utf-8') as f:
        f.write(vmr_content)
    
    print(f"\n✓ Generated {vmr_file_path} with {len(aircraft_data)} aircraft")
    return vmr_file_path

# Generate VMR file before building layout
generate_vmr_file()

project_directories = ["Effects", "html_ui", "SimObjects", "ModelBehaviorDefs", "AirTraffic", "Texture", "scenery", "VisualEffectLibs"]

content_entries = list()
total_package_size = 0

for project_directory in project_directories:
    for directory_path, directory_names, file_names in os.walk(project_directory):
        for file_name in file_names:
            file_path = os.path.join(directory_path, file_name)
            file_size = os.path.getsize(file_path)
            file_date = 116444736000000000 + int(os.path.getmtime(file_path) * 10000000.0)

            content_entry = {"path": file_path.replace(os.sep, "/"), "size": file_size, "date": file_date}
            content_entries.append(content_entry)

            total_package_size += file_size

            print("Added file: " + file_path)

layout_entries = {"content": content_entries}

layout_file = open("layout.json", "w")
json.dump(layout_entries, layout_file, indent=4)

manifest_file = open("manifest.json", "r")

manifest_entries = json.load(manifest_file)
manifest_entries["total_package_size"] = str(total_package_size).zfill(20)

manifest_file = open("manifest.json", "w")
json.dump(manifest_entries, manifest_file, indent=4)
