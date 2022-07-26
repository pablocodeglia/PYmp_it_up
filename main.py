import sys
from sys import exit

import pygame, time
from pygame import mixer

import simfile
from simfile.timing import TimingData
from simfile.notes import NoteData
from simfile.notes.timed import time_notes

from pyvidplayer import Video

def main():
    #START PYGAME

    pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.init()    

    pygame.font.init

    font = pygame.font.Font('fonts/What The FUN.otf', 24)

    # SETUP SCREEN
    global screen
    screen = pygame.display.set_mode((720,480))
    global screen_x 
    global screen_y
    screen_x, screen_y = screen.get_size()
    pygame.display.set_caption('PYMP IT UP')

    if len(sys.argv) == 2:
        print("with arg")
        song_title = sys.argv[1]
    else:
        song_title = "318 - We Are"
        print("without arg")
        print (song_title)       

    # 318 - We Are
    # 303 - Turkey March
    song = Song(song_title, screen)

    # BACKGROUND
    img_bg_surf = pygame.transform.scale((pygame.image.load(f'songs/{song.path}/{song.code}.PNG')), (screen.get_size()))
    # img_bg_surf = pygame.transform.scale((pygame.image.load(f'graphics/bg/bg_test_01.PNG')), (screen.get_size()))

    def intro():
        vid = Video("graphics/video/TEASER_2.mpg")
        vid.set_size((720,480))
        vid.restart()
        controllers_surf = pygame.image.load('graphics/ui/controls.png').convert_alpha()
        controllers_rect = controllers_surf.get_rect(center = (580,350))
        while True:
            key = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP5:
                        vid = Video("graphics/video/TEASER.mpg")

                        play(song_title, screen)
            
            vid.draw(screen, (0, 0), force_draw=False)
            
            pygame.display.update()

    def play(song_title, screen):
 
        notegrade_group = pygame.sprite.GroupSingle()
        notegrade_group.add(song.notegrade_display)

        # CREATE GROUP AND ADD HITBAR
        hitbar = HitBar() 
        hitbar_group = pygame.sprite.GroupSingle()
        hitbar_group.add(hitbar)

        # CREATE NOTES GROUP
        notes_group = pygame.sprite.Group()

        mixer.music.play()
        SONG_END = pygame.USEREVENT
        pygame.mixer.music.set_endevent(SONG_END)



        previous_time = time.time()
        while True:
            

            # CALC DELTA TIME
            dt = time.time() - previous_time
            previous_time = time.time()
            
            conductor_pos=(pygame.mixer.music.get_pos())
            # DELAYS BEGIN OF NOTES COUNT BY "SONG.DELAY"
            if conductor_pos > song.delay:

                if conductor_pos > song.last_beat:
                    time_notes_obj = time_notes(song.note_data, song.timing_data)
                    for timed_note in time_notes_obj:  
                        if (conductor_pos - song.bps/2) < float(timed_note.time)*1000 - song.extra_offset < (conductor_pos + song.bps/2):
                            song.spawn_note(timed_note.note.column, notes_group)
                            song.last_beat = conductor_pos + song.bps                

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        main()
                
                elif event.type == SONG_END:
                    score_screen()



            screen.blit(img_bg_surf,(0,0))

            hitbar_group.draw(screen)
            hitbar_group.update(dt)
            
            notes_group.draw(screen)
            notes_group.update(dt)

            notegrade_group.draw(screen)
            
            song.update_combo()

            pygame.display.update()

    def score_screen():
        
        # CREATE VIDEO STUFF
        vid = Video("graphics/video/MISSION_BG.MP4")
        vid.set_size((720,480))
        vid.restart()

        # CREATE SCORE SURFACES
        score_perfect = pygame.font.Font.render(font, str(song.score['perfect']), True, (255, 255, 255))
        score_great = pygame.font.Font.render(font, str(song.score['great']), True, (255, 255, 255))
        score_good = pygame.font.Font.render(font, str(song.score['good']), True, (255, 255, 255))
        score_bad = pygame.font.Font.render(font, str(song.score['bad']), True, (255, 255, 255))
        score_miss = pygame.font.Font.render(font, str(song.score['miss']), True, (255, 255, 255))
        score_max_combo = pygame.font.Font.render(font, str(song.max_combo), True, (255, 255, 255))
        score_total = pygame.font.Font.render(font, str(song.calc_points()), True, (255, 255, 255))



        while True:
            key = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP5:
                        main()
            vid.draw(screen, (0, 0), force_draw=False)
            screen.blit(score_perfect,(120,145))
            screen.blit(score_great,(120,173))
            screen.blit(score_good,(120,200))
            screen.blit(score_bad,(120,228))
            screen.blit(score_miss,(120,256))
            screen.blit(score_max_combo,(120,284))
            screen.blit(score_total,(120,311))
            pygame.display.update()

    intro()


