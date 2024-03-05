# https://orange3.readthedocs.io/projects/orange-development/en/latest/tutorial-settings.html
import os
import sys
import ntpath

from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output

from LTTL.Segmentation import Segmentation
from Orange.data import Domain, Table, StringVariable, ContinuousVariable, DiscreteVariable

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from AnyQt.QtWidgets import QApplication

from Orange.widgets.dev_workflow.HKH_execute_thread import ExecuteThread

from gpt4all import GPT4All


class OWChatbot(widget.OWWidget):
    name = "Chatbot"
    description = """Select a local language model (.gguf file) to process a text request ! 
    The Table "Parameters" contains the following columns :
    Max length | Temperature | Top K | Top P | Repeat penalty | Repeat last n | Batch size"""
    icon = "icons/chatbot.svg"
    priority = 10
    want_control_area = False
    signal = pyqtSignal()

    class Inputs:
        preprompt = Input("Pre-prompt", Segmentation, auto_summary=False)
        request = Input("Request", Segmentation, auto_summary=False)
        postprompt = Input("Post-prompt", Segmentation, auto_summary=False)
        parameters = Input("Parameters", Table)

    class Outputs:
        data = Output("Data", Table)

    class Error(widget.OWWidget.Error):
        load_model = widget.Msg("Could not load the model, was it a correct .gguf file ?")

    @Inputs.preprompt
    def set_preprompt(self, in_segmentation):
        self.preprompt = in_segmentation.to_string().split('content:\t"')[-1].split('"\n\tstr_index')[0]

    @Inputs.request
    def set_request(self, in_segmentation):
        self.request = in_segmentation.to_string().split('content:\t"')[-1].split('"\n\tstr_index')[0]

    @Inputs.postprompt
    def set_postprompt(self, in_segmentation):
        self.postprompt = in_segmentation.to_string().split('content:\t"')[-1].split('"\n\tstr_index')[0]

    @Inputs.parameters
    def set_parameters(self, in_table):
        try:
            max_tokens = int(in_table[0][in_table.domain.index("Max length")])
        except (ValueError, TypeError):
            max_tokens = 200
        try:
            temp = in_table[0][in_table.domain.index("Temperature")].value
        except (ValueError, TypeError):
            temp = 0.7
        try:
            top_k = int(in_table[0][in_table.domain.index("Top K")])
        except (ValueError, TypeError):
            top_k = 40
        try:
            top_p = in_table[0][in_table.domain.index("Top P")].value
        except (ValueError, TypeError):
            top_p = 0.4
        try:
            repeat_penalty = in_table[0][in_table.domain.index("Repeat penalty")].value
        except (ValueError, TypeError):
            repeat_penalty = 1.18
        try:
            repeat_last_n = int(in_table[0][in_table.domain.index("Repeat last n")])
        except (ValueError, TypeError):
            repeat_last_n = 64
        try:
            n_batch = int(in_table[0][in_table.domain.index("Batch size")])
        except (ValueError, TypeError):
            n_batch = 8
        self.parameters["max_tokens"] = max_tokens
        self.parameters["temperature"] = temp
        self.parameters["top_k"] = top_k
        self.parameters["top_p"] = top_p
        self.parameters["repeat_penalty"] = repeat_penalty
        self.parameters["repeat_last_n"] = repeat_last_n
        self.parameters["n_batch"] = n_batch

    def __init__(self):
        super().__init__()
        self.preprompt = "USER: "
        self.request = None
        self.postprompt = " ASSISTANT: "
        self.parameters = {"max_tokens": 200, "temperature": 0.7, "top_k": 40, "top_p": 0.4,
                           "repeat_penalty": 1.18, "repeat_last_n": 64, "n_batch": 8}
        self.llm = None

        self.thread = None
        self.current_answer = ""

        ### QT Management ###
        uic.loadUi(os.path.dirname(os.path.abspath(__file__)) + '/widget_designer/owchatbot.ui', self)
        self.setFixedWidth(571)
        self.setFixedHeight(468)
        self.setAutoFillBackground(True)

        self.pushbtn_selectModel = self.findChild(QtWidgets.QPushButton, "selectModel")
        self.label_selectedModel = self.findChild(QtWidgets.QLabel, "selectedModel")
        self.label_answer = self.findChild(QtWidgets.QPlainTextEdit, "answer")
        self.pushbtn_runLLM = self.findChild(QtWidgets.QPushButton, "runLLM")

        self.pushbtn_selectModel.clicked.connect(self.load_model)
        self.pushbtn_runLLM.clicked.connect(self.thread_query)


    def load_model(self):
        """Loads the selected model"""
        path = QtWidgets.QFileDialog.getOpenFileName(caption="Select a model")[0]
        try:
            self.llm = GPT4All(model_path=path,
                               model_name=path,
                               allow_download=False)
            model_name = ntpath.basename(path)
            self.label_selectedModel.setText(f"Model {model_name} successfully loaded !")
            self.Error.load_model.clear()
        except ValueError:
            self.label_selectedModel.setText(f"No model loaded")
            self.Error.load_model()


    def query(self):
        """Completes the input query"""
        prompt = self.preprompt + self.request + self.postprompt
        answer = self.llm.generate(prompt=prompt,
                                   max_tokens=self.parameters["max_tokens"],
                                   temp=self.parameters["temperature"],
                                   top_k=self.parameters["top_k"],
                                   top_p=self.parameters["top_p"],
                                   repeat_penalty=self.parameters["repeat_penalty"],
                                   repeat_last_n=self.parameters["repeat_last_n"],
                                   n_batch=self.parameters["n_batch"])
        self.create_output(answer)


    def thread_query(self):
        self.label_answer.setPlainText("")
        self.current_answer = ""
        self.thread = ExecuteThread(target=self.query_stream)
        self.thread.start()
        self.signal.connect(self.emit)


    def emit(self):
        self.label_answer.setPlainText(self.current_answer)


    def query_stream(self):
        """Completes the input query with streaming mode and a progress bar"""
        prompt = self.preprompt + self.request + self.postprompt
        answer = ""
        for token in self.llm.generate(prompt=prompt,
                                       max_tokens=self.parameters["max_tokens"],
                                       temp=self.parameters["temperature"],
                                       top_k=self.parameters["top_k"],
                                       top_p=self.parameters["top_p"],
                                       repeat_penalty=self.parameters["repeat_penalty"],
                                       repeat_last_n=self.parameters["repeat_last_n"],
                                       n_batch=self.parameters["n_batch"],
                                       streaming=True):
            self.current_answer += token
            self.signal.emit()
            self.label_answer.verticalScrollBar().setValue(self.label_answer.verticalScrollBar().maximum())
            # Insert progressbar here from current index --> max tokens
        self.create_output(answer)
        # self.thread.stop()


    def create_output(self, answer):
        """Creates an output Table to emit the answer"""
        request_domain = StringVariable(name="Request")
        answer_domain = StringVariable(name="Answer")
        domain = Domain([], metas=[request_domain, answer_domain])
        out_data = Table.from_list(domain=domain, rows=[[self.request, answer]])
        self.Outputs.data.send(out_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mon_objet = OWChatbot()
    mon_objet.show()

    mon_objet.handleNewSignals()
    app.exec_()
