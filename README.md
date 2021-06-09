# Warbler (Twitter Clone)
## Tor Kingdon
### Springboard Software Engineering Career Track Unit 26

## See conceptual.md for my answers to conceptual questions posed in the assigment

## Part One
 - fixed existing features as detailed in assignment
 - located and fixed additional issues:
   - a new user was not given any easy way to find users to follow, so I simply added a message to use the search bar to find more warblers to follow if you want to see more warbles
   - users/index.html did not show bio or location
   - fix followed users showing 'action' of `unfollow` button on users index page
   - `datetime.utcnow()` was only getting called at the beginning of a session. I changed it so that the default datetime was overridden by a new call of `datetime.utcnow()` when processing the new warble form

## Part Two: Likes
 - These likes would probably be better done on the client-side using AJAX in JavaScript, but for the purposes of this exercise, it is done in the backend.

### goals **if time permits**
   - expand search to also search for text within warbles, bios, locations, etc.
     - sort results by where item was found (what column)
     - or perhaps an advanced search
   - add to nav bar
     - show all warblers
     - show all warbles...? 
 - 