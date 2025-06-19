# [IsOddApi](https://isodd.papermatch.me/)

## API to tell if a number is [Odd](https://simple.wikipedia.org/wiki/Odd_number)

**Mitanshu Sukhwani** • _09 June 2025_

# Backstory

The other day [isEven API](https://isevenapi.xyz/) made it to the frontpage of [Hacker News](https://news.ycombinator.com/) and [one commenter](https://news.ycombinator.com/item?id=41371780#41373770) requested the odd version of it. Well, I present to you [**IsOddApi**](https://isodd.papermatch.me/)!

# Implementation

The best part? It uses [isEven API](https://isevenapi.xyz/) in the backend and inverts the answer XD

I saw this as a learning opportunity and took it. I got to use [flask](https://flask.palletsprojects.com/en/stable/), a lightweight WSGI web application framework. Given the very simple nature of the API, I thought to package it all as a Docker container. You can find the codes at [mitanshu7/IsOddApi](https://github.com/mitanshu7/IsOddApi) and [mitanshu7/IsOddApiWebsite](https://github.com/mitanshu7/IsOddApiWebsite).

The website uses [The smallest Docker image to serve static websites](https://lipanski.com/posts/smallest-docker-image-static-website) to make it _lean_.

# Outcome

isOdd API is a RESTful API that returns json.

API URL: [https://isoddapi.papermatch.me/api/](https://isoddapi.papermatch.me/api/)

**GET `/isodd/<number>/`**

Returns whether a given number is odd. Allowed numbers depend on your API tier. See Pricing below.

**URL Parameters**

number: the number you want to check

**Example**

[https://isoddapi.papermatch.me/api/isodd/7/](https://isoddapi.papermatch.me/api/isodd/7/)

```json
{
  "ad": "1995 NISSAN Maxima, green, leather, loaded, CD, auto start, sunroof, 4-door, great condtion, NOT FOR SALE",
  "isodd": true
}
```
