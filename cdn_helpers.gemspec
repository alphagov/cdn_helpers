# -*- encoding: utf-8 -*-
$:.push File.expand_path("../lib", __FILE__)

Gem::Specification.new do |s|
  s.name          = "cdn_helpers"
  s.version       = "0.8.4"
  s.platform      = Gem::Platform::RUBY
  s.authors       = ["Matt Patterson"]
  s.email         = ["matt@alphagov.co.uk"]
  s.homepage      = "http://github.com/alphagov/cdn_helpers"
  s.summary       = %q{Provides CDN helper methods for Rails}
  s.description   = %q{Provides CDN helper methods for Rails}

  s.rubyforge_project = "cdn_helpers"

  s.files         = Dir[
    'lib/**/*',
    'README.md',
    'Gemfile',
    'Rakefile'
  ]
  s.test_files    = Dir['spec/**/*']
  s.require_paths = ["lib"]

  s.add_dependency 'actionpack', '~> 3.0.0'
  s.add_dependency 'nokogiri'
  
  s.add_development_dependency 'rake', '~> 0.8.0'
  s.add_development_dependency 'rspec', '~> 2.5.0'
end
