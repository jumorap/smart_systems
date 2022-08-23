# Work:
> Desarrollar un agente inteligente que juegue picas y fijas, debe poder interactuar con un humano, o con otro agente. No solo debe adivinar sino que debe tener su propio número que otro agente puede estar adivinando. El siguiente es el conjunto de percepciones y acciones con las que cuenta el agente:

### Percepciones:
- 'S': El caracter S le indica al agente que debe iniciar un nuevo juego.
- '#': El caracter # le indica al agente que debe preguntar un número de cuatro dígitos diferentes (puede empezar con cero).
- n: Un número natural de cuatro dígitos diferentes (puede empezar con cero) a lo que debe responder con el número de picas y fijas respecto a su número. Se percibe como cadena de caracteres.
- p,f: Dos números naturales p y f (separados por una coma) tales que su suma sea menor o igual a cuatro (p+f<=4) y que son el número de picas y fijas respecto al número n que el agente actuó anteriormente. Se percibe como cadena de caracteres.

### Acciones:
- 'R': El caracter R le indica al ambiente que el agente está listo para jugar.
- 'A': El caracter A le indica al ambiente que el agente tomó nota del número de picas y fijas percibido.
- n: Un número natural de cuatro dígitos diferentes (puede empezar con cero). Se debe retornar como cadena de caracteres.
- p,f: Dos números naturales p y f (separados por una coma) tales que su suma sea menor o igual a cuatro (p+f<=4) y que se correspondan con el número de picas y fijas respecto al número n recibido como percepción y al número que tiene almacenado el agente. Se debe retornar como cadena de caracteres.
