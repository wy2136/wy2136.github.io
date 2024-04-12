#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Oct 15 16:29:10 EDT 2019
from datetime import datetime
import os.path, sys, os
import glob
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
from misc import intToRoman
#import filecmp #use filecmp_exclude_date instead
def filecmp_exclude_date(file1, file2):
    """compare two files to see if the content of them are the same, but exclude the date line (e.g  <li>2023-12-01</li>)"""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        for line1,line2 in zip(f1,f2):
            if not line1.startswith('  <li>20') and line1 != line2: #compare all lines except that starting with '  <li>20'
                return False
    return True

def main(html_file='index.html', darkmode=True, rootdir=None):
    """main function to generate the html file"""
    html_file_tmp = html_file + '.tmp'
    #get time stamp
    tformat = '%Y-%m-%d %H:%M:%S'
    time_stamp = datetime.now()
    date = time_stamp.strftime(tformat).split()[0]
    year = time_stamp.strftime(tformat).split('-')[0]
    #get rootdir
    if rootdir is None:
        rootdir = os.getcwd()
    #get webpage files of models
    ifiles = [ifile for ifile in os.listdir(rootdir) if '.by.' in ifile and ifile.endswith('.html')]
    if ifiles: ifiles.sort()
    #seperate model output in workdir from those in archive
    ifiles_archive = [ifile for ifile in ifiles if '_work' not in ifile]
    ifiles_workdir = [ifile for ifile in ifiles if '_work' in ifile]
    ifiles = ifiles_archive + ifiles_workdir
    modelers = list(set( [ifile[:-5].split('.by.')[-1] for ifile in ifiles] ))
    modelers.sort()
    modelers = [f'<span class="badge bg-secondary">{m}</span>' for m in modelers] #to bages
    modelers = ' '.join(modelers)
    #
    #test the permission
    try:
        with open(html_file_tmp, 'w') as f:
            pass
    except PermissionError:
        print('[PermissionError]')
        return
    #start to write to file
    with open(html_file_tmp, 'w') as f: 
        #html head
        name  = ''.join([chr(n) for n in [87, 101, 110, 99, 104, 97, 110, 103, 32, 89, 97, 110, 103]]) + ', \u6768\u6587\u660C'
        html_theme = 'data-bs-theme="dark"' if darkmode else ''
        s = f'''<!doctype html>
<html {html_theme}>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://wy2136.github.io/external/font-awesome-4.7.0/css/font-awesome.min.css">
    <title>numerical experiments on tiger, {name}</title>
    <style>body {{word-break: break-all}}</style>
  </head>
''' 
        f.write(s) #html head

        #body, title section
        s = f'''
<body>
<div class="container my-4">
<div>
<a href="../" class="btn btn-outline-secondary">home</a>
<i class="fa fa-adjust fa-lg" id="btnSwitch"></i>
</div> 
<div class="card card-body border-0">
<h2>numerical experiments on tiger by model</h2>
<div class="text-muted">
  <li>Wenchang Yang</li>
  <li>Princeton University</li>
  <li>{date}</li>
  <p class="mt-3 mb-0"><span class="border rounded p-1">modelers</span>: {modelers}</p>
</div> <!-- text-muted -->
</div> <!-- card -->
'''
        f.write(s) #body starts, title section

        #main content
        n_files = len(ifiles)
        n_files_archive = len(ifiles_archive)
        n_files_workdir = len(ifiles_workdir)
        #experiments in archive
        f.write('\n')
        f.write(f'<h4><span class="mx-3 badge bg-info text-dark">{n_files_archive} groups of experiments in archive</span></h4>\n')
        f.write('<div class="list-group">\n')
        for ii,ifile in enumerate(ifiles_archive, start=1):
            n_exps = len([line for line in open(ifile, 'r') if 'data-bs-target' in line]) # # of experiments for this model
            model, modeler = ifile[:-5].split('.by.')
            f.write(f'<a class=" list-group-item list-group-item-text" href="{ifile}"><span class="badge bg-secondary">{ii:02d}</span> <span class="text-info">{model}</span> <span class="badge bg-secondary mx-2">{modeler}</span> <span class="badge bg-secondary rounded-circle">{n_exps}</span></a>\n')
        f.write('</div> <!-- list-group -->\n')
        #experiments in workdir
        f.write('\n<br>')
        f.write(f'<h4><span class="mx-3 badge bg-warning text-dark">{n_files_workdir} groups of experiments still in workdir</span></h4>\n')
        f.write('<div class="list-group">\n')
        for ii,ifile in enumerate(ifiles_workdir, start=1):
            n_exps = len([line for line in open(ifile, 'r') if 'data-bs-target' in line]) # # of experiments for this model
            model, modeler = ifile[:-5].split('.by.')
            #f.write(f'<a class=" list-group-item list-group-item-text" href="{ifile}"><span class="badge bg-secondary">{ii:02d} of {n_files_workdir:02d}</span> {model} <span class="text-muted">by {modeler}</span></a>\n')
            f.write(f'<a class=" list-group-item list-group-item-text" href="{ifile}"><span class="badge bg-secondary">{ii:02d}</span> <span class="text-warning">{model}</span> <span class="badge bg-secondary mx-2">{modeler}</span> <span class="badge bg-secondary rounded-circle">{n_exps}</span></a></a>\n')
        f.write('</div> <!-- list-group -->\n')
        f.write('\n')
            
            
        #bottom
        name  = ''.join([chr(n) for n in [87, 101, 110, 99, 104, 97, 110, 103, 89, 97, 110, 103]])
        s = f'''
<!-- <p class="text-center text-muted my-4">{name}</p> -->
<p class="text-center mt-4 mb-0 opacity-50"><img width="100px" src="https://avatars.githubusercontent.com/u/8202276"></p>
<div class="text-center text-muted">{intToRoman(int(year))}</div> <!-- text-center -->

</div> <!-- container -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<script>
document.getElementById("btnSwitch").addEventListener("click",()=>{{
    if (document.documentElement.getAttribute("data-bs-theme") == "dark") {{
        document.documentElement.setAttribute("data-bs-theme","light")
    }}
    else {{
        document.documentElement.setAttribute("data-bs-theme","dark")
    }}
}})
</script>
</body>
</html>
'''
        f.write(s) #bottom
    if os.path.exists(html_file):
        #if filecmp.cmp(html_file_tmp, html_file, shallow=False):
        if filecmp_exclude_date(html_file_tmp, html_file):
            os.remove(html_file_tmp)
            print(f'  **NO update to {html_file}**')
        else:
            os.rename(html_file_tmp, html_file)
            print('[updated]:', html_file)
    else:
        os.rename(html_file_tmp, html_file)
        print('[saved]:', html_file)
    print()

if __name__ == '__main__':
    #from misc import get_kws_from_argv
    tformat = '%Y-%m-%d %H:%M:%S'
    t0 = datetime.now()
    print('[start]:', t0.strftime(tformat))

    darkmode = False if 'light' in sys.argv else True
    main(darkmode=darkmode)            
    
    t1 = datetime.now()
    print('[end]:', t1.strftime(tformat))
    print('[total time]:', f'{(t1-t0).seconds:,} seconds')
