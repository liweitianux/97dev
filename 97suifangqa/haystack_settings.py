# -*- coding: utf-8 -*-

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

HAYSTACK_CONNECTIONS = {
    'default': {
        #'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        #'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr',
        'TIMEOUT': 60*5,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
    },
}

