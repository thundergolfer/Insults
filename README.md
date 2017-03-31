# Insults [![Build Status](https://travis-ci.com/thundergolfer/Insults.svg?token=yHGWQ42iK2BPk1FjaUMc&branch=master)](https://travis-ci.com/thundergolfer/Insults)

**TLDR: This project is very similar in functionality and purpose to Google's recent [Perspective API](https://www.perspectiveapi.com/) project** ![Imgur](http://i.imgur.com/kzLNj2z.png)

-----

### Usage

```python
>>> from insults import Insults

>>> comment = "You are a disgusting maggot of a person."
>>> Insults.rate_comment(comment)
0.89

```python
>>> comments = ["You called me a 'dickhead', so I'll say you're a cunt.", "These shitakes taste like shit."]
>>> Insults.foul_language(comments, context=False)
['cunt', 'shit'], None
```

### Installation [Package]

`coming soon`

### Installation [Development]

If you'd like to contribute and hack on the newspaper project, feel free to clone a development version of this repository locally:

`git clone git://github.com/thundergolfer/Insults.git`

Once you have a copy of the source, run the following scripts:

`./install_miniconda.sh`
`./install_local.sh`

A Conda virtual environment is created and everything needed should be now installed into it. To activate the environment, run:

`source ./run_in_environment.sh`

or alternatively you can run single commands in the environment with:

`./run_in_environment.sh <COMMAND>`

##### Running The Tests

`python -m pytests tests/`

### Credit

* [cbrew](https://github.com/cbrew) for their original data-science work in [Imperium's Kaggle Competition](https://www.kaggle.com/c/detecting-insults-in-social-commentary). Code in [cbrew/Insults](https://github.com/cbrew/Insults)
