## Quick start

### Dependencies
The only one is [PyTermGUI](https://github.com/bczsalba/pytermgui).
```console
pip install -r requirements.txt
```

### To run
#### The default
```console
python3 solucao.py
```

#### If you have `mypyc` from [Mypy](https://mypy-lang.org/)
```console
mypy --strict --strict-optional --pretty solucao.py
```
And then you can do (if you want)
```console
mypyc solucao.py
python3 -c "import solucao; solucao.main()"
```
This is great for testing runtime safety due to mypy's typechecking
