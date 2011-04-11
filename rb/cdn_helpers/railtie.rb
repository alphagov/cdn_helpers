require 'cdn_helpers'
require 'rails'

module CdnHelpers
  class Railtie < Rails::Railtie
    rake_tasks do
      load "cdn_helpers/cdn_helpers.rake"
    end
  end
end
