import os
import sys
from pathlib import Path
from typing import List, Optional
from bs4 import BeautifulSoup
import csscompressor
import jsmin

class Bundler:
    def __init__(self, minify: bool = False):
        self.minify = minify
        self.common_css_patterns = ['style.css', 'styles.css', 'main.css', 'app.css', '*.css']
        self.common_js_patterns = ['script.js', 'scripts.js', 'main.js', 'app.js', '*.js']
        self.encoding = 'utf-8'

    def read_file(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding=self.encoding) as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file '{file_path}': {e}")
            sys.exit(1)

    def write_file(self, file_path: str, content: str):
        try:
            with open(file_path, 'w', encoding=self.encoding) as f:
                f.write(content)
            print(f"Successfully created bundled file: {file_path}")
        except Exception as e:
            print(f"Error writing file '{file_path}': {e}")
            sys.exit(1)

    def auto_detect_files(self, html_file: str) -> tuple[List[str], List[str]]:
        dir_path = os.path.dirname(html_file) or '.'
        css_files = []
        js_files = []
        print('Auto-detecting files...')
        import glob
        for pattern in self.common_css_patterns:
            matches = glob.glob(os.path.join(dir_path, pattern))
            for match in matches:
                if os.path.isfile(match) and match not in css_files:
                    css_files.append(match)
                    print(f"  Found CSS: {os.path.basename(match)}")
            if css_files and pattern != '*.css':
                break
        for pattern in self.common_js_patterns:
            matches = glob.glob(os.path.join(dir_path, pattern))
            for match in matches:
                if os.path.isfile(match) and match not in js_files:
                    js_files.append(match)
                    print(f"  Found JS:  {os.path.basename(match)}")
            if js_files and pattern != '*.js':
                break
        return css_files, js_files

    def parse_file_arguments(self, files: List[str]) -> tuple[str, List[str], List[str]]:
        html_file = None
        css_files = []
        js_files = []
        for file_path in files:
            if not os.path.exists(file_path):
                print(f"Warning: File '{file_path}' not found, skipping.")
                continue
            ext = os.path.splitext(file_path)[1].lower()
            if ext in ['.html', '.htm']:
                if html_file:
                    print(f"Warning: Multiple HTML files provided. Using '{file_path}' as main HTML.")
                html_file = file_path
            elif ext == '.css':
                css_files.append(file_path)
            elif ext == '.js':
                js_files.append(file_path)
            else:
                print(f"Warning: Unknown file type '{file_path}', skipping.")
        if not html_file:
            print('Error: No HTML file found in provided files.')
            sys.exit(1)
        return html_file, css_files, js_files

    def validate_files(self, html_file: str, css_files: List[str] = None, js_files: List[str] = None):
        if css_files is None:
            css_files = []
        if js_files is None:
            js_files = []
        if not os.path.exists(html_file):
            print(f"Error: HTML file '{html_file}' not found.")
            sys.exit(1)
        if not os.path.splitext(html_file)[1].lower() in ['.html', '.htm']:
            print(f"Warning: '{html_file}' doesn't have an HTML extension.")
        for css in css_files:
            if not os.path.splitext(css)[1].lower() == '.css':
                print(f"Warning: '{css}' doesn't have a CSS extension.")
        for js in js_files:
            if not os.path.splitext(js)[1].lower() == '.js':
                print(f"Warning: '{js}' doesn't have a JS extension.")

    def bundle_files(self, html_file: str, css_files: List[str] = None, js_files: List[str] = None) -> str:
        if css_files is None:
            css_files = []
        if js_files is None:
            js_files = []
        html_content = self.read_file(html_file)
        soup = BeautifulSoup(html_content, 'html.parser')
        if css_files:
            css_concat = []
            for css_path in css_files:
                if os.path.exists(css_path):
                    css_content = self.read_file(css_path)
                    css_concat.append(f"/* {os.path.basename(css_path)} */\n{css_content}")
                else:
                    print(f"Warning: CSS file '{css_path}' not found, skipping.")
            if css_concat:
                css_joined = '\n'.join(css_concat)
                if self.minify:
                    css_joined = csscompressor.compress(css_joined)
                style_tag = soup.new_tag('style')
                style_tag.string = css_joined
                if soup.head:
                    soup.head.append(style_tag)
                else:
                    html_tag = soup.find('html')
                    if html_tag:
                        head_tag = soup.new_tag('head')
                        head_tag.append(style_tag)
                        html_tag.insert(0, head_tag)
        if js_files:
            js_concat = []
            for js_path in js_files:
                if os.path.exists(js_path):
                    js_content = self.read_file(js_path)
                    js_concat.append(f"/* {os.path.basename(js_path)} */\n{js_content}")
                else:
                    print(f"Warning: JS file '{js_path}' not found, skipping.")
            if js_concat:
                js_joined = '\n'.join(js_concat)
                if self.minify:
                    js_joined = jsmin.JSMin(js_joined).minify()
                script_tag = soup.new_tag('script')
                script_tag.string = js_joined
                if soup.body:
                    soup.body.append(script_tag)
                else:
                    html_tag = soup.find('html')
                    if html_tag:
                        body_tag = soup.new_tag('body')
                        body_tag.append(script_tag)
                        html_tag.append(body_tag)
        return str(soup)

    def create_output_filename(self, html_file: str, mode: str = 'bundle') -> str:
        base = Path(html_file)
        suffix = '-auto-bundled' if mode == 'auto' else '-bundled'
        return f"{base.stem}{suffix}{base.suffix}"

    def run_bundle(self, files: List[str], output_file: Optional[str] = None, validate_only: bool = False) -> None:
        html_file, css_files, js_files = self.parse_file_arguments(files)
        self.validate_files(html_file, css_files, js_files)
        if validate_only:
            print("Validation complete. No bundling performed.")
            return
        if not output_file:
            output_file = self.create_output_filename(html_file, 'bundle')
        print("Bundling files...")
        print(f"HTML: {html_file}")
        for css in css_files:
            print(f"CSS:  {css}")
        for js in js_files:
            print(f"JS:   {js}")
        bundled = self.bundle_files(html_file, css_files, js_files)
        self.write_file(output_file, bundled)

    def run_auto_bundle(self, html_file: str, output_file: Optional[str] = None, validate_only: bool = False) -> None:
        if not os.path.exists(html_file):
            print(f"Error: HTML file '{html_file}' not found.")
            sys.exit(1)
        self.validate_files(html_file)
        css_files, js_files = self.auto_detect_files(html_file)
        if validate_only:
            print("Validation complete. No bundling performed.")
            return
        if not output_file:
            output_file = self.create_output_filename(html_file, 'auto')
        print("Auto-bundling files...")
        print(f"HTML: {html_file}")
        for css in css_files:
            print(f"CSS:  {css}")
        for js in js_files:
            print(f"JS:   {js}")
        if not css_files and not js_files:
            print('Warning: No CSS or JS files found for auto-bundling.')
        bundled = self.bundle_files(html_file, css_files, js_files)
        self.write_file(output_file, bundled)