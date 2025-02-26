from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from . import util
import json
from .models import FileUser
from random import randint

DEFAULT_ARCHIVE_NUM = 0
DEFAULT_ARCHIVE_NAME = "jsonfile.jsonl"
DEFAULT_WRITE_FILE = "jsonfile1.jsonl"
DEFAUL_FILE_ROUTE = "json_files/files/"


class editForm(forms.Form):
    new_content = forms.CharField(
		widget=forms.Textarea(attrs={'rows': 10, 'cols': 220}),
	)

class createForm(forms.Form):
    new_content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 100, 'cols': 220})
    )

class fileForm(forms.Form):
    new_file = forms.FileField()

def index(request):
    if request.method == 'POST':
        uploaded_file = request.FILES["new_file"]
        data = FileUser(
            file = uploaded_file,
            user_session = request.session.session_key
        )
        data.save()
    user_files = FileUser.objects.filter(user_session=request.session.session_key)
    return render(request, "manipulador/home.html", {
        "DEFAULT_ARCHIVE_NUM": DEFAULT_ARCHIVE_NUM,
        "DEFAULT_ARCHIVE_NAME": DEFAULT_ARCHIVE_NAME,
        "form": fileForm(),
        "user_files": user_files
    })
    # return HttpResponseRedirect(f'/{DEFAULT_ARCHIVE_NUM}')

def download_json(request, archive_name):
    uf = FileUser.objects.filter(user_session=request.session.session_key)
    # files_names = list(uf.file_name)
    # if not archive_name in files_names:
    #     pass #fazer verifcação para que o usário não faça downlaod de arquivos que não são dele.
    downlaod_file = util.file_reader(archive_name)
    response = HttpResponse(downlaod_file, content_type="aplication/jsonline")
    response["content-disposition"] =  f'attachment; filename="{archive_name}"'
    return response

def delete_json(request, archive_name):
    util.delete_file(archive_name)
    FileUser.objects.get(file_name=archive_name).delete()
    return HttpResponseRedirect("/")

def show_json(request, archive_num, archive_name):
    file_size = util.json_file_size(archive_name)
    if request.method == 'POST':
        match request.POST['ação']:
            case 'next':
                archive_num += 1
            case 'back':
                archive_num -= 1
        if archive_num < 0:
            archive_num = file_size - 1
        elif archive_num > file_size -1:
            archive_num = 0
        return HttpResponseRedirect(f'/{archive_num}/{archive_name}')

    json_dict = util.json_reader(archive_num, archive_name) # Implementar o upload de arquivos.
    content_list = util.formatador_html(json_dict)
    return render(request, "manipulador/index.html", {
        "correct_content": content_list[1:],
        "archive_num": archive_num,
        "archive_name": archive_name
    })
        

def edit_json(request, archive_num, archive_name):
    if request.method == 'POST':
        json_dict = util.json_reader(archive_num, archive_name)
        for i in range(len(request.POST) - 1):
            if isinstance(json_dict["messages"][i]["content"], list):
                json_dict["messages"][i]["content"][0]["text"] = request.POST[f"{i}"]
            else:
                json_dict["messages"][i]["content"] = request.POST[f"{i}"]
        util.json_file_editor(json_dict, archive_num, archive_name)
        return HttpResponseRedirect(f"/{archive_num}/{archive_name}")
    
    json_dict = util.json_reader(archive_num, archive_name)
    lista_forms = util.formatador_formulario(json_dict)
    return render(request, "manipulador/edit.html", {
        "lista_forms": lista_forms
    })

def create_json(request): 
    random_json_name = util.random_file_name_gen()
    if request.method == 'POST':
        form = createForm(request.POST)
        if form.is_valid():
            new_json_string = request.POST.get("new_content")
            formated_json = util.json_formater(new_json_string) # json vem formatado aleluia
            print(formated_json)
            json_dict = json.loads(formated_json)
            util.json_writer(json_dict, random_json_name, "w")
            created_file = DEFAUL_FILE_ROUTE + random_json_name
            data = FileUser(
                file = created_file,
                user_session = request.session.session_key
            )
            data.save()
            return HttpResponseRedirect(f"/") #rota antiga /{DEFAULT_ARCHIVE_NUM}/{created_file}
    return render(request, "manipulador/create.html", {
        "form": createForm()
    })
    

def append_json(request, archive_name):
    if request.method == 'POST':
        form = createForm(request.POST)
        if form.is_valid():
            new_json_string = request.POST.get("new_content")
            formated_json = util.json_formater(new_json_string) 
            json_dict = json.loads(formated_json)
            util.json_writer(json_dict, archive_name, 'a')
            return HttpResponseRedirect(f"/{DEFAULT_ARCHIVE_NUM}/{archive_name}") #rota antiga /{DEFAULT_ARCHIVE_NUM}/{created_file}
    return render(request, "manipulador/create.html", {
        "form": createForm()
    })
