from django.shortcuts import render
from .models import Tweet   
from .forms import Tweetform, CustomUserCreationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
# Create your views here.

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

# def tweet_create(request):
#     if:
#         pass
#     else: 
#         form = Tweetform()
#     return render(request, 'tweet_create.html', {'form': form})
@login_required
def tweet_create(request):
    if request.method == 'POST':
        tweet = Tweetform(request.POST, request.FILES)
        if tweet.is_valid():
            tweet_instance = tweet.save(commit=False)
            tweet_instance.user = request.user
            tweet_instance.save()
            return redirect('tweet_list')
    else: 
        form = Tweetform()
    return render(request, 'tweet_create.html', {'form': form})

@login_required
def edit_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = Tweetform(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
           tweet = form.save(commit=False)
           tweet.user = request.user
           tweet.save()
        return redirect('tweet_list')
    else:
        form = Tweetform(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()          # Saves the user
            login(request, user)        # Logs them in
            return redirect('tweet_list')

    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


    # return render(request, 'registration/register.html', {'form': form})