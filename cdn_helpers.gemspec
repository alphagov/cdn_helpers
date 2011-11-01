# -*- encoding: utf-8 -*-
$:.push File.expand_path("../lib", __FILE__)

Gem::Specification.new do |s|
  s.name          = "cdn_helpers"
  s.version       = "0.9"
  s.platform      = Gem::Platform::RUBY
  s.authors       = ["Matt Patterson", "James Stewart"]
  s.email         = ["matt@constituentparts.com", "james.stewart@digital.cabinet-office.gov.uk"]
  s.homepage      = "http://github.com/alphagov/cdn_helpers"
  s.summary       = %q{Provides CDN helper methods for Rails}
  s.description   = %q{Provides CDN helper methods for Rails as used in the Alpha.gov.uk project}

  s.rubyforge_project = "cdn_helpers"

  s.files         = Dir[
    'lib/**/*',
    'README.md',
    'Gemfile',
    'Rakefile'
  ]
  s.test_files    = Dir['spec/**/*']
  s.require_paths = ["lib"]

  s.add_dependency 'actionpack'
  s.add_dependency 'nokogiri'

  s.add_development_dependency 'rake'
  s.add_development_dependency 'rspec', '~> 2.5.0'
end
