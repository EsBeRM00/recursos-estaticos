#Importamos el framework fastapi a nuestro entorno de trabajo
from fastapi import FastAPI, Depends, HTTPException, status
#Importamos pydantic para obtener una entidad que pueda definir usuarios
from pydantic import BaseModel
#Importar para manejar las respuestas HTML en las rutas definidas
from fastapi.responses import HTMLResponse
#Importar la clase StaticFiles del módulo "staticfiles", se utiliza para servir archivos estáticos
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#Importamos librería jwt
from jose import jwt, JWTError
#Importamos libreria passlib (algoritmo de encriptación)
from passlib.context import CryptContext
#Importamos libreria de fechas para la expiración del token
from datetime import datetime, timedelta

#Implementamos algoritmo de haseo para encriptar contraseña
ALGORITHM = "HS256"
#Duración de autenticación 
ACCESS_TOKEN_DURATION= 5
#Creamos un secret
SECRET="123456789"

#Creamos un objeto o instancia a partir de la clase FastAPI
app= FastAPI()
#Ruta específica para servir archivos estáticos
app.mount("/fotos", StaticFiles(directory="fotos"), name="fotos")
#Autenticación por contraseña para eso:
#Creamos un endpoint llamado "login"
oauth2=OAuth2PasswordBearer(tokenUrl="login")

#Creamos contexto de encriptación para eso importamos libreria passlib y elegimos algoritmo de incriptación "bcrypt"
#Utilizamos bcrypt generator para encriptar nuestras contraseñas
crypt= CryptContext(schemes="bcrypt")

# generamos la contraseña encriptada para guardarla en base de datos
#https://bcrypt-generator.com/


class User(BaseModel):
    foto: str
    username:str
    full_name: str
    email:str
    disabled:bool
    number: str

#Definimos la clase para el usuario de base de datos 
class UserDB(User):
    password:str
    
#Creo una base de datos no relacional de usuarios 
users_db ={
     "Fani":{
         "foto": "/fotos/yo.jpeg",
         "username":"Fani",
         "full_name": "Estefania Berenice Rodríguez Martínez",
         "email": "estefania.rodriguezma@alumno.buap.mx",
         "disabled": False,
         "number": "2228669227",
         "password": "$2a$12$MeKPEnM6724HpkWMfZPcEeHYg1tCNkF35kKe4uqsQS4jrWmL8EgqO" # 1234

    },
    "Pili":{
         "foto": "/fotos/amigui.jpg",
         "username":"Pili",
         "full_name": "Pilar Hernandez Zambrano",
         "email": "pilar.hernandezz@alumno.buap.mx",
         "disabled": False,
         "number": "2223223454",
         "password": "$2a$12$j/nrWC0KsPG4kTSbKws3x.y/p3em3AWk3ysRbvskhepFNQi2T9YdS"# 5678
    },
    "Arrucha":{
         "foto": "/fotos/arrucha.jpg",
         "username":"Arrucha",
         "full_name": "José Eduardo Arrucha Álvarez ",
         "email": "jose.arruchaal@alumno.buap.mx",
         "disabled": False,
         "number": "2213317079",
         "password": "$2a$12$JkPeovg.kenatX2DJEM0aOStam8tWd8yxKeLzDQxpWLyZhX8NI9xm" # abc

    },
    "Kev":{
         "foto": "/fotos/kev.jpg",
         "username":"Kev",
         "full_name": "Kevin Armas Hernández",
         "email": "kevin.armas@alumno.buap.mx",
         "disabled": False,
         "number": "6141998990",
         "password": "$2a$12$MeKPEnM6724HpkWMfZPcEeHYg1tCNkF35kKe4uqsQS4jrWmL8EgqO" # 1234
    },
    "Yos":{
         "foto": "/fotos/yos.jpeg",
         "username":"Yos",
         "full_name": "Yosselin Pablo Ruiz",
         "email": "yosselin.pablo@alumno.buap.mx",
         "disabled": False,
         "number": "2288358188",
         "password": "$2a$12$j/nrWC0KsPG4kTSbKws3x.y/p3em3AWk3ysRbvskhepFNQi2T9YdS"# 5678
    },
    "Abran":{
         "foto": "/fotos/abran.jpeg",
         "username":"Abran",
         "full_name": "Abraham Coagtle Temis",
         "email": "abraham.coagtle@alumno.buap.mx",
         "disabled": False,
         "number": "2731327748",
         "password": "$2a$12$JkPeovg.kenatX2DJEM0aOStam8tWd8yxKeLzDQxpWLyZhX8NI9xm" # abc
    },
    "Vic":{
         "foto": "/fotos/vic.jpg",
         "username":"Vic",
         "full_name": "Victor Manuel Rosales Zayas ",
         "email": "victor.rosalesz@alumno.buap.mx",
         "disabled": False,
         "number": "2224415653",
         "password": "$2a$12$MeKPEnM6724HpkWMfZPcEeHYg1tCNkF35kKe4uqsQS4jrWmL8EgqO" # 1234
    },
    "Juan":{
         "foto": "/fotos/juan.jpeg",
         "username":"Juan",
         "full_name": "Juan Pablo Mendoza Armas",
         "email": "juan.mendozaar@alumno.buap.mx",
         "disabled": False,
         "number": "2281776285",
         "password": "$2a$12$j/nrWC0KsPG4kTSbKws3x.y/p3em3AWk3ysRbvskhepFNQi2T9YdS"# 5678
    },
    "Luis":{
         "foto": "/fotos/luis.jpg",
         "username":"Luis",
         "full_name": "Luis Delfino Castro Nava",
         "email": "luis.castron@alumno.buap.mx",
         "disabled": False,
         "number": "8110502639",
         "password": "$2a$12$JkPeovg.kenatX2DJEM0aOStam8tWd8yxKeLzDQxpWLyZhX8NI9xm" # abc
    },
    "Vicente":{
         "foto": "/fotos/vicente.jpg",
         "username":"Vicente",
         "full_name": "Vicente Zavaleta Sanchez",
         "email": "vicente.zavaletas@alumno.buap.mx",
         "disabled": False,
         "number": "2212671849",
         "password": "$2a$12$MeKPEnM6724HpkWMfZPcEeHYg1tCNkF35kKe4uqsQS4jrWmL8EgqO" # 1234
    }
}

