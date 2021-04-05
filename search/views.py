from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from task5_vector_search.vector_search import Query


# Create your views here.
def index(request):
    context = {
        'text': 'HUI SOSI DA',
    }
    return render(request, 'search/index.html', context)


def search(request):
    vs = Query()
    result = vs.serve_query(request.GET['query'])
    res = []
    for r in result:
        res.append(str(r.split('\\')[-1]).split('.')[0])
    if not res:
        res = None
    context = {
        'results': res,
        'message': f'No results found for: {request.GET["query"]}'
    }
    return render(request, 'search/index.html', context)


def results(request, string):
    file_name = string.split('\\')[-1]
    # Suppressed due to pages are updated since indexing
    # with open('task1_crawler/index.txt', 'r', encoding='utf-8') as file:
    #     for ele in file.readlines():
    #         if file_name in ele:
    #             return HttpResponseRedirect(ele.split('  ')[0])
    with open(f'task1_crawler/output/{file_name}.html', 'r', encoding='utf-8') as file:
        return HttpResponse(file.read())
