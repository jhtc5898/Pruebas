# Punto de entrada para la aplicación.
from . import app    # Llamado al comando 'flask'.
from datetime import datetime
from flask import Flask, render_template
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys 
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


@app.route("/hello")
def hello_there():

    val="Ingreso Metodo"
    print("HOla")
    return val
