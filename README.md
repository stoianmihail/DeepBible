# DeepBible

DeepBible offers insights into the structure of the Bible, such as the PageRank of its chapters, based on the cross-references between them.
Next idea: Return the correlation between the Bible and a given speech.
This is especially useful when one forgets a certain verse, but not the idea behind it. At that moment, instead of distorting the original meaning, one could use Speech2Bible, which would immediately recognize the verse one has in mind. 

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
