$:.unshift(File.expand_path(".")) unless $:.include?(File.expand_path("."))
$:.unshift(File.expand_path("../rb")) unless $:.include?(File.expand_path("../rb"))

require 'bundler'
Bundler.require :default, :test

require 'rspec/core'
require 'rspec/expectations'
require 'rspec/matchers'
