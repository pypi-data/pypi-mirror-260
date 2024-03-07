from collections import UserDict
import random
from threading import Timer


class GameLevel:

    def __init__(self, game_ui):
        self.game_ui = game_ui
        self.input_text: str = ''
        self.data: UserDict = UserDict()
        self.start()

    def start(self):
        pass

    def end(self):
        pass

    def on_key_press(self, c: str):
        raise NotImplemented()
    
    def on_key_del(self):
        self.input_text = self.input_text[:-1]


class Level1(GameLevel):

    def on_key_press(self, c: str):
        self.input_text += c


class Level2(GameLevel):

    def on_key_press(self, c: str):
        self.input_text += c + '_'


class Level3(GameLevel):

    def on_key_press(self, c: str):
        self.input_text = c + self.input_text


class Level4(GameLevel):

    def on_key_press(self, c: str):
        if len(self.input_text) == 3:
            self.input_text = c + self.input_text
        else:
            self.input_text += c


class Level5(GameLevel):

    def on_key_press(self, c: str):
        if c == 'k':
            c = 't'
        elif c == 't':
            c = 'k'
        self.input_text += c


class Level6(GameLevel):

    def start(self):
        self.data.nb_key_press = 0

    def on_key_press(self, c: str):
        if self.data.nb_key_press % 5 == 0:
            self.input_text += c
        self.data.nb_key_press += 1


class Level7(GameLevel):

    def on_key_press(self, c: str):
        if len(self.input_text) == 3:
            if c == 'k':
                self.input_text += 't'
            elif c == 'n':
                self.input_text += 'k'
            else:
                self.input_text = ''
        else:
            self.input_text += c


class Level8(GameLevel):

    def on_key_press(self, c: str):
        c = chr(ord(c)-1)
        self.input_text += c


class Level9(GameLevel):

    def on_key_press(self, c: str):
        c = chr(ord(c)+random.randint(1, 5))
        self.input_text += c


class Level10(GameLevel):

    def on_key_press(self, c: str):
        k = ord(c)
        if 96 <= k <= 96+26:
            k -= 96
            self.input_text = str(k)
        else:
            self.input_text += c
            self.input_text = self.input_text.replace('21', 'u').replace('11', 'k').replace('6', 'f').replace('3', 'c')


class Level11(GameLevel):

    def start(self):
        lyrics = ("Look inside,Look inside your tiny mind,Now look a bit harder,'Cause we're so uninspired,So sick and "
                  "tired of all the hatred you harbor,So you say,It's not okay to be gay,Well, I think you're just "
                  "evil,You're just some racist who can't tie my laces,Your point of view is medieval,Fuck you ,"
                  "Fuck you very, very much,'Cause we hate what you do,And we hate your whole crew,So, please don't "
                  "stay in touch,Fuck you ,Fuck you very, very much,'Cause your words don't translate,"
                  "And it's getting quite late,So, please don't stay in touch,Do you get,Do you get a little kick out "
                  "of being small-minded?,You want to be like your father,It's approval you're after,Well, "
                  "that's not how you find it,Do you,Do you really enjoy living a life that's so hateful?,"
                  "'Cause there's a hole where your soul should be,You're losing control a bit,And it's really "
                  "distasteful,Fuck you ,Fuck you very, very much,'Cause we hate what you do,And we hate your whole "
                  "crew,So, please don't stay in touch,Fuck you ,Fuck you very, very much,'Cause your words don't "
                  "translate,And it's getting quite late,So, please don't stay in touch,Fuck you, fuck you, fuck you,"
                  "Fuck you, fuck you, fuck you,Fuck you,You say,You think we need to go to war,Well, you're already "
                  "in one,'Cause it's people like you that need to get slew,No one wants your opinion,Fuck you ,"
                  "Fuck you very, very much,'Cause we hate what you do,And we hate your whole crew,So, please don't "
                  "stay in touch,Fuck you ,Fuck you very, very much,'Cause your words don't translate,"
                  "And it's getting quite late,So, please don't stay in touch,Fuck you ,Fuck you ,Fuck you ,"
                  "Fuck you ,Fuck you")
        self.input_text = 'Lily Allen - Fuck you'
        self.data.sentences = lyrics.lower().split(',')
        self.data.i_sentence = 0
        self.t = Timer(3.0, self.loop)
        self.t.start()

    def end(self):
        self.t.cancel()

    def on_key_press(self, c: str):
        pass

    def loop(self):
        sentence = self.data.sentences[self.data.i_sentence]
        self.input_text = sentence
        if self.data.i_sentence < len(self.data.sentences) - 1:
            self.data.i_sentence += 1
        else:
            self.data.i_sentence = 0
        self.game_ui.refresh_screen()

        self.t = Timer(2.0, self.loop)
        self.t.start()      
        

class Level12(GameLevel):

    def start(self):
        self.data.str = ''

    def on_key_press(self, c: str):
        self.data.str += c
        if len(self.input_text) >= 4 and self.input_text[-4:] == '****':
            self.input_text = self.input_text[:-4] + self.data.str[-4] + '****'
        else:
            self.input_text += '*'

    def on_key_del(self):
        self.input_text = self.input_text[:-1]
        self.data.str = self.data.str[:len(self.input_text)-1]


dispatcher = {
    1: Level1,
    2: Level2,
    3: Level3,
    4: Level4,
    5: Level5,
    6: Level6,
    7: Level7,
    8: Level8,
    9: Level9,
    10: Level10,
    11: Level11,
    12: Level12,
}
