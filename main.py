from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
import random
import pickle
import os.path

mainWindowManager = None
answers = None
game = None
exam = None
test_selected = 0


class MainScreen(Screen):

    yam_btn = ObjectProperty(None)
    equ_btn = ObjectProperty(None)
    mec_btn = ObjectProperty(None)

    def equ_select(self):
        global test_selected
        test_selected = 0
        self.ids['equ_btn'].background_color = 1.0, 0.0, 0.0, 1.0
        self.ids['yam_btn'].background_color = 1.0, 1.0, 1.0, 1.0
        self.ids['mec_btn'].background_color = 1.0, 1.0, 1.0, 1.0

    def yam_select(self):
        global test_selected
        test_selected = 1
        self.ids['equ_btn'].background_color = 1.0, 1.0, 1.0, 1.0
        self.ids['yam_btn'].background_color = 1.0, 0.0, 0.0, 1.0
        self.ids['mec_btn'].background_color = 1.0, 1.0, 1.0, 1.0

    def mec_select(self):
        global test_selected
        test_selected = 2
        self.ids['equ_btn'].background_color = 1.0, 1.0, 1.0, 1.0
        self.ids['yam_btn'].background_color = 1.0, 1.0, 1.0, 1.0
        self.ids['mec_btn'].background_color = 1.0, 0.0, 0.0, 1.0

    def switchsides(self, str):
        return str[::-1]

    def start_from_begin(self):
        global mainWindowManager
        mainWindowManager = self.parent
        show_config_pop()

    def start_from_saving(self):
        global mainWindowManager
        mainWindowManager = self.parent
        start_game()


class P(FloatLayout):
    def agreed(self):
        init_game()
        start_game()

    def switch_sides(self, str):
        return str[::-1]

class Help(FloatLayout):
    global test_selected
    help_img = ObjectProperty(None)
    page_num = 1
    test = "yam"

    def next_page(self):
        if self.page_num < 9:
            self.page_num += 1
        page_help = "Gen_Pages/h_" + str(self.test) + str(self.page_num) + ".png"
        if os.path.isfile(page_help):
            self.help_img.source = page_help

    def prev_page(self):
        if self.page_num > 1:
            self.page_num -= 1
        page_help = "Gen_Pages/h_" + str(self.test) + str(self.page_num) + ".png"
        if os.path.isfile(page_help):
            self.help_img.source = page_help

    def switch_sides(self, str):
        return str[::-1]

class Full(FloatLayout):
    global test_selected
    full_img = ObjectProperty(None)
    page_num = 1
    test = "yam"

    def next_page(self):
        if test_selected != 1:
            self.test = ""
        lead_zero = ""
        if self.page_num < 57:
            self.page_num += 1
        if self.page_num < 10:
            lead_zero = "0"
        page_full = "Gen_Pages/f_" + str(self.test) + "-" + lead_zero + str(self.page_num) + ".png"
        if os.path.isfile(page_full):
            self.full_img.source = page_full

    def prev_page(self):
        if test_selected != 1:
            self.test = ""
        lead_zero = ""
        if self.page_num > 1:
            self.page_num -= 1
        if self.page_num < 10:
            lead_zero = "0"
        page_full = "Gen_Pages/f_" + str(self.test) + "-" + lead_zero + str(self.page_num) + ".png"
        if os.path.isfile(page_full):
            self.full_img.source = page_full

    def switch_sides(self, str):
        return str[::-1]

