# SPDX-License-Identifier: GPL-2.0

import json

import _damon
import _damon_args

def main(args):
    _damon.ensure_root_and_initialized(args)

    feature_supports, err = _damon.get_feature_supports()
    if err != None:
        print('getting feature supports info failed (%s)' % err)
        exit(1)
    for feature in sorted(feature_supports.keys()):
        supported = feature_supports[feature]
        if args.type == 'all':
            print('%s: %s' % (feature,
                'Supported' if supported else 'Unsupported'))
        elif args.type == 'supported' and supported:
            print(feature)
        elif args.type == 'unsupported' and not supported:
            print(feature)
    if args.type == 'json':
        print(json.dumps(feature_supports, indent=4, sort_keys=True))

def set_argparser(parser):
    parser.add_argument('type', nargs='?',
            choices=['supported', 'unsupported', 'all', 'json'], default='all',
            help='type of features to listed')
    _damon_args.set_common_argparser(parser)
