import os
from .pyle import createFolder, basename, get_ext, rm
# from pdf2docx import parse as todocx

class Default:
    FUC_ROOT = "FUCRoot.tex"
    FUC_OUTPUT = "./FUCs_output/"

class Interface:

    def __init__(self: object, FUCRootFilename: str = Default.FUC_ROOT):
        self._fucRoot = FUCRootFilename
        return None

    def fillFUCRoot(self: object, content: dict[str:str]) -> (None):
        with open(self._fucRoot) as file:
            fucContent = file.read()
            fucContent.format(
                **content
            )
        return None

    def exportPDF(self: object, filename: str, path: str = Default.FUC_OUTPUT):
        createFolder(path)
        filePath = f"{path}/{filename}.pdf"
        os.system(
            f"pdflatex -interaction=batchmode -output-directory={path}\
                -jobname={filename} {self._fucRoot}"
        )
        for d in os.listdir(path):
            if get_ext(d) in ["aux", "log"]:
                print(rm(d, path))
        return filePath

    def exportDOCX(self: object, filename: str, path: str = Default.FUC_OUTPUT):
        # pdfOutput = self.exportPDF(filename, path)
        # filePath = pdfOutput.replace(".pdf", ".docx")
        # todocx(pdf_file=pdfOutput, docx_with_path=filePath)
        # return filePath
        pass

    def mergeFUCs(self: object, *filenames:str, path: str = Default.FUC_OUTPUT):
        pdfFileEditor = pdf.facades.PdfFileEditor()
        filePath = f"{path}/{filenames[0]}_merged.pdf"
        pdfFileEditor.concatenate(filenames, filePath)
        return filePath

Interface().exportPDF("FUC_IAC")
Interface().exportDOCX("FUC_IAC")

