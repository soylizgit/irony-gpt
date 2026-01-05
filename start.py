#Clave API de OpenAI
import os
import openai
openai.api_key = os.getenv("api_key")

#indica que actúe como un analizador de sentimientos
initialPrompt = """hace de cuenta que sos un analizador de sentimientos. yo te paso sentimientos y vos analizas
                   el sentimiento de los mensaje y me das una respuesta con al menos 1 caracter y un máximo de 4 caracteres
                   SOLO RESPUESTAS NUMÉRICAS, -1 es negatividad máxima, 0 es neutral y 1 es positivo. (podes usar valores flotantes)."""
#Lista para almacenar el historial de la conversación
messages = [
    {"role": "system", "content": initialPrompt}
]

#Clase para interpretar el valor de sentimiento
class AnalizadorDeSentimientos:
    def analizar_sentimiento(self, polaridad):
        #Evalúa valor de polaridad y devuelve
        if polaridad > -0.6 and polaridad <= -0.3:
            return "\x1b[1;31m"+'negativo'+"\x1b[0;37m"
        elif polaridad > -0.3 and polaridad < 0:
            return "\x1b[1;31m"+'algo negativo'+"\x1b[0;37m"
        elif polaridad == 0:
            return "\x1b[1;33m"+'neutral'+"\x1b[0;37m"
        elif polaridad > 0 and polaridad <= 0.3:
            return "\x1b[1;33m"+'algo positivo'
        elif polaridad > 0.3 and polaridad <= 0.6:
            return "\x1b[1;32m"+'positivo'
        elif polaridad > 0.6 and polaridad <= 0.9:
            return "\x1b[1;32m"+'muy positivo'
        elif polaridad > 0.9 and polaridad <= 1:
            return "\x1b[1;32m"+'muy muy positivo'
        else :
            return "\x1b[1;31m"+'muy negativo'+"\x1b[0;37m"

#Crea instancia del analizador de sentimientos
analizador = AnalizadorDeSentimientos()


while True:
    #Solicita mensaje al usuario por consola
    userPrompt = input("\x1b[1;33m"+"\nDecime algo: "+"\x1b[0;37m")
    #Agrega el mensaje del usuario al historial
    messages.append({"role": "user", "content": userPrompt})
    
    #Envía el historial de mensajes al modelo de OpenAI
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1200
    )

    # Agregar respuesta del modelo a la conversacion
    messages.append({
        "role": "assistant",
        "content": completion.choices[0].message['content']
    })
    #Analiza el sentimiento correspondiente
    sentimiento = analizador.analizar_sentimiento(float(completion.choices[0].message['content']))

    #Muestra el resultado del sentimiento
    print(sentimiento)