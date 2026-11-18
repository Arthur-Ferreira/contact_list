from django.shortcuts import render
from django.contrib import messages
from django.db import DatabaseError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import ContactForm
from .models import Contact
from .services import search_contacts

def home(request):
    return render(request, "contacts/home.html")

def add(request):
    form = ContactForm(request.POST) if request.method == "POST" else ContactForm()
    if request.method == "POST":
        if form.is_valid():
            try:
                form.save()
            except DatabaseError:
                messages.error(request, "Erro ao adicionar novo contato. Por favor, tente novamente.")
            else:
                messages.success(request, "Contato adicionado com sucesso!")
                return redirect("contacts:home")
        else:
            messages.error(request, "Não foi possivel adicionar o contato. Por favor, revise o erro abaixo.")
    return render(request, "contacts/form.html",
                  {"form": form, "title": "Adicionar contato", "submit": "Salvar"})


def search(request):
    by = request.GET.get("by", "name")
    q = request.GET.get("q", "").strip()
    results = None
    if q:
        results = search_contacts(phone=q) if by == "phone" else search_contacts(name=q)
    return render(request, "contacts/search.html", {"by": by, "q": q, "results": results})


def pick(request, mode):
    return render(request, "contacts/pick.html",
                  {"contacts": Contact.objects.all(), "mode": mode})


def edit(request, pk):
    contact = Contact.objects.filter(pk=pk).first()
    if contact is None:
        messages.error(request, "Error editing: contact not found.")
        return redirect("contacts:pick_edit")

    form = (ContactForm(request.POST, instance=contact)
            if request.method == "POST" else ContactForm(instance=contact))
    if request.method == "POST":
        if form.is_valid():
            try:
                form.save()
            except DatabaseError:
                messages.error(request, "Erro ao atualizar o contato. Por favor, tente novamente.")
            else:
                messages.success(request, "Contato atualizado com sucesso!")
                return redirect("contacts:pick_edit")
        else:
            messages.error(request, "Contato não pode ser editado. Por favor, revise o erro abaixo.")
    return render(request, "contacts/form.html",
                  {"form": form, "title": "Editar contato", "submit": "Atualizar"})


@require_POST
def delete(request, pk):
    contact = Contact.objects.filter(pk=pk).first()
    if contact is None:
        messages.error(request, "Erro ao excluir: contato não encontrado.")
    else:
        name = contact.name
        try:
            contact.delete()
        except DatabaseError:
            messages.error(request, "Erro ao excluir o contato. Por favor, tente novamente.")
        else:
            messages.success(request, f"Contato “{name}” excluido com sucesso!")
    return redirect("contacts:pick_remove")

