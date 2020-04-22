# DeepBible

DeepBible offers insights into the structure of the Bible, such as the PageRank of its chapters, based on the cross-references between them.
Next idea: Return the correlation between the Bible and a given speech. This is especially useful when one forgets a certain statement, but he does know the idea behind it.

## Installation

```bash
1) git clone https://github.com/stoianmihail/DeepBible.git
2) cd DeepBible
```

## Usage

First generate the JSON file, in which the entire Bible will be stored:
```python
python3 read.py biblia.txt
```
Then analyze the cross-references:

```python
python3 analyze.py biblia.json
```
