import pytest
from dnsurlsearch import DNSurlSearch

def test_url_filter_1():

    """ 1. Test url filter file doesn't exist"""
    url_list = DNSurlSearch.UrlFilter()
    nb_url = url_list.read_url('FileNotFound')
    assert nb_url == 0

    """ 2. Test adding new url """
    url_list.add(['rr1.sn-cv0tb0xn-uane.googlevideo.com.'])
    url_list.add(['rr2.sn-cv0tb0xn-uane.googlevideo.com.'])

    urls = url_list.get_url()
    assert urls == ['rr1.sn-cv0tb0xn-uane.googlevideo.com.', 'rr2.sn-cv0tb0xn-uane.googlevideo.com.']

    """ 3. Test adding url that already exist"""
    url_list.add(['rr1.sn-cv0tb0xn-uane.googlevideo.com.'])

    urls = url_list.get_url()
    assert urls == ['rr1.sn-cv0tb0xn-uane.googlevideo.com.', 'rr2.sn-cv0tb0xn-uane.googlevideo.com.']

    """ 4. Delete url that doesn't exist"""
    url_list.check(['rr3.sn-cv0tb0xn-uane.googlevideo.com.'])

    urls = url_list.get_url()
    assert urls == ['rr1.sn-cv0tb0xn-uane.googlevideo.com.', 'rr2.sn-cv0tb0xn-uane.googlevideo.com.']

    """ 5. Delete url that exists"""
    url_list.check(['rr2.sn-cv0tb0xn-uane.googlevideo.com.'])

    urls = url_list.get_url()
    assert urls == ['rr1.sn-cv0tb0xn-uane.googlevideo.com.']

    """ 6. Save url filter """
    url_list.write_url('url_list')

    """ 7. Test url filter file exist"""
    url_list = DNSurlSearch.UrlFilter()
    nb_url = url_list.read_url('url_list')
    assert nb_url == 1

    urls = url_list.get_url()
    assert urls == ['rr1.sn-cv0tb0xn-uane.googlevideo.com.']


