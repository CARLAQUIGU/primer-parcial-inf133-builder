
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib

# Base de datos simulada de videojuego 
personajes = {}

class Personaje:
    def __init__(self):
        self.name=None
        self.level=None
        self.role= None 
        self.charisma=None
        self.strength=None
        self.dexterity=None
        
    def __str__(self):
        return f"name: {self.name}, level: {self.level}, role: {self.role},charisma:{self.charisma},strength : {self.strength},dexterity: {self.dexterity}"
# Personaje Buuilder 
class PersonajeBuilder:
        def __init__(self):
            self.personaje = Personaje()
            
        def set_name(self, name):
            self.personaje.name = name
        def set_level(self, level):
            self.personaje.level = level
        def set_role(self, role):
            self.personaje.role = role
        def set_charisma(self, charisma):
            self.personaje.charisma = charisma
        def set_strength(self, strength):
            self.personaje.strength = strength
        def set_dexterity(self, dexterity):
            self.personaje.dexterity = dexterity
        def get_personaje(self):
            return self.personaje
# Director: Video Juego
class VideoJuego:
    def __init__(self, builder):
        self.builder = builder

    def create_personaje(self, name, level, role, charisma, strength, dexterity):
        self.builder.set_name(name)
        self.builder.set_level(level)
        self.builder.set_role(role)
        self.builder.set_charisma(charisma)
        self.builder.set_strength(strength)
        self.builder.set_dexterity(dexterity)
        
        return self.builder.get_personaje()

class PersonajeService:
    def __init__(self):
        self.builder = PersonajeBuilder()
        self.videojuego = VideoJuego(self.builder)

    def create_personaje(self, post_data):
        name = post_data.get("name", None)
        level=post_data.get("level", None)
        role = post_data.get("role", None)
        charisma = post_data.get("charisma", None)
        strength = post_data.get("strength", None)
        dexterity = post_data.get("dexterity", None)
        personaje = self.videojuego.create_personaje(name,level, role, charisma, strength, dexterity)
        personajes[len(personajes) + 1] = personaje
        
        return personaje

    def read_personajes(self):
        return {index: personaje.__dict__ for index, personaje in personajes.items()}
    
    def read_archer_level_5_charisma_10(self):
        filtered_personajes = {}
        for index, personaje in personajes.items():
            if personaje.role == "Archer" and personaje.level == 5 and personaje.charisma == 10:
                filtered_personajes[index] = personaje.__dict__
        return filtered_personajes
    
    def update_personaje(self, index, data):
        if index in personajes:
            personaje = personajes[index]
            name = data.get("name", None)
            level = data.get("level", None)
            role = data.get("role", None)
            charisma = data.get("charisma", None)
            strength = data.get("strength", None)
            dexterity = data.get("dexterity", None)
            
            if name:
                personaje.name = name
            if level:
                personaje.level = level
            if role:
                personaje.role = role
            if charisma:
                personaje.charisma = charisma
            if strength:
                personaje.strength = strength
            if dexterity:
                personaje.dexterity = dexterity

            return personaje
        else:
            return None

    def delete_personaje(self, index):
        if index in personajes:
            return personajes.pop(index)
        else:
            return None
class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))


class PersonajeHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = PersonajeService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/personajes":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.create_personaje(data)
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_GET(self):
        if self.path == "/personajes":
            response_data = self.controller.read_personajes()
            HTTPDataHandler.handle_response(self, 200, response_data)
        elif self.path == "/personajes/archer_level_5_charisma_10":
            response_data = self.controller.read_archer_level_5_charisma_10()
            HTTPDataHandler.handle_response(self, 200, response_data)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/personajes/"):
            index = int(self.path.split("/")[2])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.update_personaje(index, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Índice de pizza no válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/personajes/"):
            index = int(self.path.split("/")[2])
            deleted_personaje = self.controller.delete_personaje(index)
            if deleted_personaje:
                HTTPDataHandler.handle_response(
                    self, 200, {"message": "Personaje eliminada correctamente"}
                )
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Íd de personaje no válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


def run(server_class=HTTPServer, handler_class=PersonajeHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
    