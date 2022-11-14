# Logstats
Automated classification of unstructured log records

This Python script can be used to automatically discover message types from sample log files. It uses the Levenshtein distance for measuring the difference between two sequences. 


## Prerequisites
https://pypi.org/project/python-Levenshtein/
https://pypi.org/project/py-tlsh/
```

## Usage
```
python3 logstats.py -f input.txt -o output.txt -r 0.5 -m distance
```

[-r] The Levenshtein ratio is a value between 0 and 1 used to adjust the granularity of the classification. The higher the ratio is, the more granular will be the classification.

## Example
![Sample output](./logstats_sample.png)
