from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count

# from django.conf import settings

# Local imports
from .models import Poll, Choices, Vote
from .forms import Pollform, EditPollForm, AddPollForm

# Create your views here.
# the next @login_required will not permit the user to see the polls if not logged in
# the raw CODE to do it is the folloing,
# if not request.user.is_authenticated():
#     return redirect('{}?next={}'.format(settings.LOGIN_URL, request.PATH))

@login_required
def poll_view(request):
    """
    Renders polls_list.html template which contains all the available polls
    """
    poll_txt = Poll.objects.all()
    search_term=''


    if 'text' in request.GET:
        poll_txt = poll_txt.order_by('text') #This 'text' is from Poll class in models.py

    # commented cuz i didn't create date field in the class in models.py
    # if 'date' in request.GET:
    #     poll_txt = poll_txt.order_by('-pub_date')

    if 'num_votes' in request.GET:
        poll_txt = poll_txt.annotate(Count('vote')).order_by('vote__count') # The Vote class in models.py

    if 'search' in request.GET:
        search_term = request.GET['search']
        poll_txt = poll_txt.filter(text__icontains=search_term) # text from models.py


    paginator = Paginator(poll_txt, 5) # making it 5 pages
    page = request.GET.get('page')
    poll_txt = paginator.get_page(page)

    get_dict_copy = request.GET.copy() # Getting a copy of this dictionary
            # removing page from the dict cuz we already have it in the polls_list
            # and will add params next to page anyway
            # then urlencode to make it looks like normal string
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    params = '&'+params

    context = {
    'poll_txt':poll_txt,
    'params':params,
    'search_term':search_term,
    }
    return render(request, 'polls/polls_list.html',  context)

@login_required
def add_poll(request):
    if request.method == 'POST' :
        form = Pollform(request.POST)
        new_poll = form.save(commit=False) # commit=False is the way to tell django not to commit the data
                                          # to the database now, wait untill we finish and will commit it by us
        new_poll.number = 123 #just anything random
        new_poll.owner = request.user # attach the created poll to the user who made it
        new_poll.save() # now we saving it manually
                        # will add to Poll Class, see it in Admin page

        # to add the polls user made to the data base and to the Choices class in models.py
        # print(form.cleaned_data) to see inside form.cleaned_data
        # new_poll returns the text field by default

        choice1 = Choices(poll = new_poll, choice_text=form.cleaned_data['choice1']).save()
        choice2 = Choices(poll = new_poll, choice_text=form.cleaned_data['choice2']).save()

        messages.success(request,
                            'Poll has been updated successfully',
                            extra_tags='alert alert-success alert-dismissible fade show') # Bootstrap classes

        return redirect('polls:poll_view')
    else:
        form = Pollform()
    return render(request, 'polls/add_poll.html', context={'form':form})