class FUC:

    __hoursByEcts = 28
    __tipologies = ["T", "TP", "PL", "TC", "S", "E", "OT", "O", "total"]
    __modes = ["presencial", "assincrono", "sincrono"]

    def __init__(self):
        self._contactHours = {
            m: {t: 0 for t in self.__tipologies}
                for m in self.__modes
        } 

        # Creat all attributes seeking set functions
        [exec(f"self._{attr[4:]} = None", {"self":self})
            for attr in dir(FUC)
            if "set_" in attr]

        return None

    # ==========
    # PROPERTIES
    # ==========
    @property
    def nome(self):
        return self._nome

    @property
    def name(self):
        return self._name

    @property
    def scientificArea(self):
        return self._scientificArea

    @property
    def duration(self):
        return self._duration

    @property
    def workHours(self):
        return self._workHours

    @property
    def ects(self):
        return self._ects

    @property
    def observations(self):
        return self._observations

    @property
    def professor(self):
        return self._professor

    @property
    def teachingHours(self):
        return self._teachingHours['head']

    @property
    def objetivoAprendizagem(self):
        return self._objetivoAprendizagem

    @property
    def learningOutcome(self):
        return self._learningOutcome

    @property
    def conteudoProgramatico(self):
        return self._conteudoProgramatico

    @property
    def syllabus(self):
        return self._syllabus

    @property
    def coerenciaObjetivos(self):
        return self._coerencia

    @property
    def coherenceOutcomes(self):
        return self._coherence

    @property
    def metodologia(self):
        return self._metodologia

    @property
    def methodology(self):
        return self._methodology

    @property
    def avaliacao(self):
        return self._avaliacao

    @property
    def assessment(self):
        return self._assessment

    @property
    def coerenciaAvaliacao(self):
        return self._coerenciaAvaliacao

    @property
    def coherenceAssessment(self):
        return self._coherenceAssement

    @property
    def bibliography(self):
        return self._bibliography

    @property
    def otherProfessors(self):    
        return self._otherProfessors

    @property
    def contactHoursPresencial(self):
        return self._contactHours["presencial"]

    @property
    def contactHoursAssincrono(self):
        return self._contactHours["assincrono"]

    @property
    def contactHoursSincrono(self):
        return self._contactHours["sincrono"]

    @property
    def othersTeachingHours(self):
        copy = self._teachingHours.copy()
        copy.pop("head")
        return copy.items()

    # =======
    # GETTERS
    # =======
    def get_nome(self):
        return self._nome

    def get_name(self):
        return self._name

    def get_scientificArea(self):
        return self._scientificArea

    def get_duration(self):
        return self._duration

    def get_workHours(self):
        return self._workHours

    def get_ects(self):
        return self._ects

    def get_observations(self):
        return self._observations

    def get_professor(self):
        return self._professor

    def get_teachingHours(self):
        return self._teachingHours['head']

    def get_objetivoAprendizagem(self):
        return self._objetivoAprendizagem

    def get_learningOutcome(self):
        return self._learningOutcome

    def get_conteudoProgramatico(self):
        return self._conteudoProgramatico

    def get_syllabus(self):
        return self._syllabus

    def get_coerenciaObjetivos(self):
        return self._coerencia

    def get_coherenceOutcomes(self):
        return self._coherence

    def get_metodologia(self):
        return self._metodologia

    def get_methodology(self):
        return self._methodology

    def get_avaliacao(self):
        return self._avaliacao

    def get_assessment(self):
        return self._assessment

    def get_coerenciaAvaliacao(self):
        return self._coerenciaAvaliacao

    def get_coherenceAssessment(self):
        return self._coherenceAssement

    def get_bibliography(self):
        return self._bibliography

    def get_otherProfessors(self):
        return self._otherProfessors

    def get_contactHoursPresencial(self):
        return self._contactHours["presencial"]

    def get_contactHoursAssincrono(self):
        return self._contactHours["assincrono"]

    def get_contactHoursSincrono(self):
        return self._contactHours["sincrono"]

    def get_othersTeachingHours(self):
        copy = self._teachingHours.copy()
        copy.pop("head")
        return copy.items()

    # =======
    # SETTERS
    # =======
    def set_nome(self, value):
        self._nome = value
        return None

    def set_name(self, value):
        self._name = value
        return None

    def set_scientificArea(self, value):
        self._scientificArea = value
        return None

    def set_duration(self, value):
        self._duration = value
        return None

    def set_workHours(self, value):
        self._workHours = value
        self.__calculateECTS_WorkHours()
        return None

    def set_ects(self, value):
        self._ects = value
        self.__calculateECTS_WorkHours()
        return None

    def set_observations(self, value):
        self._observations = value
        return None

    def set_professor(self, value):
        self._professor = value
        return None

    def set_teachingHours(self, value):
        self._teachingHours['head'] = value
        return None

    def set_objetivoAprendizagem(self, value):
        self._objetivoAprendizagem = value
        return None

    def set_learningOutcome(self, value):
        self._learningOutcome = value
        return None

    def set_conteudoProgramatico(self, value):
        self._conteudoProgramatico = value
        return None

    def set_syllabus(self, value):
        self._syllabus = value
        return None

    def set_coerenciaObjetivos(self, value):
        self._coerencia = value
        return None

    def set_coherenceOutcomes(self, value):
        self._coherence = value
        return None

    def set_metodologia(self, value):
        self._metodologia = value
        return None

    def set_methodology(self, value):
        self._methodology = value
        return None

    def set_avaliacao(self, value):
        self._avaliacao = value
        return None

    def set_assessment(self, value):
        self._assessment = value
        return None

    def set_coerenciaAvaliacao(self, value):
        self._ = value
        return None

    def set_coherenceAssessment(self, value):
        self._coherenceAssement = value
        return None

    def set_bibliography(self, *value):
        self._bibliography = value
        return None

    def set_otherProfessors(self, *value):
        self._otherProfessors = value        
        self._teachingHours.update({v: 0 for v in value})
        return None

    def set_contactHoursPresencial(self, *values):
        self._contactHours["presencial"].update(
            {k: v for k, v in zip(self.__tipologies, values)}
        )
        self.__calculateTotalContactHours("presencial")
        return None

    def set_contactHoursAssincrono(self, *values):
        self._contactHours["assincrono"].update(
            {k: v for k, v in zip(self.__tipologies, values)}
        )
        self.__calculateTotalContactHours("assincrono")
        return None

    def set_contactHoursSincrono(self, *values):
        self._contactHours["sincrono"].update(
            {k: v for k, v in zip(self.__tipologies, values)}
        )
        self.__calculateTotalContactHours("sincrono")
        return None

    def set_othersTeachingHours(self, value: dict[str:int]):
        self._teachingHours.update(value)
        return None

    def __formatBibliography(self):
        pass
    
    def __calculatePercentContactHours(self, mode=None):
        totais = [self._contactHours[m]["total"] for m in self.__modes]
        presencial = sum(totais[0])
        distancia = sum(totais[1:])
        total = sum(totais)
        self._contactHoursPercent["presencial"] = 100*presencial/total
        self._contactHoursPercent["distancia"] = 100*distancia/total
        return None

    def __calculateTotalContactHours(self, mode=None):
        if mode is None:
            for m in self.__modes:
                self._contactHours[m]["total"] = sum(
                    self._contactHours[m].values()
                )
        elif mode in self._contactHours:
            self._contactHours[mode]["total"] = sum(
                self._contactHours[mode].values()
                )
        self.__calculatePercentContactHours()
        return None

    def __calculateECTS_WorkHours(self):
        if self._ects is not None and self._workHours is None:
            self._workHours = self._ects*self.__hoursByEcts
        elif self._ects is None and self._workHours is not None:
            self._ects = self._workHours/self.__hoursByEcts
        return None
FUC()
