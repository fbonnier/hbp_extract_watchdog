import argparse
import json
import sys
import os
from nilsimsa import Nilsimsa

exceptions = [".cache", ".cython", "__pycache__"]

def extract_watchdog_to_json (watchdog_file:str, json_file:str):
    
    list_of_outputs = []

    with open (watchdog_file, 'r') as watchdog_f:
        singletons = list(dict.fromkeys(watchdog_f.readlines()))

        # Add exception to remove
        # singletons_to_remove = [ifile for ifile in singletons for iexception in exceptions if iexception in ifile]
        singletons_to_remove = []
        for ifile in singletons:
            for iexception in exceptions:
                if iexception in ifile:
                    singletons_to_remove.append(ifile)

        # Split and append multiple files seperated by space
        singletons_to_add = []
        for ifile in singletons:
            if " " in ifile:
                for isubfile in ifile.split(" "):
                    singletons_to_add.append (isubfile)
                singletons_to_remove.append(ifile)
        singletons = singletons + singletons_to_add

        # Remove remaining duplicates in files to remove
        singletons_to_remove = list(dict.fromkeys(singletons_to_remove))

        # Remove temporary files
        singletons_tmp = singletons
        singletons = []
        for itokeep in singletons_tmp:
            if  not (itokeep in singletons_to_remove):
                singletons.append(itokeep)

        print ("Singletons to remove")
        print (singletons_to_remove)
        print ("\n")
        print ("Singletons")
        print (singletons)

        # Remove remaining duplicates
        singletons = list(dict.fromkeys(singletons))
        
        for ifile in singletons:
            filepath = ifile.replace("\n", "")
            all_info = os.path.basename(filepath) + str(os.path.getsize(filepath))
            filehash = Nilsimsa(all_info).hexdigest()
            list_of_outputs.append({"url": None, "path": filepath, "hash": filehash})

        
    json_content = None
    with open (json_file, 'r') as json_f:
        json_content = json.load(json_f)
        json_content["Outputs"] = list_of_outputs
    return json_content

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Extract watchdog list of files to HBP JSON metadata')
    parser.add_argument('--json', type=argparse.FileType('r'), metavar='json', nargs=1,
                        help='JSON File containing in which metadata of files are extracted', required=True)
    parser.add_argument('--watchdog', type=argparse.FileType('r'), metavar='watchdog', nargs=1,
                        help='Watchdog File containing files to extract to JSON report', required=True)


    args = parser.parse_args()
    
    json_file = args.json[0]
    watchdog_file = args.watchdog[0]

    # Convert watchdog list to JSON content
    json_content = extract_watchdog_to_json (watchdog_file.name, json_file.name)

    # Write JSON content to JSON file
    with open(json_file.name, "w") as f:
        json.dump(json_content, f, indent=4) 
    # Exit Done ?
    sys.exit()