# Dataset Building with Mechanical Turk

## Why?

I can label things myself, but it takes time and I will eventually get sick to death of doing it. I estimate I need a dataset of ~30,000 examples with a healthy mix of insults included (ie. not just 99% ok comments and 1% insults), so I'll need to distribute the work load.

#### Time Costs

In a 'good' comment set, maybe `~5%` of comments are insults. So say we want our eventual dataset to be `10,000 INSULT + 20,000 !INSULT = 30,000`, then I'll need a labelled dataset of around `~200,000` comments. Damn....

Say someone can label `20` examples a minute with solid accuracy. That's `20 * 60 = 1200` examples an hour. So to get my `200,000` labelled examples I'm looking at

**166.6667 human-hours** to complete the dataset.

-----

#### Monetary Costs

Assuming Mech. Turk workers get paid `$25 AUD` an hour this puts the dataset cost (excluding developer time cost) at around `~$4200`. A far whack, but not exorbitant, and mech. turk workers probably get significantly less than that much per hour.


## Human Intelligence Task (HIT) Specification

### Instructions
> Provide general instructions to Workers doing your HIT.

The challenge is to detect when a comment from a conversation would be considered insulting to another participant in the conversation. Samples could be drawn from conversation streams like news commenting sites, magazine comments, message boards, blogs, text messages, etc.

The idea is to create a generalizable single-class classifier which could operate in a near real-time mode, scrubbing the filth of the internet away in one pass.

Note: It is important that the comment must be insulting another participant in the conversation. For our purposes, the following are not to be classified as insults:

* President Mugabe is an absolute idiot
* The FCC are a bunch of dickheads

While these comments are insulting, they are not directed at someone else in the conversation, but distant third-parties or non-persons.

### Selection Criteria

> Workers do best if you provide selection criteria on your categories. Specify what to include and/or exclude for those categories that might be ambiguous to Workers.

###### Criteria for: Insult




###### Criteria for: NOT Insult



------

Command to pass aws credentials to `boto3` and query MTurk account balance


```
AWS_ACCESS_KEY_ID=$(aws --profile personal configure get aws_access_key_id) AWS_SECRET_ACCESS_KEY=$(aws --profile personal configure get aws_secret_access_key) python insults/data/building/mechanical_turk/blah.py
```
