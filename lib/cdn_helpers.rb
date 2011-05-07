require 'digest/sha1'
require 'pathname'
require 'uri'
require 'nokogiri'

module CdnHelpers
  require 'cdn_helpers/railtie' if defined?(Rails)

  module AssetPath
    def self.asset_cache
      @@asset_cache ||= {}
    end

    def self.call(path)
      hash_file(path, Rails.root.join('public'), Rails.logger)
    end

    def self.hash_file(path, public_root_path, logger)
      unless asset_cache.has_key?(path)
        file_path = public_root_path.join(path.sub(/^\//, '')).to_s
        unless File.file?(file_path)
          logger.warn("Cannot rewrite URL for #{path}: File not found")
          return path
        end
        sha1 = Digest::SHA1.file(file_path).hexdigest
        extension = File.extname(path)
        return asset_cache[path] = path + "/#{sha1[0..7]}#{extension}"
      end
      asset_cache[path]
    end
  end
  
  module HtmlRewriter
    def self.rewrite_file(logger, file_path, public_root_path, asset_hosts)
      html_content = open(file_path).read
      html = Nokogiri::HTML.parse(html_content)
      process_document(html, file_path, public_root_path, asset_hosts, logger)  
      File.open(file_path, 'w') { |f| f << html.to_s }
    end
    
    def self.process_asset_url(href, file_path, public_root_path, logger)
      local_url = Pathname.new(href)
      url_prefix = "/"
      if local_url.relative?
        logger.warn "We don't yet support relative paths to assets: #{local_url}"
        return href
      else
        local_url = local_url.to_s[(url_prefix.length - 1)..-1] if local_url.to_s.index(url_prefix) == 0
        file_path = public_root_path.join(local_url[1..-1]).cleanpath.relative_path_from(public_root_path).to_s
      end
      return "#{url_prefix[0..-2]}#{CdnHelpers::AssetPath.hash_file("/" + file_path, public_root_path, logger)}"
    end
    
    def self.process_document(html, file_path, public_root_path, asset_hosts, logger)
      to_handle = {
        "link[rel=stylesheet]" => "href",
        "script[src]" => "src",
        "img" => "src",
        'link[rel="shortcut icon"]' => "href"
      }
      
      to_handle.each do |selector, attribute|        
        html.search(selector).each do |elem|
          if URI.parse(elem[attribute]).scheme.nil?
            elem[attribute] = asset_hosts.sample + process_asset_url(elem[attribute], file_path, public_root_path, logger)
          end
        end
      end
      
      # The contents of any style elements should be processed as CSS files
      require 'stringio'
      html.search('style').each do |elem|
        pseudo_css_file = StringIO.new(elem.content)
        processed_css = CssRewriter.process_css_file(logger, pseudo_css_file, file_path, public_root_path, asset_hosts.sample + "/")
        elem.content = processed_css
      end

      html
    end
    
  end
  
  module CssRewriter
    def self.rewrite_css_file(logger, css_file_path, public_root_path, url_prefix = '/')
      logger.info("Rewriting CSS file URLs in #{css_file_path}")
      css_file = File.open(css_file_path)
      output = process_css_file(logger, css_file, css_file_path, public_root_path, url_prefix)
      File.open(css_file_path, 'w') { |f| f.write(output) }
    end

    def self.process_css_file(logger, css_file, css_file_path, public_root_path, url_prefix = '/')
      out_lines = []
      css_file_path = Pathname.new(css_file_path).realpath
      public_root_path = Pathname.new(public_root_path)
      context_path = css_file_path.parent
      while line = css_file.gets
        out_lines << line.gsub(/url\(["']?([^"'\)]+)["']?\)/) do |url_match|
          if URI.parse($1).scheme.nil?
            local_url = Pathname.new($1)
            if local_url.relative?
              file_path = context_path.join(local_url).cleanpath.relative_path_from(public_root_path).to_s
            else
              url_prefix = url_prefix + '/' unless url_prefix.rindex('/') == (url_prefix.length - 1)

              if local_url.to_s.index(url_prefix) == 0
                local_url = local_url.to_s[(url_prefix.length - 1)..-1] 
              else
                local_url = local_url.to_s
              end
              
              file_path = public_root_path.join(local_url[1..-1]).cleanpath.relative_path_from(public_root_path).to_s
            end
            "url(#{url_prefix[0..-2]}#{CdnHelpers::AssetPath.hash_file("/" + file_path, public_root_path, logger)})"
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