#1 Función para regresar el usuario completo de la base de datos (users_db), con contraseña encriptada
def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username]) #** devuelve todos los parámetros del usuario que coincida con username

#4 Función final para devolver usuario a la solicitud del backend   
def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    
    #3 Esta es la dependencia para buscar al usuario
async def auth_user(token:str=Depends(oauth2)):
    try:
        username= jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas")
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas")

    return search_user(username) #Esta es la entrega final, usuario sin password

#2 Función para determinar si usuario esta inactivo 
async def current_user(user:User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user
        
####################################################################################3
        
@app.post("/login/")
async def login(form:OAuth2PasswordRequestForm= Depends()):
    #Busca en la base de datos "users_db" el username que se ingreso en la forma 
    user_db= users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    # Se obtienen los atributos incluyendo password del usuario que coincida el username de la forma 
    user= search_user_db(form.username)     
    
    #user.password es la contraseña encriptada en la base de datos
    #form.password es la contraseña original que viene en formulario
    if not crypt.verify(form.password,user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    #Creamos expiración de 1 min a partir de la hora actual
    access_token_expiration=timedelta(minutes=ACCESS_TOKEN_DURATION)
    #Tiempo de expiración: hora actual mas 1 minuto
    expire=datetime.utcnow()+access_token_expiration
    
    access_token={"sub": user.username,"exp": expire}
    return {"access_token": jwt.encode(access_token, SECRET,algorithm=ALGORITHM), "token_type":"bearer"}

@app.get("/users/me/", response_class=HTMLResponse)
async def me(user:User= Depends (current_user)): #Crea un user de tipo User que depende de la función (current_user)
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Perfil de usuario</title>
</head>
<body>
<style>
html {{ 
    -webkit-text-size-adjust: 100%; 
    -ms-text-size-adjust: 100%; 
    text-size-adjust: 100%; 
    line-height: 1.4; 
}}
* {{ 
    margin: 0;
    padding: 0;
    -webkit-box-sizing: border-box; 
    -moz-box-sizing: border-box;
    box-sizing: border-box;
}}
body {{
    color: #404040;
    font-family: "Arial", Segoe UI, Tahoma, sans-serifl, Helvetica Neue, Helvetica;
}}

.seccion-perfil-usuario .perfil-usuario-body,
.seccion-perfil-usuario {{  
    display: flex; 
    flex-wrap: wrap; 
    flex-direction: column; 
    align-items: center; 
}}

.seccion-perfil-usuario .perfil-usuario-header {{
    width: 100%; 
    display: flex;
    justify-content: center;
    background: linear-gradient(#B873FF, transparent);
    margin-bottom: 1.25rem; 
}}

.seccion-perfil-usuario .perfil-usuario-portada {{
    display: block;
    position: relative;
    width: 90%;
    height: 17rem; 
    background-image: linear-gradient(to right, #3494e6, #ec6ead);
    border-radius: 0 0 20px 20px;
}}

.seccion-perfil-usuario .perfil-usuario-avatar {{ 
    display: flex;
    width: 180px;
    height: 180px;
    align-items: center;
    justify-content: center;
    border: 7px solid #FFFFFF;
    background-color: #DFE5F2;
    border-radius: 50%;
    box-shadow: 0 0 12px rgba(0, 0, 0, .2);
    position: absolute;
    bottom: -40px;
    left: calc(50% - 90px);
    z-index: 1;
}}

.seccion-perfil-usuario .perfil-usuario-avatar img {{
    width: 100%;
    position: relative;
    border-radius: 50%;
}}

.seccion-perfil-usuario .perfil-usuario-body {{
    width: 70%;
    position: relative;
    max-width: 750px;
}}

.seccion-perfil-usuario .perfil-usuario-body .titulo {{
    display: block;
    width: 100%;
    font-size: 1.75em;
    margin-bottom: 0.5rem;
}}

.seccion-perfil-usuario .perfil-usuario-body .texto {{
    color: #848484;
    font-size: 0.95em;
}}

.seccion-perfil-usuario .perfil-usuario-footer,
.seccion-perfil-usuario .perfil-usuario-bio {{
    display: flex;
    flex-wrap: wrap;
    padding: 3rem 2rem;
    box-shadow: 0 0 12px rgba(0, 0, 0, .2);
    background-color: #fff;
    border-radius: 15px;
    width: 100%;
}}

.seccion-perfil-usuario .perfil-usuario-bio {{
    margin-bottom: 1.25rem;
    text-align: center;
}}

.seccion-perfil-usuario .lista-datos {{
    width: 50%;
    list-style: none;
}}

.seccion-perfil-usuario .lista-datos li {{
    padding: 7px 0;
}}

.seccion-perfil-usuario .lista-datos li>.icono {{
    margin-right: 1rem;
    font-size: 1.2rem;
    vertical-align: middle;
}}
.seccion-perfil-usuario .redes-sociales {{
    position: absolute;
    right: calc(0px - 50px - 1rem);
    top: 0;
    display: flex;
    flex-direction: column;
}}

.seccion-perfil-usuario .redes-sociales .boton-redes {{
    border: 0;
    background-color: #fff;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    color: #fff;
    box-shadow: 0 0 12px rgba(0, 0, 0, .2);
    font-size: 1.3rem;
}}

.seccion-perfil-usuario .redes-sociales .boton-redes+.boton-redes {{
    margin-top: .5rem;
}}

.seccion-perfil-usuario .boton-redes.facebook {{
    background-color: #5955FF;
}}

.seccion-perfil-usuario .boton-redes.twitter {{
    background-color: #35E1BF;
}}

.seccion-perfil-usuario .boton-redes.instagram {{
    background: linear-gradient(45deg, #FF2DFD, #40A7FF);
}}

</style>
    <section class="seccion-perfil-usuario">
        <div class="perfil-usuario-header">
            <div class="perfil-usuario-portada">
                <div class="perfil-usuario-avatar">
                    <img src="{user.foto}" alt="img-avatar">
                </div>
            </div>
        </div>
        <div class="perfil-usuario-body">
            <div class="perfil-usuario-bio">
                <h3 class="titulo">Hello, {user.full_name}!</h3>
                <p class="texto"> 22 años | me encanta la música | "No intentes ser otra persona, intenta ser la mejor versión de ti mismo" | Good Vibes</p>
            </div>
            <div class="perfil-usuario-footer">
                <ul class="lista-datos">
                    <li><img class="icono" src="/fotos/home.ico" alt="direccion"> Direccion: Mi casa</li>
                    <li><img class="icono" src="/fotos/phone.ico" alt="telefono">Telefono: {user.number}</li>
                </ul>
                <ul class="lista-datos">
                    <li><img class="icono" src="/fotos/email.ico" alt="email">Email: {user.email}</li>
                    <li><img class="icono" src="/fotos/locate.ico" alt="ubicacion"> Ubicacion: FCC BUAP</li>
                </ul>
            </div>
            <div class="redes-sociales">
                <a href="" class="boton-redes facebook ">
                    <img src="/fotos/face.ico" alt="facebook">
                  </a>
                <a href="" class="boton-redes twitter ">
                    <img src="/fotos/twi.ico" alt="twitter">
                    </a>
                <a href="" class="boton-redes instagram">
                    <img src="/fotos/insta.ico" alt="instagram">
                    </a>
            </div>
        </div>
    </section>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

#http://127.0.0.1:8000/login/

#username:Freddy
#password:1234

#http://127.0.0.1:8000/users/me/
#Levantamos el server Uvicorn
#-uvicorn parcial:app --reload-