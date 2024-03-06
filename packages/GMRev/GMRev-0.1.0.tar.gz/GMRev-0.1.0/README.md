<p align="center">
  <i>Framework de evaluación de sistemas de Generación Mejorada por Recuperación (GMR)</i>
</p>

<h4 align="center">
    <p>
        <a href="#instalación">Instalación</a> |
        <a href="#ejemplo-de-uso">Ejemplo de uso</a> |
        <a href="#contacto">Contacto</a> |
        <a href="https://huggingface.co/PrevenIA">Hugging Face</a>
    <p>
</h4>

> GMRev es una librería preparada para la evaluación de bancos de datos de sistemas de pregunta/respuesta generados por grandes modelos de lenguaje (LLM - Large Language Model en inglés) en castellano. Se puede adaptar a las necesidades de los usuarios añadiendo métricas propias y fijando el modelo que acutará como evaluador.

## Instalación

```bash
pip install GMRev
```

## Ejemplo de uso

El siguiente código Python es un pequeño ejemplo de uso del evaluador.

```python
from GMRev import GMRev

# Creamos una instancia de la clase GMRev, como parámetro le podemos pasar nuestro modelo del lenguaje —por defecto, crea uno usando mistralai/Mixtral-8x7B-Instruct-v0.1— que es el que utilizará como evaluador.
evaluador = GMRev()

# Cargamos un dataset (solo cinco registros) para hacer la prueba de evaluación. La estructura del dataset debe ser una específica.
dataset = load_dataset("paascorb/RomancesTradicionales")
evaluador.evaluar(dataset["train"])
```

## Contacto

paascorb@unirioja.es