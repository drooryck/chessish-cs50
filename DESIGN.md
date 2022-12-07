INSTRUCTIONS: A “design document” for your project in the form of a Markdown file called DESIGN.md that discusses, technically, how you implemented your project and why you made the design decisions you did. Your design document should be at least several paragraphs in length. Whereas your documentation is meant to be a user’s manual, consider your design document your opportunity to give the staff a technical tour of your project underneath its hood.

(1500 words)

    DESIGN:

            Dries (worked a lot on frontend and some backend). Technical tour of project.

    HOW THINGS WORK:



Most of the information is documented and commented throughout our project files. To summarize:

We decided to build a website using HTML, CSS, Flask (with it, jinja) routing with Python, and backend with Javascript. We did this in part because it would make the most sense in creating the dynamic webapp we wanted to create, in having a navigable and user-friendly frontend with multiple things happening under the hood.

We took limited inspiration from the ways of working (and for the register and login feature, and password hashing) from our work on the Finance pset. Passing Session[“id”] through almost each get request allows us to display a Welcome message specific to each user. Apology messages were adjusted and used (see helpers.py).

We used Flask as a web framework and used python (in app.py) to build on what we knew from CS50 and implement novel Flask features such as dynamic routing. App.py is like a central hub taking in inputs through post requests, performing actions on them, and routing the user to the correct place thereafter. In history, for example, we used dynamic routing so that based on the /history/<username>, we could show different pages, by passing the username as an argument to an app.py function, which then used it for queries. For the simulate, Standard, and Chess960 pages, Javascript was used as a backend, which we will expand on later.

Our template .html files extend a general layout which creates a top Navbar, which we took from Bootstrap, and created custom styles for. We used a lot of jinja to factor out most things we needed for each page. Buttons from Bootstrap with “href” tags were also used, as were html forms for input. We thought it the current number of html files and different pages struck a good balance between different functionality and the factoring out (through layout.html).  Some other HTML tags we used were tables (for iterative information), img tags, and others as can be seen by inspecting the .html files.

CSS wise, we created a custom styles.css for certain color attributes, and then heavily modified existing Bootstrap elements to make our frontend look pretty. We wanted a sleek design and felt that bootstrap for js and css would be useful were. We also used css flexboxes to structure our features on the page in separate columns. Chessboard has its own CSS for the rendering of the chessboard on the screen, explained later.

We used a SQL database for storing all the information central to the application as a social network. SQL is something we were familiar with and excited about (I personally love database design).

A users table stores every users name and a unique id, as well as an optional Bio field.

A games table stores critical information about everyone’s past games, namely a primary key (which turned out to be useful to uniquely give an id tag to each entry in the History table so that these would properly copy, see history.html and the jinja used there), and the users id (a foreign key), the pgn of the game (which the js outputs), a timestamp (automatically inserted in the .db as TIMEDATE), the level of the ai played against, and whether the game was drawn, won by black or white.

A network table. This table has an active record of who is following who. It does this by having one relationship per row. The “follower” is the person who is following the “following” column, both of which fields are simply the id’s from the users table. Here is where we had an interesting design predicament. Though we initially wanted to go with a friends structure instead, the added difficulty of accepting and declining friend requests was almost impossible to get talking with our frontend. A network-style social structure turned out to be more feasible to implement (I personally spent 20 logged hours to attempt the friends structure before having a new idea) and just as fun. It provides more transparency in the end about the history of a user’s games, which generally is done on most current chess platforms for accountability and as an anti-cheat mechanism. The “status” field on the network table is a remnant of the friends structure.  All in all, the SQL was challenging to conceptualize, but very interesting to implement.

Our SQL queries are sanitized by borrowing the feature as used in the finance pset.

