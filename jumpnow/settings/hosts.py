from django_hosts import patterns, host

host_patterns = patterns(
  '',
    host(r'', 'dashboard.urls', name=' '),

    # host(r'app', 'accounts.urls', name='app'),
    # host(r'account', 'dashboard.urls', name='account'),

)