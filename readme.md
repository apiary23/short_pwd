# short_pwd.py
---
Shell prompt shortener & colorizer.

Usage:

```shell
python short_pwd.py
```
Assign command to bash's prompt command and use environment variables to customize how the prompt gets shortened.

```shell
export PROMPT_PATH_LENGTH=5 # default
export PROMPT_TRUNCATE_LENGTH=20 # default
export PROMPT_COMMAND='PS1="$(python3 /path/to/short_pwd.py"'
```