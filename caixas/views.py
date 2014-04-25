# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import Q
from .models import Caixa
from pessoas.models import Pessoa


def index(request):
    return render(request, 'index.html')


def caixaListar(request):
    caixas = Caixa.objects.all()[0:10]
    pessoas = Pessoa.objects.all()[0:10]

    return render(request, 'caixas/listaCaixas.html', {'caixas': caixas, 'pessoas': pessoas})


def caixaAdicionar(request):
    pessoas = Pessoa.objects.all()
    return render(request, 'caixas/formCaixas.html', {'pessoas': pessoas})



def caixaSalvar(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '0')

        try:
            caixa = Caixa.objects.get(pk=codigo)
        except:
            caixa = Caixa()

        caixa.pessoa_id = request.POST.get('pessoa_id', '0')
        caixa.pessoa = Pessoa.objects.get(pk=request.POST.get('pessoa','1'))
        caixa.tipo = request.POST.get('tipo', '').upper()
        caixa.descricao = request.POST.get('descricao', '').upper()
        caixa.valor = request.POST.get('valor', '').upper()
        caixa.pagseguro = request.POST.get('pagseguro', '').upper()
        caixa.data = request.POST.get('data', '')

        caixa.save()
    return HttpResponseRedirect('/caixas/')


def caixaPesquisar(request):
    if request.method == 'POST':
        textoBusca = request.POST.get('textoBusca', 'TUDO').upper()

        try:
            if textoBusca == 'TUDO':
                caixas = Caixa.objects.all()
            else:
                caixas = Caixa.objects.filter(
                    (Q(tipo__contains=textoBusca) |
                    Q(descricao__contains=textoBusca) |
                    Q(valor__contains=textoBusca) |
                    Q(pagseguro__contains=textoBusca) |
                    Q(data__contains=textoBusca))).order_by('-tipo')
        except:
            caixas = []

        return render(request, 'caixas/listaCaixas.html', {'caixas': caixas, 'textoBusca': textoBusca})


def caixaEditar(request, pk=0):
    try:
        caixa = Caixa.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/caixas/')

    return render(request, 'caixas/formCaixas.html', {'caixa': caixa})


def caixaExcluir(request, pk=0):
    try:
        caixa = Caixa.objects.get(pk=pk)
        caixa.delete()
        return HttpResponseRedirect('/caixas/')
    except:
        return HttpResponseRedirect('/caixas/')