class GradeDisplay(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/ui/score_perfect-01.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (0, 0))
        self.rect = self.image.get_rect(center = ((pygame.display.get_surface().get_width()/2),(pygame.display.get_surface().get_height()/2)))

    def update_notegrade(self, grade):
        
        self.image = pygame.image.load(f'graphics/ui/score_{grade}-01.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (192, 48))
        self.rect = self.image.get_rect(center = ((pygame.display.get_surface().get_width()/2),(pygame.display.get_surface().get_height()/2)))


class Song():
        def __init__(self, path, screen):
            self.path = path
            self.code = self.path[0:3]
            self.screen = screen

            self.songfile = simfile.open(f'songs/{self.path}/{self.path}.ssc')
            self.musicpath = f'songs/{self.path}/{self.code}.mp3'
            mixer.music.load(f'songs/{self.path}/{self.code}.mp3')

            self.last_beat = 0
            # 
            self.chart = self.songfile.charts[3]
            self.note_data = NoteData(self.chart)
            self.timing_data = TimingData(self.songfile)
            self.time_notes = time_notes(self.note_data, self.timing_data)

            self.bpm = self.timing_data.bpms[0].value
            self.bps = ((60/self.bpm)*1000)/2
            self.extra_offset = 1200
            self.delay = (self.timing_data.offset*1000)
            self.notegrade_display = GradeDisplay()
            self.points = {
                "perfect": 1200,
                "great": 800,
                "good":400,
                "bad":100,
                "miss":-300,
            }
            self.score = {
                "perfect": 0,
                "great": 0,
                "good":0,
                "bad":0,
                "miss":0,
            }
            self.max_combo = 0

            self.font_combo = pygame.font.Font('fonts/What The FUN.otf', 40)
            self.font_combo2 = pygame.font.Font('fonts/What The FUN.otf', 20)
            
            self.max_combo_text = pygame.font.Font.render(self.font_combo2, "COMBO", True, (232, 230, 230))
            self.max_combo_text_rect = self.max_combo_text.get_rect(center= (screen_x/2,screen_y/2+30))

        def __str__(self):
            return f"Song: {self.songfile.title}\n BPM: {self.bpm}\n BPS: {self.bps}\nOFFSET: {self.delay}\n {self.songfile.charts[1].description}" 

        def spawn_note(self, column, notes_group):
            if column == 0:
                notes_group.add(Note('bl_note', self))
            if column == 1:
                notes_group.add(Note('ul_note', self))
            if column == 2:
                notes_group.add(Note('c_note', self))
            if column == 3:
                notes_group.add(Note('ur_note', self))
            if column == 4:
                notes_group.add(Note('br_note', self))
        
        
        
        def calc_points(self):
            return sum(self.score[n] * self.points[n] for n in self.points)

        def update_combo(self):
            pass
            if self.max_combo > 1:
                self.screen.blit(self.max_combo_display,self.max_combo_display_rect)
                self.screen.blit(self.max_combo_text,self.max_combo_text_rect)

        def update_grade(self, grade):
            self.max_combo_display = pygame.font.Font.render(self.font_combo, str(self.max_combo), True, (230, 230, 230))
            self.max_combo_display_rect = self.max_combo_display.get_rect(center= (screen_x/2,screen_y/2+60))
            self.notegrade_display.update_notegrade(grade)
    

class HitBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/ui/BASE_01.png').convert_alpha()
        self.rect = self.image.get_rect(center = ((pygame.display.get_surface().get_width()/2),64))

        # LOADS "SPRITESHEET"
        hitbar_01 = pygame.image.load('graphics/ui/BASE_01.png').convert_alpha()
        hitbar_02 = pygame.image.load(f'graphics/ui/BASE_02.png').convert_alpha()
        self.frames=[hitbar_01, hitbar_02]
        
        self.animation_index = 0 
        self.image = self.frames[self.animation_index]
    
    def animation_state(self):
        self.animation_index += 0
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self,dt):
        self.animation_state()    


