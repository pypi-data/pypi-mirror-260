# -*- coding: utf-8 -*-
import datetime
import logging
import logging.handlers
import os
import re
import sys
import time
from abc import ABC, abstractmethod

# Mode
AUTOMATIC =  1
MANUAL = 0

# Temporary file to store search result with grep
search_file_name = 'Found_url.txt'

# Log debug --------------------------------------
LOG_FILENAME = '/tmp/CacheDns.out'

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

def get_params(param_name):
    """
    Detection of an argument on the command line like <param_name>=<value>
    Return <value> if any or ''
    Example :
      level=debug
      01234567890
           ^
      p_name=5
    """
    p_name = len(param_name)
    ret=''
    if len(sys.argv)>1:
        for ar in range(len(sys.argv)):
            arg = sys.argv[ar]
            # print("arg : %s" % arg)
            a = len(arg)
            if a > p_name:
                # print("arg[p_name] : %s" %arg[p_name])
                # print("arg[0:p_name-1] : %s" %arg[0:p_name])
                if arg[p_name] == '=' and arg[0:p_name] == param_name:
                    ret = arg[p_name+1:]
    # print("Return value : %s" %ret)
    return ret

level = logging.NOTSET  # Par défaut, pas de log

level_name = get_params('level')
if level_name:
    level = LEVELS.get(level_name, logging.NOTSET)

my_logger = logging.getLogger(__name__)
my_logger.setLevel(level)

# Add the handler
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1048576, backupCount=5)
# Formatter creation
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
# Add formatter to handler
handler.setFormatter(formatter)
my_logger.addHandler(handler)

handler = logging.StreamHandler()
# Formatter creation
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(filename)s %(lineno)d %(message)s")
# Add formatter to handler
handler.setFormatter(formatter)
my_logger.addHandler(handler)
# End log configuration --------------------------------------


class FilterTreatment(ABC):
    """Abstract interface to gather specific treatment on URL file"""

    @abstractmethod
    def urlfile_read_treatment(self, my_line, ip_addr):
        pass

    @abstractmethod
    def urlfile_write_treatment(self, url, ip_addr):
        pass


class BlackListFilterTreatment(FilterTreatment):
    """BlackList file treatment"""

    def urlfile_read_treatment(self, my_line, ip_addr):
        """
        :param my_line: line to read in the file
        :param ip_addr: pattern of ip adress at the begining of the line to add or remove
        :return:
        On reading file, ip_addr (0.0.0.0, for example)  at the beginning of each line must be removed """

        my_str = ip_addr + ' '
        return my_line.replace(my_str, '', 1)

    def urlfile_write_treatment(self, url, ip_addr):
        """
        :param url: url to read in the file
        :param ip_addr: pattern of ip adress at the begining of the line to add or remove
        :return:
        On writting file, ip_addr (0.0.0.0, for example)  at the beginning of each line must be added """

        my_line = "%s %s" % (ip_addr, url)
        return my_line


class UrlFilter(object):
    """URL filter list"""

    def __init__(self, ip_addr='', name=''):
        """
        :param ip_addr: ip address to link with url to build a blacklist
        :param name: Name of the filter
        """
        self.url_filter = []
        self.url_filter_name = name
        self.ip_addr = ip_addr
        self.treatment = None

    def set_treatment(self, treatment):
        """
        :param treatment: specific function treatment to apply when reading or writting url filter file
        :return: Line treated
        """
        self.treatment = treatment

    def read_url(self, filename):
        """
        Read url filter file
        :param filename: name of the file to read
        :return: number of url read in the file
        """
        my_logger.debug(" UrlFilter.read_url() ".center(60, '-'))
        self.url_filter = []
        try:
            f = open(filename, "r")
            for my_line in f:
                my_line = my_line.strip('\f\n')
                if self.treatment:
                    my_line = self.treatment.urlfile_read_treatment(my_line, self.ip_addr)
                my_logger.debug('%s %s', filename, my_line)
                self.url_filter.append(my_line)
            f.close()
        except IOError:
            my_logger.info('File "%s" not found. File shall be created.', filename)
            return 0

        return len(self.url_filter)

    def get_url(self):
        my_logger.debug(" UrlFilter.get_url() ".center(60, '-'))
        return self.url_filter

    def write_url(self, file_name):
        """
        Write url filter file
        :param file_name:
        :return: url list
        """
        my_logger.debug(" UrlFilter.write_url() ".center(60, '-'))
        my_logger.debug(" Number of urls to write : %d - file name : %s " %(len(self.url_filter), file_name))
        f = open(file_name, "w")
        for u in range(len(self.url_filter)):
            if self.treatment:
                my_line = self.treatment.urlfile_write_treatment(self.url_filter[u], self.ip_addr)
            else:
                my_line = self.url_filter[u]
            my_logger.debug(my_line)
            my_line += '\n'
            f.write(my_line)
        f.flush()
        f.close()
        return len(self.url_filter)

    def add(self, n_cache):
        """Add urls in list new_cache that don't exist in self.url_filter"""
        my_logger.debug(" UrlFilter.add() ".center(60, '-'))
        my_logger.debug(" Number of url to add : %d" % len(n_cache))
        new_url_found = 0
        for x in range(len(n_cache)):
            if n_cache[x] not in self.url_filter:
                self.url_filter.append(n_cache[x])
                my_logger.info("New url inserted : %s" % (n_cache[x]))
                new_url_found += 1
        my_logger.info("%d New urls inserted" % new_url_found)

    def check(self, white):
        """Delete urls in list 'white' that exist in self.url_filter"""
        my_logger.debug(" UrlFilter.check() ".center(60, '-'))
        new_url_found = 0
        for x in range(len(white)):
            if white[x] in self.url_filter:
                u = self.url_filter.index(white[x])
                del self.url_filter[u]
                my_logger.info("Url deleted (whitelist) : %s" % (white[x]))
                new_url_found += 1
        my_logger.info("%d Urls deleted (whitelist)" % new_url_found)


