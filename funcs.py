import numpy as np
import pandas as pd
from ipywidgets import interact_manual, interact
from ipywidgets import Button, HBox, IntText, HTML, VBox
from IPython.display import display


def load_data():
    "Loads presidential candidates data."
    mlp = pd.read_csv('projets/marine_le_pen.csv')['proposition'].str.replace('^.\s', '')
    mlp.name = 'proposition'
    yj = pd.read_csv('projets/yannick_jadot.csv')['proposition'].str.replace(' →', '')
    bh = pd.read_csv('projets/benoit_hamon.csv')['proposition']
    bh.name = 'proposition'
    jlm = pd.read_csv('projets/jean_luc_melenchon.csv')['proposition'].dropna().str.replace("Nous proposons de réaliser les mesures suivantes\xa0:", '').replace('\xa0', '  ')
    jlm.name = 'proposition'
    em = pd.read_csv('projets/emmanuel_macron.csv')['proposition']
    ff = pd.read_csv('projets/francois_fillon.csv')['proposition']
    candidates = [jlm, yj, bh, em, ff, mlp]
    candidate_labels = ['JLM', 'YJ', 'BH', 'EM', 'FF', 'MLP']
    return candidates, candidate_labels

class GUI:
    def __init__(self, candidate_labels, propositions):
        # internal vars
        self.candidate_labels = candidate_labels
        self.propositions = propositions
        self.choice = None
        self.clicked = dict(zip(self.candidate_labels, [False] * len(self.candidate_labels)))

        # candidate buttons
        buttons = [Button(description=label) for label in self.candidate_labels]
        for b in buttons:
            b.on_click(self.on_button_clicked)
        hbox1 = HBox()
        hbox1.children = buttons
        self.buttons = buttons

        # scorebox and new_question button
        self.scorebox = IntText(description='score', value=0)
        new_question = Button(description='nouvelle question !')
        new_question.on_click(self.create_new_question)
        hbox2 = HBox()
        hbox2.children = [self.scorebox, new_question]

        # proposition box
        self.html = HTML()

        # general layout
        vbox = VBox()
        vbox.children = [hbox1, hbox2, self.html]
        self.box = vbox

        # generate first question
        self.create_new_question()
        
    def create_new_question(self, b=None):
        choice = np.random.randint(len(self.candidate_labels))
        self.choice = choice
        current_propositions = self.propositions[choice]
        n = current_propositions.size
        self.html.value = '<p style="font-size: 150%;font-weight: 300;line-height: 1.39;margin: 0 0 12.5px;">{}</p>'.format(current_propositions[np.random.randint(n)])
        for b in self.buttons:
            b.style.button_color = None
            self.clicked = dict(zip(self.candidate_labels, [False] * len(self.candidate_labels)))
        
    def on_button_clicked(self, b):
        if not self.clicked[b.description]:
            if b.description == self.candidate_labels[self.choice]:
                self.scorebox.value += 1
                b.style.button_color = 'lightgreen'
            else:
                self.scorebox.value -= 1
                b.style.button_color = 'red'

        self.clicked[b.description] = True