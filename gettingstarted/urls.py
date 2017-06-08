from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^login/$', hello.views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', hello.views.signup, name='signup'),
    url(r'^buy/$', hello.views.buy, name='buy'),
    url(r'^profile/$', hello.views.profile, name='profile'),
    url(r'^creditcardform/$', hello.views.creditcardform, name='creditcardform'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
]
