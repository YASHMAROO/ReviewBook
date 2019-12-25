from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from games.models import GameReview, Game
from games.forms import GiveReviewForm, UpdateReviewForm
from accounts.models import Account

def give_game_review(request, game_id):

    context = {}

    user = request.user
    game = get_object_or_404(Game, id=game_id)
    if not user.is_authenticated:
        return redirect('accounts:must_authenticate')

    review = GameReview.objects.filter(game_id=game_id, author=request.user)
    if len(review)==0:
        form = GiveReviewForm(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.game = game
            obj.author = user
            obj.save()
            form = GiveReviewForm()
            return redirect('games:review_detail', obj.slug)

        context['form']=form

        return render(request, 'give_game_review.html', context)
    else:
        return redirect('games:review_detail', review[0].slug)

def select_game(request):
    games = Game.objects.all()
    context ={'games':games}

    return render(request, 'select_game.html', context)

def index(request):
    game_list= Game.objects.order_by('-name')
    context = {'game_list':game_list}
    return render(request,'games/gamelist.html',context)

def details(request,game_id):
    game= get_object_or_404(Game,pk=game_id)
    return render(request,'games/details.html',{'game':game})

def review_detail(request, slug):
    context = {}
    review = get_object_or_404(GameReview, slug=slug)
    context['review']=review

    return render(request, 'games/review_detail.html', context)

def edit_review(request, slug):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('accounts:must_authenticate')

    review = get_object_or_404(GameReview, slug=slug)
    if request.POST:
        form = UpdateReviewForm(request.POST or None, instance=review)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.update()
            context['success_message'] = "Updated"
            review = obj
    form = UpdateReviewForm(
            initial = {
                    "title": review.title,
                    "body": review.body,
                    "rating": review.rating,
                }
    )

    context['form'] = form
    return render(request, 'games/edit_review.html', context)
