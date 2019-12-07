# python3-starter
Simple Python 3 starter

## Prerequisites
* `Python 3.7`
* [`virtualenv`](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)

## Usage
```bash
git clone git@github.com:k-t-corp/python3-starter.git
cd python3-starter
rm -rf .git
nano README.md  # change readme, of course
git init
python3 -m virtualenv venv
pip install -r requirements.txt
```

## Develop
```bash
source venv/bin/activate
python main.py
```
