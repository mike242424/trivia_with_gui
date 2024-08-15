import tkinter
import html
import requests

AMOUNT = 20
THEME_COLOR = '#314857'


class TriviaInterface:

    def __init__(self):
        self.data = self.get_questions()
        self.score = 0
        self.index = 0
        self.correct_answer = self.data[self.index]['correct_answer']
        self.current_question = html.unescape(self.data[self.index]['question'])

        self.window = tkinter.Tk()
        self.window.title('Trivia')
        self.window.config(height=1200, width=900, pady=20, bg=THEME_COLOR)

        self.score_label = tkinter.Label(self.window, text=f'Score: 0', bg=THEME_COLOR, font=('Arial', 20, 'bold'))
        self.score_label.grid(row=0, column=1)

        self.canvas = tkinter.Canvas(width=600, height=300, bg='white', highlightthickness=0)
        self.trivia_question = self.canvas.create_text(300, 150, text=self.current_question, fill='black', font=('Arial', 30), width=500)
        self.canvas.grid(row=1, column=0, columnspan=2, padx=20, pady=50)

        self.true_button = tkinter.Button(
            command=self.guess_true,
            text='✔',
            fg='green',
            font=('Arial', 30),
            border=0,
            highlightthickness=0,
            borderwidth=0,
            padx=50,
            pady=50)

        self.true_button.grid(row=2, column=0)

        self.false_button = tkinter.Button(
            command=self.guess_false,
            text='X',
            fg='red',
            font=('Arial', 30),
            border=0,
            highlightthickness=0,
            borderwidth=0,
            padx=50,
            pady=50
        )

        self.false_button.grid(row=2, column=1)

        self.window.mainloop()

    def get_questions(self):
        response = requests.get(f'https://opentdb.com/api.php?amount={AMOUNT}&'
                                f'&type=boolean')
        response.raise_for_status()
        return response.json()['results']

    def start(self):
        self.data = self.get_questions()
        self.index = 0
        self.score = 0
        self.score_label.config(text=f'Score: {self.score}')
        self.correct_answer = self.data[self.index]['correct_answer']
        self.current_question = html.unescape(self.data[self.index]['question'])
        self.canvas.itemconfig(self.trivia_question, text=self.current_question)

    def next_question(self):
        self.index += 1
        if self.index == len(self.data):
            self.start()
        else:
            self.correct_answer = self.data[self.index]['correct_answer']
            self.current_question = html.unescape(self.data[self.index]['question'])
            self.canvas.itemconfig(self.trivia_question, text=self.current_question)

    def guess_true(self):
        if self.correct_answer == 'True':
            self.score += 1
            self.score_label.config(text=f'Score: {self.score}')
            self.next_question()
        else:
            self.next_question()

    def guess_false(self):
        if not self.correct_answer == 'True':
            self.score += 1
            self.score_label.config(text=f'Score: {self.score}')
            self.next_question()
        else:
            self.next_question()
