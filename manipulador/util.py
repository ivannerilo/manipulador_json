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

def formatador_html(lista, json):
    for messages in json["messages"][1:]:
        if isinstance(messages["content"], list):
            content =  f"""
                <div>
                    <p><strong>{messages["role"]}</strong></p>
                    <textarea rows="10", cols="220">{messages["content"][0]["text"]}</textarea>
                </div>
            """
            lista.append(content)
        else:
            content =  f"""
                <div>
                    <p><strong>{messages["role"]}</strong></p>
                    <textarea rows="10", cols="220">{messages["content"]}</textarea>
                </div>
            """
            lista.append(content)
    return lista


def formatador_formulario(lista, json):
    id = 0
    for messages in json["messages"]:
        if isinstance(messages["content"], list):
            content =  f"""
                <p><strong>{messages["role"]}</strong></p>
                <textarea name="{id}" rows="10", cols="220">{messages["content"][0]["text"]}</textarea>
            """
            lista.append(content)
        else:
            content =  f"""
                <p><strong>{messages["role"]}</strong></p>
                <textarea name="{id}"  rows="10", cols="220">{messages["content"]}</textarea>
            """
            lista.append(content)
        id += 1
    return lista





        
        
        
