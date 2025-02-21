from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from . import util
import json
from .models import FileUser
from random import randint

DEFAULT_ARCHIVE_NUM = 0
DEFAULT_ARCHIVE_NAME = "jsonfile.jsonl"
DEFAULT_WRITE_FILE = "jsonfile1.jsonl"


class editForm(forms.Form):
    new_content = forms.CharField(
		widget=forms.Textarea(attrs={'rows': 10, 'cols': 220}),
	)

# class fileForm(forms.Form):
#     json_file = forms.FileField(upload_to="/json_files")

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

def show_json(request, archive_num, archive_name):
    file_size = util.json_file_size(archive_name)
    if request.method == 'POST':
        match request.POST['ação']:
            case 'next':
                archive_num += 1
            case 'back':
                archive_num -= 1
        if archive_num < 0 or archive_num > file_size -1:
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

def create_json(request): #adicionar esse novo arquivo na db, não está sendo adicionado e não aparece no home
    random_json_name = f"{request.session.session_key}.jsonl"
    if request.method == 'POST':
        form = createForm(request.POST)
        if form.is_valid():
            new_json_string = request.POST.get("new_content")
            formated_json = util.json_formater(new_json_string) # json vem formatado aleluia
            json_dict = json.loads(formated_json)
            util.json_writer(json_dict, random_json_name)
            return HttpResponseRedirect(f"/{DEFAULT_ARCHIVE_NUM}/{DEFAULT_WRITE_FILE}")
    return render(request, "manipulador/create.html", {
        "form": createForm()
    })