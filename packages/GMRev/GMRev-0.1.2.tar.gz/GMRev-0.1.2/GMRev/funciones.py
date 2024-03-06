from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
from evaluate import load
import abc
import re

"""
    Clase principal y núcleo de la librería, su objetivo es hacer evaluaciones cualitativas aplicando técnicas de procesamiento del lenguaje natural.

    ...

    Attributes
    ----------
    gml : tuple
        esta tupla contiene el gran modelo de lenguaje (gml) junto con su tokenizador.

    Methods
    -------
    evaluar(dataset, metricas=None)
        el gml evaluará el dataset contra las métricas proporcionadas (si no se proporcionan métricas se utiliza el context_relevancy por defecto).
        La estructura del dataset debe ser la siguiente: 
        "question": la pregunta que reciben los modelos y con la cual generarán las respuestas.
        "ground_truth": es la respuesta canónica esperada, la "verdad" con la que podemos comparar las respuestas generadas por los modelos; es una lista, es decir puede haber varías  
        respuestas canónicas a una misma pregunta.
        "contexts": lista que contiene los contextos proporcionados al gml para que genere la respuesta.
        "asnwer": respuesta generada por el gml y la cual queremos comparar.
    """
class GMRev:
    
    def __init__(self, gml=None):
        
        if not gml:
            self.gml = self._construir_modelo()
        else:
            self.gml = gml
    
    def _construir_modelo(self):
        model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config)
        return model, tokenizer
    
    def evaluar(self, dataset, metricas=None):
        
        if not metricas:
            metricas = [Falta(self.gml)]
            
        resultados = []
        for met in metricas:
            resultados.append(met.calcular_metrica(dataset))
        
        return resultados
        
class Metrica(metaclass=abc.ABCMeta):

    def __init__(self, gml):
        self.gml = gml
    
    @abc.abstractmethod
    def calcular_metrica(self, dataset, verbose=True):
        pass
    
    @abc.abstractmethod
    def _calcular_instancia(self, instancia):
        pass
    
class Falta(Metrica):
    
    def __init__(self, gml):
        super().__init__(gml)
    
    def calcular_metrica(self, dataset, verbose=True):
        
        resultado = []
        razon = []
        for i, instancia in enumerate(dataset):
            if verbose:
                print(f"Calculando información faltante. Fase {i} de {len(dataset)}.", end='\r')
            res = self._calcular_instancia(instancia)
            aux = re.sub('\n+','\n',res).split('\n')
            val_aux = 0
            raz_aux = ""
            try:
                val_aux =  float(aux[0].split(" ")[1])
                raz_aux = aux[1].split("Razón: ")[1]
            except:
                val_aux = 0
                raz_aux = "Sin razonamiento proporcionado."
            resultado.append(val_aux)
            razon.append(raz_aux)
        return resultado, razon
    
    def _calcular_instancia(self, instancia):
        
        device = "cuda"
        pregunta, respuesta = instancia["question"], instancia["answer"]
        messages = [
            {"role": "user", "content": f"""Puntúa la respuesta según la pregunta dada atendiendo a la falta de información para estar completa.
                                            El veredícto debe ceñirse a la siguiente rúbrica:
                                            0-2) La frase no responde en absoluto a la pregunta.
                                            3-4) La frase responde muy por encima o parcialmente, faltándole bastante que responder para que se considere que responde a la pregunta.
                                            5-6) La frase responde pero aún le falta bastante información para completar la pregunta.
                                            7-8) La frase responde a la pregunta en su mayoría pero aún le falta algo de información para completar la pregunta.
                                            9-10) La frase responde a la pregunta perfectamente.
                                            Pregunta: {pregunta},
                                            Respuesta: {respuesta}
                                            Obligatorio, escribe "Veredícto:" para la evaluación y "Razón:" para el razonamiento. Es muy importante que NO esté en inglés, debe estar en castellano."""}
        ]

        encodeds = self.gml[1].apply_chat_template(messages, return_tensors="pt")
        model_inputs = encodeds.to(device)
        generated_ids = self.gml[0].generate(model_inputs, max_new_tokens=1000, pad_token_id=self.gml[1].eos_token_id)
        decoded = self.gml[1].batch_decode(generated_ids)[0]
        return decoded.split('[/INST]')[1].split('</s>')[0][1:]
    
