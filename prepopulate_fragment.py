        def setUp(self)
            User.query.delete()
            Message.query.delete()
            Follow.query.delete()
            Like.query.delete()



        # prepopulate database with test users, message, follow and like:
        u1 = User(
                username = "test_user1",
                email = "test1@test.com",
                password = "HASHED_PASSWORD1"    
            )
        u2 = User(
                username = "test_user2",
                email = "test2@test.com",
                password = "HASHED_PASSWORD2"    
            )

        db.session.add_all([u1, u2])
        db.session.commit()

        f = Follow(user_being_followed_id=u2.id, user_following_id=u1.id)
        db.session.add(f)
        db.session.commit()

        m = Message(text="warble warble", user_id=u1.id)

        u1.messages.append(m)
        db.session.commit()

        l = Like(user_id = u1.id, message_id = m.id)

        db.session.add(l)
        db.session.commit()
