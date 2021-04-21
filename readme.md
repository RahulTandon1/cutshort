# Cutshort

Please note: This readme is currently incomplete. It might be worked around Aug 2021 or later. Till then I hope what's written is suffice.

Cutshort is URL Shortner built with Django, MySQL, and Sass.

---

## System Design

![System Design Chart of Cutshort](https://i.imgur.com/nTuQDmD_d.webp?maxwidth=760&fidelity=grand "System Design Diagram")

It's live at [cutshort.in](https://cutshort.in)

> Some notes/brainstorming for myself

## How we'll build this out

So we'll be dividing this into 2 parts

- The shortner
- The redirector

The shorter will basically do all the **create/write** stuff to the db table. It'll be hosted/operate on `create.cutshort.in`
And the redirector will do all the redirecting and hence will mostly just do **read** operations on the db table. It'll be hosted on `cutshort.in/<shortlink if any>`

## Environment Variables

Current have 3 environment variables:

```
- secret_key // django secret key
- DEBUG_COLLECTSTATIC=1 // for static files stuff in production. TBH Kinda forgot what this does exactly
- DATABASE_URL // db url for dj-database-url
```

Since I didn't like typing `export env_variable=value` thrice, I just put three export commands in a bash script (i.e. `.sh` file).
Example file:

```
#! /bin/bash
export secret_key=<value goes here>
export DEBUG_COLLECTSTATIC=1
export DATABASE_URL=<value goes here>
```

To use this I need to type in `source <file name>.sh` and we're good to go!

## Backend basic logic

- Shortner

  > Make a RESTish API to check whether the shortlink exists
  > Form which will POST to `/create`.
  > If no shortlink tho create random, write to db and send back.
  > If shortlnk
  > -- Will check internally using REST API ke function to confirm ki it exists.
  > --- If it does exist tho error page/404 with a message.
  > --- If it doesn't exist, tho create and redirect to Success page.

- Redirector
  > Read the shortlink from `cutshort.in/<shortlink>` and then see if it exists in table. If it does exist, then redirect to corresponding hyperlink. If it doesn't exist then retun 404 page.

## Schema stuff

## Where to pick off from

- In views.py need to use back https://github.com/jd/tenacity or https://github.com/litl/backoff
  to ensure retrys on queries.
- get_stats v/s getStats will need to be fixed in both views.py and urls.py
- Querying DB everytime for rendering homepage probably not good. Maybe use Cronjobs or time
  to update a variable/value regularly and just use that. Maybe use env_variables. Look into good use cases
  of env variables.

- I've made changes with tenacity.
- Querying the database to load the homepage seems a bit much. I'll need to figure something out. Might use orjson (https://github.com/ijl/orjson#install) and read from a json file. And write to it using a library called schedule (https://github.com/dbader/schedule)
