"""
FUC maker chat messages versions
"""

from pyidebug import debug

# Evidence ILO and Syllabus
# Evidence of the each syllabus topics coherence with the previous ILOs topics:
# - ILO1 relates to S1 and S3, emphasizing the importance of understanding internal organization for logical functions.
# - ILO2 connects to S2, delving into digital representation and its significance in studying a didactic architecture.
# - ILO3 ties to S3 and S6, highlighting logical functions' role in arithmetic circuits.
# - ILO4 correlates with S4, emphasizing the study of a didactic architecture.
# - ILO5 links to S5, exploring the architecture of a processor.
# - ILO6 relates to S6 and S7, delving into arithmetic and sequential circuits' interplay.
# - ILO7 connects to S7 and S8, showcasing the relationship between sequential circuits and the memory system.
# - ILO8 ties to S8 and S9, emphasizing the importance of memory systems in input/output peripherals.
# - ILO9 links to S9, focusing on input/output peripherals and their significance.
# Summary:
# A) ILO1 -> S1, S3
# B) ILO2 -> S2
# C) ILO3 -> S3, S6
# D) ILO4 -> S4
# E) ILO5 -> S5
# F) ILO6 -> S6, S7
# G) ILO7 -> S7, S8
# H) ILO8 -> S8, S9
# I) ILO9 -> S9

# =========================
# Suggestion to assessments
# =========================
# The distribution of assessments over the course should be structured as follows:
# - Two exams, each accounting for 15% of the total grade, to assess understanding of digital representation of information, logical functions, architecture of a processor, arithmetic circuits, and memory system.
# - Weekly quizzes, contributing 5% each to the final grade, to evaluate knowledge on internal organization of a computer, study of a didactic architecture, sequential circuits, and input/output peripherals.
# - Bi-weekly individual assignments, worth 10% each, focused on practical applications and problem-solving related to the topics covered.


PEDAGOGICAL_MODEL = """
We are Polytechnic Institute with bachelor's degrees. The total contact hours for this course is about {contactHours} hours, the ECTS equal {ECTS}, and the estimated total working hours are around {workingHours}.
"""
#  The tutorial must have until 4 hours to Mathematics and fundamental curricular units, and until 8 hours to applied curricular units.

#"PARA FUCs 1º NA: Mencionar Supera-te. Metodologias Ativas: Aprendizagem cooperativa. "

PROMPT_DEFAULT = {
    "system": "You are world class technical documentation writer.\
        Optimize your answer like a Engenieer.\
        Calculate the number of characters typed after your answer including whitespace, punctuations and breaklines.\
        Review your text grammar with Grammarly web tool.\
        Display answer in bullet list whenever possible.\
        Avoid using line breaks in your answer.",
    "user": "{input}",
}


