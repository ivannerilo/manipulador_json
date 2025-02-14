import json 

def json_reader(num):
    with open("json_files/jsonfile2.jsonl","r") as f:
        jsonfiles = list(f)
        jsonfile = json.loads(jsonfiles[num])
        return jsonfile

def json_file_size():
    with open("json_files/jsonfile2.jsonl","r") as f:
        jsonfiles = list(f)
        return len(jsonfiles)






        
        
        