Our app.py runs commands on our SQL database through db.execute. It uses different queries to INSERT games, but also to retrieve information about a user’s friends and the like. Look at app.py to see our interesting queries. This information is then passed in the route along with the .html in render_template, which then jinja makes use of on the .html pages to render for example, a table of the history of games. Some SQL query commands go through Javascript, this design decision happened as we realized we needed information from Stockfish in the backend, so we settled on a mix of both python and js for the purpose of querying. The smallest of unresolved errors remains: the difficulty level in some edge cases logs 20 by default instead of 1-20 as based on input.

Importantly, we made sure that our frontend was pretty watertight in terms of security. We made sure to not pass hashed passwords to the frontend at all, even accidentally in a list of dicts such as “queried_user”. We made sure to sanitize inputs. And we made sure that we didn’t encounter server errors by always checking that input was valid and complete, and, if not, rendering an apology template with some specific instruction of what went wrong.



        WHERE THEY ARE STORED:



Our html is in a templates folder.
 css, and js is stored in a static folder (we needed to fenagle a lot with Jinja to get the directories to work well, see for example “{{ url_for('static', filename='chessboard-1.0.0.css') }}”.
App.py (mainframe), helpers.py, stock.py (stockfish chess ai), register. Js (warning alerts) chessish.db, and our .md files, are stored in the master folder.
Other files are byproducts of flask and imported libraries (chess.js for chess rule implementation).

            Roddie (did JS and chess AI integration, and backend):

enginegame.js

This file was the most challenging to conceptualize. The code here allows one to pass arguments from html in the form of input-accepting elements (for skill/time limits) as well as through events recorded via the chessboard “board” variable. The html elements have their values sent via “radio” or calling onClick functions, which then initialize and parse the values of the html inputs through JavaScript functions at the bottom of index.html. The newGame(); function helps communicate these to enginegame.js. The onDrop/onDragStart are examples of functions initated via the chessboard js object in the frontend, which are then interpreted through chessboard.js and finally activated in enginegame.js. The actual enginegame.js file communicates with stockfish.js through Uci protocol commands (which took hours to work with) and imported functions. All the player moves and settings are fed through this function, into stockfish.js which interacts directly with the stockfish API (programmed in C++, accessed non-locally). The stockfish API will then return a move through a Uci command, which is then interpreted in stockfish.js, returned to enginegame.js, and updated on the frontend via the updateStatus()/board.position() functions. The PGN exporting function is technically handled via this JS too, despite the code primarily being found in index.html. The PGN is exported using jinja and HTTP magic: the PGN element is returned from enginegame.js, sent to html via the Pgnexport function, set as the value of the “End Game” button, and instantly posted all within the button being pressed and the pgn being sent. Took a long time to figure that one out too. This file and associated HTML took me around 22 hours to work on based on my recorded working time.

simulate.js
A built-in chess pgn parser from the chess.js library is imported, the user input is checked and validated locally (via pgn.join) and sent to app.py via post, where it is then returned to the JavaScript as a jinja element. By far the hardest part of this file was figuring out how to get app.py to grab a value from front end and return it to the JS. The pgn is then iterated via a for loop with length of the pgn and a timeout function. Each time the pgn is iterated by one move, the position is updated and timer is set before the next move updates. The entire board is updated every time the loop is executed, via board.position()

chess960.js
This file uses a unique function called frcGen which gives a randomly generated board position from a seed (hence the inclusion of math.random to randomize the seed) and sets it as the starting position via chessboard.js. From there, user moves are communicated to the backend via chessboard.js functions such as onDragStart(); as with in enginegame.js

index.js
This codes for a random move generator, which was the first iteration of enginegame.js. This code so took a few hours to figure out, hence the inclusion of this file despite it being a less useful version of enginegame.js

To keep things clean to any user who stumbles upon our github, we have properly indented things and left many comments. The "problems" tab of a terminal mostly warns of deprecated things and things that don't conform to naming style, we solved all issues that arose there that were serious to the best of our ability.





As a last note, we to the very best of our ability cited wherever we used features implemented from somewhere else, or imported libraries, etc. We really did our best in documenting everything properly. A lot of googling went into this, and we take academic honesty very seriously. We affirm our commitment to the Honor Code.


Dries & Roddie