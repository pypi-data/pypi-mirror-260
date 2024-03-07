import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

"""
=========
TO UPDATE
=========
export PYAGET_VERSION=1.0.4 && python3 uploadPackageInPypi.py
"""

if __name__ != "__main__":
    from .chatMessagesVersions import UserI2terface
    from .pyle import readFile

else:
    openai_key_choice = 5
    openai_key = {
        1: os.environ["OPENAI_API_KEY_GONCALO"], # GPT 4
        2: os.environ["OPENAI_API_KEY"], # GPT 3.5
        3: os.environ["OPENAI_API_KEY_2"], # GPT 3.5
        4: os.environ["OPENAI_API_KEY_3"], # GPT 3.5
        5: os.environ["OPENAI_API_KEY_4"], # GPT 3.5
    }[openai_key_choice]

    from chatMessagesVersions import UserInterface
    from pyle import readFile

    # ===============================
    # Not implemented
    # ===============================
    expertiseChoice = 1
    expertise = {
        1: "Cibersecurity",
        2: "Artificial Intelligence"
    }[expertiseChoice]
    # ===============================

    contactHours = 50
    ECTS = 6
    workingHours = ECTS*25

    fucsPath = "./fucs/ciber"

    fucsList = [
        "Ataques de Engenharia Social.txt",
        "Criptografia.txt",
        "Estrutura de Dados e Algoritmos.txt",
        "Fundamentos Cibersegurança.txt",
        "Fundamentos de Administracao de Sistemas.txt",
        "Fundamentos de Internet das Coisas.txt",
        "Fundamentos de Machine Learning e Data Science.txt",
        "Fundamentos de Programação.txt",
        "Fundamentos de Redes de Computadores.txt",
        "Fundamentos de Sistemas Operativos.txt",
        "Fundamentos de Sistemas de Informacao e Bases de Dados.txt",
        "Matematica.txt",
        "Metologia investigacao.txt",
        "Probabilidade e Estatistica.txt",
        "Programacao para Dispositivos Moveis.txt",
        "Seguranca de Equipamento Ativo de Rede.txt",
        "Seguranca por Monitorizacao.txt",
        "Sistemas Digitais Microprocessadores e Arquitetura.txt",
        "Tecnologia de Administracao de Sistemas.txt",
        "Tecnologias de Redes de Computadores.txt",
        "Tecnologias de Sistemas Operativos.txt",
        "Tecnologias de Sistemas de Informação e Bases de Dados.txt",
        "Vulnerabilidades em Aplicacoes Web.txt",
        "Vulnerabilidades em Sistemas Informaticos.txt",
        "Álgebra Linear e Geometria Analítica.txt",
    ]

    slices = {
        2: slice(0,7),
        3: slice(7,13),
        4: slice(13,19),
        5: slice(19,None)
    }[openai_key_choice]

    for fuc in os.listdir(fucsPath)[slices]:
        if ".txt" not in fuc:
            continue
        fucName = fuc.split("_")[2]
        fucName, ext = fucName.split(".")
        with open(f"{fucsPath}/{fuc}", "r", encoding="latin-1") as file:
            syllabus = file.read().replace("  ","")\
                                  .replace("\n\n","\n")\
                                  .replace("ï»¿", "")\
                                  .replace("Syllabus:", "")
        message = f"Generating FUC to {fucName.title()}"
        delim = len(message)*"="
        print(delim, message, delim, sep="\n", end="\n\n")

        interface = UserInterface(
            1.0, syllabus, contactHours, workingHours, ECTS, expertise,
            apiKey=openai_key, showQuestions=True
            )

        interface.showAnswers()
        interface.exportAnswers(fucName, "txt", "./output")

        #interface._UserInterface__translateAnswersToPT()
        interface.showTranslations()
        interface.exportTranslations(f"{fucName}_translation", "txt", "./output")

        # interface.exportAnswersTranslations("fullText", "txt")

        # interface.sendByEmail(
        #     "answers.txt",
        #     send_from="natanael.quintino@ipiaget.pt",
        #     send_to="natanael.quintino@ipiaget.pt"
        #     )

# import docx2txt
# import docx

# def getText(filename):
#     doc = docx.Document(filename)
#     fullText = []
#     for para in doc.paragraphs:
#         fullText.append(para.text)
#         input(para.style)
#     return '\n'.join(fullText)


    # syllabusChoice = 4
    # syllabus = {
    #     1: """
    #         1. Introduction and overview: internal organization of a computer 
    #         2. Digital representation of information 
    #         3. Logical functions 
    #         4. Study of a didactic architecture 
    #         5. Architecture of a processor 
    #         6. Arithmetic circuits 
    #         7. Sequential circuits 
    #         8. Memory system 
    #         9. Input / Output Peripherals 
    #     """,
    #     2: """
    #     1. Digital Systems 
    #     1.1. Numbering systems and codes. 
    #     1.2. Boolean algebra, postulates and theorems. Simplification of Boolean functions, algebraic method and Karnaugh maps. 
    #     1.3. Design of combinatorial circuits, adder/subtractor, multiplexer, encoder and decoder. 
    #     1.4. Synchronous and asynchronous sequential circuits. 
    #     1.5. Representation in state diagram and state table, simplification and encoding of memory states. 
    #     1.6. SR, JK, D and T Flip-Flops. 
    #     1.7. Design of synchronous seque
    #     ntial circuits. counters, shift-register. 
    #     1.8. TTL C-MOS logic families. 
    #     1.9. ROM and RAM memories, operating principles and decoding circuits. 
    #     2. Microprocessors and Microcontrollers 
    #     2.1. Base Computer Architecture 
    #     2.2. Structure of a CPU 
    #     2.3. Base architecture - Harvard Architecture 
    #     2.4. Memory management system 
    #     2.5. Program memory 
    #     2.6. Data memory (internal / external) 
    #     2.7. EPROM data memory 
    #     2.8. IO ports 
    #     2.9. Hardware associated with ports 
    #     2.10. Records and programming 
    #     2.11. Interruption system 
    #     2.12. Timers / Counters 
    #     2.13. A/D Conversion 
    #     2.14. Data Communication 
    #     2.15. Communication protocols 
    #     """,
    #     3: """
    #     1. Life cycle of computer program development  
    #     2. Algoritmia 
    #     2.1. Data types 
    #     2.2. Concepts: constant and variable 
    #     2.3. Types of variables 
    #     2.4. Algorithmic structures 
    #     2.5. Modularization of programs 
    #     3. Programming in imperative language (C/python language) 
    #     4. File processing 
    #     5. Complexity measurement 
    #     5.1 O notation 
    #     """, 
    #     4: """
    #     1. Information Security and the Organization: Challenges 
    #     1.1. Fundamental aspects; 
    #     1.2. Security basic concepts – principals and strategies; 
    #     1.3. Security mechanisms – network vulnerabilities; 
    #     1.4. Forensic analysis – data recovery, audit and network traffic analysis; 
    #     1.5. States of information; 
    #     2. Information security management strategy in an organization 
    #     2.1. Security policy; 
    #     2.2. Information security management; 
    #     2.3. Operational issues – analysis models; 
    #     2.4. Configuration management; 
    #     2.5. Contingency plans; 
    #     2.6. Monitoring compliance of security policy; 
    #     """
    # }[syllabusChoice]

    # fucName = {
    #     1: "Introdução à Arquitetura de Computadores",
    #     2: "Sistemas Digitais, Microprocessadores e Arq de Comp.",
    #     3: "Fundamentos de programação",
    #     4: "Fundamentos de Cibersegurança"
    # }[syllabusChoice]