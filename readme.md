# Cutshort

Please note: This readme is currently incomplete. It might be worked around Aug 2021 or later. Till then I hope what's written is suffice.

Cutshort is URL Shortner built with Django, MySQL, and Sass.

---

> Some notes/brainstorming for myself

## How we'll build this out

So we'll be dividing this into 2 parts

- The shortner
- The redirector

The shorter will basically do all the **create/write** stuff to the db table. It'll be hosted/operate on `create.cutshort.in`
And the redirector will do all the redirecting and hence will mostly just do **read** operations on the db table. It'll be hosted on `cutshort.in/<shortlink if any>`

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
