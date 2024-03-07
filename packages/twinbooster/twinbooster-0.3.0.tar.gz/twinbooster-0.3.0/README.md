# Python package for TwinBooster

[![arXiv](https://img.shields.io/badge/arXiv-2401.04478-b31b1b.svg)](https://arxiv.org/abs/2401.04478)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Python version](https://img.shields.io/badge/python-v.3.8-blue)
![License](https://img.shields.io/badge/license-MIT-orange)

### Synergising Chemical Structures and Bioassay Descriptions for Enhanced Molecular Property Prediction in Drug Discovery

Maximilian G. Schuh, Davide Boldini, Stephan A. Sieber

@ Technical University of Munich, TUM School of Natural Sciences, Department of Bioscience, Center for Functional Protein Assemblies (CPA)

### Installation

Install the package with ```pip install twinbooster```.
Then you can download the pretrained models with ```twinbooster.download_models()```.
For FS-Mol, you can download the data with ```twinbooster.download_data()```.

An example script can be found here ```./twinbooster/twinbooster_example.ipynb```.

### Citation

If you use TwinBooster in your research, please cite our preprint:

```
@misc{schuh2024twinbooster,
      title={TwinBooster: Synergising Large Language Models with Barlow Twins and Gradient Boosting for Enhanced Molecular Property Prediction}, 
      author={Maximilian G. Schuh and Davide Boldini and Stephan A. Sieber},
      year={2024},
      eprint={2401.04478},
      archivePrefix={arXiv},
      primaryClass={q-bio.BM}
}
```
