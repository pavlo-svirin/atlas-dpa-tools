#!/usr/bin/env python

import pycurl
#from StringIO import StringIO
from io import StringIO
from io import BytesIO
from pprint import pprint
import json
import operator
import sys
import argparse
from tabulate import tabulate

# https://bigpanda.cern.ch/jobs/?computingsite=UKI-NORTHGRID-LIV-HEP_SL7_UCORE&jobtype=production&jobstatus=failed&hours=12
# https://bigpanda.cern.ch/dash/production/?cloudview=region&sortby=pctfail

__DEFAULT_HOURS__=12
__DEFAULT_DIAG_COLWIDTH__=80

def print_tabled_errors(table, headers):
    print(tabulate(table, headers, tablefmt="fancy_grid"))


def get_aggregates(hours, sort_mode='pctfail', show_all=False, only_real=False):
    #url = "https://bigpanda.cern.ch/dash/production/?cloudview=region&sortby=pctfail&json"
    url = f"https://bigpanda.cern.ch/dash/production/?cloudview=region&hours={hours}&json"
    storage = BytesIO()

    try:
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)   
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.setopt(curl.WRITEFUNCTION, storage.write)

        curl.perform()
        curl.close()
        #pprint(storage.getvalue().decode('UTF-8'))
    except:
        print('Exception occured in CURL call')
        return 

    sites_failures = []
    sites_failures_array = []

    summary = json.loads(storage.getvalue().decode('UTF-8'))
    
    for s in summary['summary']:
        if s['name']=='': continue
        for site, siteinfo in s['sites'].items():
            if not show_all and ('status' not in siteinfo or siteinfo['status']=='test' or ((siteinfo['pctfail']<15 or siteinfo['pctfail']>30) and siteinfo['states']['failed']['count']<50)):
                continue
            if only_real and site.find(' ')!=-1:
                continue
            #print("%-50s%-15s\t%-4d\t%-4d" % (site, siteinfo['status'], siteinfo['pctfail'], siteinfo['states']['failed']['count']) )
            #sites_failures.append({'site' : site.replace(' ', '/'),
            #                        'status' : siteinfo['status'],
            #                        'pctfail' : siteinfo['pctfail'],
            #                        'count' : siteinfo['states']['failed']['count'],
            #                        'activated' : siteinfo['states']['activated']['count'],
            #                        'jobsno' : siteinfo['nojobabs'],
            #                        'pilotsno' : siteinfo['pilots']})
            sites_failures_array.append([site.replace(' ', '/'),
                                         siteinfo['status'],
                                         siteinfo['pctfail'],
                                         siteinfo['states']['failed']['count'],
                                         siteinfo['states']['activated']['count'],
                                         siteinfo['nojobabs'],
                                         siteinfo['pilots']])
    use_sort_mode = 2
    if sort_mode=='site': use_sort_mode=0
    if sort_mode=='status': use_sort_mode=1
    if sort_mode=='failed': use_sort_mode=3
    if sort_mode=='activated': use_sort_mode=4
    if sort_mode=='jobsno': use_sort_mode=5
    if sort_mode=='pilotsno': use_sort_mode=6

    #sites_failures.sort(key=lambda s: s['pctfail'], reverse=True)
    #sites_failures_array.sort(key=lambda s: s[use_sort_mode], reverse=True)
    sites_failures_array.sort(key=lambda s: s[use_sort_mode], reverse=False)
    #for sf in sites_failures:
    #        print("%-50s%-15s\t%-4d\t%-4d" % (sf['site'], sf['status'], sf['pctfail'], sf['count']) )
    print_tabled_errors(sites_failures_array, ['Site', 'status', '% failed', 'Failed #', 'Activated #', 'Jobs #', 'Pilots #'])
    


def get_aggregates_per_site(sites, hours):
    if not any(sites):
       print('No sites given')
       return

    for site in sites:
        
        sitedetails = site.split('/')
        sitename=sitedetails[0]
        resource_param = "" if len(sitedetails)<2 or sitedetails[1]==""  else "&resourcetype=%s" % sitedetails[1] 

        url = f"https://bigpanda.cern.ch/jobs/?computingsite={sitename}&jobtype=production&jobstatus=failed&hours={hours}&display_limit=100&json{resource_param}"
        storage = BytesIO()

        try:
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, url)
            curl.setopt(pycurl.SSL_VERIFYPEER, 0)   
            curl.setopt(pycurl.SSL_VERIFYHOST, 0)
            curl.setopt(curl.WRITEFUNCTION, storage.write)

            curl.perform()
            curl.close()
            #pprint(storage.getvalue().decode('UTF-8'))
        except:
            print('Exception occured in CURL call')
            return 

        summary = json.loads(storage.getvalue().decode('UTF-8'))
        data = []
        print(f'\n============== Errors for: {site} =============')
        for e in summary['errsByCount']:
            data.append( [e['error'], "\n".join([ e['diag'][i:i+__DEFAULT_DIAG_COLWIDTH__] for i in range(0, len(e['diag']), __DEFAULT_DIAG_COLWIDTH__) ]), e['count']] )
            #print("%-50s %s : %i" % (e['error'], e['diag'], e['count']))
        #print('================================================\n\n')
        print_tabled_errors(data, ['Error type', 'Diagnostics', 'Count'])
        print()


def print_sites_error_details(sites, hours, select):
    for site in sites:
        pass


def print_sites_error_aggregates():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hours", help="Hours for which we fetch errors", default=__DEFAULT_HOURS__)
    parser.add_argument("--show", help="Show only these types of errors", default="taskbuffer,exe,pilot,jobdispatcher,ddm")
    parser.add_argument("--sort", help="Sort modes: site,status,pct,failed,activated,jobsno,pilotsno", default="pct")
    parser.add_argument("--all", help="Show all sites", default=False, action='store_true')
    parser.add_argument("--real", help="Show only real sites", default=False, action='store_true')
    #parser.add_argument("--taskbuffer", help="Show taskbuffer errors", default=False, action='store_true')
    #parser.add_argument("--exe", help="Show executable errors", default=False, action='store_true')
    #parser.add_argument("--pilot", help="Show pilot errors", default=False, action='store_true')
    #parser.add_argument("--jobdispatcher", help="Show job dispatcher errors", default=False, action='store_true')
    #parser.add_argument("--ddm", help="Show job ddm errors", default=False, action='store_true')
    parser.add_argument('sites', metavar='S', nargs='*',
                    help='sites to be queried')
    args = parser.parse_args()

    #print(args)
    #sys.exit(0)

    #if len(sys.argv)==1:
    if not any(args.sites):
        get_aggregates(args.hours, args.sort, args.all, args.real)
    else:
        #sites=sys.argv[1:]
        #resourcetype=sys.argv[2] if len(sys.argv)>2 else None
        
        #print(f'Now getting info for {site}/{resourcetype}')
        #get_aggregates_per_site('BU_ATLAS_Tier2_UCORE', 'SCORE')
        get_aggregates_per_site(args.sites, args.hours)