def init_game():
    global exam
    global game
    global answers
    global test_selected

    answer_file = "Files/a_equ.txt"

    if test_selected == 1:
        answer_file = "Files/a_yam.txt"
    elif test_selected == 2:
        answer_file = "Files/a_mec.txt"

    with open(answer_file, 'r', encoding='utf8') as f:
        ans = f.read()

    answers = {}
    sum = [1, 31, 61, 91, 121, 151, 181]
    num = [0, 0, 0, 0, 0, 0, 0]
    if test_selected == 1:
        sum = [1, 61, 121, 181, 241, 301, 361]
        num = [0, 0, 0, 0, 0, 0, 0]
    elif test_selected == 2:
        sum = [1, 46, 91, 136]
        num = [0, 0, 0, 0]
    index = 0
    for a in ans.split('\n'):
        if test_selected == 0:
            for b in a.split()[::2][::-1]:
                if b == 'א':
                    b = 'a'
                elif b == 'ב':
                    b = 'b'
                elif b == 'ג':
                    b = 'c'
                elif b == 'ד':
                    b = 'd'

                answers.update({num[index] + sum[index]: b})
                num[index] += 1
                index = (index + 1) % 7
        elif test_selected == 1:
            for b in a.split()[::2][::-1]:
                if b == 'א':
                    b = 'a'
                elif b == 'ב':
                    b = 'b'
                elif b == 'ג':
                    b = 'c'
                elif b == 'ד':
                    b = 'd'

                answers.update({num[index] + sum[index]: b})
                num[index] += 1
                index = (index + 1) % 7
        else:
            for b in a.split()[1::2]:
                if b == 'א':
                    b = 'a'
                elif b == 'ב':
                    b = 'b'
                elif b == 'ג':
                    b = 'c'
                elif b == 'ד':
                    b = 'd'

                answers.update({num[index] + sum[index]: b})
                num[index] += 1
                index = (index + 1) % 4

    quest_file = "Files/q_equ.txt"

    if test_selected == 1:
        quest_file = "Files/q_yam.txt"
    elif test_selected == 2:
        quest_file = "Files/q_mec.txt"

    with open(quest_file, 'r', encoding='utf8') as f:
        q = f.read()

    exam = {}
    cur_q = None
    for a in q.split('\n'):
        split = a.split()
        if split == []:
          continue
        elif split[0][0].isdigit() > 0:
            print(split[0])
            split[0] = split[0].replace('.', '')
            split[1] = split[1].replace('.', '')
            l = [int(s) for s in split if s.isdigit()]
            exam[l[0]] = {
                'q': ' '.join(split[1:]),
                'opts': {},
                'ans': answers[l[0]]
            }

            cur_q = l[0]
        else:
            op = split[0][0]
            if op == 'א':
                op = 'a'
            elif op == 'ב':
                op = 'b'
            elif op == 'ג':
                op = 'c'
            elif op == 'ד':
                op = 'd'

            exam[cur_q]['opts'][op] = ' '.join(split[1:])
            print(exam[cur_q]['opts'][op])
    game = {}
    for key in exam.keys():
        game[key] = {'success_count': 0}

        save_game()


def save_game():
    global exam
    global game
    global answers
    global test_selected

    if test_selected == 0:
        exam_txt = 'Files/' + 'equ' + '_save_exam.pickle'
        game_txt = 'Files/' + 'equ' + '_save_game.pickle'
        answers_txt = 'Files/' + 'equ' + '_save_answers.pickle'
    elif test_selected == 1:
        exam_txt = 'Files/' + 'yam' + '_save_exam.pickle'
        game_txt = 'Files/' + 'yam' + '_save_game.pickle'
        answers_txt = 'Files/' + 'yam' + '_save_answers.pickle'
    else:
        exam_txt = 'Files/' + 'mec' + '_save_exam.pickle'
        game_txt = 'Files/' + 'mec' + '_save_game.pickle'
        answers_txt = 'Files/' + 'mec' + '_save_answers.pickle'
    with open(exam_txt, 'wb') as f:
        pickle.dump(exam, f)
    with open(game_txt, 'wb') as f:
        pickle.dump(game, f)
    with open(answers_txt, 'wb') as f:
        pickle.dump(answers, f)


def start_game():
    global mainWindowManager
    load_game()
    mainWindowManager.current = 'SecondScreen'


