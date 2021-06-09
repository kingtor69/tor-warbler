# Warbler Project: answers to conceptual questions brought up in assigment
## by Tor Kingdon
### Springboard Software Engineering Career Track Unit 26

### Part One
#### Step Six
##### How is the loggin in user being kept track of?

The user_id is being saved in the Flask session

##### What is Flask's *g* object?

*`g`* is storing the logged in user in the session in `g.user`

##### What is the purpose of `add_user_to_g`?

The logged in user is being stored in the *`g`* object using the method `add_user_to_g`

##### What does `@app.before_request` mean?

The code following that line runs before each request (such as viewing a user profile, editing your own user profile, following another user, &c) and loads the logged in user to the *`g`* object.