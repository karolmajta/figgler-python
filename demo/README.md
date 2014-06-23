To see how the autodetection works just:

    $ fig up

Want to see how extra containers get detected? In one terminal run:

    $ fig scale db=2 redis=3 mongo=1

And in another:

    $ fig up app

Enjoy!
