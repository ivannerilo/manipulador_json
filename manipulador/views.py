from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import util

DEFAULT_ARCHIVE_NUM = 0

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
    return render(request, 'manipulador/index.html', {
        "json": util.json_reader(archive_num)
    })

def edit_json(request, archive_num):
    return render(request, 'manipulador/edit.html', {
        "json": util.json_reader(archive_num)
    })





