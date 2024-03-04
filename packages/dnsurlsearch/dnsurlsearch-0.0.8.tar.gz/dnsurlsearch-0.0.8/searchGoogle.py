from dnsurlsearch import DNSurlSearch

# First create url filter
whitelist = DNSurlSearch.UrlFilter()

# Create the cache
cache = DNSurlSearch.CacheDns()

# Set the SnifferCacheHandler to snif DNS protocol
h = DNSurlSearch.SnifferCacheHandler(DNSurlSearch.MANUAL)
h.set_cache_file_name('/tmp/log')

# The sniffer used is tcpdump
h.set_start_cmd('sudo /home/nicolas/PycharmProjects/Cache/tcpdump_cache_dns.sh')
h.set_kill_cmd('sudo /home/nicolas/PycharmProjects/Cache/k_tcpdump_cache_dns.sh')
cache.set_handler(h)
    
# Set patterns to search in the cache
cache.set_filter('.googlevideo.com.')
    
# Launch the sniffer to get url and search urls
new_cache = cache.get_cache_dns()
        
# Add urls found in the whitelist
whitelist.add(new_cache)
# Save the whitelist in a file
whitelist.write_url('whitelist')
