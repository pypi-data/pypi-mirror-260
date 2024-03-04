from dnsurlsearch import DNSurlSearch

# Read Whitelist if any
whitelist = DNSurlSearch.UrlFilter()
whitelist.read_url('whitelist')

# To get some measurements of urls found in the cache sent by mail
# See https://docs.python.org/2.6/library/logging.html?highlight=logger#smtp-handler for more information on parameters
# Mesure period                          : 2024-02-05 18:51:01.128016 - 2024-02-05 18:51:42.497950
#        Number of new url found on the period  : 4
#        Total number of url found              : 4
stats = DNSurlSearch.CacheDnsStat('rasp', 'nicolas@jeudy.mooo.com', 'nicolas@jeudy.mooo.com', 'Filtered url stats test with tcpdump')

# First create url filter
# '0.0.0.0' parameter is the IP address to add in the file for each url
blacklist = DNSurlSearch.UrlFilter('0.0.0.0', 'black_list')

# treatment  
#  - when reading blacklist file : remove ip_address to get url only
#  - when writting blacklist file : add ip_address 
blacklist.set_treatment(DNSurlSearch.BlackListFilterTreatment())

nb_url_start = blacklist.read_url('blacklist')

# Create the cache
cache = DNSurlSearch.CacheDns()

# Set the SnifferCacheHandler to snif DNS protocol
h = DNSurlSearch.SnifferCacheHandler(DNSurlSearch.AUTOMATIC, 20)
h.set_cache_file_name('/tmp/log')

h.set_start_cmd('sudo /home/nicolas/PycharmProjects/Cache/tcpdump_cache_dns.sh')
h.set_kill_cmd('sudo /home/nicolas/PycharmProjects/Cache/k_tcpdump_cache_dns.sh')
cache.set_handler(h)

# Set patterns to search in the cache
cache.set_filter('.googlevideo.com.')

# Launch the update of cache and search urls
new_cache = cache.get_cache_dns()

# Add urls found in the blacklist
blacklist.add(new_cache)

# Check urls and remove url from blacklist if present in whitelist
blacklist.check(whitelist.get_url())

nb_url_end = blacklist.write_url('blacklist')

stats.save_stats(nb_url_start, nb_url_end, 1)