def load_game():
    global exam
    global game
    global answers
    if test_selected == 0:
        exam_txt = 'Files/' + 'equ' + '_save_exam.pickle'
        game_txt = 'Files/' + 'equ' + '_save_game.pickle'
        answers_txt = 'Files/' + 'equ' + '_save_answers.pickle'
    elif test_selected == 1:
        exam_txt = 'Files/' + 'yam' + '_save_exam.pickle'
        game_txt = 'Files/' + 'yam' + '_save_game.pickle'
        answers_txt = 'Files/' + 'yam' + '_save_answers.pickle'
    else:
        exam_txt = 'Files/' + 'mec' + '_save_exam.pickle'
        game_txt = 'Files/' + 'mec' + '_save_game.pickle'
        answers_txt = 'Files/' + 'mec' + '_save_answers.pickle'
    with open(exam_txt, 'rb') as f:
        exam = pickle.load(f)
    with open(game_txt, 'rb') as f:
        game = pickle.load(f)
    with open(answers_txt, 'rb') as f:
        answers = pickle.load(f)

    if game is None:
        init_game()


def switch_sides(str):
    return str[::-1]


def show_config_pop(flag=True):
    show = P()

    popup_window = Popup(title=switch_sides("האם אתה בטוח?"),
                        title_font="Fonts/VarelaRound-Regular",
                        title_align="center",
                        content=show,
                        size_hint=(None,None), size=(400,400))

    popup_window.open()


