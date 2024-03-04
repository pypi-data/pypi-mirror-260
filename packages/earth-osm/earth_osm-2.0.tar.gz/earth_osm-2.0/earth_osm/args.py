__author__ = "PyPSA meets Earth"
__copyright__ = "Copyright 2022, The PyPSA meets Earth Initiative"
__license__ = "MIT"

"""CLI interface for earth_osm project.

This module provides a CLI interface for the earth_osm project.

"""

import argparse
import os

from earth_osm.tagdata import get_feature_list, get_primary_list
from earth_osm.eo import save_osm_data
from earth_osm.gfk_data import get_all_valid_list, view_regions


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m earth_osm` and `$ earth_osm `.
    It parses the command line and executes the appropriate function.
    """

    class _HelpAction(argparse._HelpAction):
        def __call__(self, parser, namespace, values, option_string=None):
            parser.print_help()

            # retrieve subparsers from parser
            subparsers_actions = [
                action
                for action in parser._actions
                if isinstance(action, argparse._SubParsersAction)
            ]

            for subparsers_action in subparsers_actions:
                # get all subparsers and print help
                for choice, subparser in subparsers_action.choices.items():
                    print("Subparser '{}'".format(choice))
                    print(subparser.format_help())

            parser.exit()

    # Argparser Notes
    # '+' == 1 or more.
    # '*' == 0 or more.
    # '?' == 0 or 1.

    parser = argparse.ArgumentParser(
        description='Earth-OSM by PyPSA-meets-Earth',
        # epilog='''Example:''',
        add_help=False) # hide default help

    parser.add_argument('-h', '--help', action=_HelpAction,
                        help='earth-osm help')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.1.0')

    subparser = parser.add_subparsers(dest='command', required=True, title='Sub Parser', description='''View Supported Regions or Extract OSM Data''')

    extract_parser = subparser.add_parser('extract', help='Extract OSM Data')

    extract_parser.add_argument('primary', choices=get_primary_list(), type=str, help='Primary Feature')

    # region_group = extract_parser.add_mutually_exclusive_group(required=True) # Get regions using ids or coordinates
    # region_group.add_argument('--regions',nargs="+", type=str, help='Region Identifier')
    # region_group.add_argument('--coords', nargs='+', type=float, help='Region Bounds') #TODO: Change to >3

    extract_parser.add_argument('--regions', nargs="+", type=str, help='Region Identifier') # TODO: replace with region group
    extract_parser.add_argument('--features', nargs="*", type=str, help='Sub-Features')
    extract_parser.add_argument('--update', action='store_true', default=False, help='Update Data')
    extract_parser.add_argument('--no_mp',  action='store_false', default=True, help='No Multiprocessing')
    extract_parser.add_argument('--data_dir', nargs="?", type=str, help='Earth Data Directory')
    extract_parser.add_argument('--out_dir', nargs="?", type=str, help='Earth Output Directory')
    extract_parser.add_argument('--out_format', nargs="*", type=str, help='Export options')
    extract_parser.add_argument('--agg_feature', action='store_true', default=False, help='Aggregate Outputs by feature')
    extract_parser.add_argument('--agg_region', action='store_true', default=False, help='Aggregate Outputs by region')
    
    view_parser = subparser.add_parser('view', help='View OSM Data')
    view_parser.add_argument('type', help='View Supported', choices=['regions', 'primary'])

    args = parser.parse_args()

    print("\n".join(["",
        "  _   _   _   _   _   _   _   _   _",
        " / \ / \ / \ / \ / \ / \ / \ / \ / \ ",
        "( E | a | r | t | h | - | O | S | M )",
        " \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ "]))

    if args.command == 'view':
        print('Viewing OSM Data')
        view_regions(level=0)
    elif args.command == 'extract':
        if args.regions:
            region_list = list(args.regions)
            if not set(region_list) <= set(get_all_valid_list()):
                raise KeyError(f'Invalid Region {" ".join(set(region_list) - set(get_all_valid_list()))} , run earth_osm view regions to view valid regions')
        else:
            # TODO: ask for confirmation to proceed with all regions
            raise KeyError(f'Missing --regions <regions>. Use earth_osm view regions to view valid regions')
        # elif args.coords:
            # TODO: change coords to shapely polygon, implement geom=True, get regions that way
            # raise NotImplementedError('Bounding Box Region Identifier Not Implemented')

        if args.features:
            feature_list = list(args.features)
            if not (set(feature_list) <= set(get_feature_list(args.primary)) or set(feature_list) == {'ALL'}):
                raise KeyError(f'Invalid Feature {" ".join(set(feature_list) - set(get_feature_list(args.primary)))}, run earth_osm view features to view valid features')
        else:
            feature_list = list(get_feature_list(args.primary))
            assert isinstance(feature_list, list), f'Invalid Feature List {feature_list}'

        if args.data_dir:
            if not os.path.exists(args.data_dir):
                os.makedirs(args.data_dir, exist_ok=True)
            if os.path.isdir(args.data_dir):
                data_dir = args.data_dir
            else:
                raise NotADirectoryError(f'Invalid Data Directory {args.data_dir}')
        else:
            data_dir = os.path.join(os.getcwd(), 'earth_data')

        if args.out_dir:
            if not os.path.exists(args.out_dir):
                os.makedirs(args.out_dir, exist_ok=True)
            if os.path.isdir(args.out_dir):
                out_dir = args.out_dir
            else:
                raise NotADirectoryError(f'Invalid Output Directory {args.out_dir}')
        else:
            out_dir = data_dir
        
        if args.out_format:
            out_format = set(args.out_format)
            if not out_format.issubset(['csv', 'geojson']):
                raise KeyError(f'Contains invalid format. Valid formats are: csv, geojson')
        else:
            out_format = ['csv', 'geojson']

        if args.agg_feature and args.agg_region:
            raise KeyError(f'Cannot aggregate by both feature and region')
        elif args.agg_feature:
            out_aggregate = 'feature'
        elif args.agg_region:
            out_aggregate = 'region'
        else:
            out_aggregate = False



        print('\n'.join(['',
            f'Primary Feature: {args.primary}',
            f'Sub Features: {" - ".join(feature_list)}',
            f'Regions: {" - ".join(region_list)}',
            f'Multiprocessing = {args.no_mp}',
            f'Update Data = {args.update}',
            f'Data Directory = {data_dir}',
            f'Output Directory = {out_dir}',
            f'Output Format = {" - ".join(out_format)}',
            f'Aggregate Outputs = {out_aggregate}',
            ]))

        save_osm_data(
            region_list=region_list,
            primary_name=args.primary,
            feature_list=feature_list,
            data_dir=data_dir,
            out_dir=out_dir,
            # move to kwargs
            update=args.update,
            mp=args.no_mp,
            out_format=out_format,
            out_aggregate=out_aggregate,
        )

    else:
        # import inquirer #https://github.com/magmax/python-inquirer
        raise NotImplementedError('Interactive Mode Not Implemented')


