#!/usr/bin/env python3
"""Extract every ```mermaid block from the given .md files and render each with
mmdc to catch syntax errors. Prints OK/FAIL per block. Exit 1 if any fail."""
import sys, re, subprocess, tempfile, os
fail=0; total=0
for path in sys.argv[1:]:
    s=open(path,encoding='utf-8').read().replace('⁦','').replace('⁩','')
    blocks=re.findall(r'```mermaid\n(.*?)```', s, re.S)
    for k,b in enumerate(blocks,1):
        total+=1
        with tempfile.NamedTemporaryFile('w',suffix='.mmd',delete=False,encoding='utf-8') as f:
            f.write(b); src=f.name
        out=src+'.svg'
        r=subprocess.run(['mmdc','-i',src,'-o',out,'-q','-p','_build/puppeteer.json'],capture_output=True,text=True)
        ok = r.returncode==0 and os.path.exists(out)
        if not ok:
            fail+=1
            print(f"FAIL {path} block#{k}")
            print((r.stderr or r.stdout).strip().splitlines()[-3:] if (r.stderr or r.stdout) else '')
        else:
            print(f"ok   {path} block#{k}")
        for fp in (src,out):
            try: os.remove(fp)
            except OSError: pass
print(f"\n{total-fail}/{total} diagrams render cleanly")
sys.exit(1 if fail else 0)
