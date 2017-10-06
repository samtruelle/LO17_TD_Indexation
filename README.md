Get archive on http://www4.utc.fr/~lo17/TELECHARGE/
Install Conda https://conda.io/miniconda.html
```
conda env create -f environment.yml
source activate LO17
python /home/tdancois/PycharmProjects/LO17_TD_Indexation/main_parser.py
```
List of useful commands:
```
perl segmente_TT.pl corpus_P17_ss_balise.xml | sort | uniq | perl successeurs_P16.pl > /tmp/successeurs.txt
perl filtronc_P16.pl -v /tmp/successeurs.txt /tmp/successeurs2.txt
cat corpus_P17_ss_balise.xml| perl index.pl titre
```
