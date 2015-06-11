shared-lib
==========

Web app to keep track of our family music collection.

## TODO
- [ ] start with only sharing features, add user groups for people who can just share vs those who can also claim and download music from the library
- [x] add is_explicit field to album
- [ ] make main page a "shares" or "inbox" view, that shows all albums in order of share date
    - [ ] show vote order in side bar with claim link
    - [ ] check for newly shared
- [ ] add creation and purchase dates to albums
- [ ] integrate album art automatically via some api (amazon?)
- [ ] package a chrome apps for mobile frontend with push notifications for android and ios 
      `https://developer.chrome.com/apps/chrome_apps_on_mobile`
- [ ] integrate with spotify api to auto-add suggestions that end up in a spotify playlist

Inbox: all shares, reverse sorted
Ranks: all shares for the year sorted by votes (year is selectable)

`+ Add to Library`

itunes api: `https://itunes.apple.com/search?term=dale+earnhardt+jr+jr&entity=album&limit=10`
    - docs: `http://www.apple.com/itunes/affiliates/resources/documentation/itunes-store-web-service-search-api.html#searchexamples`