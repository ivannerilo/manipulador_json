from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from . import util

DEFAULT_ARCHIVE_NUM = 0

class editForm(forms.Form):
    new_content = forms.CharField(
		widget=forms.Textarea(attrs={'rows': 10, 'cols': 220}),
	)

# Create your views here.
def index(request):
    return HttpResponseRedirect(f'/{DEFAULT_ARCHIVE_NUM}')

def show_json(request, archive_num):
    num = archive_num
    file_size = util.json_file_size()
    if request.method == 'POST':
        match request.POST['ação']:
            case 'next':
                num += 1
            case 'back':
                num -= 1
        if num < 0 or num > file_size -1:
            num = 0
        return HttpResponseRedirect(f'/{num}')

    correct_content = []
    json = util.json_reader(archive_num)
    correct_content = util.formatador_html(correct_content, json)
    return render(request, "manipulador/index.html", {
        "correct_content": correct_content
    })
        

def edit_json(request, archive_num):
    if request.method == 'POST':
        return render(request, "manipulador/teste.html", {
            "teste": request.POST
        })

    correct_form = []
    json = util.json_reader(archive_num)
    correct_form = util.formatador_formulario(correct_form, json)
    return render(request, "manipulador/edit.html", {
        "correct_form": correct_form
    })





