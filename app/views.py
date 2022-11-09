from django.shortcuts import render

QUESTIONS = [
    {
        "title": f"Question №{i}",
        "text": f"# {i} Question text",
        "q_num": i
    } for i in range(1, 4)
]

TAGS = [
    {
        "name": f"Tag#{i}",
        "t_num": i
    } for i in range(1, 10)
]

def index(request):
    return render(request, 'index.html', {"questions": QUESTIONS, "tags": TAGS})

def ask(request):
    return render(request, 'ask.html', {"tags": TAGS})

def question(request, i: int):
    return render(request, 'question.html', {"question": QUESTIONS[i-1], "tags": TAGS})

def login(request):
    return render(request, 'login.html', {"tags": TAGS})

def register(request):
    return render(request,'regster.html', {"tags": TAGS})
