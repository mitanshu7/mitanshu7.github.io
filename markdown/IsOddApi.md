---
# 1. Basic Identification
title: "IsOddApi"
subtitle: "**A playful REST API to check if a number is odd**"
author: "_Mitanshu Sukhwani_"
date: "`2025-06-09`"
lang: en
mainfont: 'Helvetica'

# 2. Metadata / SEO
description: "A playful REST API that tells you if a number is odd—powered by isEven API under the hood and built with Flask and Docker. Visit isodd.papermatch.me for docs, source code, and usage examples."
keywords: "IsOddApi, REST API, Flask, Docker, isEven API, odd number checker, playful API"
---

# Backstory

The other day [isEven API](https://isevenapi.xyz/) made it to the frontpage of [Hacker News](https://news.ycombinator.com/) and [one commenter](https://news.ycombinator.com/item?id=41371780#41373770) requested the odd version of it. Well, I present to you [**IsOddApi**](https://mitanshu7.github.io/IsOddApiWebsite)!

# Implementation

The best part? It uses [isEven API](https://isevenapi.xyz/) in the backend and inverts the answer XD

I saw this as a learning opportunity and took it. I got to use [flask](https://flask.palletsprojects.com/en/stable/), a lightweight WSGI web application framework. Given the very simple nature of the API, I thought to package it all as a Docker container. You can find the codes at [mitanshu7/IsOddApi](https://github.com/mitanshu7/IsOddApi) and [mitanshu7/IsOddApiWebsite](https://github.com/mitanshu7/IsOddApiWebsite).

The website uses [The smallest Docker image to serve static websites](https://lipanski.com/posts/smallest-docker-image-static-website) to make it _lean_.

# Outcome

isOdd API is a RESTful API that returns json.

API URL: [https://isoddapi.onrender.com/api/](https://isoddapi.onrender.com/api/)

**GET `/isodd/<number>/`**

Returns whether a given number is odd. Allowed numbers depend on your API tier. See Pricing below.

**URL Parameters**

number: the number you want to check

**Example**

[https://isoddapi.onrender.com/api/isodd/7/](https://isoddapi.onrender.com/api/isodd/7/)

```json
{
  "ad": "1995 NISSAN Maxima, green, leather, loaded, CD, auto start, sunroof, 4-door, great condtion, NOT FOR SALE",
  "isodd": true
}
```
