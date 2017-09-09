import json
import langdetect
from langdetect import detect
import logging
import os
import time

CURR_FILES_PATH = os.path.dirname(os.path.abspath(__file__))

# Initialise Logger
logging.basicConfig(filename=os.path.join(CURR_FILES_PATH, time.strftime("%Y%m%d_%H%M%S") + "_criteria.log"), level=logging.DEBUG)

with open(os.path.join(CURR_FILES_PATH, 'default_dataset_criteria.json')) as config_file:
    DEFAULT_CONFIG = json.load(config_file)


def validate_comment(comment, config=DEFAULT_CONFIG):
    logging.info("Validating Comment: {}".format(comment.encode('utf-8')))

    validate_dataset_criteria_config(config)
    comment_len = len(comment)

    # There's no point processing empty comments or comments too short
    # to possibly contain an insult.
    if comment_len < config["min_comment_length"]:
        return False

    # Long form comments are far more difficult to process with current
    # NLP techniques. Most work is on 1-2 sentences examples. A decent paragraph
    # is 6-10 sentences and around 600-1000 characters.
    # We want to avoid having essays as part of our dataset.
    valid_length = comment_len <= config["max_comment_length"]

    # Ignore comments that aren't in a language our model will handle. This
    # will very likely just be english ('en')
    try:
        valid_language = detect(comment) in config["allowed_languages"]
    except langdetect.lang_detect_exception.LangDetectException:
        logging.error("Comment: '{}' caused an error in language detection".format(comment.encode('utf-8')))
        return False

    return valid_length and valid_language


def validate_parent_comments(parent, grandparent):
    valid_parent, valid_grandparent = True, True
    if parent:
        valid_parent = validate_comment(parent)
    if grandparent:
        valid_grandparent = validate_comment(grandparent)

    return valid_parent and valid_grandparent


def validate_dataset_criteria_config(config):
    if "min_comment_length" not in config:
        raise ValueError("Need to specify a number for 'min_comment_length' in config")

    if "max_comment_length" not in config:
        raise ValueError("Need to specify a number for 'max_comment_length' in config")

    if "allowed_languages" not in config:
        raise ValueError("Need to specify a list of valid language codes as 'allowed_languages'")

    if not type(config["allowed_languages"]) is list:
        raise ValueError("'allowed_languages' needs to be a list of valid language codes")

    return True
