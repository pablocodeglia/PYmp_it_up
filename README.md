## **Harvard's CS50X: Final Project**

### **Requirements**

The climax of this course is its final project. The final project is your opportunity to take your newfound savvy with programming out for a spin and develop your very own piece of software. So long as your project draws upon this course’s lessons, the nature of your project is entirely up to you. You may implement your project in any language(s). You are welcome to utilize infrastructure other than the CS50 Codespace. All that we ask is that you build something of interest to you, that you solve an actual problem, that you impact your community, or that you change the world. Strive to create something that outlives this course.
<br>
<br>

### **Video Demo**:

<https://youtu.be/142LD38WC0E>

### **Installation:**

- Install project dependencies by running pip install -r requirements.txt.
- Run the python program with command 'python main.py'. Optionally, an extra argument can be added to run a custom song:  
  i.e. **python main.py "303 - Turkey March"**
- Use the numpad '5' key to begin the song. The numpad keys 1,3,5,7,9 control the game.
- Press 'ESC' at any time during the song to go back to the main menu, and '5' on the score screen to play again.  
  <br>

### **Building tools:**

-Python  
-External libraries: PYgame, simfile, pyvidplayer.  
<br>

### **Project description: PYmp it up**

For my final project for CS50x, I aimed to replicate the functionality of the Rythm game emulator StepMania/StepF2, using python, specifically the PYgame module library.

The **main()** function consists of 3 functions, one for each of the following: Intro Screen ( **intro()** ), Main Game ( **play()** ), and the Score Screen ( **score_screen()** ).

The **intro()** function consists mainly of a video background, and it calls the **play()** function when the NUMPAD5 key is pressed.

The **play()** function handles most of the gameplay.
First, all the game settings such as screen size, fonts, and song-title are set-up. By default, the song loaded with the game is "We Are", but this can be overridden by running the game with the name of a song inside the **songs** folder, as an extra argument (i.e. **python main.py "303 - Turkey March"**)
Upon initializing the game, the .ssc file of the selected song is parsed with the help of the [Simfile library](https://simfile.readthedocs.io/en/main/), which gives us the data needed, such as all the notes sequence (and their release time), song delay (the time it takes between the start of the song and the first note), etc.

Once the mp3 song file has started, the ellapsed time is checked at every frame and, once it has reached the value of the 'Song.delay' variable, the first Note Class object is created. Then the 'Song.last_beat' variable is set as the sum of the current song time + 'Song.bps' (time difference between each note). Then at everyframe we loop through the notes generator, and when the current time matches a note, another Note Class object is spawned, until the song reaches its end.

The Note Class has functions that check wether the instance is overlapping the Hitbar (the bar on top of the screen) and, if it is and the proper key is hit, it updates the score, taking into consideration the precision of the hit. If it's a miss it also registers as such, and zeroes out the combo counter as well. At every hit or miss, a visual indicator of the grade and the combo amount pops-up in the center of the screen.

At anytime, by pressing the ESCAPE key, **main()** is called and the game resets.

When the mp3 file reaches the end, it calls the **score_screen()** function.

The **score_screen()** function plays a video background and displays all the hits/misses data stored in the **Song Class**, as well as calling the **Song.calc_points()** function, to calculate the total score points.

By pressing the NUMPAD5 key, **main()** is called and the game resets.

For both the Intro and Score Screen, the [PYVidPlayer](http://github.com/ree1261/pyvidplayer) library was used to display the background videos.

<br>

### **Files and directories**

- `pymp it up/` - Project directory.

  - `fonts/` - contains project typefaces.
  - `graphics/` - project visual files

    - `bg/` - contains background images
      - `bg_test_01.png` - fallback background.
    - `ui/` - contains all user interface graphics.
    - `video/` - contains all video backgrounds

      - `mission_bg.mp4` - score screen video background
      - `teaser.mpg` - intro screen background

    - `songs/` - songs folders, same hierarchy layout as Stepmania/StepF2 emulators

    - `admin.py` - Registers models access to Admin.
    - `apps.py` - Registers the main App.
    - `forms.py` - Contains all forms.
    - `models.py` - Contains all models.
    - `urls.py` - Contains all views URLs.
    - `views.py` - Contains all project views.

  - `templates/capstone` - contains all application templates.
