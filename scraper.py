#Libreria para realizar solicitudes a laginas web
import requests
#convertir html a un archivo que podremos manejar con XPath
import lxml.html as html
#Lo usaremos para crear una carpeta
import os
#Lo usaremos para obtener la fecha actual
import datetime


#Constantes que usaremos en el scraper
HOME_URL = "https://www.larepublica.co/"
XPATH_LINK_TO_ARTICLE = "//text-fill/a/@href"
XPATH_TITLE = '//div[@class = "mb-auto"]/text-fill/span/text()'
XPATH_SUMMARY = '//div[@class = "lead"]/p/text()'
XPATH_BODY = '//div[@class = "html-content"]/p/text()'


#La funcion entrara al link y extraera el titulo, resumen y cuerpo y lo guardara en una carpeta con el nombre de la fecha de hoy
def parse_notice(link, today):
    HOME_URL = "https://www.larepublica.co/"
    XPATH_LINK_TO_ARTICLE = "//h2/a/@href"
    XPATH_TITLE = '//div[@class = "mb-auto"]/h2/span/text()'
    XPATH_SUMMARY = '//div[@class = "lead"]/p/text()'
    XPATH_BODY = '//div[@class = "html-content"]/p/text()'
    try:
        #Hacemos el request a la pagina guardando el archivo html en response
        response = requests.get(link)
        #Si el status code es 200
        if response.status_code == 200:
            #decodifica el contenido del archivo html
            notice = response.content.decode('utf-8')
            #Toma el contenido de la variable home (archivo html de la web) y lo transforma en un documento en el cual puedo aplicar xpath
            parsed = html.fromstring(notice)

            try:
                #Extraemos los titulos, Retornara una lista y el primer elemento es el titulo
                title = parsed.xpath(XPATH_TITLE)[0]
                #Eliminamos las comillasque pudieran existir y los espacios al inicio y final del titulo
                title = title.replace('\"','')
                title = title.strip()
                #Extraemos el resumen, retornara una lista donde el primer elemento es el resumen 
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                #Extraemos el cuerpo de la noticia, retornara una lista y en este caso no le indicaremos indice porque sabemos que body esta compuesto por varios parrafos
                body = parsed.xpath(XPATH_BODY)
            #Algunas noticias podrian no tener resumen, si existe ese error nos saldremos de la funcion
            except IndexError:
                return
            
            #Crearemos una carpeta y un archivo de texto cuyo nombre es la fecha de hoy
            with open(f'{today}/{title}.txt', 'w', encoding = "utf-8") as f:
                #Escribimos el titulo en el archivo txt, seguido del resumen y cuerpo, divididos por saltos de linea
                f.write(title)
                f.write("\n\n")
                f.write(summary)
                f.write("\n\n")
                for parrafo in body:
                    f.write(parrafo)
                    f.write("\n")

        else:
            raise ValueError(f"Error: {response.status_code}")
    except ValueError as ve:
        print(ve)


#función para extraer los link de las noticias
def parse_home():
    try:
        #Hacemos el request a la pagina guardando el archivo html en response
        response = requests.get(HOME_URL)
        #Si el status code es 200
        if response.status_code == 200:
            #decodifica el contenido del archivo html
            home = response.content.decode('utf-8')
            #Toma el contenido de la variable home (archivo html de la web) y lo transforma en un documento en el cual puedo aplicar xpath
            parsed = html.fromstring(home)
            #Aplicamos Xpath a la lista de links y obtendremos una lista de links de las noticias
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #Imprime los links para verlos en consola
            #print(links_to_notices)
            
            #Obtenemos al fecha de hoy en formato d/m/a y lo guardamos en la variable today
            today = datetime.date.today().strftime('%d-%m-%Y')
            #Si no existe una carpeta con el nombre de la fecha de hoy
            if not os.path.isdir(today):
                #creamos una carpeta con el nombre de la fecha de hoy
                os.mkdir(today)
            #A partir de cada link se ejecutara una funcion
            for link in links_to_notices:
                #Por cada link, ejecutara la funcion que extrae titulo, resumen y cuerpo
                parse_notice(link, today)
                    


        #Si el status_code no es igual a 200
        else:
            #eleva un error
            raise ValueError(f"Error: {response.status_code}")
    #Si ocurre un error
    except ValueError as ve:
        #Imprime el error
        print(ve)
        

#función que correrá la función principal
def run():
    parse_home()

#Entrypoint de mi archivo
if __name__ == "__main__":
    run()