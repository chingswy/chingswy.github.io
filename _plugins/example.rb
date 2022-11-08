require "jekyll"

module SamplePlugin
    class CategoryPageGenerator < Jekyll::Generator
      safe true

      DEFAULTS = {
        "layout"     => "reading",
        "tags"       => [],
        "permalinks" => "/tag/:tag"
      }.freeze

      def initialize(config = {})
        archives_config = config.fetch("reading", {})
        if archives_config.is_a?(Hash)
          @config = archives_config
        else
          @config = nil
          Jekyll.logger.warn "Archives:", "Expected a hash but got #{archives_config.inspect}"
          Jekyll.logger.warn "", "Archives will not be generated for this site."
        end
      end

      def generate(site)
        return if @config.nil?

        dir = 'tags'
        name = 'my-file.html'
        @config['tags'] = site.data['reading']['tags']
        # site.pages << Jekyll::PageWithoutAFile.new(site, site.source, dir, name).tap do |file|
        #     file.content = '<p>abcdef ghji</p>'
        #     file.data.merge!(
        #     "layout"     => nil,
        #     "sitemap"    => false,
        #     )
        #     file.output
        # end
        @config['tags'].each do |tag|
            site.pages << Jekyll::PageWithoutAFile.new(site, site.source, dir, tag+'.html').tap do |file|
                file.data.merge!(
                    "title"      => tag,
                    "layout"     => "bib-tag",
                    "sitemap"    => false,
                )
                file.output
            end
        end
      end
    end
  
    # Subclass of `Jekyll::Page` with custom method definitions.
    class CategoryPage < Jekyll::PageWithoutAFile
      def initialize(site, tag)
        @site = site             # the current site instance.
        @base = site.source      # path to the source directory.
        @dir  = tag         # the directory the page will reside in.
  
        # All pages have the same filename, so define attributes straight away.
        @basename = 'index'      # filename without the extension.
        @ext      = '.html'      # the extension.
        @name     = 'index.html' # basically @basename + @ext.
  
        # Initialize data hash with a key pointing to all posts under current category.
        # This allows accessing the list in a template via `page.linked_docs`.
        @data = {
          'linked_docs' => tag
        }
  
        # Look up front matter defaults scoped to type `categories`, if given key
        # doesn't exist in the `data` hash.
        # data.default_proc = proc do |_, key|
        #   site.frontmatter_defaults.find(relative_path, :tag, key)
        # end
      end
  
    #   # Placeholders that are used in constructing page URL.
    #   def url_placeholders
    #     {
    #       :path       => @dir,
    #       :tag        => @dir,
    #       :basename   => @name,
    #       :output_ext => output_ext,
    #     }
    #   end
    end
  end