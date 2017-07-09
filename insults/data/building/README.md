#### Building a new dataset for insult classification

Ok, so the original Imperium dataset only has around 6,000-7,000 examples total, which is an inadequate number for neural network training.
Because I want to play around with different NN architectures on this problem, I'm going to need to get a dataset of at least around 30,000 examples. This is a significant undertaking so I'm going to want to have a good process lined up for this.

##### Basic process

1. Scrape comments off the default subreddits according to certain criteria
2. Place those scraped comments into an 'unlabelled' group file (likely `.csv`)
  1. Have this file go in version control
3. Write a script that can feed those 'unlabelled' examples to console and then once labelled into a new 'labelled' group file
  1. Allow for UNDO functionality
  2. Have this 'labelled' group file go in version control
4. Write code to allow for mechanical turk job submissions
