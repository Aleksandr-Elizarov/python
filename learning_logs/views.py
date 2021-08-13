from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.

def index(request):
    """Home page of the application Learning Log."""
    return render(request, 'learning_logs/index.html')


@login_required()
def topics(request):
    """Displays a list of topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required()
def topic(request, topic_id):
    """Displays a topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    # Checking that the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required()
def new_topic(request):
    """Defines a new topic."""
    if request.method != 'POST':
        # No data was sent; an empty form is created.
        form = TopicForm()
    else:
        # POST data sent; process the data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # Display an empty or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required()
def new_entry(request, topic_id):
    """Adds a new entry for a specific topic."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # No data was sent; an empty form is created.
        form = EntryForm()
    else:
        # POST data sent; process the data.
        form = EntryForm(data=request.POST)
        if topic.owner != request.user:
            raise Http404
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Output an empty or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required()
def edit_entry(request, entry_id):
    """Edits an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # The original request; The form is filled in with the current entry data.
        form = EntryForm(instance=entry)
    else:
        # POST data sent; process the data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
