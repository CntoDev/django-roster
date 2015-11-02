from django.utils import timezone
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.http import Http404
from django.template.context_processors import csrf
from cnto.models import Member
from cnto_notes.forms import NoteForm

from models import Note


def activate_note(request, pk):
    """Browse reports
    """

    success = True
    if not request.user.is_authenticated():
        success = False
    else:
        try:
            note = Note.objects.get(pk=pk)
            note.active = True
            note.save()
        except Note.DoesNotExist:
            return JsonResponse({
                "success": False
            })

        notes = Note.objects.filter(active=True, member=note.member)
        for note in notes:
            note.active = False
            note.save()

        note.active = True
        note.save()

    return JsonResponse({
        "success": success
    })


def delete_note(request, note_pk):
    """Return the daily process main overview page.
    """

    if not request.user.is_authenticated():
        return redirect("login")

    print "Deleting %s" % (note_pk, )

    try:
        note = Note.objects.get(pk=note_pk)
        note.delete()
        return JsonResponse({"success": True})
    except Note.DoesNotExist:
        return JsonResponse({"success": False})


def handle_note_change_view(request, edit_mode, note):
    if request.POST:
        form = NoteForm(request.POST, instance=note)
        if request.POST.get("cancel"):
            return redirect('edit-note-collection', note.member.pk)
        elif form.is_valid():
            try:
                active_note = Note.objects.get(member=note.member, active=True)
                active_note.active = False
                active_note.save()
            except Note.DoesNotExist:
                pass

            form.instance.active = True
            form.instance.dt = timezone.now()
            form.save()
            return redirect('edit-note-collection', note.member.pk)
    else:
        form = NoteForm(instance=note)

    context = {}
    context.update(csrf(request))

    context['form'] = form
    context["edit_mode"] = edit_mode
    context["member"] = note.member

    return render_to_response('cnto_notes/edit.html', context)


def create_note(request, member_pk):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")

    try:
        member = Member.objects.get(pk=member_pk)
    except Member.DoesNotExist:
        raise Http404()

    note = Note(member=member)

    return handle_note_change_view(request, edit_mode=False, note=note)


def edit_note(request, note_pk):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")

    try:
        note = Note.objects.get(pk=note_pk)
    except Note.DoesNotExist:
        raise Http404()

    return handle_note_change_view(request, edit_mode=True, note=note)


def edit_note_collection(request, member_pk):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")

    try:
        member = Member.objects.get(pk=member_pk)
    except Member.DoesNotExist:
        raise Http404()

    context = {
        "member": member,
        "notes": sorted(Note.objects.filter(member=member), key=lambda x: x.dt,
                        reverse=True),
    }

    return render(request, 'cnto_notes/list-for-member.html', context)