class Note(pygame.sprite.Sprite):
        def __init__(self,type_note,song):
            super().__init__()
            self.type_note = type_note
            self.song = song
            
            # INIT X/Y POS
            self.init_x = ((pygame.display.get_surface().get_width())/2)
            self.x_pos = self.init_x
            self.y_pos = ((pygame.display.get_surface().get_height())-48)

            # SPAWNS NOTES ON THE PROPER X_POS
            if self.type_note == 'bl_note':
                self.x_pos = (self.init_x - 100) 
            elif self.type_note == 'br_note':
                self.x_pos = (self.init_x + 100) 
            elif self.type_note == 'c_note':
                self.x_pos = (self.init_x) 
            elif self.type_note == 'ul_note':
                self.x_pos = (self.init_x - 49) 
            elif self.type_note == 'ur_note': 
                self.x_pos = (self.init_x + 49)    
            
            # LOADS "SPRITESHEET"
            note_01 = pygame.image.load(f'graphics/ui/{self.type_note}_01.png').convert_alpha()
            note_02 = pygame.image.load(f'graphics/ui/{self.type_note}_02.png').convert_alpha()
            note_03 = pygame.image.load(f'graphics/ui/{self.type_note}_03.png').convert_alpha()
            note_04 = pygame.image.load(f'graphics/ui/{self.type_note}_04.png').convert_alpha()
            note_05 = pygame.image.load(f'graphics/ui/{self.type_note}_05.png').convert_alpha()
            note_06 = pygame.image.load(f'graphics/ui/{self.type_note}_06.png').convert_alpha()
            self.frames=[note_01, note_02, note_03, note_04, note_05, note_06]
            
            self.animation_index = 0 
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(center = (self.x_pos,self.y_pos))
            self.pos = pygame.math.Vector2(self.rect.center)
            
            self.move_speed = 300            

        def animation_state(self, dt):
            self.animation_index += 10 * dt
            if self.animation_index >= len(self.frames): self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]

        def key_input(self):
            keys = pygame.key.get_pressed()
            # GET HEIGHT OF HITBAR, SO ONLY THOSE NOTES OVER ARE CHECKED
            if self.rect.bottom < 90:
                if keys[pygame.K_KP1]:
                    self.calc_grade()
                elif keys[pygame.K_KP3]:
                    self.calc_grade()
                elif keys[pygame.K_KP5]:
                    self.calc_grade()
                elif keys[pygame.K_KP7]:
                    self.calc_grade()
                elif keys[pygame.K_KP9]:
                    self.calc_grade()
            # IF IT REACHES THE TOP MISSES
            if self.rect.bottom < 0:
                self.calc_grade()               
        
        def calc_grade(self):
            # CALCULATE DIFFERENCE TO ASSESS STOMP TIMING
            pos_at_stomp = abs(self.rect.centery - 64)

            if pos_at_stomp < 8:
                self.song.score['perfect'] += 1
                self.song.update_grade('perfect')
            elif pos_at_stomp < 20:
                self.song.score['great'] += 1
                self.song.update_grade('great')
            elif pos_at_stomp < 35:
                self.song.score['good'] += 1
                self.song.update_grade('good')
            elif pos_at_stomp < 64:
                self.song.score['bad'] += 1
                self.song.update_grade('bad')
            self.song.max_combo += 1

            if pos_at_stomp > 64:
                self.song.max_combo = 0
                self.song.score['miss'] += 1
                self.song.update_grade('miss')
            
            self.kill()
            
            

        def update(self,dt):
            self.animation_state(dt)
            self.pos.y -= self.move_speed * dt
            self.rect.y = round(self.pos.y)
            self.key_input()

if __name__ == "__main__":
    main()
