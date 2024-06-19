import unittest
from flask import current_app
from app import create_app
from routes.marcas import add_marca

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def agregar_marca(self):
        self.app= add_marca()

    
if __name__ == '__main__':
    unittest.main()