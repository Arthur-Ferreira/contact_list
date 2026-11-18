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
                messages.error(request, "Error adding the contact. Please try again.")
            else:
                messages.success(request, "Contact added successfully!")
                return redirect("contacts:home")
        else:
            messages.error(request, "Could not add the contact. Fix the errors below.")
    return render(request, "contacts/form.html",
                  {"form": form, "title": "Add contact", "submit": "Save"})


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
                messages.error(request, "Error updating the contact. Please try again.")
            else:
                messages.success(request, "Contact updated successfully!")
                return redirect("contacts:pick_edit")
        else:
            messages.error(request, "Could not update the contact. Fix the errors below.")
    return render(request, "contacts/form.html",
                  {"form": form, "title": "Edit contact", "submit": "Update"})


@require_POST
def delete(request, pk):
    contact = Contact.objects.filter(pk=pk).first()
    if contact is None:
        messages.error(request, "Error deleting: contact not found.")
    else:
        name = contact.name
        try:
            contact.delete()
        except DatabaseError:
            messages.error(request, "Error deleting the contact. Please try again.")
        else:
            messages.success(request, f"Contact “{name}” deleted successfully!")
    return redirect("contacts:pick_remove")


def exit_page(request):
    return render(request, "contacts/exit.html")