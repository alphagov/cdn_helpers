# -*- encoding: utf-8 -*-
$:.push File.expand_path("../lib", __FILE__)

Gem::Specification.new do |s|
  s.name          = "cdn_helpers"
  s.version       = "0.1.1"
  s.platform      = Gem::Platform::RUBY
  s.authors       = ["Matt Patterson"]
  s.email         = ["matt@alphagov.co.uk"]
  s.homepage      = "http://github.com/alphagov/cdn_helpers"
  s.summary       = %q{TODO: Write a gem summary}
  s.description   = %q{TODO: Write a gem description}

  s.rubyforge_project = "cdn_helpers"

  s.files         = Dir[
    'rb/**/*',
    'README.md',
    'Gemfile',
    'Rakefile'
  ]
  s.test_files    = Dir['spec/**/*']
  s.require_paths = ["rb"]

  s.add_dependency 'actionpack', '~> 3.0.0'
end
