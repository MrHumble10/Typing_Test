from random import *
from tkinter import *
from tkinter import TclError

sentences = ['One of the best way to eradicate any kind of corruption is selecting a well-educated candidate for the'
             ' cabinet',
             'The day is celebrated to highlight the problems of the girl child in these countries',
             'It is very sad that girl children are subjected to extreme neglect and disrespect, especially in '
             'underdeveloped countries',
             'The birth of a girl child is seen by parents as a cause of pity. They are deprived of proper nutrition, '
             'education, economic opportunities and social status or respect']
sentence = sentences[randint(0, 3)]

INCORRECT = 0
wpm = 0
CPW = 0
time = 60
stop = False


def app():

    def key_pressed(evt=None):
        input_entry.unbind('<Key>')

        timer_update()

    def timer_update():

        global time, stop
        stop_timer()

        try:

            if sentence.split(' ')[-1] == input_entry.get().split(' ')[-1]:
                stop = True

                get_input()
        except TclError:
            pass
        if not stop:

            time -= 1
            seconds.config(text=time)
            seconds.after(1000, timer_update)
        else:
            try:

                get_input()
            except TclError:
                pass

    def stop_timer():
        global stop
        if seconds['text'] == 0:
            stop = True


        # window.destroy()
        # sentence = sentences[randint(0, 3)]
        # app()

    def get_input():
        text_box.destroy()

        global wpm, INCORRECT, sentence, CPW
        entry_text = input_entry.get().upper().split(' ')
        sentence_text = sentence.upper().split(' ')
        y = 50
        idx = 0
        # print(entry_text, sentence_text)
        error = 0
        for word in entry_text:
            if sentence_text[idx] == word:
                CPW += len(word.strip())
                input_entry.delete(0, END)
            else:
                error += 1
                print(word)
                data = {
                    error: f'* Instead of "{sentence_text[idx].lower()}", you typed "{word.lower()}".'
                }
                for (value, key) in data.items():
                    y += 30
                    Label(text=key, bg='gray', fg='#8ECDDD', font=('Times New Roman', 12)).place(x=80, y=y)
            idx += 1

        if error == 0:
            Label(text='Well Done You did not have any mistake', bg='gray', fg='#8ECDDD',
                  font=('Times New Roman', 12)).place(x=80, y=y + 30)

        cpm_calculator()
        try:
            with open('record.csv', mode='r')as data:
                best_record = data.read()
        except FileNotFoundError:
            with open('record.csv', mode='w')as data:
                best_record = data.write('0')

        best_score = Label(text="Your Best:", fg='white', bg='gray', pady=15, padx=25)
        best_score.place(x=150, y=100)
        if int(best_record) > char_num['text']:
            best = Label(text=best_record, bg='gray', fg='#8ECDDD', padx=10)
            best.place(x=230, y=115)
        else:
            with open('record.csv', mode='w')as data:
                data.write(f'{char_num['text']}')
                best = Label(text=char_num['text'], bg='gray', fg='#8ECDDD', padx=10)
                best.place(x=230, y=115)

    def cpm_calculator():
        global wpm
        if seconds['text'] == 0:
            wpm = (CPW / 5)
            word_per_min['text'] = round(wpm)
        else:
            timing = (60 - seconds['text']) / 60
            wpm = (CPW / 5) / timing
            word_per_min['text'] = round(wpm)
            print((60-seconds['text']) / 60)

        input_entry.destroy()
        char_num['text'] = round(CPW / ((60 - seconds['text']) / 60))

        print(CPW)


    # creating a window
    window = Tk()
    window.geometry('500x380')
    window.config(bg='gray')
    corrected_label = Label(text="corrected CPM", fg='white', bg='gray', pady=15, padx=10)
    corrected_label.place(x=20, y=25)
    wpm_label = Label(text="WPM", fg='white', bg='gray', pady=15, padx=25)
    wpm_label.place(x=150, y=25)
    time_label = Label(text="Time Left", fg='white', bg='gray', pady=15)
    time_label.place(x=280, y=25)

    def reset():
        global sentence, time, INCORRECT, CPW, wpm, stop
        try:
            text_box.delete("0.1", END)
            input_entry.delete(0, END)
            sentence = sentences[randint(0, 3)]
            text_box.insert('1.0', chars=sentence)
            window.destroy()
            app()
        except TclError:
            INCORRECT = 0
            wpm = 0
            CPW = 0
            time = 60
            stop = False
            sentence = sentences[randint(0, 3)]
            window.destroy()
            app()
    reset_btn = Button(text='Reset', command=reset)
    reset_btn.place(x=430, y=38)

    char_num = Label(text='?', bg='white', padx=10)
    char_num.place(x=120, y=38)

    word_per_min = Label(text='?', bg='white', padx=10)
    word_per_min.place(x=220, y=38)

    seconds = Label(text='60', bg='white', padx=10)
    seconds.place(x=350, y=38)

    text_box = Text(width=55, bg='light blue', height=6, relief=SUNKEN, highlightthickness=3, font=('Times New Roman', 12),
                    yscrollcommand='3.0', highlightcolor='light blue', highlightbackground='light blue', wrap=WORD)
    text_box.insert('1.0', chars=sentence)
    text_box.place(x=25, y=100)

    input_entry = Entry(width=55, bg='light blue', relief=SUNKEN, highlightthickness=3, font=('Times New Roman', 12),
                        justify='center', highlightbackground='light blue', highlightcolor='light blue')

    input_entry.bind('<Key>', key_pressed)

    input_entry.place(x=25, y=223)

    window.mainloop()


app()
