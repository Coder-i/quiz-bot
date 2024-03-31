from django.shortcuts import render
from .models import Session

def chat(request):
  if not request.session.session_key:
    request.session.create()

  # Check if a session object exists for the current session_key
  session, created = Session.objects.get_or_create(session_key=request.session.session_key)

  context = {
    'session': session,
  }
  return render(request, 'chat.html', context)
