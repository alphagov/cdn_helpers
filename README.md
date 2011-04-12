CDN asset URL helpers
=====================

This library contains a Rubygem and Django custom templatetag library to do the following:

turn an asset path like

    /images/thing.png

into a CDN-pointed URL like

    http://cdn.name.com/images/thing.png/{sha1}.png

Rails
-----

Add `cdn_helpers` to your `Gemfile`:

    gem 'cdn_helpers', :git => 'git@github.com:alphagov/cdn_helpers.git'

In your `environments/production.rb`:

    require 'cdn_helpers'
    config.action_controller.asset_host = "http://cdn.url.gov.uk"
    config.action_controller.asset_path = CdnHelpers::AssetPath

The gem also make the `rake` task `cdn:css_urls` available to you. This is for post-deployment rewriting of URLs within CSS files. It's destructive - it rewrites the files in place - but it doesn't require that the config vars above are set since it leaves URLs as absolute local URLs.

Django
------

Add `cdn_helpers` to your `requirements.txt`:

    -e git+ssh://git@github.com/alphagov/cdn_helpers.git#egg=cdn_helpers
    
in `settings.py` add cdn_helpers to your list of installed apps:

    INSTALLED_APPS = (
        'django.contrib.auth',
        ...
        'cdn_helpers'
    )

in the appropriate `local_settings.py`:

    APP_DEPLOYMENT_ENV = 'dev'   # (or staging, production)
    CDN_HOSTS = ['cdn1', 'cdn2'] # (as appropriate for the environment)
    
    
in templates use the `asset_url` helper:

    <img src="{% asset_url "/images/thing.png" %}">
    <img src="{% asset_url thing.image.src %}">

The app provides the `cdn_css` command for `manage.py`. This uses the Ruby script process_css to do the heavy lifting, but relies on the `MEDIA_ROOT` and `MEDIA_URL` settings in `settings.py` to tell where to look and how to construct the URLs.