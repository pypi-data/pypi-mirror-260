# Co2 Switzerland
This project was created during the GovTech Hackathon 2024 in Berne, Switzerland.
The theme is "Network Switzerland." Under this title, participants will be seeking solutions for digital networking - both within the public administration and with third parties. Meet developers, experts, and interested parties from administration, business, and civil society and collaborate on laying the digital foundations of our society.

## Project
[Our project](https://hack.opendata.ch/project/1091) in the hackathon aims to retrieve the Carbon Footprint data from cities. We were able to achieve this in [France](https://mycityco2.org). The downside is that in Switzerland, the data are not universally available and not in the same format everywhere. That's why we aim to raise awareness of this issue by participating in Federal Events. Through these events, we hope to be contacted by the right people to effect change.

## Rules

### Commit
In this project we follow the [Angular Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/). If you wish to participate, please follow them.

### Branchs
Please create you're own branch with you're name and with the features that you wish to implement, once the features done, create a pull request with all the required details. The branchs naming should follow this pattern: main+\<trigram\>+\<feature\> per example for Adam Bonnet it's main+abo+init.

## How-To
### Setup / Install
In order to make this project work you'll need to install the following:
- at least [python 3.10](https://www.python.org/downloads/release/python-3100/)
- [pipx](https://pipx.pypa.io/stable/installation/)
- [poetry (using pipx)](https://python-poetry.org/docs/)
- [pre-commit](https://pre-commit.com/)
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

once all these packages installed you can now do the following:
if the first one isn't working use the second link
```bash
git clone git@github.com:MyCityCO2/co2-switzerland.git

git clone https://github.com/MyCityCO2/co2-switzerland.git
```
```bash
cd co2-switzerland
pre-commit install
```
now you should be all goods to run the project

### Run the project
Since were using poetry as our package manager you'll need to do the following:
```bash
poetry shell
```
now you are in the right environnment. Try to do the commands ```co2```, if it work and showing you 3 commands: switzerland, plugins, version. To be really sure you can do ```co2 plugins list``` and if switzerland is showing then nice job, you just install the project. Now let's work together in order to finish this GovTech Hackathon


### Changelog and Versionning
The changelog and versionning is managed by semantic release, so once you're finish you're features, create a merge request and it get merged, you'll need to ```git checkout main && git pull```, in order to get the news values.
PLEASE DO NOT TOUCH THE VERSION VARIABLE OTHERWISE YOU'RE FEATURES WON'T BE MERGED.
