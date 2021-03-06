from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse

from memopol2 import utils

from mps.models import MP, Group, Department
from votes.models import Proposal, Vote, Recommendation
from mps.views import VoteRecommendation, VoteRecommendationChoice
from reps.models import Opinion


# TODO: refactor this function, should probably be moved to class based generic views if possible
def proposal_rep(request, proposal_id, mp_id):
    representative = get_object_or_404(MP, id=mp_id)
    proposal = get_object_or_404(Proposal, id=proposal_id)
    # dirty query because we don't store absent vote
    votes = [Vote.objects.get(representative=representative, recommendation=r)
             if Vote.objects.filter(representative=representative, recommendation=r)
             else {'choice': 'absent', 'recommendation': r, 'representative': representative}
             for r in proposal.recommendation_set.all()]
    context = {'representative': representative, 'proposal': proposal, 'votes': votes}
    return render(request, 'meps/per_mep.html', context)


urlpatterns = patterns('mps.views',
    # the /names view is *very* expansive. we cache it in RAM for a week
    url(r'^$', utils.cached(3600*24*7)(ListView.as_view(queryset=MP.objects.filter(active=True))), name='index'),

    url(r'^depute/(?P<pk>[a-zA-Z]+)/$', DetailView.as_view(model=MP, context_object_name='mp'), name='mp'),
    url(r'^depute/(?P<pk>[a-zA-Z]+)/contact$', DetailView.as_view(model=MP, context_object_name='mp', template_name='mps/mp_contact.html'), name='mp_contact'),
    url(r'^group/$', ListView.as_view(model=Group), name='index_groups'),
    url(r'^group/(?P<pk>.+)/$', DetailView.as_view(model=Group, template_name='mps/container_detail.html'), name='index_by_group'),
    url(r'^department/$', ListView.as_view(queryset=Department.objects.order_by('number')), name='index_departments'),
    url(r'^department/(?P<pk>.+)/$', DetailView.as_view(model=Department, template_name='mps/container_detail.html'), name='index_by_department'),
    url(r'^opinion/$', ListView.as_view(queryset=Opinion.objects.filter(institution="FR")), name='index_opinions'),
    url(r'^opinion/(?P<pk>[0-9]+)/$', DetailView.as_view(model=Opinion, template_name="mps/opinion_detail.html"), name='index_by_opinions'),

    url(r'^vote/$', ListView.as_view(queryset=Proposal.objects.filter(institution="FR")), name='index_votes'),
    url(r'^vote/(?P<proposal_id>[a-zA-Z/-_]+)/(?P<pk>\d+)/(?P<recommendation>[\w.]+)/$', VoteRecommendationChoice.as_view(model=Recommendation), name='recommendation_choice'),
    url(r'^vote/(?P<proposal_id>[a-zA-Z/-_]+)/(?P<pk>\d+)/$', VoteRecommendation.as_view(model=Recommendation, template_name="mps/recommendation_detail.html"), name='recommendation'),
    url(r'^vote/(?P<pk>[a-zA-Z/-_]+)/dataporn/$', DetailView.as_view(model=Proposal, context_object_name='vote', template_name="mps/proposal_dataporn.html"), name='vote_dataporn'),
    url(r'^vote/(?P<proposal_id>[a-zA-Z/-_]+)/(?P<mep_id>.+)/$', proposal_rep, name='votes_mp'),
    url(r'^vote/(?P<pk>[a-zA-Z/-_]+)/$', DetailView.as_view(model=Proposal, context_object_name='vote', template_name="mps/proposal_detail.html"), name='vote'),

    url(r'^votes/$', lambda request: redirect(reverse("mps:index_votes"))),

    url(r'^nosdeputes/(?P<pk>.+)/$', 'get_nosdeputes_widget')
)