class CacheDnsStat(object):
    """Simple statistic on url found
        After a number of measure, a mail is sent containing these data  :
        Mesure period                          : 2024-02-05 18:51:01.128016 - 2024-02-05 18:51:42.497950
        Number of new url found on the period  : 4
        Total number of url found              : 4
    """

    def __init__(self, mailhost, fromaddr, toaddrs, subject):
        self.file_name = 'StatsDomain'
        self.Cache_SMTP_logger = logging.getLogger('smtp')
        self.Cache_SMTP_logger.setLevel(logging.INFO)
        # Add the log message handler to the logger
        hand = logging.handlers.SMTPHandler(mailhost, fromaddr, toaddrs, subject)
        self.Cache_SMTP_logger.addHandler(hand)

    def send_message(self, ma_date_deb, nb_new_url, n_url):
        """
        Send a mail with simple stats
        Mesure period                          : 2024-02-05 18:51:01.128016 - 2024-02-05 18:51:42.497950
        Number of new url found on the period  : 4
        Total number of url found              : 4
        See https://docs.python.org/2.6/library/logging.html?highlight=logger#smtp-handler for more information on parameters

        :param ma_date_deb: Start date of the period
        :param nb_new_url: Number of new url found
        :param n_url: Total number of url found
        :return: None
        """
        my_logger.debug(" CacheDnsStat.send_message() ".center(60, '-'))
        my_logger.debug("Start date : %s nb new url : %d total nb url : %d" % (ma_date_deb, nb_new_url, n_url))
        ma_date_fin = datetime.datetime.today()
        ma_date_fin = str(ma_date_fin).strip('\f\n')
        ma_date_deb = str(ma_date_deb).strip('\f\n')

        text_message =  "Mesure period                          : %s - %s\n" % (ma_date_deb, ma_date_fin)
        text_message += "Number of new url found on the period  : %d\n" % nb_new_url
        text_message += "Total number of url found              : %d" % n_url
        self.Cache_SMTP_logger.info(text_message)
        my_logger.debug("Message : \n%s" % text_message)

    def save_stats(self, pnb_start_url, pnb_end_url, pnb_measure):
        """
        Simple stats are saved in a file
        :param pnb_start_url: number of url found in the DNS cache file
        :param pnb_end_url: number of url found at the end of the script
        :param pnb_measure: number of measurements to take before sending a message to give stats

        For example, if the script to get new url from the cache is sent every 10 minutes
        To get simple stats every day, pnb_measure must be set to 144
        => 6 mesures for one hour
        => 24 x 6 = 144 mesures for a day
        """

        # File contents
        #  - start date of the period
        #  - number of measurements
        #  - nb_new_url: number of new url found in the DNS cache
        #  - nb_url: total number of url found

        my_logger.debug(" CacheDnsStat.save_stats() ".center(60, '-'))
        try:
            f = open(self.file_name, "r")
            ma_date_deb = f.readline()
            n_measure, n_new_url, n_url = f.readline(), f.readline(), f.readline()
            f.close()
            n_measure, n_new_url, n_url = int(n_measure), int(n_new_url), int(n_url)
        except:
            my_logger.info('File "%s" not found. File shall be created.', self.file_name)
            n_measure, n_new_url, n_url = 0, 0, 0
            ma_date_deb = '-'

        n_measure += 1
        n_new_url += (pnb_end_url - pnb_start_url)

        my_logger.debug("Start date: %s nb url orig: %d total nb url: %d" % (ma_date_deb, pnb_start_url, pnb_end_url))

        if n_measure == pnb_measure:
            self.send_message(ma_date_deb, n_new_url, pnb_end_url)
            n_measure = 0
            n_new_url = 0

        ma_date_deb = datetime.datetime.today()
        ma_date_deb = str(ma_date_deb).strip('\f\n')

        f = open(self.file_name, "w")
        f.write("%s\n" % ma_date_deb)
        f.write("%d\n" % n_measure)
        f.write("%d\n" % n_new_url)
        f.write("%d\n" % pnb_end_url)
        f.flush()
        f.close()


