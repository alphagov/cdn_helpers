namespace :cdn do
  task :css_urls => :environment do
    require 'cdn_helpers'
    require 'pathname'

    public_root_path = Pathname.new('public').realpath
    FileList['public/**/*.css'].each do |css_file_path|
      css_file_path = Pathname.new(css_file_path).realpath
      public_path = Rails.root.join('public')
      CdnHelpers.CssRewriter.rewrite_css_file(css_file_path, public_path)
    end
  end
end
