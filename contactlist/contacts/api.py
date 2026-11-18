from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Router, Schema

from .models import Contact
from .services import search_contacts

api = NinjaAPI(title="Contact List API", version="1")
router = Router(tags=["contacts"])


class ContactIn(Schema):
    name: str
    phone: str
    email: str


class ContactPatch(Schema):
    name: str | None = None
    phone: str | None = None
    email: str | None = None


class ContactOut(Schema):
    id: int
    name: str
    phone: str
    email: str


@api.exception_handler(ValidationError)
def on_validation_error(request, exc):
    return api.create_response(
        request,
        {"detail": "Validation failed.", "errors": exc.message_dict},
        status=422,
    )


def _save(contact, data):
    for field, value in data.items():
        setattr(contact, field, value)
    contact.full_clean()
    contact.save()
    return contact


@api.get("/", summary="Options menu")
def menu(request):
    return {
        "options": ["add", "search", "edit", "remove", "exit"],
        "endpoints": {
            "add": "POST /api/v1/contacts",
            "search": "GET /api/v1/contacts?name={text} | ?phone={text}",
            "list": "GET /api/v1/contacts",
            "get": "GET /api/v1/contacts/{id}",
            "edit": "PUT|PATCH /api/v1/contacts/{id}",
            "remove": "DELETE /api/v1/contacts/{id}",
        },
    }


@router.get("", response=list[ContactOut])
def list_contacts(request, name: str | None = None, phone: str | None = None):
    return search_contacts(name=name, phone=phone)


@router.post("", response={201: ContactOut})
def create_contact(request, payload: ContactIn):
    return 201, _save(Contact(), payload.model_dump())


@router.get("/{contact_id}", response=ContactOut)
def get_contact(request, contact_id: int):
    return get_object_or_404(Contact, id=contact_id)


@router.put("/{contact_id}", response=ContactOut)
def replace_contact(request, contact_id: int, payload: ContactIn):
    contact = get_object_or_404(Contact, id=contact_id)
    return _save(contact, payload.model_dump())


@router.patch("/{contact_id}", response=ContactOut)
def update_contact(request, contact_id: int, payload: ContactPatch):
    contact = get_object_or_404(Contact, id=contact_id)
    return _save(contact, payload.model_dump(exclude_unset=True))


@router.delete("/{contact_id}", response={204: None})
def delete_contact(request, contact_id: int):
    get_object_or_404(Contact, id=contact_id).delete()
    return 204, None


api.add_router("/contacts", router)