class CacheDns(object):
    """Class that manages cache DNS """

    handler = None

    def __init__(self):
        self.handler = None
        self.cache_dns = None
        self.patterns = []

    @staticmethod
    def set_handler(ha):
        my_logger.debug(" CacheDns.set_handler()() ".center(60, '-'))
        CacheDns.handler = ha

    def set_filter(self, pattern):
        my_logger.debug(" CacheDns.set_filter()() ".center(60, '-'))
        self.patterns.append(pattern)
        my_logger.debug("filters : %s" % self.patterns)

    def get_cache_dns(self):
        if CacheDns.handler:
            CacheDns.handler.init_dns_cache()
            self.cache_dns = CacheDns.handler.dns_cache_selection(self.patterns)
        else:
            my_logger.warning('Hanler not defined on CacheDns object')
        return self.cache_dns


class CacheHandler(object):
    """Class that manage DNS cache"""

    @staticmethod
    def _date_size_cache_dns(fich):
        """
        Log the date and size of the cache file for bind software to check the update
        :param fich: File name
        :return: None
        """
        stat_r = os.stat(fich)
        my_time_str = datetime.datetime.fromtimestamp(stat_r.st_mtime).strftime('%d-%m-%Y %H:%M')
        my_str = "Cache DNS : {} {} {} Ko".format(fich, my_time_str, stat_r.st_size / 1024)
        my_logger.info(my_str)

    @staticmethod
    def _search_string(pattern, filename):
        my_logger.debug(" CacheHandler._search_string() ".center(60, '-'))
        my_logger.debug(" pattern : %s - filename : %s" %(pattern,filename))
        search_file_string = "/bin/grep %s %s>%s" % (pattern[0], filename, search_file_name)
        my_logger.debug(search_file_string)
        os.system(search_file_string)
        for x in range(len(pattern)):
            if x:
                search_file_string = "/bin/grep %s %s>>%s" % (pattern[x], filename, search_file_name)
                my_logger.debug(search_file_string)
                os.system(search_file_string)

    @staticmethod
    def _search_url(pattern, file_name):
        my_logger.debug(" CacheHandler._search_url() ".center(60, '-'))
        my_logger.debug(" pattern : %s - filename : %s" %(pattern,file_name))

        try:
            f = open(file_name, 'r')
            line_with_urls_found = f.read()

            for i in range(len(pattern)):
                my_logger.debug('%d. Finding regular expression : %s ----' % (i+1, pattern[i]))
                regex = re.compile(pattern[i])
                res = regex.findall(line_with_urls_found)
                for x in range(len(res)):
                    my_logger.info('Url found : %s' % res[x])
                    yield res[x]
        except IOError:
            my_logger.debug('Le cache est vide')

    @abstractmethod
    def set_cache_file_name(self, file_name):
        pass

    @staticmethod
    def set_start_cmd(cmd):
        """
        Abstract method : set the command to initialize the cache file
        :param cmd: String populating with the command to initialize the cache file
        :return: None
        """
        pass

    @staticmethod
    def set_kill_cmd(cmd):
        """
        Abstract method : set the command to kill the process that initialize the cache file
        :param cmd: String populating with e command to initialize the cache file
        :return:
        """
        pass

    @abstractmethod
    def init_dns_cache(self):
        """
        Abstract method : Cache file initialization.
        :return: None
        """
        pass

    @abstractmethod
    def dns_cache_selection(self, pattern):
        """
        Abstract method : Selection of url in the cache file
        :param pattern: regular expression to select url
        :return: None
        """
        pass


