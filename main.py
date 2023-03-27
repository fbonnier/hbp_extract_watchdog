import argparse
import json
import sys

def extract_watchdog_to_json (watchdog_file:str, json_file:str):
    
    list_of_outputs = []

    with open (watchdog_file, 'r') as f:
        singletons = list(dict.fromkeys(f.readlines()))

        for ifile in singletons:
            list_of_outputs.append({"url": None, "path": ifile})

    json_content = json.load(json_file)
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
    json_content = extract_watchdog_to_json (watchdog_file.name, json_file).name

    # Write JSON content to JSON file
    with open(json_file, "w") as f:
        json.dump(json_content, f, indent=4) 
    # Exit Done ?
    sys.exit()