# Taim trackkr

Simple timespan tracking

## Why

I needed something to track how much time I spend on some projects. There are hundreds of alternatives but I need something really simple, when I started and when I finish, there is some tags and notes support but idk.

## How to run

- `git clone https://github.com/baldosa/taim-trackrr.git`
- `cp .env.example .env`
- `vim .env`
- `docker compose up -d`

Then you can POST to /api/timer to start or stop a timespan.

If you GET to that endpoint you get the current timespan (if any)

## Chrome extension

Theres a simple chrome extension in the folder `taim-trackrr-extension` with a START/STOP button that can talk to the app.

## CLI

There's a bash script to use to login/set timer/get timer.

## How to colaborate

- IDK
