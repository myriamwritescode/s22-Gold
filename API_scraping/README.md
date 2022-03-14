This directory contains submodules:
- /congress
- /congress-legislators

All that means is that these are git repositories we are using within our 
project's repository.
We did not create them, we are using them.

Initially you will not be able to see the contents of these submodules on 
your local machine. For your future knowledge if you are ever cloning a 
repository with submodules, you can run <br>
(git clone --recurse-submodules https://github.com/...whatever...) <br>
That will do for you what we are about to do.

Obviously, the above command is not an option in this case since I added 
these submodules (repositories) after everyone had local clones of our 
project's repository.

So do this from the project's root directory (/s22-Gold): <br>
$ git submodule init <br>
This should display: <br>
Submodule 'API_scraping/congress' (git@github.com:unitedstates/congress.git) registered for path 'API_scraping/congress' <br>
Submodule 'API_scraping/congress-legislators' (git@github.com:unitedstates/congress-legislators.git) registered for path 'API_scraping/congress-legislators' <br>
Then run: <br>
$ git submodule update <br>
This should display something similar to: <br>
Cloning into '/home/brett/PycharmProjects/s22-Gold/API_scraping/congress'... <br>
Cloning into '/home/brett/PycharmProjects/s22-Gold/API_scraping/congress-legislators'... <br>
Submodule path 'API_scraping/congress': checked out 'c10772e3f33ec2d14f7eb442f8af8661e6a3b876' <br>
Submodule path 'API_scraping/congress-legislators': checked out '576f13132dddd7d2d33785722fc15081997bee78' <br>

That should give you the ability to access the contents of the submodules.
You will also need some tools to fully utilize the repositories they built. 
If you want to do that, let me know, I will help.