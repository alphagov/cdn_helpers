require 'spec_helper'
require 'stringio'

describe CdnHelpers::CssRewriter do
  def css_path
    File.expand_path('fixtures/dir/spec.css', File.dirname(__FILE__))
  end

  def public_root_path
    Pathname.new(File.expand_path('fixtures', File.dirname(__FILE__)))
  end

  it "correctly rewrites a relative URL (no ../)" do
    CdnHelpers::CssRewriter.process_css_file(StringIO.new('background-image: url("eg.txt")'), css_path, public_root_path).
      should == 'background-image: url(/dir/eg.txt/1ba05a2d.txt)'
  end

  it "correctly rewrites a relative URL (with ../)" do
    CdnHelpers::CssRewriter.process_css_file(StringIO.new("background-image: url('../eg.txt')"), css_path, public_root_path).
      should == 'background-image: url(/eg.txt/13c1f102.txt)'
  end

  it "correctly rewrites an absolute local URL (starts with /)" do
    CdnHelpers::CssRewriter.process_css_file(StringIO.new('background-image: url("/eg.txt")'), css_path, public_root_path).
      should == 'background-image: url(/eg.txt/13c1f102.txt)'
  end

  it "correctly ignores an http:// url" do
    CdnHelpers::CssRewriter.process_css_file(StringIO.new('background-image: url("http://things.com/nice.png")'), css_path, public_root_path).
      should == 'background-image: url(http://things.com/nice.png)'
  end
end