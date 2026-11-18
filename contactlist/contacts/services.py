from .models import Contact


def search_contacts(name=None, phone=None):
    contacts = Contact.objects.all()
    if phone:
        contacts = contacts.filter(phone__contains=phone.strip())
    contacts = list(contacts)
    if name:
        needle = name.strip().casefold()
        contacts = [c for c in contacts if needle in c.name.casefold()]
    return contacts