CHAT_MESSAGES = {
    1.0: {# ILO and Evidence OK, but Teaching Methodologies nope
        "importantTopics": [
            # ("Syllabus",
            #     "provide optimization of the the syllabus program",
            #     "in a bullet list",
            #     "If able, to "),

            ("Contact hours",
                "divide the contact hours into the following teaching typologies:\
                theoretical (T), theoretical-practical (TP), laboratory (LP), and tutorial(TO).",
                "specify number of hours to teaching typologies and display it on table",
                "estimate the number of hours of each tipologies to each syllabus topics",
                "optimize your answer and display it on table (shorten the syllabus topics description)"),

            ("Intended learning outcomes (ILOs)",
                "use the Bloom's taxonomy verbs to develop your answer in a hidden way",
                "display answer in a list such as ILO<number>: ",
                "don't quote syllabus topic",
                "don't quote verbs",
                #"be brief",
                "review and optimize your answer",
                "join the topics of the same category",
                "review and optimize your answer"),

            ("Evidence of the each syllabus topics and subtopics coherence with the ILOs topics",
                "think hard and relate each ILOs topics to, one or more, syllabus topics",
                "use verbs such as connects, relate, corresponds and link",
                "be brief and coherent in your words",
                "don't quote syllabus topics description",
                #"show answer in a bullet list",
                "review and optimize your answer citing only respective topics numbers",
                #"cover necessarily all ILOs",
                #"display answer in summarized bullet list",
                "attach to your answer a summary using only letters and numbers",
                "like that S<topic number> and ILO<ILO number>", 
                "display it as ILO<number> -> S<number> in a vertical bullet list"),

            ("Teaching Methodologies (TMs) and specific learning of this curricular unit",
                "include TMs for the tipologies: theoretical (T), theoretical-practical (TP), laboratory (LP) and tutorial(TO) to contact lecturer and student and specify how to",
                #"specify how for autonomous student time to study and ",
                "specify how students can study independently, complementing lessons with the teacher",
                "cite digital technology applications that could be used in TMs by lecturer",
                "associate syllabus topics to your specifc learning",
                "display answer in a list such as TM<number>: <content>",
                "review and optimize your answer"),

            ("Assessments",
                "Between types: exams, tests, quizzes, individual, group work, debates and others, which are the most suitable for this curricular unit",
                "Articulate your answer with the pedagogical model",
                "Based on syllabus",
                "Distribute percents to each assessment",
                "Group assessments must not exceed 40% of the assessment total",
                "Specifying how to lecturer distribute assessments over the course",
                "Tell me if final exam is recommended or not",
                "Summarize your answer in a bullet list"),

            ("Evidence of the your TM and assessments suggestions coherence with you ILO topics suggestion",
                "link each ILOs number to respectives TMs and assessment",
                #"optimize your answer quoting ILOs numbers",
                "display answer in a summarized bullet list",
                "attach to your answer a summary using only letters and numbers",
                "like that ILO<topic number> and TM<TM number>", 
                #"display it as ILO<number> -> S<number> in a vertical bullet list",
                ),

            ("Suggest current and relevant books to this curricular unit",
                "display bibliography in APA style",
                "sort this bibliographies by relevancy",
                "split bibliographies in fundamentals and complementary",
                "Consider until two complementary bibliographies",
                "After your bibliography suggestion, show me a bullet list with which of these books the each syllabus topics are found, quoting only the author book surname in parenthesis.",
                "Don't forget: display bibliography in APA style",),

            # ("Observations",
            #     # "Summary of key Concepts/topics of the course; reference to ECTS,  Pedagogical Model, the aim to equip students with the ability to achieve to ILOs.",
            #     # "highlight the practical applications that contribute to the development of desired skills or outcomes.",
            #     # "highlight the course emphasises and the use of pegagogial model, including tools and methods, to foster students for challenges in the field of work of the Bachelor Degree.",
            #     # "quote the ultimate goal for students"
            #     "Tell if have some curricular unit as pre-requisite"),

            ("Suggestions",
                "How we can integrate applied psychology in this curricular unit and where in the syllabus?"),
        ],
        "messageRoot": """
            Develop a text about the topic '{importantTopic}', considering the follow requirements: {requirements} and based on the syllabus:
            {syllabus}
            Your text must be less than {chars} characters.
            Considering the pedagogical model: \n%s
            """.lstrip(" ")%PEDAGOGICAL_MODEL
            #After optimize and summarize your text.
        ,

        "characterLimits": [1000, 1000, 1000, 3000, 3000, 3000, 1000, 1000],
    },
    0.9: {# ILO and Evidence OK, but Teaching Methodologies nope
        "importantTopics": [
            ("Intended learning outcomes (ILOs)",
                "using the Bloom's taxonomy verbs",
                "in a numeric list",
                "do not quote syllabus topic",
                "do not explain it"),

            # ("Evidence of the each syllabus topic coherence with the previous ILOs",
            #     "linking each ILOs topics to respective syllabus topic numbers",
            #     "optimize your answer quoting syllabus by numbers",
            #     "in a summarized bullet list"),

            # ("Optimized Teaching Methodologies (TMs) and specific learning of the curricular unit",
            #     "articulated with the pedagogical model teorethical and pratical",
            #     "including autonomous student time to study",
            #     "quote digital technology applications to integrate to TMs",
            #     "quote previous syllabus topics"),

            # ("Suggest assessments to ensure that students are learning what they know",
            #     "articulated with the pedagogical model teorethical and pratical"),

            # ("Evidence of the each syllabus topic coherence with the previous ILOs",
            #     "linking each ILOs topics to respective syllabus topic numbers",
            #     "optimize your answer quoting syllabus by numbers",
            #     "in a summarized bullet list"),

            # ("Suggest current and relevant books to this curricular unit",
            #     "show this bibliograthies in APA style",
            #     "sort descending this bibliographies by year"),
        ],
        "messageRoot": """
            Develop a text about the topic '{importantTopic}', considering the follow requirements: {requirements} and based on the syllabus:
            {syllabus}
            Your text must be less than {chars} characters.
            Review your text grammar with Grammarly web tool.
            """.lstrip(" ")
            #After optimize and summarize your text.
        ,
        "characterLimits": [1000, 1000, 3000, 1000, 1000, 1000],
    },
}

