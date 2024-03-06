"""
   Este es el modulo que incluye la clase de reproducción de musica
"""

class Player:
   """
   Esta clase crea un reproductor de musica
   """
   
   def play(self, song):
      """
      Reproduce la canción que recibio como parametro
      
      parameters:
      song: str: este es un string con el path de la canción
      
      returns:
      int: devuelve 1 si reproduce con exito en caso de fracaso devuelve 0
      """
      print(f"Reproduciendo {song}")
      
      def stop(self):
         """
         Detiene la canción que se esta reproduciendo
         """
         print("Canción detenida")