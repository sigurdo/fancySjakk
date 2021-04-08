
# fancyChess

Trying to make fancy chess in pyhton. Looks something like this:

```
                        _             ____             ____           ____            _____           _____            ____           _   _
                       / \           | __ )           / ___|         |  _ \          | ____|         |  ___|          / ___|         | | | |
                      / _ \          |  _ \          | |             | | | |         |  _|           | |_            | |  _          | |_| |
                     / ___ \         | |_) |         | |___          | |_| |         | |___          |  _|           | |_| |         |  _  |
                    /_/   \_\        |____/           \____|         |____/          |_____|         |_|              \____|         |_| |_|


       ___      XXXXXXXXXXXXXXXX     (\=,       XXXXXX () XXXXXX       ()       XXXXX _:_ XXXXXX       ()       XXXX (\=, XXXXXX                       ___
      ( _ )     XXX |'-'-'-| XXX    //  .\      XXXXXX /\ XXXXXX    .-:--:-.    XXXX '-.-' XXXXX       /\       XXX //  .\ XXXXX    |'-'-'-|          ( _ )
      / _ \     XXX |______| XXX   (( \_  \     XXXXX //\\ XXXXX     \____/     XXXX _.'._ XXXXX      //\\      XX (( \_  \ XXXX    |______|          / _ \
     | (_) |    XXXX |====| XXXX    ))  `\_)    XXXX (    ) XXXX     {====}     XX |_______| XXX     (    )     XXX ))  `\_) XXX     |====|          | (_) |
      \___/     XXXX |    | XXXX   (/     \     XXXXX )  ( XXXXX      )__(      XXX \=====/ XXXX      )  (      XX (/     \ XXXX     |    |           \___/
                XXXX |____| XXXX     )___(      XXXX /____\ XXXX     /____\     XXXX )___( XXXXX     /____\     XXXX )___( XXXXX     |____|
                XXX (______) XXX    (_____)     XXX (______) XXX    (______)    XX (_______) XXX    (______)    XXX (_____) XXXX    (______)
      _____                     XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX      _____
     |___  |           __       XXXXXX __ XXXXXX       __       XXXXXX __ XXXXXX       __       XXXXXX __ XXXXXX       __       XXXXXX __ XXXXXX     |___  |
        / /           /  \      XXXXX /  \ XXXXX      /  \      XXXXX /  \ XXXXX      /  \      XXXXX /  \ XXXXX      /  \      XXXXX /  \ XXXXX        / /
       / /            \  /      XXXXX \  / XXXXX      \  /      XXXXX \  / XXXXX      \  /      XXXXX \  / XXXXX      \  /      XXXXX \  / XXXXX       / /
      /_/             /==\      XXXXX /==\ XXXXX      /==\      XXXXX /==\ XXXXX      /==\      XXXXX /==\ XXXXX      /==\      XXXXX /==\ XXXXX      /_/
                     /____\     XXXX /____\ XXXX     /____\     XXXX /____\ XXXX     /____\     XXXX /____\ XXXX     /____\     XXXX /____\ XXXX
                    (______)    XXX (______) XXX    (______)    XXX (______) XXX    (______)    XXX (______) XXX    (______)    XXX (______) XXX
       __       XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                       __
      / /_      XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                      / /_
     | '_ \     XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                     | '_ \
     | (_) |    XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                     | (_) |
      \___/     XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                      \___/
                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX
                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX
      ____                      XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX      ____
     | ___|                     XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX     | ___|
     |___ \                     XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX     |___ \
      ___) |                    XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX      ___) |
     |____/                     XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX     |____/
                                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX
                                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX
     _  _       XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                     _  _
    | || |      XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                    | || |
    | || |_     XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                    | || |_
    |__   _|    XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                    |__   _|
       |_|      XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                       |_|
                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX
                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX
      _____                     XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX      _____
     |___ /                     XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX     |___ /
       |_ \                     XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX       |_ \
      ___) |                    XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX      ___) |
     |____/                     XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX     |____/
                                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX
                                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX
      ____      XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                      ____
     |___ \     XXXXXX __ XXXXXX       __       XXXXXX __ XXXXXX       __       XXXXXX __ XXXXXX       __       XXXXXX __ XXXXXX       __            |___ \
       __) |    XXXXX /##\ XXXXX      /##\      XXXXX /##\ XXXXX      /##\      XXXXX /##\ XXXXX      /##\      XXXXX /##\ XXXXX      /##\             __) |
      / __/     XXXXX \##/ XXXXX      \##/      XXXXX \##/ XXXXX      \##/      XXXXX \##/ XXXXX      \##/      XXXXX \##/ XXXXX      \##/            / __/
     |_____|    XXXXX /==\ XXXXX      /==\      XXXXX /==\ XXXXX      /==\      XXXXX /==\ XXXXX      /==\      XXXXX /==\ XXXXX      /==\           |_____|
                XXXX /####\ XXXX     /####\     XXXX /####\ XXXX     /####\     XXXX /####\ XXXX     /####\     XXXX /####\ XXXX     /####\
                XXX (######) XXX    (######)    XXX (######) XXX    (######)    XXX (######) XXX    (######)    XXX (######) XXX    (######)
        _                       XXXX (\=, XXXXXX       ()       XXXXXX () XXXXXX      _:_       XXXXXX () XXXXXX     (\=,       XXXXXXXXXXXXXXXX        _
       / |          |'-'-'-|    XXX //##.\ XXXXX       /\       XXX .-:--:-. XXX     '-.-'      XXXXXX /\ XXXXXX    //##.\      XXX |'-'-'-| XXX       / |
       | |          |######|    XX ((#\_##\ XXXX      //\\      XXXX \####/ XXXX     _.'._      XXXXX //\\ XXXXX   ((#\_##\     XXX |######| XXX       | |
       | |           |====|     XXX ))##`\_) XXX     (####)     XXXX {====} XXXX   |#######|    XXXX (####) XXXX    ))##`\_)    XXXX |====| XXXX       | |
       |_|           |####|     XX (/#####\ XXXX      )##(      XXXXX )##( XXXXX    \=====/     XXXXX )##( XXXXX   (/#####\     XXXX |####| XXXX       |_|
                     |####|     XXXX )###( XXXXX     /####\     XXXX /####\ XXXX     )###(      XXXX /####\ XXXX     )###(      XXXX |####| XXXX
                    (######)    XXX (#####) XXXX    (######)    XXX (######) XXX   (#######)    XXX (######) XXX    (#####)     XXX (######) XXX
                        _             ____             ____           ____            _____           _____            ____           _   _
                       / \           | __ )           / ___|         |  _ \          | ____|         |  ___|          / ___|         | | | |
                      / _ \          |  _ \          | |             | | | |         |  _|           | |_            | |  _          | |_| |
                     / ___ \         | |_) |         | |___          | |_| |         | |___          |  _|           | |_| |         |  _  |
                    /_/   \_\        |____/           \____|         |____/          |_____|         |_|              \____|         |_| |_|
```
