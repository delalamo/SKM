#!/usr/bin/env python3
"""
migrate_wikilink_citations.py

Converts remaining mis-formatted citations to [^key] footnote format:

  1. Single-bracket DOI links in notes (broken markup):
       [10.xxxx__yyy|Author Year]  →  [^key]
       plus appends  [^key]: Full citation  at bottom of file

  2. [[DOI|Author Year]] wikilinks in tag-page *Figure from* lines:
       *Figure from [[10.xxxx__yyy|Author Year]]*  →  *Figure from [^key]*
       plus appends footnote definition

  3. *Figure from DOI 10.xxx/yyy*  →  *Figure from [^key]*
     (when [^key] definition is already present in the file)

  4. (Didi et al 2026a) parenthetical stubs → [^didi2026a] + footnote def

Usage:
    python3 scripts/migrate_wikilink_citations.py [--dry-run] [file ...]
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import REPO_ROOT

NOTES_DIR = REPO_ROOT / "content" / "notes"
TAGS_DIR  = REPO_ROOT / "content" / "tags"

FM_RE = re.compile(r'\A---\n.*?\n---\n', re.DOTALL)

# ---------------------------------------------------------------------------
# Complete footnote-definition table  (DOI normalised to lowercase for lookup)
# DOI values here use the canonical form  10.xxxx/yyy  (slash, not __)
# ---------------------------------------------------------------------------
# fmt: off
_DEFS_RAW = {
    '10.1126/science.adq1741':      ('frank2024',        'Frank et al. (2024) "Scalable protein design using optimization in a relaxed sequence space." *Science*. https://doi.org/10.1126/science.adq1741'),
    '10.1101/2023.05.24.542179':    ('baek2023',         'Baek et al. (2023) "Efficient and accurate prediction of protein structure using RoseTTAFold2." https://doi.org/10.1101/2023.05.24.542179'),
    '10.48550/arxiv.2206.06583':    ('hu2022',           'Hu et al. (2022) "Exploring evolution-aware & -free protein language models as protein function predictors." https://doi.org/10.48550/arXiv.2206.06583'),
    '10.1016/j.cels.2025.101387':   ('li2024c',          'Li et al. (2025) "Evaluation of machine learning-assisted directed evolution across diverse combinatorial landscapes." *Cell Systems*. https://doi.org/10.1016/j.cels.2025.101387'),
    '10.48550/arxiv.2507.11839':    ('gong2025',         'Gong et al. (2025) "Protenix-Mini: Efficient Structure Predictor via Compact Architecture, Few-Step Diffusion and Switchable pLM." https://doi.org/10.48550/ARXIV.2507.11839'),
    '10.48550/arxiv.2312.00080':    ('wang2023',         'Wang et al. (2023) "PDB-Struct: A Comprehensive Benchmark for Structure-based Protein Design." https://doi.org/10.48550/arXiv.2312.00080'),
    '10.1101/2023.05.22.541652':    ('heo2023',          'Heo & Feig (2023) "One particle per residue is sufficient to describe all-atom protein structures." https://doi.org/10.1101/2023.05.22.541652'),
    '10.48550/arxiv.2210.01776':    ('corso2023',        'Corso et al. (2022) "DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking." https://doi.org/10.48550/arXiv.2210.01776'),
    '10.1101/2022.11.20.517210':    ('ahdritz2024',      'Ahdritz et al. (2022) "OpenFold: Retraining AlphaFold2 yields new insights into its learning mechanisms and capacity for generalization." https://doi.org/10.1101/2022.11.20.517210'),
    '10.1101/2023.12.20.572683':    ('matthews2023',     'Matthews et al. (2023) "Leveraging ancestral sequence reconstruction for protein representation learning." https://doi.org/10.1101/2023.12.20.572683'),
    '10.1101/2024.10.23.619915':    ('muir2024',         'Muir et al. (2024) "Evolutionary-Scale Enzymology Enables Biochemical Constant Prediction Across a Multi-Peaked Catalytic Landscape." https://doi.org/10.1101/2024.10.23.619915'),
    '10.48550/arxiv.2411.12957':    ('sandhu2024',       'Sandhu et al. (2024) "Computational and Experimental Exploration of Protein Fitness Landscapes: Navigating Smooth and Rugged Terrains." https://doi.org/10.48550/ARXIV.2411.12957'),
    '10.1038/s41586-021-03819-2':   ('jumper2021',       'Jumper et al. (2021) "Highly accurate protein structure prediction with AlphaFold." *Nature*. https://doi.org/10.1038/s41586-021-03819-2'),
    '10.1101/2023.10.06.561180':    ('topolska2023',     'Topolska et al. (2023) "Deep indel mutagenesis reveals the impact of amino acid insertions and deletions on protein stability and function." https://doi.org/10.1101/2023.10.06.561180'),
    '10.1126/science.add2187':      ('dauparas2022',     'Dauparas et al. (2022) "Robust deep learning\u2013based protein sequence design using ProteinMPNN." *Science*. https://doi.org/10.1126/science.add2187'),
    '10.1021/acs.jcim.4c00036':     ('zhou2024',         'Zhou et al. (2024) "Protein Engineering with Lightweight Graph Denoising Neural Networks." *Journal of Chemical Information and Modeling*. https://doi.org/10.1021/acs.jcim.4c00036'),
    '10.1016/j.cels.2022.01.003':   ('hie2022',          'Hie et al. (2022) "Evolutionary velocity with protein language models predicts evolutionary dynamics of diverse proteins." *Cell Systems*. https://doi.org/10.1016/j.cels.2022.01.003'),
    '10.1002/pro.5216':             ('nikolaev2024',     'Nikolaev et al. (2024) "Re\u2010engineering of a carotenoid\u2010binding protein based on NMR structure." *Protein Science*. https://doi.org/10.1002/pro.5216'),
    # Titles found via web search
    '10.1038/s41586-021-04043-8':   ('frazer2021',       'Frazer et al. (2021) "Disease variant prediction with deep generative models of evolutionary data." *Nature*. https://doi.org/10.1038/s41586-021-04043-8'),
    '10.48550/arxiv.2205.13760':    ('notin2022b',       'Notin et al. (2022) "Tranception: Protein Fitness Prediction with Autoregressive Transformers and Inference-Time Retrieval." https://doi.org/10.48550/arXiv.2205.13760'),
    '10.1126/science.abn2100':      ('wang2022',         'Wang et al. (2022) "Scaffolding protein functional sites using deep learning." *Science*. https://doi.org/10.1126/science.abn2100'),
    '10.48550/arxiv.2404.02258':    ('raposo2024',       'Raposo et al. (2024) "Mixture-of-Depths: Dynamically Allocating Compute in Transformers." https://doi.org/10.48550/arXiv.2404.02258'),
    '10.1038/s42003-023-04773-7':   ('mccafferty2023',   'McCafferty et al. (2023) "Does AlphaFold2 model proteins\u2019 intracellular conformations? An experimental test using cross-linking mass spectrometry of endogenous ciliary proteins." *Communications Biology*. https://doi.org/10.1038/s42003-023-04773-7'),
    '10.1126/sciadv.adr2641':       ('jiang2024b',       'Jiang et al. (2024) "A general temperature-guided language model to design proteins of enhanced stability and activity." *Science Advances*. https://doi.org/10.1126/sciadv.adr2641'),
    '10.7554/elife.89386.1':        ('karelina2023',     'Karelina et al. (2023) "How accurately can one predict drug binding modes using AlphaFold models?" *eLife*. https://doi.org/10.7554/elife.89386.1'),
    '10.1002/pro.4653':             ('goverde2023',      'Goverde et al. (2023) "De novo protein design by inversion of the AlphaFold structure prediction network." *Protein Science*. https://doi.org/10.1002/pro.4653'),
    '10.1101/2023.05.05.539648':    ('mukhopadhyay2023', 'Mukhopadhyay et al. (2023) "ZymePackNet: rotamer-sampling free graph neural network method for protein sidechain prediction." https://doi.org/10.1101/2023.05.05.539648'),
    '10.1101/2023.06.02.543382':    ('ueki2023',         'Ueki & Ohue (2023) "Antibody Complementarity-Determining Region Sequence Design using AlphaFold2 and Binding Affinity Prediction Model." https://doi.org/10.1101/2023.06.02.543382'),
    '10.1101/2023.08.11.553028':    ('gamouh2023',       'Gamouh et al. (2023) "Hybrid protein-ligand binding residue prediction with protein language models: Does the structure matter?" https://doi.org/10.1101/2023.08.11.553028'),
    '10.1101/2023.09.18.558189':    ('kliche2023',       'Kliche et al. (2023) "Proteome-scale characterisation of motif-based interactome rewiring by disease mutations." https://doi.org/10.1101/2023.09.18.558189'),
    '10.1021/acs.jcim.3c01976':     ('gu2024',           'Gu et al. (2024) "Evaluation of AlphaFold2 Structures for Hit Identification across Multiple Scenarios." *Journal of Chemical Information and Modeling*. https://doi.org/10.1021/acs.jcim.3c01976'),
    '10.1021/acs.jcim.4c00049':     ('landrum2024',      'Landrum & Riniker (2024) "Combining IC50 or Ki Values from Different Sources Is a Source of Significant Noise." *Journal of Chemical Information and Modeling*. https://doi.org/10.1021/acs.jcim.4c00049'),
    '10.1126/science.adn6354':      ('lyu2024',          'Lyu et al. (2024) "AlphaFold2 structures guide prospective ligand discovery." *Science*. https://doi.org/10.1126/science.adn6354'),
    '10.1016/j.tibs.2022.09.005':   ('aung2023',         'Aung et al. (2023) "Recent and Future Perspectives on Engineering Interferons and other Cytokines as Therapeutics." *Trends in Biochemical Sciences*. https://doi.org/10.1016/j.tibs.2022.09.005'),
    '10.1371/journal.pcbi.1011288': ('chari2023',        'Chari & Pachter (2023) "The specious art of single-cell genomics." *PLOS Computational Biology*. https://doi.org/10.1371/journal.pcbi.1011288'),
    '10.1038/s41589-023-01389-0':   ('guo2023',          'Guo et al. (2023) "A method for structure determination of GPCRs in various states." *Nature Chemical Biology*. https://doi.org/10.1038/s41589-023-01389-0'),
    '10.64898/2025.12.17.693105':   ('ohnuki2025',       'Ohnuki & Okazaki (2025) "Enhanced sampling of protein conformations in AlphaFold3 with repulsive bias in the diffusion generative model." https://doi.org/10.64898/2025.12.17.693105'),
    '10.64898/2026.02.10.704873':   ('lam2026',          'Lam et al. (2026) "Metadiffusion: inference-time meta-energy biasing of biomolecular diffusion models." https://doi.org/10.64898/2026.02.10.704873'),
    '10.64898/2026.03.02.709004':   ('smorodina2026',    'Smorodina et al. (2026) "Structural Plausibility Without Binding Specificity: Limits of AI-Based Antibody-Antigen Structure Prediction Confidence Scores." https://doi.org/10.64898/2026.03.02.709004'),
    '10.48550/arxiv.2603.27950':    ('didi2026a',        'Didi et al. (2026) "Proteina-Complexa: Scaling Atomistic Protein Binder Design with Generative Pretraining and Test-Time Compute." https://doi.org/10.48550/arXiv.2603.27950'),
    # Tag-page figure-caption entries (from second pass)
    '10.1038/nature17995':          ('sarkisyan2016',    'Sarkisyan et al. (2016) "Local fitness landscape of the green fluorescent protein." *Nature*. https://doi.org/10.1038/nature17995'),
    '10.1038/s41551-023-01079-1':   ('tennenhouse2023',  'Tennenhouse et al. (2023) "Computational optimization of antibody humanness and stability by systematic energy-based ranking." *Nature Biomedical Engineering*. https://doi.org/10.1038/s41551-023-01079-1'),
    '10.1038/s41586-023-06328-6':   ('tsuboyama2023',    'Tsuboyama et al. (2023) "Mega-scale experimental analysis of protein folding stability in biology and design." *Nature*. https://doi.org/10.1038/s41586-023-06328-6'),
    '10.1038/s42003-023-05241-y':   ('bahrami2023',      'Bahrami Dizicheh et al. (2023) "VHH CDR-H3 conformation is determined by VH germline usage." *Communications Biology*. https://doi.org/10.1038/s42003-023-05241-y'),
    '10.1101/2021.02.12.430858':    ('rao2021',          'Rao et al. (2021) "MSA Transformer." https://doi.org/10.1101/2021.02.12.430858'),
    '10.1101/2022.04.10.487779':    ('hsu2022',          'Hsu et al. (2022) "Learning inverse folding from millions of predicted structures." https://doi.org/10.1101/2022.04.10.487779'),
    '10.1101/2023.04.26.538476':    ('singh2023',        'Singh et al. (2023) "Learning the Language of Antibody Hypervariability." https://doi.org/10.1101/2023.04.26.538476'),
    '10.1101/2023.10.01.560349':    ('su2023',           'Su et al. (2023) "SaProt: Protein Language Modeling with Structure-aware Vocabulary." https://doi.org/10.1101/2023.10.01.560349'),
    '10.1101/2024.09.21.614257':    ('hitawala2024',     'Hitawala & Gray (2024) "What does AlphaFold3 learn about antigen and nanobody docking, and what remains unsolved?." https://doi.org/10.1101/2024.09.21.614257'),
    '10.1126/science.abd8700':      ('dishman2021',      'Dishman et al. (2021) "Evolution of fold switching in a metamorphic protein." *Science*. https://doi.org/10.1126/science.abd8700'),
    '10.1126/science.adc9498':      ('shrock2023',       'Shrock et al. (2023) "Germline-encoded amino acid-binding motifs drive immunodominant public antibody responses." *Science*. https://doi.org/10.1126/science.adc9498'),
    '10.1126/science.adg7492':      ('cheng2023',        'Cheng et al. (2023) "Accurate proteome-wide missense variant effect prediction with AlphaMissense." *Science*. https://doi.org/10.1126/science.adg7492'),
    '10.48550/arxiv.2008.11687':    ('neyshabur2020',    'Neyshabur et al. (2020) "What is being transferred in transfer learning?." *arXiv*. https://doi.org/10.48550/ARXIV.2008.11687'),
    '10.1002/adtp.202100035':       ('pires2021',        'Pires et al. (2021) "Engineering Strategies for Immunomodulatory Cytokine Therapies: Challenges and Clinical Progress." *Advanced Therapeutics*. https://doi.org/10.1002/adtp.202100035'),
    '10.1016/j.bpj.2017.08.039':   ('tian2017',         'Tian & Best (2017) "How Many Protein Sequences Fold to a Given Structure? A Coevolutionary Analysis." *Biophysical Journal*. https://doi.org/10.1016/j.bpj.2017.08.039'),
    '10.1016/j.str.2014.11.010':    ('weitzner2015',     'Weitzner et al. (2015) "The Origin of CDR H3 Structural Diversity." *Structure*. https://doi.org/10.1016/j.str.2014.11.010'),
    '10.1021/acssynbio.3c00674':    ('hansen2024',       'Hansen et al. (2024) "Carving out a Glycoside Hydrolase Active Site for Incorporation into a New Protein Scaffold Using Deep Network Hallucination." *ACS Synthetic Biology*. https://doi.org/10.1021/acssynbio.3c00674'),
    '10.1021/jacs.7b12191':         ('husic2018',        'Husic & Pande (2018) "Markov State Models: From an Art to a Science." *Journal of the American Chemical Society*. https://doi.org/10.1021/jacs.7b12191'),
    '10.1038/246096a0':             ('ohta1973',         'Ohta (1973) "Slightly Deleterious Mutant Substitutions in Evolution." *Nature*. https://doi.org/10.1038/246096a0'),
    '10.1038/s41573-024-00896-6':   ('klein2024',        'Klein et al. (2024) "The present and future of bispecific antibodies for cancer therapy." *Nature Reviews Drug Discovery*. https://doi.org/10.1038/s41573-024-00896-6'),
    '10.1038/s41592-023-02087-4':   ('terwilliger2023',  'Terwilliger et al. (2023) "AlphaFold predictions are valuable hypotheses and accelerate but do not replace experimental structure determination." *Nature Methods*. https://doi.org/10.1038/s41592-023-02087-4'),
    '10.1038/s41594-022-00910-8':   ('burke2023',        'Burke et al. (2023) "Towards a structurally resolved human protein interaction network." *Nature Structural & Molecular Biology*. https://doi.org/10.1038/s41594-022-00910-8'),
    '10.1042/etls20200331':         ('chan2021',          'Chan et al. (2021) "Affinity maturation: highlights in the application of in vitro strategies for the directed evolution of antibodies." *Emerging Topics in Life Sciences*. https://doi.org/10.1042/ETLS20200331'),
    '10.1073/pnas.2311887121':      ('lupo2024',         'Lupo et al. (2024) "Pairing interacting protein sequences using masked language modeling." *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.2311887121'),
    '10.1093/bib/bbae602':          ('postovskaya2024',  'Postovskaya et al. (2024) "tcrBLOSUM: an amino acid substitution matrix for sensitive alignment of distant epitope-specific TCRs." *Briefings in Bioinformatics*. https://doi.org/10.1093/bib/bbae602'),
    '10.1101/2024.06.23.600144':    ('johnston2024',     'Johnston et al. (2024) "A combinatorially complete epistatic fitness landscape in an enzyme active site." https://doi.org/10.1101/2024.06.23.600144'),
    '10.1101/2024.10.27.620454':    ('furui2024',        'Furui & Ohue (2024) "Benchmarking HelixFold3-Predicted Holo Structures for Relative Free Energy Perturbation Calculations." https://doi.org/10.1101/2024.10.27.620454'),
    '10.1126/science.abd3623':      ('otten2020',        'Otten et al. (2020) "How directed evolution reshapes the energy landscape in an enzyme to boost catalysis." *Science*. https://doi.org/10.1126/science.abd3623'),
    '10.3390/antib8040055':         ('chiu2019',         'Chiu et al. (2019) "Antibody structure and function: The basis for engineering therapeutics." *Antibodies*. https://doi.org/10.3390/antib8040055'),
    '10.48550/arxiv.2212.04089':    ('ilharco2022',      'Ilharco et al. (2022) "Editing Models with Task Arithmetic." https://doi.org/10.48550/arxiv.2212.04089'),
    '10.48550/arxiv.2306.05445':    ('zheng2023',        'Zheng et al. (2023) "Towards Predicting Equilibrium Distributions for Molecular Systems with Deep Learning." https://doi.org/10.48550/arxiv.2306.05445'),
    '10.64898/2025.12.12.694033':   ('chow2025',         'Chow et al. (2025) "Sequence and structural determinants of efficacious de novo chimeric antigen receptors." https://doi.org/10.64898/2025.12.12.694033'),
}
# fmt: on

# Normalise keys to lowercase for case-insensitive lookup
DEFS = {k.lower(): v for k, v in _DEFS_RAW.items()}


def doi_from_link(link_doi: str) -> str:
    """Convert 10.xxxx__yyy (vault encoding) to 10.xxxx/yyy.

    The vault encodes every '/' in a DOI as '__'.  Some DOIs have more than
    one slash (e.g. 10.1093/bib/bbae602 → 10.1093__bib__bbae602), so we must
    replace ALL occurrences, not just the first.
    """
    return link_doi.replace('__', '/')


def lookup(link_doi: str):
    """Return (key, footnote_definition_line) or None."""
    canonical = doi_from_link(link_doi).lower()
    return DEFS.get(canonical)


# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

# Matches [10.xxx__yyy|Author Year] (single bracket, broken markup in notes)
SINGLE_RE = re.compile(
    r'\[('
    r'10\.[^\]|]+?'
    r')\|'
    r'([^\]]+?)'
    r'\]'
    r'(?!\])'   # not followed by ] (would be [[...]])
)

# Matches [[10.xxx__yyy|Author Year]] (Obsidian wikilink in tag pages)
DOUBLE_RE = re.compile(
    r'\[\[('
    r'10\.[^\]|]+'
    r')\|'
    r'([^\]]+)'
    r'\]\]'
)

# *Figure/Table from DOI 10.xxx/yyy*  (bare-DOI variant)
BARE_DOI_FIG_RE = re.compile(
    r'(\*(?:Figure|Table)[^*]*?from\s+DOI\s+)(10\.[^\s*]+)(\*)',
    re.IGNORECASE,
)

# (Didi et al 2026a)  parenthetical stub
DIDI_STUB_RE = re.compile(r'\(Didi et al 2026a\)')

# Footnote definition line
FN_DEF_RE = re.compile(r'^\[\^(\w+)\]:', re.MULTILINE)


def _footnote_line(key: str, defn: str) -> str:
    return f'[^{key}]: {defn}'


def _already_defined(text: str, key: str) -> bool:
    return bool(re.search(rf'^\[\^{re.escape(key)}\]:', text, re.MULTILINE))


# ---------------------------------------------------------------------------
# Core per-file processing
# ---------------------------------------------------------------------------

def process_notes_file(path: Path, dry_run: bool) -> bool:
    """Fix [DOI|Author Year] single-bracket citations in a notes file."""
    original = path.read_text('utf-8')

    m = FM_RE.match(original)
    fm, body = (original[:m.end()], original[m.end()]) if m else ('', original)
    # Actually need full body after fm
    fm = original[:m.end()] if m else ''
    body = original[m.end():] if m else original

    new_body = body
    new_defs: dict[str, str] = {}   # key -> def line (to append once)

    # --- Pass 1: single-bracket [DOI|Author Year] ---
    def replace_single(match):
        link_doi, author_year = match.group(1), match.group(2)
        result = lookup(link_doi)
        if result is None:
            return match.group(0)   # unknown DOI: leave unchanged
        key, defn = result
        new_defs[key] = _footnote_line(key, defn)
        return f'[^{key}]'

    new_body = SINGLE_RE.sub(replace_single, new_body)

    # --- Pass 2: bare "Figure from DOI 10.xxx/yyy" ---
    def replace_bare_doi(match):
        prefix, raw_doi, suffix = match.group(1), match.group(2), match.group(3)
        # raw_doi is already slash-separated; normalise for lookup
        canonical = raw_doi.lower()
        result = DEFS.get(canonical)
        if result is None:
            # Also try looking up via the file's existing [^key]: definition
            fn_def_m = re.search(
                rf'\[\^(\w+)\]:.*https://doi\.org/{re.escape(raw_doi)}',
                new_body, re.IGNORECASE,
            )
            if fn_def_m:
                key = fn_def_m.group(1)
                return f'{prefix}[^{key}]{suffix}'
            return match.group(0)
        key, defn = result
        new_defs[key] = _footnote_line(key, defn)
        return f'{prefix}[^{key}]{suffix}'

    new_body = BARE_DOI_FIG_RE.sub(replace_bare_doi, new_body)

    # --- Pass 3: (Didi et al 2026a) stub ---
    didi_result = DEFS.get('10.48550/arxiv.2603.27950')
    if didi_result and DIDI_STUB_RE.search(new_body):
        key, defn = didi_result
        new_body = DIDI_STUB_RE.sub(f'[^{key}]', new_body)
        new_defs[key] = _footnote_line(key, defn)

    # --- Append missing footnote definitions ---
    defs_to_add = [
        line for key, line in sorted(new_defs.items())
        if not _already_defined(new_body, key)
    ]
    if defs_to_add:
        # Ensure a blank line before first definition
        if not new_body.endswith('\n\n'):
            new_body = new_body.rstrip('\n') + '\n\n'
        new_body += '\n'.join(defs_to_add) + '\n'

    updated = fm + new_body
    if updated == original:
        return False
    if not dry_run:
        path.write_text(updated, 'utf-8')
    return True


def process_tag_file(path: Path, dry_run: bool) -> bool:
    """Fix [[DOI|Author Year]] wikilinks in tag-page *Figure from* lines only."""
    original = path.read_text('utf-8')

    m = FM_RE.match(original)
    fm = original[:m.end()] if m else ''
    body = original[m.end():] if m else original

    new_lines = []
    new_defs: dict[str, str] = {}
    changed = False

    for line in body.splitlines(keepends=True):
        # Only touch lines that look like figure/table captions
        stripped = line.strip()
        if stripped.startswith('*') and re.search(
            r'\*\s*(?:Figure|Table|Image)\b', stripped, re.IGNORECASE
        ):
            def replace_double(match):
                link_doi, author_year = match.group(1), match.group(2)
                result = lookup(link_doi)
                if result is None:
                    return match.group(0)
                key, defn = result
                new_defs[key] = _footnote_line(key, defn)
                return f'[^{key}]'

            new_line = DOUBLE_RE.sub(replace_double, line)
            if new_line != line:
                changed = True
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    if not changed and not new_defs:
        return False

    new_body = ''.join(new_lines)

    defs_to_add = [
        line for key, line in sorted(new_defs.items())
        if not _already_defined(new_body, key)
    ]
    if defs_to_add:
        if not new_body.endswith('\n\n'):
            new_body = new_body.rstrip('\n') + '\n\n'
        new_body += '\n'.join(defs_to_add) + '\n'

    updated = fm + new_body
    if updated == original:
        return False
    if not dry_run:
        path.write_text(updated, 'utf-8')
    return True


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args     = sys.argv[1:]
    dry_run  = '--dry-run' in args
    file_args = [a for a in args if not a.startswith('--')]

    if file_args:
        targets = [Path(p) for p in file_args]
    else:
        targets = (
            sorted(NOTES_DIR.glob('*.md'))
            + sorted(TAGS_DIR.glob('*.md'))
        )

    if dry_run:
        print('DRY RUN — no files will be modified\n')

    modified = 0
    for path in targets:
        if path.parent.name == 'notes':
            changed = process_notes_file(path, dry_run)
        elif path.parent.name == 'tags':
            changed = process_tag_file(path, dry_run)
        else:
            changed = process_notes_file(path, dry_run)

        if changed:
            modified += 1
            print(f'  ✓  {path.name}')

    print(f'\n{"Would modify" if dry_run else "Modified"} {modified}/{len(targets)} file(s).')


if __name__ == '__main__':
    main()
