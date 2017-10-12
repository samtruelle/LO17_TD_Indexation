Get archive on http://www4.utc.fr/~lo17/TELECHARGE/
Install Conda https://conda.io/miniconda.html
```
conda env create -f environment.yml
source activate LO17
python /home/tdancois/PycharmProjects/LO17_TD_Indexation/main_parser.py
```
List of useful commands for indexation:
```
LANG=C
python make_stop_list.py | grep -v texte | perl perl_scripts/newcreeFiltre.pl > /tmp/filtre.pl
perl /tmp/filtre.pl corpus_P17_ss_balise.xml > corpus_P17_ss_balise_filtre.xml

perl perl_scripts/segmente_TT.pl corpus_P17_ss_balise_filtre.xml | sort | uniq | perl perl_scripts/successeurs_P16.pl > /tmp/successeurs.txt
perl perl_scripts/filtronc_P16.pl -v /tmp/successeurs.txt /tmp/successeurs2.txt

cat corpus_P17_ss_balise_filtre.xml | perl perl_scripts/index.pl titre
perl perl_scripts/segmente_TT.pl -f -r -n corpus_P17_ss_balise_filtre.xml | perl perl_scripts/indexTexte.pl
```

# Compile report
Get Latex compiler;
Compite:
```bash
pdflatex -output-directory /tmp/lo17 rapport/rapport.tex
```
(be sure to not push intermediate latex files)