# Logstats
Automated classification of unstructured log records

This Python script can be used to automatically discover message types from sample log files. It uses the Levenshtein distance for measuring the difference between two sequences. 


## Prerequisites
This script uses a Levenshtein library, get it from https://code.google.com/archive/p/pylevenshtein/downloads and install it using the command below:

```
python setup.py build
sudo python setup.py install

```

## Usage
```
python logstats.py -f input.txt -o output.txt -r 0.9
```

[-r] The Levenshtein ratio is a value between 0 and 1 used to adjust the granularity of the classification. The higher the ratio is, the more granular will be the classification.

If you have a very large file, you can run Logstats against a sample of the file. To sample ~1% of a file you can use this command:
```
cat input.txt | awk 'BEGIN {srand()} !/^$/ { if (rand() <= .01) print $0}' > sample.txt
```

## Example
![Sample output](./logstats_sample.png)
