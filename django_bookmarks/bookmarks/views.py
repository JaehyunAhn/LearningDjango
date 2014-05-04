# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.template import Context
from django.template.loader import get_template
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django_bookmarks.bookmarks.forms import *
from django_bookmarks.bookmarks.models import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.core.paginator import Paginator
# Caching
from django.views.decorators.cache import cache_page

# 번역을 위한 as 는 ~ 로 만드는 것을 의미: 단축키와 비슷
from django.utils.translation import gettext as _

# 임시방편: line 90 @csrf_exempt
from django.views.decorators.csrf import csrf_exempt

# 인기 순서대로 정렬
from datetime import datetime, timedelta

ITEMS_PER_PAGE = 10

def friends_page(request, username):
	user = get_object_or_404(User, username=username)
	friends = [friendship.to_friend for friendship in user.friend_set.all()]
	friend_bookmarks = Bookmark.objects.filter(user__in=friends).order_by('-id')
	variables = RequestContext(request, {
		'username': username,
		'friends': friends,
		'bookmarks': friend_bookmarks[:10],
		'show_tags': True,
		'show_user': True
	})
	return render_to_response('friends_page.html',variables)


@login_required
def friend_add(request):
	# no query field
	if request.GET.has_key('username'):
		friend = get_object_or_404(User, username=request.GET['username'])
		friendship = Friendship (
				from_friend = request.user,
				to_friend = friend,
		)
		friendship.save()
		return HttpResponseRedirect(
				'/friends/%s/' % request.user.username
		)
	else:
		raise Http404

def bookmark_page(request, bookmark_id):
	shared_bookmark = get_object_or_404(
			SharedBookmark,
			id = bookmark_id
			)
	variables = RequestContext(request, {
		'shared_bookmark': shared_bookmark
		})
	return render_to_response('bookmark_page.html', variables)

def popular_page(request):
	today = datetime.today()
	yesterday = today - timedelta(1)
	shared_bookmarks = SharedBookmark.objects.filter(
			date__gt=yesterday
			)
	shared_bookmarks = shared_bookmarks.order_by(
			'-votes'
			)[:10]
	variables = RequestContext(request, {
		'shared_bookmarks': shared_bookmarks
		})
	return render_to_response('popular_page.html', variables)

def ajax_tag_autocomplete(request):
	if request.GET.has_key('q'):
		tags = Tag.objects.filter(name__istartswith=request.GET['q'])[:10]
		return HttpResponse('\n'.join(tag.name for tag in tags))
	return HttpResponse()

def search_page(request):
	form = SearchForm()
	bookmarks = []
	show_results = False
	if request.GET.has_key('query'):
		show_results = True
		query = request.GET['query'].strip()
		# 쿼리를 이용하여 search 기능 향상
		if query:
			keywords = query.split()
			q = Q() # Empty query object
			for keyword in keywords:
				q = q & Q(title__icontains=keyword)
			form = SearchForm({'query':query})
			bookmarks = Bookmark.objects.filter (q)[:10]

	variables = RequestContext(request, { 'form':form,
		'bookmarks':bookmarks,
		'show_results': show_results,
		'show_tags': True,
		'show_user': True
		})

	# if request is ajax
	if request.is_ajax():
		return render_to_response('bookmark_list.html', variables)
	else:
		return render_to_response('search.html', variables)

#@cache_page # Server error occurred
def tag_cloud_page(request):
	MAX_WEIGHT = 5
	tags = Tag.objects.order_by('name')

	# Calculate tag, min and max counts
	min_count = max_count = tags[0].bookmarks.count()
	for tag in tags:
		tag.count = tag.bookmarks.count()
		if tag.count < min_count:
			min_count = tag.count
		if max_count < tag.count:
			max_count = tag.count

	# Calculate count range. Avoid dividing by zero.
	range = float(max_count - min_count)
	if range == 0.0:
		range = 1.0

	# Calculate tag weights.
	for tag in tags:
		tag.weight = int(
				MAX_WEIGHT * (tag.count - min_count) / range
				)
		variables = RequestContext(request, {
			'tags':tags
			})
	return render_to_response('tag_cloud_page.html', variables)

def tag_page(request, tag_name):
	tag = get_object_or_404(Tag, name=tag_name)
	bookmarks = tag.bookmarks.order_by('-id')
	variables = RequestContext(request, {
		'bookmarks': bookmarks,
		'tag_name': tag_name,
		'show_tags': True,
		'show_user': True
		})
	return render_to_response('tag_page.html', variables)

