
26.03.25 log E.W
added a tiny bit of css. 
"If browser window size changed, is the change handled neatly?" - css for responsive stuff
@media only screen and (max-width: 700px) {
    body {
      background-color: lightblue;
    }
  }

this is a tester. I think mostly it's just making sure stuff is still visible and doesn't warp - like making the nav bar 2-level or vertical so it fits on the screen. may do that later

added some models, it appears to be migrated ok but needs checking/testing. 
added superuser 
    username Blake
    email BShelley@gmail.com
    password #Pass123#               (with the hashes)
but honestly not sure if that'll work for you like me?
http://127.0.0.1:8000/admin/ and then logging in using those details


I think discounts should be removed for now, it'll add complexity to memberships and can be added after - could be an enum for membership type, discount type with default none, but idk






