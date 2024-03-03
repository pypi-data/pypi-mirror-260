<h1 align="center">
    <img src="https://github.com/2003100127/pcser/blob/main/img/pcser-logo.png?raw=true" width="200" height="70">
    <br>
</h1>


![PyPI](https://img.shields.io/pypi/v/pcser?logo=PyPI)
![](https://img.shields.io/github/stars/cribbslab/pcser?logo=GitHub&color=blue)
[![Downloads](https://pepy.tech/badge/pcser)](https://pepy.tech/project/pcser)

<hr>


![Python](https://img.shields.io/badge/-Python-000?&logo=Python)
![PyPI](https://img.shields.io/badge/-PyPI-000?&logo=PyPI)

###### tags: `protein corona` `nanoparticles` `stealth effect` `machine learning`

## Overview
PCSER is a computational tool for predicting protein corona stealth effects. It was built using the random forest machine learning approach.

## 📔 Documentation
Please check https://2003100127.github.io/pcser for how to use PCSER.

## 🛠️ Installation

PCSER can be installed in the following ways.

* ![PyPI](https://img.shields.io/badge/-PyPI-000?&logo=PyPI) (https://pypi.org/project/pcser)

  ```bash
  conda create --name pcser python=3.11
      
  conda activate pcser
  
  pip install pcser --upgrade
  ```

* ![Github](https://img.shields.io/badge/-Github-000?&logo=Github)

  ```bash
  conda create --name pcser python=3.11
    
  conda activate pcser
  
  git clone https://github.com/2003100127/pcser.git
  
  cd pcser
  
  pip install .
  ```

## 🚀 Quick start

```python
import pcser as pcs

pcs.load.evaluate(
    data_ref_fpn='./Proteomics_07262023_rv_C57BL6_spl54.xlsx',
    sv_fp='./',  # None to('data/')
    input_fpn='./example.xlsx',
    model_fpn='./best_cv.joblib',
    sheet_name='a', # a b
    # mfi_ref=[10271.33333, 10747, 10303.33333, 9663.333333, 10056],
    mfi_ref=[3606.333333, 3606.333333, 3606.333333, 3606.333333],

    # is_norm=True,
    # norm_met='minmax',  # minmax std maxabs
    # mode='compo',  # compo annot
    # mark='spl54',  # spl54 spl63
    # version='extended',  # extended old
)
```

Then, it outputs what is shown below.

```python
# You are using extended sheets.
# You have selected the minmax normalization method.
# Data summary:
# Number of samples: 54
# Number of features: 419
# You have the samples: ['HuApoA1', 'MoApoA1', 'HuClusterin', 'MoClusterin']
# PCSER predictions: 
#              stealth_effect          MFI
# HuApoA1            0.670762  3099.790003
# MoApoA1            0.662108  3189.458730
# HuClusterin        0.634621  3474.270396
# MoClusterin        0.633914  3481.599008
# stealth_effect	MFI
# HuApoA1	0.670762	3099.790003
# MoApoA1	0.662108	3189.458730
# HuClusterin	0.634621	3474.270396
# MoClusterin	0.633914	3481.599008
```

## 📄 Citation
```angular2html
@article{PCSER,
    title = {PCSER},
    author = {Jianfeng Sun},
    doi = {xxx},
    url = {https://github.com/2003100127/pcser},
    journal = {xxx}
    year = {2024},
}
```

## 🏠 Homepage
[📍Oxford University](https://www.ndorms.ox.ac.uk/team/jianfeng-sun) 

## 📧 Reach us
[![Linkedin Badge](https://img.shields.io/badge/-Jianfeng_Sun-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/jianfeng-sun-2ba9b1132)](https://www.linkedin.com/in/jianfeng-sun-2ba9b1132) 
[![Gmail Badge](https://img.shields.io/badge/-jianfeng.sunmt@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:jianfeng.sunmt@gmail.com)](mailto:jianfeng.sunmt@gmail.com)
[![Outlook Badge](https://img.shields.io/badge/jianfeng.sun@ndorms.ox.ac.uk--000?style=social&logo=microsoft-outlook&logoColor=0078d4&link=mailto:jianfeng.sun@ndorms.ox.ac.uk)](mailto:jianfeng.sun@ndorms.ox.ac.uk)
<a href="https://twitter.com/Jianfeng_Sunny" ><img src="https://img.shields.io/twitter/follow/Jianfeng_Sunny.svg?style=social" /> </a>