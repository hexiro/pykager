# pykager

📦 setup.py generator with smart defaults

## Showcase

the setup.py file generated can be viewed in this project.

![example showcase gif](https://i.imgur.com/NFxWAMK.gif)

## Installation

download the latest development build from GitHub

```shell
$ pip3 install -U git+https://github.com/Hexiro/pykager
```

## 🧠 Smart Defaults

the place where each argument can be fetched from <br/>
values set by the user override all defaults

| argument | setup.py | .git | \_\_init\_\_.py | other |
| :----|:----:|:----:|:----:|:----:|
| name                          |✔️|✔️|❌|❌|
| version                       |✔️|❌|✔️|❌|
| description                   |✔️|❌|❌|❌|
| author                        |✔️|✔️|✔️|❌|
| author email                  |✔️|✔️|✔️|❌|
| url                           |✔️|✔️|❌|❌|
| license                       |✔️|❌|✔️|❌|
| long description              |❌|❌|❌|README file|
| long description content type |❌|❌|❌|README file|
| keywords                      |✔️|❌|❌|❌|
| classifiers                   |✔️|❌|❌|❌|
| python requires               |✔️|❌️|❌️|❌|
| install_requires              |❌|❌️|❌️|requirements.txt|
| zip_safe                      |✔️|❌️|❌️|❌|
| packages                      |❌️|❌️|❌️|setuptools|
| entry_points                  |✔️|❌|❌|❌|

## 🐞 Contributing

This project has a lot of room for improvement. Mainly cleaning up code, more modularity, and bug fixes. <br/>
If you make an issue, pr, or suggestion, it'll be very appreciated <3.