#!/usr/bin/env python3
"""Generate and validate the numbered examples in the Antibody numbering note.

Default: validate the frozen CSV and regenerate Markdown, without dependencies/network.
To recompute labels: install anarcii==2.0.8 in an isolated environment and download
https://raw.githubusercontent.com/oxpig/ANARCI/79f6c575056dedef86cb8f405ebb039197923eec/lib/python/anarci/schemes.py
then run with --renumber --anarci-schemes /path/to/schemes.py. Its hash is checked
before import. ANARCII supplies IMGT/Kabat/Chothia/Martin/AHo; the pinned author
implementation supplies WolfGuy from the SAME IMGT alignment. No HMM run is implied.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'content/assets'
NOTE = ROOT / 'content/notes/Antibody numbering.md'
INPUTS = ASSETS / 'antibody-numbering-inputs.json'
OUTPUT = ASSETS / 'antibody-numbering-crosswalk.csv'
SCHEMES = ['imgt', 'kabat', 'chothia', 'martin', 'aho', 'wolfguy']
FIELDS = ['example', 'sequence_position', 'aa', *SCHEMES, 'imgt_region', 'feature']
REGIONS = [(26, 'FR1'), (38, 'CDR1'), (55, 'FR2'), (65, 'CDR2'),
           (104, 'FR3'), (117, 'CDR3'), (128, 'FR4')]
FEATURES = {23: 'Cys; B strand / disulfide', 41: 'Trp; C strand / core',
            80: 'H2-supporting H71 site (VH only)', 89: 'Hydrophobic; E strand / core',
            104: 'Cys; F strand / disulfide', 118: 'Phe/Trp; G strand / J motif',
            119: 'Gly; J motif', 121: 'Gly; J motif'}


def label(position, scheme, chain_type):
    number, insertion = position
    insertion = insertion.strip()
    if scheme == 'imgt' and insertion:
        # Examples currently have no IMGT insertion codes; fail on unsupported format.
        assert len(insertion) == 1 and insertion.isalpha()
        insertion = '.' + str(ord(insertion.upper()) - ord('A') + 1)
    prefix = ('H' if chain_type == 'H' else 'L') if scheme in ('kabat', 'chothia', 'martin') else ''
    return f'{prefix}{number}{insertion}'


def rows_from_results(meta, results):
    rows = []
    for example in meta['examples']:
        name = example['id']
        base = results['imgt'][name]
        assert base['error'] is None and base['chain_type'] == example['chain_type']
        start, end = base['query_start'], base['query_end']
        sequence = example['sequence'][start:end + 1]
        numbered = {}
        for scheme in SCHEMES:
            result = results[scheme][name]
            assert result['error'] is None
            occupied = [(p, a) for p, a in result['numbering'] if a != '-']
            assert ''.join(a for _, a in occupied) == sequence, (name, scheme, 'sequence changed')
            labels = [label(p, scheme, example['chain_type']) for p, _ in occupied]
            assert len(set(labels)) == len(labels), (name, scheme, 'duplicate label')
            numbered[scheme] = labels
        for index, aa in enumerate(sequence):
            imgt = numbered['imgt'][index]
            number = int(imgt.split('.')[0])
            region = next(region for last, region in REGIONS if number <= last)
            feature = FEATURES.get(number, '')
            if number == 80 and example['chain_type'] != 'H':
                feature = ''
            rows.append(dict(example=name, sequence_position=start + index + 1, aa=aa,
                             **{s: numbered[s][index] for s in SCHEMES},
                             imgt_region=region, feature=feature))
    return rows


def renumber(meta, module_path):
    import anarcii
    assert anarcii.__version__ == meta['anarcii_version']
    assert module_path is not None, '--anarci-schemes is required for WolfGuy'
    assert hashlib.sha256(module_path.read_bytes()).hexdigest() == meta['anarci_schemes_sha256']
    spec = importlib.util.spec_from_file_location('author_schemes', module_path)
    author_schemes = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(author_schemes)
    model = anarcii.Anarcii(seq_type='antibody', mode='accuracy', cpu=True, ncpu=2)
    seqs = {e['id']: e['sequence'] for e in meta['examples']}
    results = {'imgt': model.number(seqs)}
    for scheme in ('kabat', 'chothia', 'martin', 'aho'):
        results[scheme] = model.to_scheme(scheme)
    results['wolfguy'] = {}
    for name, entry in results['imgt'].items():
        index = entry['query_start']
        states = []
        for (number, insertion), aa in entry['numbering']:
            state = 'd' if aa == '-' else ('i' if insertion.strip() else 'm')
            states.append(((number, state), None if aa == '-' else index))
            index += aa != '-'
        fn = author_schemes.number_wolfguy_heavy if entry['chain_type'] == 'H' else author_schemes.number_wolfguy_light
        numbering, start, end = fn(states, seqs[name])
        assert (start, end) == (entry['query_start'], entry['query_end'])
        results['wolfguy'][name] = {**entry, 'numbering': numbering, 'scheme': 'wolfguy'}
    return rows_from_results(meta, results)


def validate(meta, rows):
    expected_types = {'1N8Z_2': 'H', '1MJU_1': 'K', '5GRJ_2': 'L'}
    for e in meta['examples']:
        rs = [r for r in rows if r['example'] == e['id']]
        assert rs and e['chain_type'] == expected_types[e['id']]
        indices = [int(r['sequence_position']) for r in rs]
        assert indices == list(range(indices[0], indices[-1] + 1))
        assert ''.join(r['aa'] for r in rs) == e['sequence'][indices[0] - 1:indices[-1]]
        for scheme in SCHEMES:
            assert len({r[scheme] for r in rs}) == len(rs)
        anchors = {r['imgt']: r for r in rs}
        heavy = e['chain_type'] == 'H'
        for i, aa, aho, h, l in [('23', 'C', '23', 'H22', 'L23'),
                                ('41', 'W', '43', 'H36', 'L35'),
                                ('104', 'C', '106', 'H92', 'L88'),
                                ('118', 'W' if heavy else 'F', '139', 'H103', 'L98'),
                                ('119', 'G', '140', 'H104', 'L99'),
                                ('121', 'G', '142', 'H106', 'L101')]:
            r = anchors[i]
            assert r['aa'] == aa and r['aho'] == aho, (e['id'], i)
            for scheme in ('kabat', 'chothia', 'martin'):
                assert r[scheme] == (h if heavy else l), (e['id'], scheme, i)
        assert anchors['89']['kabat'] == ('H80' if heavy else 'L73')
        assert anchors['89']['martin'] == ('H77' if heavy else 'L73')
        assert anchors['89']['aho'] == '91'
        if heavy:
            assert anchors['80']['kabat'] == 'H71' and anchors['80']['aho'] == '82'
            for i, k in [('42', 'H37'), ('49', 'H44'), ('50', 'H45'), ('52', 'H47')]:
                assert anchors[i]['kabat'] == k
    const = list(csv.DictReader((ASSETS / 'antibody-numbering-igg1-eu-imgt.csv').open()))
    assert [int(r['eu_position']) for r in const] == list(range(118, 448))
    glycan = next(r for r in const if r['eu_position'] == '297')
    assert (glycan['domain'], glycan['imgt_position'], glycan['aa']) == ('CH2', '84.4', 'N')
    for domain, cys1, trp, cys2 in [('CH1', '144', '158', '200'), ('CH2', '261', '277', '321'), ('CH3', '367', '381', '425')]:
        for imgt, eu, aa in [('23', cys1, 'C'), ('41', trp, 'W'), ('104', cys2, 'C')]:
            r = next(r for r in const if r['domain'] == domain and r['imgt_position'] == imgt)
            assert (r['eu_position'], r['aa']) == (eu, aa)


def render(meta, rows):
    chunks = []
    for e in meta['examples']:
        rs = [r for r in rows if r['example'] == e['id']]
        lengths = [sum(r['imgt_region'] == f'CDR{i}' for r in rs) for i in (1, 2, 3)]
        chunks += [f"<details>\n<summary>{e['label']}: {len(rs)} residues; IMGT CDR lengths {'.'.join(map(str, lengths))}</summary>\n",
                   f"\n[PDB {e['pdb']}](https://www.rcsb.org/structure/{e['pdb']}), author chain **{e['author_chain']}**, entity **{e['entity_id']}**. Sequence position counts from the beginning of the deposited sequence; it is not a PDB residue label.\n",
                   '\n| Seq. | AA | IMGT | Kabat | Chothia | Martin | AHo | WolfGuy | Region / landmark |',
                   '| --- | --- | --- | --- | --- | --- | --- | --- | --- |']
        for r in rs:
            feature = r['imgt_region'] + ('; ' + r['feature'] if r['feature'] else '')
            chunks.append('| ' + ' | '.join([str(r['sequence_position']), r['aa'], *[r[s] for s in SCHEMES], feature]) + ' |')
        chunks.append('\n</details>\n')
    block = '\n'.join(chunks)
    text = NOTE.read_text()
    pattern = r'<!-- BEGIN GENERATED CROSSWALK -->.*?<!-- END GENERATED CROSSWALK -->'
    assert re.search(pattern, text, re.S), 'Missing generated-block markers'
    text = re.sub(pattern, '<!-- BEGIN GENERATED CROSSWALK -->\n\n' + block + '\n<!-- END GENERATED CROSSWALK -->', text, flags=re.S)
    NOTE.write_text(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--renumber', action='store_true')
    parser.add_argument('--anarci-schemes', type=Path)
    args = parser.parse_args()
    meta = json.loads(INPUTS.read_text())
    if args.renumber:
        rows = renumber(meta, args.anarci_schemes)
        validate(meta, rows)
        with OUTPUT.open('w', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
    else:
        rows = list(csv.DictReader(OUTPUT.open()))
        validate(meta, rows)
    render(meta, rows)
    print(f'Validated and rendered {len(rows)} variable-domain residue mappings plus 330 constant-region mappings.')


if __name__ == '__main__':
    main()
