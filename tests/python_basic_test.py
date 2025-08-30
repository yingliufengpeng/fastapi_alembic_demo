import unittest

 
class TestBasic(unittest.TestCase):
  
    def test_add(self):
        m = 3 + 4


    def test_app(self):
        import uvicorn
        uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True,

                )

 

if __name__ == "__main__":
    unittest.main()