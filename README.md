SEE YOUTUBE:
https://www.youtube.com/watch?v=A3BSOX9DwiE


Documentation for your project in the form of a Markdown file called README.md. This documentation is to be a user’s manual for your project. Though the structure of your documentation is entirely up to you, it should be incredibly clear to the staff how and where, if applicable, to compile, configure, and use your project. Your documentation should be at least several paragraphs in length. It should not be necessary for us to contact you with questions regarding your project after its submission. Hold our hand with this documentation; be sure to answer in your documentation any questions that you think we might have while testing your work.

(770 words)

Vision:
Our vision for Chessish was for it to be an interactive chess website which uses the open-source stockfish chess engine to allow human vs AI gameplay, with unique gamemodes setting it apart from existing websites.



Features:
Though our vision was very ambitious, our excitement and perseverance about the project meant we were able to go further than even our best-case implementation (A chess website with an AI opponent, multiple game modes, custom game modes and/or input position/start AI game or random game from position, complex UI options (rematch, select AI difficulty, randomize position), and UX features (piece animations)). All of these goals were achieved in the Play pages of Chessish. We simultaneously went in the direction of making Chessish a social platform, complete with a Networking feature to follow friends and the history of both your own and other people's games, and those games notations. We created a simulation tab where one could input a Portable Game Notation (PGN) text into a field and see move by move what transpired in that game. We made it possible to copy, from the clipboard, other user's games from their History and thus simulate those. We spent over 50 logged hours each, combined on the project



User guide:

3 METHODS FOR INITIAL SETUP

1)
The process for use is the following. It should normally work without issue.

You should unzip the Chess_Project folder, and should see a folder with different subfolders (_pycache, css, flask_session, node-modules, static, as well as app.py and a database). You should open this folder with VSCode. Then open a new terminal in VSCode. Navigate inside the master folder. Install Flask if you don't have it, by running "pip install Flask". Also pip install (cs50, flask_session, helpers) just in case. Install Python as an extension (if needed). Now execute “flask run” when in the master folder.

2)
**if flask run STILL does not work**
On one of our (4) computers, the directory was very buggy for some reason. Here, we needed to follow some extra steps. Try these, otherwise revert to method 3.
Run “python -m venv venv”
On Windows, run “venv/scripts/activate/”, on Linux/Mac, do “source venv/bin/activate”.
Then, pip install flask and the other programs as needed.
In some edge cases, one may need to bypass “powershell execution policies”, by running PowerSHell on your PC as an admin, running “Set-ExecutionPolicy -ExecutionPolicy RemoteSigned” and accepting changes (A).
Now, flask run should run as normal

3)
The third method (to play it safe in a controlled environment if all else fails) is to unzip the folder in a code50 space. This almost is guaranteed to work. One might need to pip install flask, however.





USERGUIDE FOR WHEN WEBSITE IS UP:

Follow the link in the new terminal you created to go to the website!!!
It will bring you to the login page. Since you don’t have an account yet, Register with a username and password and provide biographical information. Registering will automatically log you in. If you already have an account, you can log in. Of course, you can also log out. You will be greeted as you enter.

The homepage is where you can start a new chess game against an AI. The buttons allow you to change base time for the chess match, the increment of how much time you’ll gain with each move, and the skill level of the AI you’ll be playing against. New Game starts the timer. When you have finished your game, press End Game to have this game logged into your history.

Now visit the Chess960 tab. This tab allows you to play games in the Chess960 variant of the normal game of chess, giving users an interesting gamemode. This page is Pass-and-Play, as the Stockfish AI does not natively work with nonstandard games. Since there is no standardized notation for Chess960, these games are not logged to your history.

Visit the Simulate tab. You can input any PGN (a notation system for standard chess games) and the visual chessboard will simulate this game in a completely automated way. 

The history tab shows you whose History you are viewing, and gives you a complete table of the result of the game, the difficulty of ai they were playing against, the PGN (with an automated Copy to Clipboard button), and an automatic way to simulate that game in the simulate tab.

Head over to the Social tab. Under network, this is where you can see the people you are currently following. You can see their biographical information. And you can click on "See History" to access their game history tab. Follow and unfollow allow you to do exactly what they specify, removing and adding users to your network.

That’s the functionality of our website! All tabs work nicely together to form a cohesive project. Now for what happens under the hood, see the DESIGN.md page.


Dries & Roddie