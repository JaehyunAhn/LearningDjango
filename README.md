## DJANGO & PYTHON
Jaehyun Ahn (jaehyunahn@sogang.ac.kr)

: 장고와 파이썬을 모두 최신 버전을 사용해서 완성한 북마크 튜토리얼 앱입니다. 버전 충돌과 사라진 정보가 너무나도 많아 즐거운 시간을 보냈습니다.

> 현재 사용된 

> python 버전: 2.7

> 장고 1.6

> GNU gettext [0.18.3.1](https://gist.github.com/mbillard/1647940)

> [compile-messages.py](https://github.com/pelle/talk.org/blob/master/django/bin/compile-messages.py)


<hr>
### 구현 못한 기능
- 이메일 기능(p.199) : localhost에 ISP가 뭐지?
- 국제화 기능(p.216) : complie-messages.py 를 제대로 구하지 못함

### 치명적 문제점
> 본 서비스는 '삭제' 기능을 제공하지 않고 있다. 이건 스스로 공부해야 하는건가!! (미결)
> 그렇다! DELETE는 스스로 공부해야 하는 것이었다! (이것은 어쩌면 작가의 들깨 속 잣 같은(발음 주의) 숙제일 수도 있겠다!
> [여기](http://stackoverflow.com/questions/311188/how-do-i-edit-and-delete-data-in-django)를 참고하여 문제를 해결하여 작가의 숨은 의도를 충족시켜보자!

### 문제해결 과정 및 정보

#### 오탈자
- [인사이트](http://www.insightbook.co.kr/books/programming-insight/쉽고-빠른-웹-개발-django/정오표-8)

#### RSS Feed 문제 (해결)
> 신생 언어의 패러다임은 빠르게 바뀌며, 대부분 객체화를 바탕으로 변화한다

- [표준문서](https://docs.djangoproject.com/en/1.2/ref/contrib/syndication/)
- RSS Feed URL 분배가 버전이 달라 제대로 구현이 어려웠다.
- 너무 답답해서 올린 질문에 현답이 달렸다! 참고:[스택오버플로우](http://stackoverflow.com/questions/23424650/url-hashing-in-django-web-application/23425103?noredirect=1#23425103)
- URL Hashing Error : 패러다임 문제로 판결 및 해결!

#### Custom Feed 제작 (미궁)
- Page not found 404 Error occurred

#### Pagination 문제와 해결
- github [참조](https://github.com/dcramer/django-paging/commit/d6e67d60a9aa7ff26c3821537a5ab946505fe9af)로 해결!
