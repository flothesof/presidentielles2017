import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ipywidgets import interact_manual, interact
from ipywidgets import Button, HBox, IntText, HTML, VBox
from IPython.display import display, clear_output
import os.path as op


def load_data(projects_path='../projets'):
    "Loads presidential candidates data."
    mlp = pd.read_csv(op.join(projects_path, 'marine_le_pen.csv'))
    mlp['proposition'].str.replace('^.\s', '')
    bh = pd.read_csv(op.join(projects_path, 'benoit_hamon.csv'))
    jlm = pd.read_csv(op.join(projects_path, 'jean_luc_melenchon.csv'))
    jlm['proposition'].dropna().str.replace("Nous proposons de réaliser les mesures suivantes\xa0:", '').replace('\xa0', '  ')
    em = pd.read_csv(op.join(projects_path, 'emmanuel_macron.csv'))
    ff = pd.read_csv(op.join(projects_path, 'francois_fillon.csv'))
    nda = pd.read_csv(op.join(projects_path, 'nicolas_dupont-aignan.csv'))
    candidates = [jlm, bh, em, ff, nda, mlp]
    candidate_labels = ['JLM', 'BH', 'EM', 'FF', 'NDA', 'MLP']
    return candidates, candidate_labels


class GUI:
    def __init__(self, candidate_labels, propositions):
        # internal vars
        self.header = '<p style="font-size: 150%;font-weight: 300;line-height: 1.39;margin: 0 0 12.5px;">{} <a target="_blank" href="{}">source</a></p>'
        self.candidate_labels = candidate_labels
        self.propositions = propositions
        self.choice = None
        self.clicked = dict(zip(self.candidate_labels, [False] * len(self.candidate_labels)))
        self.confusion_matrix = np.zeros((len(candidate_labels), len(candidate_labels)))
        
        # candidate buttons
        buttons = [Button(description=label) for label in self.candidate_labels]
        for b in buttons:
            b.on_click(self.on_button_clicked)
        hbox1 = HBox()
        hbox1.children = buttons
        self.buttons = buttons

        # scorebox and new_question button and confusion matrix
        self.scorebox = IntText(description='score', value=0)
        new_question = Button(description='nouvelle question !')
        new_question.on_click(self.create_new_question)
        confusion_matrix_button = Button(description='afficher matrice de confusion')
        confusion_matrix_button.on_click(self.show_confusion_matrix)
        hbox2 = HBox()
        hbox2.children = [self.scorebox, new_question, confusion_matrix_button]

        # proposition box
        self.html = HTML()

        # general layout
        vbox = VBox()
        vbox.children = [hbox1, hbox2, self.html]
        self.box = vbox

        # generate first question
        self.create_new_question()
        
    def create_new_question(self, b=None):
        clear_output()
        choice = np.random.randint(len(self.candidate_labels))
        self.choice = choice
        current_propositions = self.propositions[choice]
        n = current_propositions.shape[0]
        m = np.random.randint(n)
        self.html.value = self.header.format(current_propositions['proposition'][m],
                                             current_propositions['source'][m])
        for b in self.buttons:
            b.style.button_color = None
            self.clicked = dict(zip(self.candidate_labels, [False] * len(self.candidate_labels)))
        
    def on_button_clicked(self, b):
        clear_output()
        if not self.clicked[b.description]:
            if b.description == self.candidate_labels[self.choice]:
                self.scorebox.value += 1
                b.style.button_color = 'lightgreen'
                self.update_confusion_matrix(b.description, self.candidate_labels[self.choice])
            else:
                self.scorebox.value -= 1
                b.style.button_color = 'red'
                self.update_confusion_matrix(b.description, self.candidate_labels[self.choice])
        self.clicked[b.description] = True
        
    def update_confusion_matrix(self, clicked_label, true_label):
        "Updates confusion matrix with answer."
        clicked = self.candidate_labels.index(clicked_label)
        true = self.candidate_labels.index(true_label)
        self.confusion_matrix[true, clicked] += 1
        
    def show_confusion_matrix(self, b):
        classes = self.candidate_labels
        plt.imshow(self.confusion_matrix)
        plt.colorbar(label='nombre de réponses')
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)
        plt.ylabel('Vraie réponse')
        plt.xlabel('Ce que vous avez répondu')
        print(self.confusion_matrix)