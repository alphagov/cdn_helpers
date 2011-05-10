require 'spec_helper'
require 'stringio'

describe CdnHelpers::CssRewriter do
  def css_path
    File.expand_path('fixtures/dir/spec.css', File.dirname(__FILE__))
  end

  def public_root_path
    Pathname.new(File.expand_path('fixtures', File.dirname(__FILE__)))
  end

  class MockLogger
    attr_reader :logged

    def initialize
      @logged = []
    end

    def warn(msg)
      @logged << msg
    end
  end

  it "correctly rewrites a relative URL (no ../)" do
    CdnHelpers::CssRewriter.process_css_file(MockLogger.new, StringIO.new('background-image: url("eg.txt")'), css_path, public_root_path).
      should == 'background-image: url(/dir/eg.txt/1ba05a2dX.txt)'
  end

  it "correctly rewrites a relative URL (with ../)" do
    CdnHelpers::CssRewriter.process_css_file(MockLogger.new, StringIO.new("background-image: url('../eg.txt')"), css_path, public_root_path).
      should == 'background-image: url(/eg.txt/13c1f102X.txt)'
  end

  it "correctly rewrites an absolute local URL (starts with /)" do
    CdnHelpers::CssRewriter.process_css_file(MockLogger.new, StringIO.new('background-image: url("/eg.txt")'), css_path, public_root_path).
      should == 'background-image: url(/eg.txt/13c1f102X.txt)'
  end

  it "correctly rewrites an absolute local URL given a non-/ URL prefix" do
    CdnHelpers::CssRewriter.process_css_file(MockLogger.new, StringIO.new('background-image: url("/prefix/eg.txt")'), css_path, public_root_path, '/prefix/').
      should == 'background-image: url(/prefix/eg.txt/13c1f102X.txt)'
  end

  it "correctly ignores an http:// url" do
    CdnHelpers::CssRewriter.process_css_file(MockLogger.new, StringIO.new('background-image: url("http://things.com/nice.png")'), css_path, public_root_path).
      should == 'background-image: url(http://things.com/nice.png)'
  end

  it "logs and passes-through an unfound file" do
    logger = MockLogger.new
    CdnHelpers::CssRewriter.process_css_file(logger, StringIO.new('background-image: url("/nice.png")'), css_path, public_root_path).
      should == 'background-image: url(/nice.png)'
    logger.logged.should include("Cannot rewrite URL for /nice.png: File not found")
  end

  context "Salting the hash" do
    it "correctly rewrites an absolute local URL (starts with /)" do
      CdnHelpers::AssetPath.set_hash_salt('Y')
      CdnHelpers::CssRewriter.process_css_file(MockLogger.new, StringIO.new('background-image: url("/other_asset.txt")'), css_path, public_root_path).
        should == 'background-image: url(/other_asset.txt/56f0cb6dY.txt)'
    end
  end
end