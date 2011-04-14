$:.unshift(File.expand_path(".")) unless $:.include?(File.expand_path("."))
$:.unshift(File.expand_path("../lib")) unless $:.include?(File.expand_path("../lib"))

require 'bundler'
Bundler.require :default, :test

require 'rspec/core'
require 'rspec/expectations'
require 'rspec/matchers'