class BindCacheHandler(CacheHandler):
    """Cache manager for bind softare installed on local host."""
    # Localization of bind cache (default)
    bind_cache_file = "/var/cache/bind/named_dump.db"
    start_cmd = ""
    kill_cmd = ""
    # Regular expression to apply on pattern to get only URLs (default)
    reg_ex = ['(.+{}).*CNAME', '(.+{})[ \t0-9]+ A', '(.+{})[ \t0-9]+\tA', 'CNAME (.+{})']

    @staticmethod
    def set_regular_expression(r):
        """
        To set other regular expression than default one
        Default regular expressions used are the following :
        reg_ex = ['(.+{}).*CNAME', '(.+{})[ \t0-9]+ A', '(.+{})[ \t0-9]+\tA', 'CNAME (.+{})']

            Regular expression uses re module
            {} designates the pattern to search provided via the method CacheDns.set_filter()
            to get a regular expression with reg_ex[i].format(pattern)

        :param r: regular expression like '(.+{}).*CNAME'
        :return: None
        """
        BindCacheHandler.reg_ex = r

    @staticmethod
    def set_start_cmd(cmd):
        """
        String populating with command to launch to generate the cache file based on DNS protocol
        :param cmd: command to launch in a string
        :return: None
        """
        BindCacheHandler.start_cmd = cmd

    @staticmethod
    def set_kill_cmd(cmd):
        """
        String populating with command to kill the command that generate the cache file based on DNS protocol
        :param cmd: command to launch in a string
        :return: None
        """
        BindCacheHandler.kill_cmd = cmd

    def set_cache_file_name(self, file_name):
        """
        File name of the cache of bind software
        :param file_name: File name 'ex: /var/cache/bind/named_dump.db on Linux Ubuntu)
        :return: None
        """
        BindCacheHandler.bind_cache_file = file_name

    def init_dns_cache(self):
        """
        Update cache file of bind installed locally on the host
        Wait 2 seconds to update file.
        :return: None
        """
        os.system(BindCacheHandler.start_cmd)
        time.sleep(2)
        CacheHandler._date_size_cache_dns(BindCacheHandler.bind_cache_file)

    def dns_cache_selection(self, pattern):
        """
        Select url in cache file
        :param pattern: pattern used to search url (reg expression)
        :return: list of urls found
        """
        # First selection to only get lines with patterns
        my_logger.debug(" dns_cache_selection() ".center(60, '-'))
        CacheHandler._search_string(pattern, BindCacheHandler.bind_cache_file)

        # Second selection to get only url with pattern
        urls_found = []
        for x in range(len(pattern)):
            pat = pattern[x].replace('.', '\\.')
            ex = []
            for i in range(len(BindCacheHandler.reg_ex)):
                ex.append(BindCacheHandler.reg_ex[i].format(pat))
            for url in CacheHandler._search_url(ex, search_file_name):
                urls_found.append(url)
        return urls_found


