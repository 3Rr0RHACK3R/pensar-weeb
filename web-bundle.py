#!/usr/bin/env python3
# Thank you Python Minifier for making this file smaller!
O='auto'
G='bundle'
N='.js'
M='.css'
L='.htm'
K='.html'
F='utf-8'
J='*.js'
I='*.css'
C=Exception
E=None
A=print
import argparse as P,os as B,re,sys as D,glob as H
from pathlib import Path
from typing import List,Tuple,Dict
class Q:
	def __init__(A):A.common_css_patterns=['style.css','styles.css','main.css','app.css',I];A.common_js_patterns=['script.js','scripts.js','main.js','app.js',J]
	def read_file(H,file_path):
		B=file_path
		try:
			with open(B,'r',encoding=F)as E:return E.read()
		except FileNotFoundError:A(f"Error: File '{B}' not found.");D.exit(1)
		except C as G:A(f"Error reading file '{B}': {G}");D.exit(1)
	def write_file(H,file_path,content):
		B=file_path
		try:
			with open(B,'w',encoding=F)as E:E.write(content)
			A(f"Successfully created bundled file: {B}")
		except C as G:A(f"Error writing file '{B}': {G}");D.exit(1)
	def auto_detect_files(K,html_file):
		L=B.path.dirname(html_file)or'.';E=[];F=[];A('Auto-detecting files...')
		for D in K.common_css_patterns:
			G=H.glob(B.path.join(L,D))
			for C in G:
				if C not in E and B.path.isfile(C):E.append(C);A(f"  Found CSS: {B.path.basename(C)}")
			if E and D!=I:break
		for D in K.common_js_patterns:
			G=H.glob(B.path.join(L,D))
			for C in G:
				if C not in F and B.path.isfile(C):F.append(C);A(f"  Found JS:  {B.path.basename(C)}")
			if F and D!=J:break
		return E,F
	def parse_file_arguments(J,files):
		F=E;H=[];I=[]
		for C in files:
			if not B.path.exists(C):A(f"Warning: File '{C}' not found, skipping.");continue
			G=C.lower()
			if G.endswith((K,L)):
				if F:A(f"Warning: Multiple HTML files provided. Using '{C}' as main HTML.")
				F=C
			elif G.endswith(M):H.append(C)
			elif G.endswith(N):I.append(C)
			else:A(f"Warning: Unknown file type '{C}', skipping.")
		if not F:A('Error: No HTML file found in provided files.');D.exit(1)
		return F,H,I
	def bundle_files(F,html_file,css_files=E,js_files=E):
		N='</body>';M='</head>';J=js_files;I=css_files;C=F.read_file(html_file)
		if I:
			G=[]
			for D in I:
				if B.path.exists(D):O=F.read_file(D);G.append(f"/* {B.path.basename(D)} */\n{O}")
				else:A(f"Warning: CSS file '{D}' not found, skipping.")
			if G:
				P='\n'.join(G);K=f"\n<style>\n{P}\n</style>\n"
				if M in C:C=C.replace(M,f"{K}</head>")
				else:C+=K
		if J:
			H=[]
			for E in J:
				if B.path.exists(E):Q=F.read_file(E);H.append(f"/* {B.path.basename(E)} */\n{Q}")
				else:A(f"Warning: JS file '{E}' not found, skipping.")
			if H:
				R='\n'.join(H);L=f"\n<script>\n{R}\n</script>\n"
				if N in C:C=C.replace(N,f"{L}</body>")
				else:C+=L
		return C
	def validate_files(G,html_file,css_files,js_files):
		C=html_file
		if not B.path.exists(C):A(f"Error: HTML file '{C}' not found.");D.exit(1)
		if not C.lower().endswith((K,L)):A(f"Warning: '{C}' doesn't have an HTML extension.")
		for E in css_files:
			if not E.lower().endswith(M):A(f"Warning: '{E}' doesn't have a CSS extension.")
		for F in js_files:
			if not F.lower().endswith(N):A(f"Warning: '{F}' doesn't have a JS extension.")
	def create_output_filename(C,html_file,mode=G):
		A=Path(html_file)
		if mode==O:B='-auto-bundled'
		else:B='-bundled'
		return A.stem+B+A.suffix
	def run_bundle(B,files,output_file=E):
		D=output_file;C,E,F=B.parse_file_arguments(files);B.validate_files(C,E,F)
		if not D:D=B.create_output_filename(C,G)
		A(f"Bundling files...");A(f"HTML: {C}")
		for H in E:A(f"CSS:  {H}")
		for I in F:A(f"JS:   {I}")
		J=B.bundle_files(C,E,F);B.write_file(D,J)
	def run_auto_bundle(E,html_file,output_file=E):
		F=output_file;C=html_file
		if not B.path.exists(C):A(f"Error: HTML file '{C}' not found.");D.exit(1)
		G,H=E.auto_detect_files(C)
		if not F:F=E.create_output_filename(C,O)
		A(f"Auto-bundling files...");A(f"HTML: {C}")
		for I in G:A(f"CSS:  {I}")
		for J in H:A(f"JS:   {J}")
		if not G and not H:A('Warning: No CSS or JS files found for auto-bundling.')
		K=E.bundle_files(C,G,H);E.write_file(F,K)
def R():
	B=P.ArgumentParser(description='Bundle HTML, CSS, and JS files into a single HTML file',usage='web-bundler.py [--bundle FILES... | --auto-bundle HTML_FILE] [--output OUTPUT_FILE]');C=B.add_mutually_exclusive_group(required=True);C.add_argument('--bundle',nargs='+',help='Files to bundle: HTML file (required), CSS files (optional), JS files (optional)',metavar='FILES');C.add_argument('--auto-bundle',help='Auto-detect and bundle CSS and JS files for the given HTML file',metavar='HTML_FILE');B.add_argument('--output','-o',help='Output file name (default: auto-generated)',metavar='OUTPUT_FILE');A=B.parse_args();D=Q()
	if A.bundle:D.run_bundle(A.bundle,A.output)
	elif A.auto_bundle:D.run_auto_bundle(A.auto_bundle,A.output)
if __name__=='__main__':R()