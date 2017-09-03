## Developer Notes

Sunday 3rd September 2017 I explored for the first time the *Amazon AWS Mechanical Turk* platform for the purposes of building a
large dataset for classifying insulting comments.

Each Human Intelligence Task (HIT) contains a *single* classification task. So if I want to classify `100` comments I'll need to submit `100` HITs.

Seeing as each HIT is one task, there needs to be a way to track individual HITs to individual dataset entries.
