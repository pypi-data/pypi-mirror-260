
[![PyPI - Version](https://img.shields.io/pypi/v/zshgpt.svg)](https://pypi.org/project/zshgpt)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zshgpt.svg)](https://pypi.org/project/zshgpt)
[![zshgpt](https://snapcraft.io/zshgpt/badge.svg)](https://snapcraft.io/zshgpt)

# zshgpt

-----

**Table of Contents**

- [About](#about)
- [Installation](#installing-zshgpt)
- [Adding plugin](#adding-plugin)
- [Logo](#logo)
- [License](#license)

## About
![Gif of usage](<Peek 2023-07-17 17-27.gif>)

Heavily inspired by the abandoned project [https://github.com/microsoft/Codex-CLI](https://github.com/microsoft/Codex-CLI)
Made into a oh-my-zsh plugin.

In your zsh console, type a question, starting with comment sign `#`, hit `ctrl+g` and get an answer.

> [!TIP]
> New in v. 1.1.1 Use doble `##` to use gpt-4 model.

```bash
# Who edited README.MD last according to git history?
```
ChatGPT will then answer with e.g.:
```bash
git log -1 --format="%an" README.md
```
Hit `enter` to execute or `ctrl+c` to deny.

If asked a question that will not resolve in a command, GPT is instructed to use `#`.

```bash
# Who was Norways first prime minister?
# Norway's first prime minister was Frederik Stang, serving from 1873 to 1880.
```

## Prerequisite


## Installing zshgpt
First install zshgpt application, then [add the plugin](#adding-plugin).
### Prerequisite
> [!WARNING]
> Valid Openai API-key
>
> make sure to save under `OPENAI_API_KEY` env.
> ```bash
> export OPENAI_API_KEY='sk-...'
> ```
>

### With snap
Snap comes preinstalled and is probalby the fastest way if you are on Linux and do not want to use pipx.
#### Prerequisite
* snap
```sh
sudo snap install zshgpt
```
[Instructions if you don't have snap](https://snapcraft.io/zshgpt#:~:text=Install%20zshgpt%20on%20your%20Linux%20distribution).

### With pipx
#### Prerequisite
* python >= 3.8
* [pipx](https://pypa.github.io/pipx/installation/)
```sh
pipx install zshgpt
```

### WIth pip
#### Prerequisite
* python >= 3.8
* pip
```sh
pip install zshgpt
```

### With homebrew
This is not yet automated and you might get an older version.
#### Prerequisite
* Homebrew
```sh
brew install AndersSteenNilsen/zshgpt/zshgpt
```

## Adding plugin
### With Zsh
```zsh
curl https://raw.githubusercontent.com/AndersSteenNilsen/zshgpt/main/zshgpt.plugin.zsh -o ~ # Copy plugin
echo "source ~/zshgpt.plugin.zsh" >> ~/.zshrc # Add to zshrc
exec zsh # Reload zsh
```

### With Oh My Zsh
#### Prerequisite
* [Oh My Zsh](https://ohmyz.sh/)
```zsh
mkdir $ZSH_CUSTOM/plugins/zshgpt
curl https://raw.githubusercontent.com/AndersSteenNilsen/zshgpt/main/zshgpt.plugin.zsh -o $ZSH_CUSTOM/plugins/zshgpt/zshgpt.plugin.zsh
```
Then add zshgpt in your list of plugins in `~/.zshrc`

```
plugins(
    ...
    zshgpt
    ...
)
```

```zsh
omz reload
```

### With zplug
`~/.zshrc`
```
...
zplug "AndersSteenNilsen/zshgpt"
zplug load
```

## LOGO
*Made with DALL-E*

![Icon](icon.png)
## License

`zshgpt` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