class SnifferCacheHandler(CacheHandler):
    """Cache manager for sniffer softare (like tcpdump)."""

    # Localization of bind cache (default)
    bind_cache_file = "/tmp/log"
    start_cmd = ""
    kill_cmd = ""
    # Regular expression to apply on pattern to get only URLs (default)
    reg_ex = ['.* (.+{}).*']

    def __init__(self, mode = AUTOMATIC, timing = 10 ):
        """

        :param mode: AUTOMATIC or MANUAL (default : AUTOMATIC)
        :param timing: time to wait before killing sniffer process (in seconds) (default : 10s) in AUTOMATIC mode
        """
        self.mode = mode
        self.timing = timing


    @staticmethod
    def set_regular_expression(r):
        """To set other regular expression than default one
            Regular expression uses re module
            {} designates the pattern to search provided via the method CacheDns.set_filter()
            to get a regular expression with reg_ex[i].format(pattern) """

        SnifferCacheHandler.reg_ex = r

    def set_cache_file_name(self, file_name):
        """
        File name for the log generated by the sniffer
        :param file_name: File name 'ex: /tmp/log)
        :return: None
        """
        SnifferCacheHandler.bind_cache_file = file_name

    @staticmethod
    def set_start_cmd(cmd):
        """
        String populating with sniffer command to launch to get a log based on DNS protocol
        :param cmd: command to launch sniffer
        :return: None
        """
        SnifferCacheHandler.start_cmd = cmd

    @staticmethod
    def set_kill_cmd(cmd):
        """
        String populating with command to stop sniffer (like kill or pkill)
        :param cmd: command to stop sniffer
        :return:
        """
        SnifferCacheHandler.kill_cmd = cmd

    def init_dns_cache(self):
        """
        Generate a log with a sniffer (see set_start_cmd())
        Type any key to stop log generation
        :return: None
        """
        my_logger.debug(" init_dns_cache() ".center(60, '-'))
        my_cmd = "%s %s" % (SnifferCacheHandler.start_cmd, SnifferCacheHandler.bind_cache_file)
        my_logger.debug(my_cmd)
        # subprocess.Popen([my_cmd, " "])
        # pid = subprocess.Popen(my_cmd, shell=True).pid
        # os.spawnl(os.P_NOWAIT,'/usr/bin/sudo', my_cmd)
        os.system(my_cmd)
        my_logger.debug(datetime.datetime.today().strftime('%d-%m-%Y %H:%M:%S'))
        if self.mode == AUTOMATIC:
            my_logger.debug('Waiting for %d seconds (%d minutes) before killing sniffer' %(self.timing, self.timing/60))
            time.sleep(self.timing)
        else:
            a = input("Type enter to stop tcpdump...")
        my_logger.debug(datetime.datetime.today().strftime('%d-%m-%Y %H:%M:%S'))
        my_logger.debug(SnifferCacheHandler.kill_cmd)
        os.system(SnifferCacheHandler.kill_cmd)
        CacheHandler._date_size_cache_dns(SnifferCacheHandler.bind_cache_file)

    def dns_cache_selection(self, pattern):
        """
        Select url in cache file
        :param pattern: pattern used to search url (reg expression)
        :return: list of urls found
        """

        # Selection to get only url with pattern
        urls_found = []
        for x in range(len(pattern)):
            pat = pattern[x].replace('.', '\\.')
            ex = []
            for i in range(len(SnifferCacheHandler.reg_ex)):
                ex.append(SnifferCacheHandler.reg_ex[i].format(pat))
            for url in CacheHandler._search_url(ex, search_file_name):
                urls_found.append(url)
        return urls_found


if __name__ == "__main__":

    # Test
    # Launch test with following command line :
    # $ python CacheDns.py debug

    stats = CacheDnsStat('rasp', 'root@jeudy', 'nicolas@jeudy.mooo.com', 'Filtered url stats')

    file_not_found = UrlFilter('FileNotFound')
    nb_url = file_not_found.read_url('FileNotFound')

    whitelist = UrlFilter('white_list')
    whitelist.read_url('whitelist')

    # Blacklist --------------------------------------------
    blacklist = UrlFilter('0.0.0.0', 'black_list')
    blacklist.set_treatment(BlackListFilterTreatment())
    nb_url_start = blacklist.read_url('blacklist')
    blacklist.write_url('blacklistbis')

    cache = CacheDns()
    h = BindCacheHandler()
    h.set_cache_file_name('named_dump.db')
    h.set_start_cmd('/usr/sbin/rndc dumpdb -cache')
    h.set_kill_cmd('')
    cache.set_handler(h)
    cache.set_filter('.googlevideo.com.')
    cache.set_filter('.gslb.com.')
    new_cache = cache.get_cache_dns()
    blacklist.add(new_cache)
    blacklist.check(whitelist.get_url())
    nb_url_end = blacklist.write_url('blacklistbis')

    stats.save_stats(nb_url_start, nb_url_end, 1)

    # Whitelist --------------------------------------------
    cache = CacheDns()
    h = SnifferCacheHandler('MANUAL')
    h.set_cache_file_name('/tmp/log')
    # File tcpdump_cache_dns.sh contains the following command :
    # /usr/bin/tcpdump -n -s 0 port 53 > argv[1] &
    # Permission is done to execute the file with sudo without password
    h.set_start_cmd('/usr/bin/sudo /usr/bin/tcpdump -n -s 0 port 53 ')
    # To kill process
    # File k_tcpdump_cache_dns.sh contains the following command :
    # pkill tcpdump
    # Permission is done to execute the file with sudo without password
    # Note that pkill doesn't work when launched from Pycharms IDE
    h.set_kill_cmd('/usr/bin/sudo /usr/bin/pkill tcpdump ')
    cache.set_handler(h)
    cache.set_filter('.googlevideo.com.')
    new_cache = cache.get_cache_dns()

    whitelist.add(new_cache)
    nb_url_end = whitelist.write_url('whitelistbis')