import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from os.path import basename

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

try:
    from .pyle import createFolder 
except Exception:
    from pyle import createFolder 

class Verbose:
    __endPrint = "..."
    __endMessage = "Done"

    def __init__(self: object, enable: bool):
        self._enable = enable
        return None

    def beginProcess(self: object, msg: str) -> (None):
        if self._enable:
            print(msg, end=self.__endPrint)
        return None

    def endProcess(self: object) -> (None):
        if self._enable:
            print(self.__endMessage)
        return None


class UserInterface(Verbose):

    def __init__(
            self: object,
            version: int,
            syllabus: str,
            contactHours: int,
            workingHours: int,
            ECTS: int,
            expertise: str,
            *,
            message: str = None,
            prompt: dict[str:str] = PROMPT_DEFAULT,
            apiKey: str = None,
            verbose: bool = True,
            translateTo: str = None,
            animated: bool = False,
            questions: dict[str:str] = None, # Edit Important Topics manually
            showQuestions: bool = False
            ) -> (None):

        super(UserInterface, self).__init__(verbose)

        self._importantTopics = [
            topic[0] for topic in CHAT_MESSAGES.get(version, {}).get("importantTopics", [])
        ]
        self._syllabus = syllabus
        self._version = version
        self._message = message
        self._questions = questions
        self._contactHours = contactHours
        self._workingHours = workingHours
        self._ECTS = ECTS
        self._expertise = expertise
        self._ilo = None
        
        self.beginProcess("Formatting the chat messages")
        self.__generateChatMessage(version, message, verbose)
        self.endProcess() if verbose else None

        if apiKey is None:
            raise ValueError("You need an Openai api key!")

        self.beginProcess("Connecting to chat gpt")
        self.__openChat(
            apiKey,
            prompt
            )
        self.endProcess()

        self._answers = {}
        self._translations = {}
        self._file = None

        if showQuestions:
            print(40*"=",*self._chatMessage, sep="\n", end="\n"+40*"="+"\n")

        self.ask(animated=animated)

        if translateTo is not None:
            self.__translateAnswers(language=translateTo)

        return None

    def __translateAnswers(
            self: object,
            language: str = "PT-PT",
            tool: str = "DeepL",
            grammar: str = "LanguageTool"
            ) -> (list[str]):

        translations = []
        for tag, answer in self._answers.items():
            translation = self.__ask(
                f"Translate follow text, using a web translator {tool}, to {language} and check your text grammar using the web tool {grammar}: \n\n{answer}",
                suffix="(Translations)"
            )
            translations[tag+"_translate"] = translation

        self._translations = translations

        return translations

    def __translateAnswersToPT(
            self: object,
            tool: str = "DeepL",
            grammar: str = "Flip"
            ) -> (list[str]):

        translations = {}
        for tag, answer in self._answers.items():
            translation = self.__ask(
                f"Translate follow text, using a web translator {tool}, to PT-PT and check your text grammar using the Flip: \n\n{answer}",
                suffix="(Translations)"
            )
            translations[tag] = translation

        self._translations = translations

        return translations

    def __generateChatMessage(
            self: object,
            version: int,
            message: str = None,
            verbose: bool = False
        ):

        if self._questions is None and message is None:
            _message = CHAT_MESSAGES.get(version)
        elif self._questions is not None:
            _message = self._questions
        else:
            _message = message

        if _message is not None:
            _chatMessage = ChatMessage(
                self._syllabus, **_message,
                ECTS=self._ECTS, contactHours=self._contactHours,
                workingHours=self._workingHours,
                expertise=self._expertise,
                verbose=verbose
                ) if type(_message) is dict\
                  else ChatMessage(None, _message, verbose=verbose)
            self._chatMessage = _chatMessage.getChatMessage()
        else:
            self._chatMessage = None
            raise ValueError(f"Version '{version}' not found. Available versions {list(d.keys())}")

        return None

    def __openChat(
            self: object,
            apiKey: str,
            prompt: dict[str:str]
            ) -> (None):

        self._chat = Chat(apiKey, prompt, self._enable)

        return None

    @property
    def syllabus(self: object):
        return self._syllabus

    @property
    def answers(self: object):
        return self._answers

    @property
    def translations(self: object):
        return self._translations

    @property
    def prompt(self: object):
        return self._prompt

    def getSyllabus(self: object):
        return self._syllabus

    def getAnswers(self: object):
        return self._answers

    def getTranslations(self: object):
        return self._translations

    def getPrompt(self: object):
        return self._prompt

    def setPrompt(self: object, prompt: dict[str:str]):
        self._chat.setPrompt(prompt)
        return None

    def __ask(self: object, msg: str, suffix: str = "") -> (str):
        answer = self._chat.invoke(msg, suffix).content
        return answer

    def showAnswers(self: object, animated: bool = False) -> (None):
        print(
            *[f"{k}:\n{v}" for k, v in self._answers.items()],
            sep="\n\n"
        )
        return None

    def showTranslations(self: object, animated: bool = False) -> (None):
        print(
            *[f"{k}:\n{v}" for k, v in self._translations.items()],
            sep="\n\n"
        )
        return None

    def ask(
            self: object,
            showAnswer: bool = False,
            animated: bool = False
            ) -> (list[str]):

        answers = {}
        total = len(self._chatMessage)
        try:
            for i, message in enumerate(self._chatMessage):
                message.format(ilo=self._ilo)
                answer = self.__ask(message, suffix=f"{i+1}/{total}")
                topic = self._importantTopics[i]
                if "ILO" in topic:
                    self._ilo = answer
                answers[topic] = answer
        except KeyboardInterrupt:
            pass

        if showAnswer and animated:
            botprint(*answers.values(), sep="\n")
        elif showAnswer:
            self.showAnswers(animated)

        self._answers = answers

        return answers

    def __fileExist(self: object, filePath: str) -> (str):
        filepath, extension = os.path.splitext(filePath)
        filename = os.path.basename(filepath)
        path = filepath[:-len(filename)-1]
        extension = extension[1:]

        candidate = filename

        candidatePath = f"{path}/{candidate}.{extension}"

        # fileAmount = filePath.split("_")
        # fileAmount = int(fileAmount)\
        #     if fileAmount.isdigit()\
        #     else None
        amount = 1
        while os.path.exists(candidatePath):
            if f"_{amount-1}" in candidate:
                candidate = candidate.replace(
                    f"_{amount-1}",
                    f"_{amount}"
                    )
            else:
                candidate = f"{candidate}_{amount}"
            candidatePath = f"{path}/{candidate}.{extension}"
            amount += 1
        return candidatePath

    def __export(
            self: object,
            text: str,
            filename: str,
            extension: str = "txt",
            path: str = ".",
            dontClose: bool = False
            ) -> (str):

        # Create the path folder
        createFolder(f"{path.strip('/')}/")

        # Turn to lower case
        filename = filename.lower()

        # Remove the filename accents and white spaces
        filename = removeAccents(filename)
        filename = removeWhitespaces(filename)

        if self._file is None or self._file.closed:
            filePath = f"{path.strip('/')}/{filename}.{extension}"

            filePath = self.__fileExist(filePath)

            self._file = open(filePath, "x", encoding="utf-8")

            self.__filePath = filePath

        self._file.write(text)

        if not dontClose:
            self._file.close()

        return self.__filePath

    def __exportParam(
            self: object,
            param: str,
            *args
            ) -> (str):

        if param == "translations" and not any(self._translations):
            # Translate to portuguese
            self.__translateAnswersToPT()

        _param = {
            "answers": self._answers.copy(),
            "translations": self._translations.copy(),
            "answers & translations": self._answers | self._translations
        }[param]

        total = len(_param)

        for tag in ["Contact hours", "Observations"]:
            if tag not in _param:
                continue
            content = _param.pop(tag)
            _del = len(tag)*"="
            title = "\n{}\n{}\n{}\n".format(
                _del, tag.title(), _del
                )
            filePath = self.__export(
                title + content,
                *args,
                dontClose=True
            )
            total -= 1

        for i, (tag, content) in enumerate(_param.items()):
            _del = len(tag)*"="
            title = "\n{}\n{}\n{}\n".format(
                _del, tag.title(), _del
                )
            filePath = self.__export(
                title + content,
                *args,
                dontClose=i<(total-1)
            )

            if "Intended Learning Outcomes (Ilos)" in title:
                title = title.replace(tag.title(), "Syllabus")\
                             .replace(_del, 8*"=")
                filePath = self.__export(
                    title + self._syllabus,
                    *args,
                    dontClose=True
                )

        return filePath

    def __exportContent(self: object) -> (None):
        for k, v in self._answers:
            pass
        return None

    def exportAnswers(
            self: object,
            filename: str,
            extension: str = "txt",
            path: str = "./"
            ) -> (str):

        if extension == "txt":
            filePath = self.__exportParam("answers", filename, extension, path)
        elif extension == "json":
            pass

        return filePath

    def exportTranslations(
            self: object,
            filename: str,
            extension: str = "txt",
            path: str = "./"
            ) -> (str):

        filePath = self.__exportParam("translations", filename, extension, path)

        return filePath

    def exportAnswersTranslations(
            self:object,
            filename: str,
            extension: str = "txt",
            path: str = "./"
            ) -> (str):

        filePath = self.__exportParam(
            "answers & translations", filename, extension, path
            )

        return filePath


    def __startServer(self: object, email: str) -> (None):
        import getpass
        self.__server = server = smtplib.SMTP(
            #host='smtp.outlook.com', port=587
            host="smtp.office365.com", port=587
            #host='smtp.gmail.com', port=587
            )
        server.starttls()
        while True:
            try:
                server.login(
                    email,
                    getpass.getpass(f"\n\nOUTLOOK ACCESS\nlogin: {email}\npassword: ")
                )
            except smtplib.SMTPAuthenticationError as err:
                print(err)
            else:
                break
        return None

    def sendByEmail(
            self: object,
            *filename: str,
            send_from: str = "natanael.quintino@ipiaget.pt",
            send_to: str = "natanael.quintino@ipiaget.pt"
            ) -> (None):
        self.__startServer(send_from)
        subject = f'''FUC "{', '.join(filename)}" finished'''
        bodyMessage = f'''Caro(a), A(s) FUC(s) "{', '.join(filename)}" foi(ram) concluida(s). Meus cordiais cumprimentos, Pyaget FUC Generator'''
        send_mail(
            send_from,
            send_to,
            subject,
            bodyMessage,
            filename,
            self.__server
            )

        return None