@login_required
def poll_delete(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.user != poll.owner:
        redirect('/')
    if request.method == 'POST':
        poll.delete()
        messages.success(
            request,
            'Poll has been deleted successfully',
            extra_tags='alert alert-success alert-dismissible fade show'
        )
        return redirect('polls:poll_view')
    return render(request, 'polls/delete_poll.html', {'poll': poll})


@login_required
def edit_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    # to check if it's user who's trying to edit it
    # if it's another user, will redirect him to home page
    if request.user != poll.owner:
        return redirect('/')

    # to edit the choosen poll
    # grapping the text field from Poll class with EditPollForm
    # then adding a new value into it in edit_poll.html
    # then passing it again using the ifs below

    if request.method == 'POST':
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            messages.success(request,
                            'Poll has been Edited successfully',
                            extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:poll_view')
    else:
        form = EditPollForm(instance=poll)

    return render(request, 'polls/edit_poll.html', {'form':form, 'poll':poll})


@login_required
def add_choice(request, poll_id):
        poll = get_object_or_404(Poll, id=poll_id)
        # to check if it's user who's trying to edit it
        # if it's another user, will redirect him to home page
        if request.user != poll.owner:
            return redirect('/')

        if request.method == 'POST':
            form = AddPollForm(request.POST)
            if form.is_valid():
                new_choice = form.save(commit=False)
                new_choice.poll = poll
                # new_choice.poll, poll is from Choices class from models.py
                # = poll , poll is the variable above
                new_choice.save()
                messages.success(request,
                                'Choice has been Added successfully',
                                extra_tags='alert alert-success alert-dismissible fade show')
                return redirect('polls:poll_view')
        else:
            form = AddPollForm()

        return render(request, 'polls/add_choice.html', {'form':form})


@login_required
def edit_choice(request, choice_id):
        choice = get_object_or_404(Choices, id=choice_id)
        poll = get_object_or_404(Poll, id=choice.poll.id)

        if request.user != poll.owner:
            return redirect('/')

        if request.method == 'POST':
            form = AddPollForm(request.POST, instance=choice)
            if form.is_valid():
                new_choice = form.save(commit=False)
                new_choice.poll = poll
                # new_choice.poll, poll is from Choices class from models.py
                # = poll , poll is the variable above
                new_choice.save()
                messages.success(request,
                                'Choice has been Edited successfully',
                                extra_tags='alert alert-success alert-dismissible fade show')
                return redirect('polls:poll_view')
        else:
            form = AddPollForm(instance=choice)

        return render(request, 'polls/add_choice.html', {'form':form,'choice':choice, 'edit_mode':True} )

@login_required
def choice_delete(request, choice_id):
        choice = get_object_or_404(Choices, id=choice_id)
        poll = get_object_or_404(Poll, id=choice.poll.id)

        if request.user != poll.owner:
            return redirect('/')

        if request.method == 'POST':
            choice.delete()
            messages.success(request,
                                'Choice has been Edited successfully',
                                extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:poll_view')

        return render(request, 'polls/delete_choice.html', {'choice':choice} )



@login_required
def poll_detailes(request, poll_id): # poll_id passed from urls.py file
    '''
    Renders poll_details.html which allow the user to vote
    '''
    poll_choice = get_object_or_404(Poll, id=poll_id) # id gets it's value from the polls_list.html

    # get_object_or_404 returns a 404 page if it couldn't get the id instead of displaying the server error page
    # to display server error page use:
        # poll_choice = Poll.objects.get(id=poll_id)

    user_can_vote = poll_choice.user_can_vote(request.user)
    resaults = poll_choice.get_percentages()

    context = {
        'poll_choice':poll_choice,
        'user_can_vote':user_can_vote,
        'resaults':resaults
    }

    # a way to check the request whether it's a POST or a GET from polls_detailes.html
    # if request.method == 'POST':
    #      print(request.POST)
    #     print('you POSTED !!!')
    # if request.method == 'GET':
    #     print(request.GET)
    #     print('you GET')

    return render(request, 'polls/polls_detailes.html', context)

@login_required
def poll_vote(request, poll_id):
    poll_choice = get_object_or_404(Poll, id=poll_id)
    choice_id = request.POST.get('choice', None) # this choice is the key from a dictionary caused by the POST method
                                           # here we are getting the value of that key which will be the id
                                           # from form of the polls_details.html
                                           # print(request.POST) #putting it first in this def to see that dict
                                           # POST[''] using those brackets is how to get the value of a key from dict
    # use .get() above to check if 'choice'
    # is available or not in the POST dict
    # .get() is a built-in python method

    if not poll_choice.user_can_vote(request.user):
                messages.error(request, 'You have already voted here !!!')
                return HttpResponseRedirect(reverse('polls:poll_details', args=(poll_id,)))

    if choice_id: # check if choice_id is not a None
        choice = Choices.objects.get(id=choice_id) # will return an entire object of the value of this id
        # print(choice) just for testing purposes
        # poll_choice = choice.poll # to get poll_choice var from poll_details above
        new_vote = Vote(user=request.user, poll=poll_choice, choice=choice)
        new_vote.save()
        return render(request, 'polls/polls_detailes.html', {'poll_choice':poll_choice})
        # return redirect('polls:poll_details', poll_id=poll_id) Doing the same as above

            # the old poll_choice in line 58 just imported it as a variable above
            # follow models.py and poll_details def above to get the idea
    else:
        messages.error(request, 'No Choice Was Found !!!')
        return HttpResponseRedirect(reverse('polls:poll_details', args=(poll_id,)))
        # polls and poll_detailes are namespace and name from the urls.py files
        # and it redirecting to def poll_results cuz i wanna to dispaly the error in the same page
