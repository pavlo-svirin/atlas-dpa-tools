#!/usr/bin/env python3

import argparse
import core.bigpanda.monitor_query
import core.display.cli_tables

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hours", help="Hours for which we fetch errors", default=core.bigpanda.monitor_query.__DEFAULT_HOURS__)
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
        sites_aggregates = core.bigpanda.monitor_query.get_aggregates(args.hours, args.sort, args.all, args.real)
        core.display.cli_tables.print_tabled_errors(sites_aggregates, ['Site', 'status', '% failed', 'Failed #', 'Activated #', 'Jobs #', 'Pilots #'])
    #else:
        #sites=sys.argv[1:]
        #resourcetype=sys.argv[2] if len(sys.argv)>2 else None
        
        #print(f'Now getting info for {site}/{resourcetype}')
        #get_aggregates_per_site('BU_ATLAS_Tier2_UCORE', 'SCORE')
    #    get_aggregates_per_site(args.sites, args.hours)
#    curl = Curl()
#    print(curl.perform('https://bigpanda.cern.ch/errorslist/?codename=jobdispatchererrorcode&codeval=100&tk=735147&json'))
#    curl.close()