class Sobra(Metrica):
    
    def __init__(self, gml):
        super().__init__(gml)
    
    def calcular_metrica(self, dataset, verbose=True):
        
        resultado = []
        razon = []
        for i, instancia in enumerate(dataset):
            if verbose:
                print(f"Calculando información sobrante. Fase {i} de {len(dataset)}.", end='\r')
            res = self._calcular_instancia(instancia)
            aux = re.sub('\n+','\n',res).split('\n')
            val_aux = 0
            raz_aux = ""
            try:
                val_aux =  float(aux[0].split(" ")[1])
                raz_aux = aux[1].split("Razón: ")[1]
            except:
                val_aux = 0
                raz_aux = "Sin razonamiento proporcionado."
            resultado.append(val_aux)
            razon.append(raz_aux)
        return resultado, razon
    
    def _calcular_instancia(self, instancia):
        
        device = "cuda"
        pregunta, respuesta = instancia["question"], instancia["answer"]
        messages = [
            {"role": "user", "content": f"""Puntúa la respuesta según la pregunta penalizando la información repetida o redundante.
                                            El veredícto debe ceñirse a la siguiente rúbrica:
                                            0-2) La  información que contiene la frase no corresponde a la pregunta.
                                            3-4) La frase contiene mucha información que no corresponde a la pregunta.
                                            5-6) La frase contiene bastante información que no corresponde a la pregunta.
                                            7-8) La frase contiene algo de información que no corresponde a la pregunta.
                                            9-10) Toda la información que contiene la frase corresponde con la pregunta.
                                            Pregunta: {pregunta},
                                            Respuesta: {respuesta}
                                            Obligatorio, escribe "Veredícto:" para la evaluación y "Razón:" para el razonamiento. Es muy importante que NO esté en inglés, debe estar en castellano."""}
        ]

        encodeds = self.gml[1].apply_chat_template(messages, return_tensors="pt")
        model_inputs = encodeds.to(device)
        generated_ids = self.gml[0].generate(model_inputs, max_new_tokens=1000, pad_token_id=self.gml[1].eos_token_id)
        decoded = self.gml[1].batch_decode(generated_ids)[0]
        return decoded.split('[/INST]')[1].split('</s>')[0][1:]
    
class Fidelidad(Metrica):
    
    def __init__(self, gml):
        super().__init__(gml)
    
    def calcular_metrica(self, dataset, verbose=True):
        
        resultado = []
        razon = []
        for i, instancia in enumerate(dataset):
            if verbose:
                print(f"Calculando fidelidad. Fase {i} de {len(dataset)}.", end='\r')
            res = self._calcular_instancia(instancia)
            aux = re.sub('\n+','\n',res).split('\n')
            val_aux = 0
            raz_aux = ""
            try:
                val_aux =  float(aux[0].split(" ")[1])
                raz_aux = aux[1].split("Razón: ")[1]
            except:
                val_aux = 0
                raz_aux = "Sin razonamiento proporcionado."
            resultado.append(val_aux)
            razon.append(raz_aux)
        return resultado, razon
    
    def _calcular_instancia(self, instancia):
        
        device = "cuda"
        pregunta, respuesta, contexto = instancia["question"], instancia["answer"], instancia["contexts"]
        messages = [
        {"role": "user", "content": f"""Tu tarea es determinar si una respuesta es consistentemente verídica o fiel a la realidad; es decir, partiendo de la pregunta, la respuesta tiene que ver con el contexto proporcionado y sus afirmaciones son ciertas.
                                        El veredícto debe ceñirse a la siguiente rúbrica:
                                        0-2) La respuesta no contiene ningún dato cierto o contrastable.
                                        3-4) La respuesta contiene poca información fiable o la mayoría es ambigua.
                                        5-6) En general la respuesta está bien pero parte de la información que contiene es falsa o ambigua.
                                        7-8) A excepción de alguna afirmación proporcionada que es ambigua o no del todo cierta, está bien.
                                        9-10) La pregunta contiene en su totalidad información fiable y afirmaciones ciertas.
                                        Pregunta: {pregunta},
                                        Respuesta: {respuesta},
                                        Contexto: {contexto}
                                        Obligatorio, escribe "Veredícto:" para la evaluación y "Razón:" para el razonamiento. Es muy importante que NO esté en inglés, debe estar en castellano."""}
        ]
        
        encodeds = self.gml[1].apply_chat_template(messages, return_tensors="pt")
        model_inputs = encodeds.to(device)
        generated_ids = self.gml[0].generate(model_inputs, max_new_tokens=1000, pad_token_id=self.gml[1].eos_token_id)
        decoded = self.gml[1].batch_decode(generated_ids)[0]
        return decoded.split('[/INST]')[1].split('</s>')[0][1:]