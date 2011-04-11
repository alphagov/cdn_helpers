require 'digest/sha1'
require 'pathname'

module CdnHelpers
  module AssetPath
    def self.asset_cache
      @@asset_cache ||= {}
    end

    def self.call(path)
      hash_file(path, Rails.root.join('public'))
    end

    def self.hash_file(path, public_root_path)
      unless asset_cache.has_key?(path)
        file_path = public_root_path.join(path.sub(/^\//, '')).to_s
        sha1 = Digest::SHA1.file(file_path).hexdigest
        extension = File.extname(path)
        return asset_cache[path] = path + "/#{sha1[0..7]}#{extension}"
      end
      asset_cache[path]
    end
  end
  
  module CssRewriter
    def self.rewrite_css_file(css_file_path, public_root_path, url_prefix = '/')
      css_file = File.open(css_file_path)
      output = process_css_file(css_file, css_file_path, public_root_path, url_prefix)
      File.open(css_file_path, 'w') { |f| f.write(output) }
    end

    def self.process_css_file(css_file, css_file_path, public_root_path, url_prefix = '/')
      out_lines = []
      css_file_path = Pathname.new(css_file_path).realpath
      context_path = css_file_path.parent
      while line = css_file.gets
        out_lines << line.gsub(/url\(["']?([^"'\)]+)["']?\)/) do |url_match|
          if URI.parse($1).scheme.nil?
            local_url = Pathname.new($1)
            if local_url.relative?
              url = context_path.join(local_url).cleanpath.relative_path_from(public_root_path).to_s
            else
              url_prefix = url_prefix + '/' unless url_prefix.rindex('/') == (url_prefix.length - 1)
              local_url = local_url.to_s[(url_prefix.length - 1)..-1] if local_url.to_s.index(url_prefix) == 0
              url = public_root_path.join(local_url[1..-1]).cleanpath.relative_path_from(public_root_path).to_s
            end
            "url(#{CdnHelpers::AssetPath.hash_file("/" + url, public_root_path)})"
          else
            "url(#{$1})"
          end
        end
      end
      css_file.close
      out_lines.join("")
    end
  end
end
