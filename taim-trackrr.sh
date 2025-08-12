#!/bin/bash
# this scripts interacts with the Taim Trackrr API

# load environment variables
load_setting() {
    if [[ -f ~/.taim-tracker.ini ]]; then
        export $(grep -v '^#' ~/.taim-tracker.ini | xargs)
    else
        echo "Settings file not found"
        exit 1
    fi
}

# login function
login() {
    local url=$1
    local username=$2
    local password=$3
    response=$(curl -s -X 'POST' "$url"/api/login \
        -H 'accept: application/json' \
        -H 'Content-Type: application/x-www-form-urlencoded' \
        -d "grant_type=password&username=${username}&password=${password}&scope=&client_id=&client_secret=")
    if [[ $(echo "$response" | jq -r .token_type) == "bearer" ]]; then
        echo "Login successful"
        echo "API_URL="$url > ~/.taim-tracker.ini
        echo "API_TOKEN="$(echo "$response" | jq -r .access_token) >> ~/.taim-tracker.ini
    else
        echo "Login failed: $(echo "$response")"
    fi
}

# create/stop timer function
set() {
    load_setting
    response=$(curl -s -X POST "$API_URL/api/timer" -H "Content-Type: application/json" -H "Authorization: Bearer $API_TOKEN")
    
    start_time=$(echo "$response" | jq -r '.start_time // empty')
    if [[ -n "$start_time" ]]; then
        echo "Timer set"
    else
        echo "Error: $(echo "$response")"
    fi
}

# get current timer function
get() {
    load_setting
    response=$(curl -s -X GET "$API_URL/api/timer" -H "Authorization: Bearer $API_TOKEN")
    start_time=$(echo "$response" | jq -r '.start_time // empty')
    if [[ -n "$start_time" ]]; then
        echo "Current timer: $(echo "$response")"
    elif [[ $(echo "$response" | jq -r '.detail') == "No active timer found" ]]; then
        echo "No active timer found"
    else
        echo "Error: $(echo "$response")"
    fi
}

case $1 in
login) "$@"; exit;;
set) "$@"; exit;;
get) "$@"; exit;;
esac
