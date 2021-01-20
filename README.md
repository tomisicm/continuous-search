# Contious Search

For the ones who are looking to speed up the application process.

## prerequisite:
### install latex
### install dependancies (requests, bs4, pandas, ...)

## How to:
### clone the directory and change it so it fits your job profile and skills

There are 3 scripts:

One for scrapping, one for creating coverletters and one for sending mails.
Some jobs you can directly send mails, some jobs you have to apply through form (haven't eve tried automating this
because each job can be using different forms).

1) jobs.py
- Will scrap for jobs for the each provided strategy.

Each strategy represents one site.
Currently there is one strategy implemented, for other sites you have to write down the strategy implementation.
Strategy implementation is specific for each site.

As an example I've created one strategy for stackoverflow.
Jobs are collected then filtered and stored in the dedicated csv file.

Basically for the strategy implementation you have to setup BaseURL, and Search Path which defines your criteria.
Then the request is made and results is parsed to the html which is then processed.
Then each job position data depends on the html element. Each piece of data will require different selector.

There are also some filters. I am only interested in jobs posted in the last 24 hours.
Run the script each day or tailor the filters according to your needs.
Jobs will be collected in the companies.csv.

Some of the parameters can be missing.

2) create-cl.py
- I am using latex for tailoring my coverletter for each company according to the job position.

In order to make each coverletter dynamic parameters are passed to the build process. You will easly see how to
create your desired params from the examples.

As a first step write the coverlettter, determine which params need to be provided at build time and tailor the coverletter
according to the params.

Jobs are read from the companies.csv file and the coverletter is created only for jobs that sentAt is NULL, meaning job hasn't been applied for.

I've given an example how to provide at several buildtime parameters. Some of them are strings, some of them are boolean flags.
E.g. of boolean flag is isLaravelPosition.

The process of building dynamic coverletter is using LuaTex and awesome-cv coverletter template
( https://www.overleaf.com/latex/templates/awesome-cv/dfnvtnhzhhbm ).

3) send-emails
for the positions with given email, can apply dirrectly. Others you have to go through the given form manually.

## TODO:
# - other strategies
# - send-mails.py
# - clean the repo and create flow where user will pull the code via command, clone the repo and be able to start with scrapping
# - add more detailed description about the setup
# - some sites have protection, is it posible to avoid it? mimicking user agent and request headers didn't do the trick
# - dislike fiter


COVERED STRATEGIES:
- Stack Overflow

Good luck my friend. I hope you find this useful and I hope you find what are you looking for.