@csrf_exempt # 임시방편 : import
@login_required
def bookmark_save_page(request):
	# POST 요청일 경우 : 갱신
	ajax = request.GET.has_key('ajax')
	if request.method == 'POST':
		form = BookmarkSaveForm(request.POST)
		if form.is_valid():
			bookmark = _bookmark_save(request, form)
			if ajax:
				variables = RequestContext(request, {
					'bookmarks': [bookmark],
					'show_edit': True,
					'show_tags': True
					})
				return render_to_response('bookmark_list.html',variables)
			else:
				return HttpResponseRedirect(
						'/user/%s/' % request.user.username
						)
		else:
			if ajax:
				return HttpResponse('failure')
	elif request.GET.has_key('url'):
		url = request.GET['url']
		title = ''
		tags = ''
		try:
			link = Link.objects.get(url=url)
			bookmark = Bookmark.objects.get(
					link=link,
					user=request.user
					)
			title = bookmark.title
			tags = ' '.join(
					tag.name for tag in bookmark.tag_set.all()
					)
		except ObjectDoesNotExist:
			pass
		form = BookmarkSaveForm({
			'url':url,
			'title':title,
			'tags':tags
			})
	# GET 요청일경우
	else:
		form = BookmarkSaveForm()
	variables = RequestContext(request, {
		'form': form
	})
	if ajax:
		return render_to_response(
				'bookmark_save_form.html',
				variables
				)
	else:
		return render_to_response(
				'bookmark_save.html',
				variables
				)

def _bookmark_save(request, form):
	# 링크 가져오기
	link, dummy = Link.objects.get_or_create(url=form.cleaned_data['url'])
	# 북마크 가져오기
	bookmark, created = Bookmark.objects.get_or_create(
			user=request.user,
			link=link
			)
	# 북마크 제목 수정
	bookmark.title = form.cleaned_data['title']
	# 예전 태그 제거
	if not created:
		bookmark.tag_set.clear()
	# 새로운 태그 입력
	tag_names = form.cleaned_data['tags'].split()
	for tag_name in tag_names:
		tag, dummy = Tag.objects.get_or_create(name=tag_name)
		bookmark.tag_set.add(tag)
	# 첫 페이제어 공유하도록 설정
	if form.cleaned_data['share']:
		shared_bookmark, created = SharedBookmark.objects.get_or_create(
				bookmark=bookmark
		)
		if created:
			shared_bookmark.users_voted.add(request.user)
			shared_bookmark.save()

	# 저장 및 공유
	bookmark.save()
	return bookmark

@login_required
def bookmark_vote_page(request):
	if request.GET.has_key('id'):
		try:
			id = request.GET['id']
			shared_bookmark = SharedBookmark.objects.get(id=id)
			user_voted = shared_bookmark.users_voted.filter(
					username=request.user.username
			)
			if not user_voted:
				shared_bookmark.votes += 1
				shared_bookmark.users_voted.add(request.user)
				shared_bookmark.save()
		except ObjectDoesNotExist:
			raise Http404(_('북마크를 찾을 수 없습니다.'))

# Syntax Error: page 153
	if request.META.has_key('HTTP_REFERER'):
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	
	return HttpResponseRedirect('/')

def register_page(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
					username=form.cleaned_data['username'],
					password=form.cleaned_data['password1'],
					email=form.cleaned_data['email']
			)
			return HttpResponseRedirect ('/register/success')
	else:
		form = RegistrationForm()

	variables = RequestContext(request, {
		'form':form
	})
	return render_to_response(
			'registration/register.html', variables
	)


def logout_page(request):
	logout(request)
	# '/' main page를 의미함
	return HttpResponseRedirect('/')

def user_page(request, username):
	user = get_object_or_404(User, username=username)
	query_set = user.bookmark_set.order_by('-id')
	paginator = Paginator(query_set, ITEMS_PER_PAGE)
	# Friend Part
	is_friend = Friendship.objects.filter(
			from_friend = request.user,
			to_friend = user
	)

	try:
		page = int(request.GET['page'])
	except:
		page = 1
	try:
		bookmarks = paginator.page(page)
	except:
		raise Http404

	variables = RequestContext(request, {
		'bookmarks':bookmarks.object_list,
		'username':username,
		'show_tags':True,
		'show_edit': username == request.user.username,
		'show_paginator': paginator.num_pages > 1,
		'has_prev' : bookmarks.has_previous(),
		'has_next' : bookmarks.has_next(),
		'page'	   : page,
		'pages'    : paginator.num_pages,
		# if ~ else None version changed!! 
		'next_page': bookmarks.next_page_number() if bookmarks.has_next() else None,
		'prev_page': bookmarks.previous_page_number() if bookmarks.has_previous() else None,
		# Friendship
		'is_friend': is_friend,
	})
	return render_to_response('user_page.html', variables)

def main_page (request):
	shared_bookmarks = SharedBookmark.objects.order_by(
			'-date'
	)[:10]
	variables = RequestContext(request, {
		'shared_bookmarks': shared_bookmarks
	})
	return render_to_response('main_page.html', variables)
