require 'cdn_helpers'
require 'rails'

module CdnHelpers
  class Railtie < Rails::Railtie
    railtie_name :cdn_helpers

    rake_tasks do
      load "cdn_helpers.rake"
    end
  end
end
