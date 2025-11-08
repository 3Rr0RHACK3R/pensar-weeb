#!/usr/bin/env python3
import argparse
import sys
sys.path.append('web-bundle-backend')
from logic import Bundler
def main():
    parser=argparse.ArgumentParser(description='Bundle HTML, CSS, and JS files into a single HTML file')
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--bundle',nargs='+',help='Files to bundle: HTML file (required), CSS files (optional), JS files (optional)',metavar='FILES')
    group.add_argument('--auto-bundle',help='Auto-detect and bundle CSS and JS files for the given HTML file',metavar='HTML_FILE')
    parser.add_argument('--output','-o',help='Output file name (default: auto-generated)',metavar='OUTPUT_FILE')
    parser.add_argument('--minify',action='store_true',help='Minify CSS and JS code')
    parser.add_argument('--validate-only',action='store_true',help='Validate files without bundling')
    args=parser.parse_args()
    bundler=Bundler(minify=args.minify)
    if args.bundle:
        bundler.run_bundle(args.bundle,args.output,args.validate_only)
    elif args.auto_bundle:
        bundler.run_auto_bundle(args.auto_bundle,args.output,args.validate_only)
if __name__=='__main__':
    main()