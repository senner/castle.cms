from castle.cms import audit
from AccessControl.SecurityManagement import newSecurityManager
from castle.cms.cron.utils import setup_site
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from tendo import singleton
from castle.cms.utils import ESConnectionFactoryFactory
from datetime import datetime, date
from elasticsearch.helpers import scan

from re import sub
from os import path, makedirs
import argparse
import json

def get_args():
    parser = argparse.ArgumentParser(
        description='Import Audit Logs from file and index in Elasticsearch')
    parser.add_argument('--outdir', dest='output_directory', default='audit_logs')
    parser.add_argument('--type', dest='type', default=None)
    parser.add_argument('--user', dest='user', default=None)
    parser.add_argument('--content', dest='content', default=None)
    parser.add_argument('--after', dest='after', default=None)
    parser.add_argument('--before', dest='before', default=None)
    args, _ = parser.parse_known_args()
    return args

def get_query(args):
        filters = []
        if args.type:
            filters.append(
                {'term': {'type': args.type}}
            )
        if args.user:
            filters.append(
                {'term': {'user': args.user}}
            )
        if args.content:
            items = args.content.split(';')
            cqueries = [{'term': {'object': item}} for item in items]
            filters.append(
                {'or': cqueries}
            )
        if args.after:
            filters.append(
                {'range': {'date': {'gte': args.after}}}
            )
        if args.before:
            filters.append(
                {'range': {'date': {'lte': args.before}}}
            )
        if len(filters) == 0:
            query = {
                "query": {'match_all': {}}
            }
        else:
            if len(filters) > 1:
                qfilter = {'and': filters}
            else:
                qfilter = filters[0]
            query = {
                "query": {
                    'filtered': {
                        'filter': qfilter,
                        'query': {'match_all': {}}
                    }
                }
            }
        return query

def export_audit_log(site, args):
        log_entries = []
        setup_site(site)

        index_name = audit.get_index_name()
        es = ESConnectionFactoryFactory()()
        query = get_query(args)
        scroll_duration = '1m'

        start_time = datetime.now()
        export_date = date.today()
        print('\nLooking for audit logs...')

        results = scan(
            es,
            index=index_name,
            doc_type=audit.es_doc_type,
            query=query,
            size=3000,
            scroll=scroll_duration)
        for result in results:
            log_entries.append(result)

        end_time = datetime.now()
        tdelta = end_time - start_time
        print('\nFound {} logs in {}'.format(len(log_entries), str(tdelta)))

        audit_log = {
            'export_timestamp': str(start_time),
            'audit_log': log_entries
        }

        if not path.exists(args.output_directory):
            makedirs(args.output_directory)
            print('\nCreated directory {}'.format(args.output_directory))

        formatted_time = sub(r'[ :]', '_', str(start_time))
        filepath = args.output_directory + '/audit_log_{}.json'.format(formatted_time)
        print('\nWriting File {}'.format(filepath))

        with open(filepath, 'w') as file:
            json.dump(audit_log, file)

        print('\nYour file is ready')

def run(app):
    singleton.SingleInstance('exportauditlog')

    user = app.acl_users.getUser('admin')  # noqa
    newSecurityManager(None, user.__of__(app.acl_users))  # noqa

    for oid in app.objectIds():  # noqa
        obj = app[oid]  # noqa
        if IPloneSiteRoot.providedBy(obj):
            export_audit_log(obj, get_args())


if __name__ == '__main__':
    run(app)  # noqa
