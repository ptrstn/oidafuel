[![Python Package](https://github.com/ptrstn/oidafuel/actions/workflows/python-package.yml/badge.svg)](https://github.com/ptrstn/oidafuel/actions/workflows/python-package.yml)
[![codecov](https://codecov.io/gh/ptrstn/oidafuel/branch/master/graph/badge.svg)](https://codecov.io/gh/ptrstn/oidafuel)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# oidafuel

## Installation

```bash
pip install --user git+https://github.com/ptrstn/oidafuel
```

## Usage
### Help
```bash
oidafuel --help
```

```
usage: oidafuel [-h] [--version] [--list-regions] [--fuel-type {SUP,DIE,GAS}] [--region REGION | --address ADDRESS]

Check gas prices for a given location

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --list-regions        List Regions
  --fuel-type {SUP,DIE,GAS}
                        SUP (Super 95), DIE (Diesel) or GAS (Compressed natural gas)
  --region REGION       Region code
  --address ADDRESS     Address
```
### Example 

```bash
oidafuel --region 9 --fuel-type SUP
```

```
1.489 Turmöl Quick, 1140 Wien, Schlossallee 2 
1.494 Shell Austria, 1150 WIEN, LINZER STR 2A 
1.497 TURMÖL powered by boesch energy, 1160 Wien, Baldiagasse 14a 
1.497 TURMÖL powered by boesch energy, 1120 Wien, Schoenbrunner Strasse 213 
1.497 Turmöl Quick, 1230 Wien, Breitenfurterstraße 473 
1.497 Turmöl Quick, 1100 Wien, Hardtmuthgasse 51 
1.497 Turmöl Quick, 1120 Wien, Altmannsdorfer Straße 96 
1.497 Diskont Tankstelle, 1230 Wien, Wien Breitenfurter Strasse 261 ("Hofer-Parkplatz") 
1.497 Strohmeier Tankstelle, 1050 Wien, Am Hundsturm 2-4 
1.498 NNB BRUNNENTANKSTELLE, 1160 WIEN, Brunnengasse 4 
```

## Development

```bash
git clone https://github.com/ptrstn/oidafuel
cd oidafuel
python -m venv venv
. venv/bin/activate
pip install -e .
pip install -r testing-requirements.txt
```

### Testing

```bash
pytest --cov .
```