class Chat(Verbose):

    __defaultApiKey = None

    def __init__(
            self: object,
            apiKey: str = None,
            prompt: dict[str: str] = PROMPT_DEFAULT,
            verbose: bool = False
            ) -> (None):

        super(Chat, self).__init__(verbose)

        self.__apiKey = apiKey\
            if apiKey is not None\
            else self.__defaultApiKey

        self._chat = ChatOpenAI(openai_api_key=self.__apiKey)
        if prompt is not None:
            self.__generatePrompt(prompt)

        return None

    def __generatePrompt(
            self: object,
            prompt: dict[str:str]
            ) -> (None):

        self._prompt = ChatPromptTemplate.from_messages(
            prompt.items() if prompt is not None
                           else ("user", "{input}")
        )

        # Chainning prompt to char
        self._chain = self._prompt | self._chat

        return None

    def setPrompt(
            self: object,
            prompt: dict[str:str]
            ) -> (None):
        self.__generatePrompt(prompt)
        return None

    def invoke(
            self: object,
            userMessage: str,
            suffix: str = ""
            ) -> (str):

        self.beginProcess(f"Asking to ChatGPT {suffix}")
        answer = self._chain.invoke(
            {"input": userMessage},
        )
        self.endProcess()

        return answer


class ChatMessage(Verbose):

    def __init__(
            self: object,
            syllabus: str,
            messageRoot: str,
            importantTopics: list[str] = None,
            characterLimits: list[int] = None,
            contactHours: int = None,
            workingHours: int = None,
            ECTS: int = None,
            expertise: str = None,
            verbose: bool = False
            ) -> (None):
        self._messageRoot = messageRoot
        self._syllabus = syllabus
        self._importantTopics = importantTopics
        self._characterLimits = characterLimits
        self._contactHours = contactHours
        self._workingHours = workingHours
        self._ECTS = ECTS
        self._expertise = expertise

        super(ChatMessage, self).__init__(verbose)

        if importantTopics is not None and characterLimits is not None:
            self.__formatMessage()
        else:
            self._chatMessage = self._messageRoot

        return None

    def __formatMessage(
            self: object,
            ) -> (None):

        if self._syllabus is None:
            self._chatMessage = None
            return None

        self._chatMessage = []
        for i, topic in enumerate(self._importantTopics):
            message = self._messageRoot.format(
                importantTopic=topic[0],
                requirements=', '.join(topic[1:]),
                chars=int(self._characterLimits[i]*0.95),
                syllabus=self._syllabus,
                contactHours=self._contactHours,
                workingHours=self._workingHours,
                ECTS=self._ECTS,
                expertise=self._expertise
            ).strip("\t ")

            if len(topic) == 1:
                message.replace(
                    ", considering the follow requirements: and",
                    ""
                )

            self._chatMessage.append(message)

        return None

    @property
    def chatMessage(self: object):
        return self._chatMessage

    def getChatMessage(self: object):
        return self._chatMessage


import sys
import time
def botprint(
        *text: str,
        sep: str = "",
        end: str = "\n",
        delay_time: float = .01
        ) -> (None):
    for _text in text:
        for character in _text:
            sys.stdout.write(character)
            sys.stdout.flush()
            #print(character, end="")
            if character not in "\n\t ":
                time.sleep(delay_time)
    return None


def send_mail(send_from, send_to, subject, text, files=None,
              server="127.0.0.1"):

    if type(send_to) is not list:
        send_to = [send_to]

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    print ('Sending email to outlook', end="...")
    server.sendmail(send_from, send_to, subject, text)
    # smtp = smtplib.SMTP(server)
    # smtp.sendmail(send_from, send_to, msg.as_string())
    print("Done")
    server.quit()
    #smtp.close()
    return None


def removeAccents(text: str) -> (str):
    accentsMap = zip("áéíóúàèìòùäëïöüãẽĩõũâêîôûçñ", 5*"aeiou"+"cñ")
    withoutAccents = text
    for old, new in accentsMap:
        if old not in text:
            continue
        withoutAccents = withoutAccents.replace(old, new)
    return withoutAccents


def removeWhitespaces(text: str) -> (str):
    return text.replace(" ","_")
