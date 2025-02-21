import json 
import re

DEFAUL_FILE_ROUTE = "json_files/files/"

def json_reader(archive_num, archive_name):
    with open(f"{DEFAUL_FILE_ROUTE}{archive_name}", "r") as file:
        json_files = list(file)
        json_file = json.loads(json_files[archive_num])
        return json_file

def json_writer(json_dict, archive_name):
    with open(f"{DEFAUL_FILE_ROUTE}{archive_name}", "a", encoding="utf-8") as file:
        file.write(json.dumps(json_dict, ensure_ascii=False)+ '\n')

def json_file_editor(json_dict, archive_num, archive_name):
    with open(f"{DEFAUL_FILE_ROUTE}{archive_name}", "r") as file_read:
        json_files = list(file_read)
        with open(f"{DEFAUL_FILE_ROUTE}{archive_name}", "w", encoding="utf-8") as file_write:
            for i in range(len(json_files)):
                if i == archive_num:
                    file_write.write(json.dumps(json_dict, ensure_ascii=False)+ '\n')
                else:
                    jsonzinho = json.loads(json_files[i].strip())
                    file_write.write(json.dumps(jsonzinho, ensure_ascii=False)+ '\n')


        
def json_file_size(archive_name):
    with open(f"{DEFAUL_FILE_ROUTE}{archive_name}","r") as f:
        jsonfiles = list(f)
        return len(jsonfiles)

# Formatadores ----
def json_formater(json_string):
    pattern = r'response_format=\s*{\s*"type":\s*"text"\s*},?'
    json_string = json_string.replace("messages=", '{"messages": ')
    json_string = re.sub(pattern, '', json_string)
    json_string = json_string.replace('tools=', '"tools": ')
    json_string = json_string.replace('"strict": False,', "")
    json_string = json_string + '}'
    return json_string

def formatador_html(json_dict):
    lista_json_formatado = []
    for messages in json_dict["messages"]:
        if isinstance(messages["content"], list):
            content =  f"""
                <div>
                    <p><strong>{messages["role"]}</strong></p>
                    <textarea rows="10", cols="220">{messages["content"][0]["text"]}</textarea>
                </div>
            """
            lista_json_formatado.append(content)
        else:
            content =  f"""
                <div>
                    <p><strong>{messages["role"]}</strong></p>
                    <textarea rows="10", cols="220">{messages["content"]}</textarea>
                </div>
            """
            lista_json_formatado.append(content)
    return lista_json_formatado


def formatador_formulario(json_dict):
    lista_json_formatado = []
    id = 0
    for messages in json_dict["messages"]:
        if isinstance(messages["content"], list):
            content =  f"""
                <p><strong>{messages["role"]}</strong></p>
                <textarea name="{id}" rows="10", cols="220">{messages["content"][0]["text"]}</textarea>
            """
            lista_json_formatado.append(content)
        else:
            content =  f"""
                <p><strong>{messages["role"]}</strong></p>
                <textarea name="{id}" rows="10", cols="220">{messages["content"]}</textarea>
            """
            lista_json_formatado.append(content)
        id += 1
    return lista_json_formatado





        
        
        
