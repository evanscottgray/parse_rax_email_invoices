#!/usr/bin/env python
import re
import sys
import json


def get_stdin():
    stdin_lines = []
    for line in sys.stdin:
        stdin_lines.append(line)
    return ''.join(stdin_lines)


def get_domains(text):
    # NOTE(evanscottgray) YES I KNOW THAT THIS IS NOT PEP8
    rgx = re.compile(r'(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|([a-zA-Z0-9][a-zA-Z0-9-_]{1,61}[a-zA-Z0-9]))\.([a-zA-Z]{2,6}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})')
    raw_domains = rgx.findall(text)
    domains = ['.'.join(d[-2:]) for d in raw_domains]
    return set(domains)


def read_invoice(filename='inv.txt'):
    with open(filename, 'r') as f:
        d = f.read()
    return d


def dom_cost(txt, dom):
    c = [float(l.split()[-1].strip('$'))
         for l in txt.splitlines() if len(l.split()) > 4 and dom in l.split()]
    return sum(c)


def calculate_totals(doms, txt):
    t = {d: dom_cost(txt, d) for d in doms}
    return t

text = get_stdin()
domains = get_domains(text)
totals = calculate_totals(list(domains), text)

print json.dumps(totals)
