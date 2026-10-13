# vlbinfra.com

Website of Vaibhav Laxmi Builders (VLB), Saharanpur. Hosted on GitHub Pages.

## How to update

All content (contact details, registration, departments, services, projects) lives in `tools/build.py`.

1. Edit the CONTENT section of `tools/build.py`
2. Put project photos in `images/projects/`
3. Run `python3 tools/build.py`
4. Commit and push; the site updates in about a minute

## Files

- `index.html`, `about.html`, `services.html`, `projects.html`, `contact.html`: generated pages
- `assets/`: stylesheet, script and logo
- `images/projects/`: project photos
- `CNAME`: custom domain for GitHub Pages
