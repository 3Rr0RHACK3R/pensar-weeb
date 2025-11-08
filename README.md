# Pensar Weeb .
Is a buncha web tools made to take off the headache of creating web apps and more .

# TOOLS:
# 1. Web bundler.
# What Is Web Bundler?

So Web Bundler is Basically a Bundler which bundles ur CSS HTML and JS code together and boom easier to create a website 
without billions of files scattered all around.

Usage:

# multiple file bundling

```bash
# Bundle multiple CSS and JS files
python web-bundler.py --bundle index.html style.css theme.css script.js utils.js

# Bundle only with multiple CSS files
python web-bundler.py --bundle index.html style.css responsive.css dark-mode.css

# Bundle only with multiple JS files  
python web-bundler.py --bundle index.html main.js helpers.js components.js
```
# auto detection to where the files are. we use index.html's reference to finding the file tbh.

```bash

# Auto-detect and bundle CSS/JS files
python web-bundler.py --auto-bundle index.html

# Auto-bundle with custom output
python web-bundler.py --auto-bundle index.html --output my-app.html

```
# mixed usages

```bash
# Manual bundling with custom output
python web-bundler.py --bundle index.html style.css script.js --output dist/final.html
```

so pretty much you can also make this really easily. But why make it again when we got web-bundle?