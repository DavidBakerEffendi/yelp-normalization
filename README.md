# Yelp Challenge Dataset Normalization

The following project aims to normalize and perform feature selection on the dataset. The
motivation of this project is to prepare the dataset to be imported into databases and/or
only make use of subsets of the dataset. The resulting normalized JSON file would not
need any validation when importing e.g. does this user's friend exist? This project only 
considers `review.json`, `business.json`, and `user.json`.

## Getting Started

This project has a single depedency, `tqdm`, which manages the progress bar. `INSTALL.sh` will
create a virtual environment and install packages listed in `requirements.txt`. 

`RUN.sh` will run the project according to the configurations set in `config.py`. All processed
files will be written to `./out`.

## Configuration

`config.py` lists three main configuration settings:

* `NORMALIZE_DATASET`: Enables the normalization and feature selection of the original dataset.
* `NORMALIZE_SETTINGS`: Sets the file location of the original dataset files and enables which
  files are selected for the processing.
* `GEN_SUBSET`: Enables the ability for selecting a subset of the normalized dataset (dependent)
  on files from `NORMALIZE_DATASET` to be present in `./out`.
* `SUBSET_SETTINGS`: Allows the user to set the percentage of the dataset to extract and which 
  files to generate subsets for.
* `PREPARE_CSV`: Enables the ability to create CSV files from a JSON subset of the dataset.
* `PREPARE_SETTINGS`: Allows the user to specify which files need to be converted to CSV.

## Feature Selection

The core features of the dataset are selected and those which can be calculated (e.g. `average_stars`)
are discarded. `user.json` includes user friends who may not be in the dataset and these friends are
removed. The following features are what you can expect to be in 
`./out/{business, review, user}_norm.json`.

| Business    | User          | Review      |
|-------------|---------------|-------------|
| business_id | user_id       | review_id   |
| name        | name          | user_id     |
| address     | friends       | business_id |
| city        | yelping_since | stars       |
| state       | useful        | date        |
| postal_code | funny         | text        |
| latitude    | cool          | useful      |
| longitude   | fans          | funny       |
| stars       |               | cool        |
| is_open     |               |             |
| categories  |               |             |

## Subset Generation

Subsets of the dataset are generated according to `SUBSET_SETTINGS.PERC` under `config.py`. Businesses
and users are handled first. If a user has friends who are no longer in the dataset, they are removed
from that user's friends list. Once this is done, the reviews which have businesses and users within the
resulting subsets are kept. The reviews which have businesses or users not in the subsets are discarded.

## CSV Generation

Certain databases have bulk offline import tools (e.g. TigerGraph, Amazon Neptune) and they primarily
read data using CSV. Since there are list attributes in the dataset, these one-to-many relationships
are converted into separate CSV files e.g. categories, friends, etc.