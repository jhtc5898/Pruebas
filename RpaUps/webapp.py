# Punto de entrada para la aplicación.
#from . import app    # Llamado al comando 'flask'.
from __init__ import app
from flask import Flask, render_template , request

#Permite iniciar el navegador 
from selenium import webdriver
#Permite comprobar si se han cumplido diferentes aparatados dentro de nuestra pagina Web
from selenium.webdriver.support import expected_conditions as EC
#Tiempos de espera para controlar la carga de las paginas
from selenium.webdriver.support.ui import WebDriverWait
#Buscar elementos dentro de nuestra pagina
from selenium.webdriver.common.by import By
#driver interno que controla el navegador Firefox
#import geckodriver_autoinstaller
#Permite el uso de teclas 
from selenium.webdriver.common.keys import Keys
#control teclado
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#Tiempos Pruebas
import time
#json
import json


@app.route("/hello")
def hello_there():
    prub="entr"
    print(prub)

    driver = webdriver.Remote(
    'http://selenium:4444/wd/hub',
    desired_capabilities=webdriver.DesiredCapabilities.FIREFOX
    )
    print("Driver: "+str(driver))
    print("Sale")
    driver.get ('https://www.google.com/')
    time.sleep(4)
    resp=driver.find_element_by_css_selector("#SIvCob")
    print(resp.text)    
    return resp.text

@app.route('/facebook', methods=["POST"])
def facebook(): 
    def login_facebook(email,contrasena,post,list_grupos,list_imagenes):
        try:
            driver = webdriver.Remote('http://selenium:4444/wd/hub',desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)
            wait = WebDriverWait(driver, 10)
            driver.get ('https://m.facebook.com/')
            log_email='m_login_email'
            log_contra='m_login_password'
            bot_iniciar='login'

            #Busqueda por ID
            email_input = driver.find_element_by_id (log_email) 
            email_input.send_keys (email)

            #Busqueda por ID
            password_input = driver.find_element_by_id (log_contra) 
            password_input.send_keys (contrasena)

            #Click Inicion de Sesion
            driver.find_element_by_name(bot_iniciar).click()
            
            #Validacion Correo Contrasena.
            try:   
                wait.until(EC.url_changes('https://m.facebook.com/'))         
                if driver.current_url[0:46]=="https://m.facebook.com/login/identify/confirm/":
                    print("Login Fallido")
                    driver.delete_all_cookies()
                    driver.quit()
                    return json.loads('{"fac":{"fac":"Error Login"}}')
                else:
                    if driver.find_element_by_id('header').text=="Buscar":
                        print("Login Exitoso")
                        driver.get ('https://m.facebook.com/')
                        return postperfil(driver,post,list_imagenes,list_grupos) 
                    else: 
                        print("Login Fallido")
                        driver.delete_all_cookies()
                        driver.quit()
                        return json.loads('{"fac":{"fac":"Error Login"}}')
            except:
                if driver.current_url[0:41]=="https://m.facebook.com/login/save-device/":
                    print("Login  exitoso")
                    driver.get ('https://m.facebook.com/')
                    return postperfil(driver,post,list_imagenes,list_grupos)
                else:
                    driver.delete_all_cookies()
                    driver.quit()
                    return json.loads('{"fac":{"fac":"Informacion incorrecta"}}')
            
        except:
            driver.delete_all_cookies()
            driver.quit()
            return json.loads('{"fac":{"fac":"Error Login"}}')

    def postperfil(driver,post,list_imagenes,list_grupos):
        try:
            driver.get ('https://mbasic.facebook.com/')
            box_perfil=driver.find_element_by_name("xc_message")
            box_perfil.send_keys(post)

            #Validacion Imagenes
            if len(list_imagenes)!=0:
                wait = WebDriverWait(driver, 10)
                driver.find_element_by_name("view_photo").click()
                for i in range(len(list_imagenes)):
                    directorio="/home/john/Documents/Imagenes/"+list_imagenes[i]
                    wait.until (EC.presence_of_element_located ((By.NAME, 'file1')))
                    driver.find_element_by_name("file1").send_keys(directorio)
                    driver.find_element_by_name("add_photo_done").click()
                    wait.until (EC.presence_of_element_located ((By.NAME, 'view_photo')))
                    driver.find_element_by_name("view_photo").click()
                driver.find_element_by_link_text("Cancelar").click()
                driver.find_element_by_name("view_post").click()
                if driver.current_url[0:45]=="https://mbasic.facebook.com/photos/xtag_faces":
                    wait.until (EC.presence_of_element_located ((By.LINK_TEXT, 'Omitir')))
                    driver.find_element_by_link_text("Omitir").click()
            else:
                #Boton De  Publicar
                driver.find_element_by_name("view_post").click()

            return postGrupos(driver,post,list_imagenes,list_grupos)

        except:
            driver.delete_all_cookies()
            driver.quit()
            return json.loads('{"fac":{"fac":"Error Perfil"}}')
        
    def postGrupos(driver,post,list_imagenes,list_grupos): 
        try:
            #Bucle de ingreso a grupos.
            for i in range(len(list_grupos)):
                    print(len(list_grupos))
                    print(list_grupos)
                    driver.get(list_grupos[i]+'/?ref=bookmarks')
                    #Ingreso a la box de post de la pagina
                    driver.find_element_by_css_selector(".dr").click()
                    box_post=driver.find_element_by_name("xc_message")
                    box_post.send_keys(post)
                    if len(list_imagenes)!=0:
                        wait = WebDriverWait(driver, 10)
                        driver.find_element_by_name("view_photo").click()
                        
                        for j in range(len(list_imagenes)):
                            directorio="/home/john/Documents/Imagenes/"+list_imagenes[j]
                            wait.until (EC.presence_of_element_located ((By.NAME, 'file1')))
                            driver.find_element_by_name("file1").send_keys(directorio)
                            driver.find_element_by_name("add_photo_done").click()
                            wait.until (EC.presence_of_element_located ((By.NAME, 'view_photo')))
                            driver.find_element_by_name("view_photo").click()
                        driver.find_element_by_link_text("Cancelar").click()
                        driver.find_element_by_name("view_post").click()
                    else:
                        #Boton De  Publicar
                        driver.find_element_by_name("view_post").click()
            driver.delete_all_cookies()
            driver.quit()
            return json.loads('{"fac":{"fac":"Publicado"}}') 
        
        except:
            return json.loads('{"fac":{"fac":"Error Grupos"}}')        
                          
    def entrada(facebook):
        try:
            email = facebook['email']
            contrasena = facebook['contrasena']
            post = facebook['post']
            
            postgrup = facebook['share']
            list_grupos=[]
            if postgrup != "0" :
                for i in range(len(postgrup)):
                    list_grupos.append(postgrup[str(i)])

            
            imagenes = facebook['imagenes']
            list_imagenes=[]
            if imagenes != "0" :
                for i in range(len(imagenes)):
                    list_imagenes.append(imagenes[str(i)])
            
            return login_facebook(email,contrasena,post,list_grupos,list_imagenes)
        except:
            return json.loads('{"fac":{"fac":"Error valores entrada"}}')
    
    test = request.data.decode("utf-8")
    test=json.loads(test)
    facebook = test["fac"]

    return entrada(facebook)

