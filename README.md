# CloudFlare CNAME Flattener

Need to use a CNAME at the root of your website at CloudFlare?
Is that causing email deliverability issues?

This should help.

## High level

This resolves the CNAME record to the associated A record(s), makes an API call to CloudFlare, and creates the necessary A record(s). This way you can have an A record at the root even if your host only provides you with a CNAME, and your email deliverability issues should be fixed.

## Instructions

After cloning this repository, set environment variables with your CloudFlare settings. To do so, you can copy `env.sample.sh` to `env.sh` and insert your own values. Then run `$ . env.sh` to set the environment variables.

Run the script an initial time and verify you now have A records in place of the CNAME you previously had. Confirm it's working correctly.

Finally, schedule the script to as often as you feel comfortable with, the suggestion being every minute. You can do so by setting up a `cron` job (remember to run the environment variables script first), or by deploying to Heroku (see below).

## Heroku

This script is ready to deploy to [Heroku](https://get.heroku.com/).

Create a new app:

```bash
$ heroku create example-cname-flattener
```

Set all environment variables:

```bash
$ heroku config:add \
  CF_CNAME='[INSERT CNAME VALUE HERE]' \
  CF_API_KEY='[YOUR CLIENT API KEY]' \
  CF_EMAIL='[YOUR CLOUDFLARE E-MAIL]' \
  CF_DOMAIN='[CLOUDFLARE DOMAIN NAME]' \
  CF_RECORD_NAME='[NAME OF RECORD]'
```

Push the code:

```bash
$ git push heroku master
```

Launch the worker dyno:

```bash
$ heroku ps:scale worker=1
```

Check that the script is running with:

```bash
$ heroku logs -t
```
