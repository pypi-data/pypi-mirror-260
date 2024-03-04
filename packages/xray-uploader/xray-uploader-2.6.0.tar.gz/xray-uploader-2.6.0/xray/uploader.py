import sys
import argparse
import logging
import requests
import json
import os

try:
    from .logger import logger
except ImportError:
    from logger import logger
# from .xml import JunitXml


class Uploader:
    VALID_FORMATS = ('testng', 'junit')

    def __init__(self, client_id, client_secret):
        self._id = client_id
        self._secret = client_secret
        self._token = None

    def fetch_token(self):
        url = 'https://xray.cloud.getxray.app/api/v1/authenticate'
        cloud_auth = {
            'client_id': self._id,
            'client_secret': self._secret
        }
        logger.debug('try to get the token from xray.')
        res = requests.post(url=url, data=cloud_auth)
        try:
            assert res.status_code == 200
        except:
            logging.error(res.text)
            raise
        self._token = res.text.strip('"')
        logger.debug('Get the token successfully.')

    @staticmethod
    def dump_info(info_json, execution_summary, project_id, testplan_id):
        info = {
            'fields': {
                'project': {
                    'id': project_id
                },
                'summary': execution_summary,
                'issuetype': {
                    'id': '10221'
                }
            }
        }
        if testplan_id:
            info['xrayFields'] = {'testPlanKey': testplan_id}
        logger.info(f'Posted info {info}')
        json.dump(info, open(info_json, 'w'))

    def import_execution(self, res_file, execution_summary, project_id, res_format, testplan_id=''):
        """
        :param res_file: result file path
        :param execution_summary: test execution summary
        :param project_id: jira project id, string type
        :param testplan_id: test plan id, string type
        :param res_format: result format, string type
        # :param safe_mode: boolean type, false by default, otherwise it will remove test case nodes which do not have
        child node "property" and corresponding attributes "test_key" and "value" inside.
        """
        self.fetch_token()
        # if safe_mode:
        #     updated_file = res_xml.replace('py_result', 'xray_result').replace('.xml', '_xray.xml')
        #     JunitXml(res_file).dump_xray_format_xml(updated_file)
        # else:
        #     updated_file = res_file
        updated_file = res_file
        url = f'https://xray.cloud.getxray.app/api/v1/import/execution/{res_format}/multipart'
        headers = {
            'Authorization': f'Bearer {self._token}'
        }
        info_json = os.path.join(os.path.dirname(__file__), 'info_temp.json')
        self.dump_info(info_json, execution_summary, project_id, testplan_id)
        files = {
            'info': open(info_json, 'rb'),
            'results': open(updated_file, 'rb')
        }
        logger.debug('Try to import the execution into xray.')
        # logger.info(f'Headers: {json.dumps(headers)}')
        res = requests.post(url, headers=headers, files=files)
        logger.info(f'Status code: {res.status_code}')
        try:
            assert res.status_code == 200
            logger.info(res.text)
        except:
            logging.error(res.text)
            raise
        logger.debug('Import the execution into xray successfully.')


def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, prog='xray-uploader',
                                     epilog="General purpose xray uploader.\n"
                                            "Currently either specify a testng or a junit style xml file .\n")

    parser.add_argument('-r', '--result', required=True, help='A result file with absolute path.')
    parser.add_argument('-f', '--format', required=True,
                        help=f'Format of the result file. Valid formats are {", ".join(Uploader.VALID_FORMATS)}')
    parser.add_argument('-pi', '--projectId', required=True,
                        help='ID of the project where the test execution is going to be created.')
    parser.add_argument('-s', '--summary', required=True, help='Summary of the test execution.')
    parser.add_argument('-ci', '--clientId',
                        help='Client ID to authorize if it is specified, otherwise will read from env CLIENT_ID.')
    parser.add_argument('-cs', '--clientSecret',
                        help='Client secret to authorize if it is specified, '
                             'otherwise will read from env CLIENT_SECRET.')
    parser.add_argument('-tp', '--testPlan', default='',
                        help='The tests will be added automatically to the test plan if it is specified.')

    if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
        parser.print_help()
        sys.exit(0)
    else:
        args, _ = parser.parse_known_args()
        return vars(args)


def main_cli():
    args = parse_arguments()
    try:
        client_id = args.get('clientId') if args.get('clientId') is not None else os.environ['CLIENT_ID']
    except KeyError:
        logger.error('Either specifying "clientId" in the arguments or predefining the env var CLIENT_ID.')
        raise
    try:
        client_secret = args.get('clientSecret') if args.get('clientSecret') is not None else os.environ['CLIENT_SECRET']
    except KeyError:
        logger.error('Either specifying "clientSecret" in the arguments or predefining the env var CLIENT_SECRET.')
        raise
    try:
        assert args['format'] in Uploader.VALID_FORMATS
    except AssertionError:
        logger.error(f'{args["format"]} is not supported now, valid formats are {", ".join(Uploader.VALID_FORMATS)}')
        raise
    uploader = Uploader(client_id, client_secret)
    uploader.import_execution(args['result'], args['summary'], args['projectId'], args['format'], args['testPlan'])


# main_cli()
