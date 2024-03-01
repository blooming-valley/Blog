from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    '''Main page for blogs'''
    return render(request, 'blogs/index.html')

@login_required
def topics(request):
    """Showing all Blogs."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'blogs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Showing a single Blog and all its Post."""
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'blogs/topic.html', context)

@login_required
def new_topic(request):
    '''Add a new blog'''
    if request.method != 'POST':
        form = TopicForm()
    else:
        # POST data submitted; process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('blogs:topics')
    
    # Shoing a blank form
    context = {'form' : form}
    return render(request, 'blogs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    '''Add a new post for a select blog'''
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request.user)
    
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('blogs:topic', topic_id=topic_id)
        
    # Displaying blank form
    context = {'topic': topic, 'form': form}
    return render(request, 'blogs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    '''Edit an existing post'''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic 
    check_topic_owner(topic, request.user)
    
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:topic', topic_id=topic.id)
        
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'blogs/edit_entry.html', context)

def check_topic_owner(topic, user):
    """Make sure the currently logged-in user owns the Blog that's 
    being requested.

    Raise Http404 error if the user does not own the Blog.
    """
    if topic.owner != user:
        raise Http404 