@app.route('/twitter', methods=["POST"])
def twitter():
    def login_twitter(emailTwitter,contraseñaTwitter,postTwitter,mencionesString,list_imagenes):
        try:
            driver = webdriver.Remote('http://selenium:4444/wd/hub',desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)
            wait = WebDriverWait(driver, 10)
            #Ingreso directo al login de Twitter
            driver.get ('https://twitter.com/i/flow/login')
            #Espera explicita del id del USERNAME
            wait.until (EC.presence_of_element_located ((By.NAME, 'username')))
            #Ingreso al elemento "username"
            box_user=driver.find_element_by_name("username")
            box_user.send_keys(emailTwitter)
            #Uso del "enter"
            actions = ActionChains(driver) 
            actions.send_keys(Keys.ENTER)
            actions.perform()

            #Espera explicita del id del password
            wait.until (EC.presence_of_element_located ((By.NAME, 'password')))
            #Ingreso al elemento "password"
            box_password=driver.find_element_by_name("password")
            box_password.send_keys(contraseñaTwitter)
            #Uso del "enter"
            actions = ActionChains(driver) 
            actions.send_keys(Keys.ENTER)
            actions.perform()
            wait.until (EC.presence_of_element_located ((By.ID, 'accessible-list-0')))
            return cargarTwitter(postTwitter,mencionesString,wait,list_imagenes,driver)
        except:
            driver.delete_all_cookies()
            driver.quit()
            return json.loads('{"twi":{"twi":"Error login Twitter"}}')
         
    def cargarTwitter(postTwitter,mencionesString,wait,list_imagenes,driver):
        try:
            #Comprobracion de session
            wait.until(EC.presence_of_element_located ((By.ID, 'accessible-list-0'))) 
            #Ingreso a la pagina de estados de Twitter
            driver.get("https://twitter.com/compose/tweet") 
            wait.until(EC.presence_of_element_located ((By.CLASS_NAME, 'DraftEditor-editorContainer')))   
            actions = ActionChains(driver) 
            actions.send_keys(postTwitter+" "+mencionesString)
            actions.perform()

            #Validacion de Imagenes
            if len(list_imagenes)!=0:
                for i in range(len(list_imagenes)):
                    directorio="/home/john/Documents/Imagenes/"+list_imagenes[i]
                    driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[1]/input").send_keys(directorio)
                    wait.until (EC.presence_of_element_located ((By.XPATH, '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[1]/div[1]/div/div/img')))
                actions = ActionChains(driver) 
                actions.send_keys(Keys.TAB*4)
                actions.send_keys(Keys.ENTER)
                actions.perform()
            else:
                # "enter" para publicar el estado
                actions = ActionChains(driver) 
                actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER)
                actions.perform()
            #Espera de la publicacion.
            wait.until (EC.presence_of_element_located ((By.XPATH,"/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div[1]/span")))
            driver.delete_all_cookies()
            driver.quit()
            return json.loads('{"twi":{"twi":"Publicado Correctamente"}}')
        except:
            driver.delete_all_cookies()
            driver.quit()
            return json.loads('{"twi":{"error":"Error Publicacion"}}')

    def principal (twitter):  
        try:
            #Recuperamos los valores del json
            emailTwitter = twitter['email']
            contraseñaTwitter = twitter['contrasena']
            postTwitter = twitter['post']
            postMenciones= twitter['share']
            list_menciones=[]
            imagenes = twitter['imagenes']
            list_imagenes=[]
            
            #Valdacion de las menciones.
            if postMenciones != "0":
                for i in range(len(postMenciones)):
                    list_menciones.append(postMenciones[str(i)])
            mencionesString = ','.join(list_menciones)

            #Validacion de las imagenes
            if imagenes != "0" :
                for i in range(len(imagenes)):
                    list_imagenes.append(imagenes[str(i)])   
            
            #Ingreso a la funcion login.
            return login_twitter(emailTwitter,contraseñaTwitter,postTwitter,mencionesString,list_imagenes)

        except:
            return json.loads('{"twi":{"twi":"Error valores entrada"}}')

    #Recuperacion de los datos
    test = request.data.decode("utf-8")
    test=json.loads(test)
    twitter = test["twi"]
    #Ingreso a todos los metodos internos.
    return principal(twitter)
