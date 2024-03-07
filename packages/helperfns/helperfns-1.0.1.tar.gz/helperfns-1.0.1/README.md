### `helperfns`

🎀 This is a python package that contains some helper functions for machine leaning.

<p align="center">
   <img src="https://github.com/CrispenGari/helperfns/blob/main/images/logo.png?raw=true" alt="logo" width="60%"/>
</p>

---

<p align="center">
  <a href="https://pypi.python.org/pypi/helperfns"><img src="https://badge.fury.io/py/helperfns.svg"></a>
  <a href="https://github.com/crispengari/helperfns/actions/workflows/CI.yml"><img src="https://github.com/crispengari/helperfns/actions/workflows/CI.yml/badge.svg"></a>
  <a href="/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green"></a>
  <a href="https://pypi.python.org/pypi/helperfns"><img src="https://img.shields.io/pypi/pyversions/helperfns.svg"></a>
</p>

### Table of Contents

- [`helperfns`](#helperfns)
- [Table of Contents](#table-of-contents)
- [Getting started](#getting-started)
- [Usage](#usage)
- [tables](#tables)
- [text](#text)
- [utils](#utils)
- [visualization](#visualization)
- [Contributing to `helperfns`.](#contributing-to-helperfns)
- [License](#license)

### Getting started

To start using `helperfns` in your project you run the following command:

```shell
pip install helperfns
```

Or if you wan to install it in notebooks such as jupyter notebooks you can run the code cell with the following code:

```shell
!pip install helperfns
```

### Usage

The `helperfns` package is made up of different sub packages such as:

1. tables
2. text
3. utils
4. visualization

### tables

In the tables sub package you can print your data in tabular form for example:

```python
from helperfns.tables import tabulate_data

column_names = ["SUBSET", "EXAMPLE(s)", "Hello"]
row_data = [["training", 5, 4],['validation', 4, 4],['test', 3, '']]
tabulate_data(column_names, row_data)

```

Output:

```shell
Table
+------------+------------+-------+
| SUBSET     | EXAMPLE(s) | Hello |
+------------+------------+-------+
| training   |          5 |     4 |
| validation |          4 |     4 |
| test       |          3 |       |
+------------+------------+-------+
```

### text

The text package offers two main function which are `clean_sentence`, `de_contract`, `generate_ngrams` and `generate_bigrams`

```python
from helperfns.text import *

# cleans the sentence
print(clean_sentence("text 1 # https://url.com/bla1/blah1/"))
# list of all english words
print(english_words)
# converts strings like `I'm` to 'I am'
print(de_contract("I'm"))

# generate bigrams from a list of word
print(text.generate_bigrams(['This', 'film', 'is', 'terrible']))

# generates n-grams from a list of words
print(text.generate_ngrams(['This', 'film', 'is', 'terrible']))
```

### utils

utils package comes with a simple helper function for converting seconds to hours, minutes and seconds.

Example:

```python
from helperfns.utils import hms_string

start = time.time()
for i in range(100000):
   pass
end = time.time()

print(hms_string(end - start))
```

Output:

```shell
'0:00:00.01'
```

### visualization

This sub package provides different helper functions for visualizing data using plots.

Examples:

```python
from helperfns.visualization import plot_complicated_confusion_matrix, plot_images, plot_images_predictions, plot_simple_confusion_matrix,
plot_classification_report


# plotting classification report

fig, ax = plot_classification_report(labels, preds,
                    title='Classification Report',
                    figsize=(10, 5), dpi=70,
                    target_names = classes)

# plot predicted image labels with the images
plot_images_predictions(images, true_labels, preds, classes=["dog", "cat"] ,cols=8)

# plot the images with their labels
plot_images(images[:24], true_labels[:24], cols=8)

# plot a simple confusion matrix
y_true = [random.randint(0, 1) for _ in range (100)]
y_pred = [random.randint(0, 1) for _ in range (100)]
classes =["dog", "cat"]
plot_simple_confusion_matrix(y_true, y_pred, classes)

# plot a confusion matrix with percentage value of confusion
y_true = [random.randint(0, 1) for _ in range (100)]
y_pred = [random.randint(0, 1) for _ in range (100)]
classes =["dog", "cat"]
plot_complicated_confusion_matrix(y_true, y_pred, classes)
```

### Contributing to `helperfns`.

To contribute to `helperfns` read the [CONTRIBUTION.md](https://github.com/CrispenGari/helperfns/blob/main/CONTRIBUTION.md) file.

### License

This project is licensed under the MIT License - see the [LICENSE](/LISENSE) file for details.
