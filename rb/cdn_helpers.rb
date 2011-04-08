require 'digest/sha1'
module CdnHelpers
  module AssetPath
    def self.asset_cache
      @@asset_cache ||= {}
    end

    def self.call(path)
      unless asset_cache.has_key?(path)
        file_path = Rails.root.join('public', path.sub(/^\//, '')).to_s
        sha1 = Digest::SHA1.file(file_path).hexdigest
        extension = File.extname(path)
        return asset_cache[path] = path + "/#{sha1[0..7]}#{extension}" 
      end
      asset_cache[path]
    end
  end
end