class SecondScreen(Screen):
    try_title = ObjectProperty(None)
    quest_title = ObjectProperty(None)
    ans1 = ObjectProperty(None)
    ans2 = ObjectProperty(None)
    ans3 = ObjectProperty(None)
    ans4 = ObjectProperty(None)
    global game
    global exam
    global answers
    num_of_q = 0
    correct = 0
    q, val = None, None
    q_stock = []
    correct_live = 0
    curr_ans = 0

    def enter(self):
        self.next_quest()

    def next_quest(self, spec_question=0):
        global game
        global exam
        global answers
        global mainWindowManager
        self.num_of_q = len(game.keys())

        for k, v in game.items():
            self.correct_live += v['success_count']
        if exam == {}:
            popup = Popup(title=(self.switch_sides('סטטוס')),
                          title_font="Fonts/VarelaRound-Regular",
                          title_align="center",
                          content=Label(text=self.switchsides('סיימת את המשחק!'),
                                        font_name="Fonts/VarelaRound-Regular",
                                        halign="center"),
                          size_hint=(None, None), size=(400, 400))

            popup.open()
            mainWindowManager.current = 'MainScreen'
        else:
            if self.q is not None:
                self.q_stock.append(self.q)
            if spec_question != 0:
                self.q, self.val = list(exam.items())[self.q - 1]
            else:
                self.q, self.val = random.choice(list(exam.items()))

            print(self.q)

            self.ans1.text = "a"
            self.ans2.text = "b"
            self.ans3.text = "c"
            self.ans4.text = "d"
            self.try_title.text = self.switch_sides('{0} of 2'.format(game[self.q]['success_count']))
            self.quest_title.text = '{0} - {1}'.format(self.q, self.switch_sides(self.val['q']))
            for k, opt in self.val['opts'].items():
                if k == 'a':
                    self.ans1.text = self.switch_sides('{0} - {1}'.format(k, opt))
                    print(self.ans1.text)
                if k == 'b':
                    self.ans2.text = self.switch_sides('{0} - {1}'.format(k, opt))
                    print(self.ans2.text)
                if k == 'c':
                    self.ans3.text = self.switch_sides('{0} - {1}'.format(k, opt))
                    print(self.ans3.text)
                if k == 'd':
                    self.ans4.text = self.switch_sides('{0} - {1}'.format(k, opt))
                    print(self.ans4.text)

            self.curr_ans = self.val['ans']

    def switch_sides(self, str):
        return str[::-1]

    def show_help(self):
        show = Help()

        popup_window = Popup(title=switch_sides("חומר עזר"),
                             title_font="Fonts/VarelaRound-Regular",
                             title_align="center",
                             content=show,
                             size_hint=(None, None), size=(800, 800))

        popup_window.open()

    def show_full_test(self):
        show = Full()

        popup_window = Popup(title=switch_sides("המבחן המלא"),
                             title_font="Fonts/VarelaRound-Regular",
                             title_align="center",
                             content=show,
                             size_hint=(None, None), size=(800, 800))

        popup_window.open()

    def show_img_quest(self):
        global test_selected
        test_type = "equ"
        if test_selected == 1:
            test_type = "yam"
        elif test_selected == 2:
            test_type = "mec"
        quest_txt = f"images/{test_type}_q{self.q}.png"
        if os.path.isfile(quest_txt):
            popup = Popup(title=(self.switch_sides('תמונת שאלה')),
                          title_font="Fonts/VarelaRound-Regular",
                          title_align="center",
                          content=Image(source=quest_txt),
                          size_hint=(None, None), size=(600, 400))

            popup.open()
        else:
            popup = Popup(title=(self.switch_sides('תמונת שאלה')),
                          title_font="Fonts/VarelaRound-Regular",
                          title_align="center",
                          content=Label(text=self.switch_sides('לא זמין בעבור שאלה זו'),
                                        font_name="Fonts/VarelaRound-Regular",
                                        halign="center"),
                          size_hint=(None, None), size=(400, 400))

            popup.open()

    def status(self):
        text = ('סיימת כבר ' + self.switch_sides(str(self.correct)) + ' שאלות ' +
            'בצורה נכונה. נשארו ' + self.switch_sides(str(self.num_of_q - self.correct)) + '\n' +
            self.switch_sides(str(self.correct_live)) + ' נענו נכונה')
        popup = Popup(title=(self.switch_sides('סטטוס')),
                      title_font="Fonts/VarelaRound-Regular",
                      title_align="center",
                      content=Label(text=self.switch_sides(text),
                                    font_name="Fonts/VarelaRound-Regular",
                                    halign="center"),
                      size_hint=(None, None), size=(400, 400))

        popup.open()

    def prev_question(self):
        if self.q_stock:
            self.q = self.q_stock.pop()
            self.next_quest(self.q)

    def save(self):
        save_game()
        popup = Popup(title=(self.switch_sides('שמירה')),
                      title_font="Fonts/VarelaRound-Regular",
                      title_align="center",
                      content=Label(text=self.switch_sides('המשחק נשמר!'),
                                    font_name="Fonts/VarelaRound-Regular",
                                    halign="center"),
                      size_hint=(None, None), size=(400, 400))

        popup.open()

    def skip_question(self):
        self.next_quest()

    def answer1_clicked(self):
        self.check_answer('a')

    def answer2_clicked(self):
        self.check_answer('b')

    def answer3_clicked(self):
        self.check_answer('c')

    def answer4_clicked(self):
        self.check_answer('d')

    def check_answer(self, ans_char):
        global answers
        global exam
        global game
        if ans_char == self.curr_ans:
            text = "כל הכבוד!"
            self.correct_live += 1
            game[self.q]['success_count'] += 1
            if game[self.q]['success_count'] == 2:
                game.pop(self.q)
                exam.pop(self.q)
                answers.pop(self.q)
                self.correct += 1
        else:
            if len(self.val['opts']) == 4:
                text = "{0} - {1}".format(
                        answers[self.q], self.val['opts'][answers[self.q]]
                    ) + '\n' + 'התשובה הנכונה היא:' + '\n' + "טעות!" + '\n\n\n' + "התשובה לשאלה מספר {0}".format(self.switch_sides(str(self.q)))
            else:
                text = "{0}".format(
                    answers[self.q]
                    ) + '\n' + 'התשובה הנכונה היא:' + '\n' + "טעות!" + '\n\n\n' + "התשובה לשאלה מספר {0}".format(self.switch_sides(str(self.q)))

            self.correct_live -= game[self.q]['success_count']
            game[self.q]['success_count'] = 0

        popup = Popup(title=(self.switch_sides('תוצאה')),
                      title_font="Fonts/VarelaRound-Regular",
                      title_align="center",
                      size=(400, 400),
                      size_hint=(None, None),
                      content=Label(text=self.switch_sides(text),
                                    font_name="Fonts/VarelaRound-Regular",
                                    text_size=(self.width /2, self.height /2),
                                    valign= 'middle',
                                    halign="center"),
                      )

        popup.open()
        self.next_quest()


class WindowManager(ScreenManager):
    pass


with open("my.kv", encoding='utf8') as f:
    kv = Builder.load_string(f.read())


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
