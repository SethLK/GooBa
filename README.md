

# Gooba  
   
**Gooba** is a frontend framework written in Python, inspired by **React**, aimed at ***beginners*** who want to build web UIs with Python.    
    
Precautions:    
 - **DO NOT USE THIS ON PRODUCTION**: Gooba is a work in progress and not yet considered safe for production environments.   
 - **Fun Project**:  
   This project is developed for fun and learning purposes.     
  
**Features**:  
  
 - **Component-Based**: Gooba allows you to build reusable components similar to how you would in React.    
 -  **Pythonic Syntax**: Write your  
   UI components and logic entirely in Python, making it accessible for  
   Python developers.     
 - **Lightweight**: Designed to be simple and easy    to understand, perfect for learning and experimentation.  
  
**Getting Started:**  
  
 **Installation**: Instructions on how to install Gooba using pip or by cloning the repository.   
  
  
**Hello World Example**: A simple example to get new users up and running quickly.    
  
  

    #main.py
    from GooBa import Document, Element  
      
    # Initialize Document and Router  
    doc = Document()  
      
    h1 = Element("h1")  
    h1.text = "Hello World"  
      
    doc.body(h1)  
    doc.build()

    


  
For server
 

     #run.py
     import http.server
     import socketserver
     import os
        
     PORT = 8000
     DIRECTORY = "output"
        
        
     class CustomHandler(http.server.SimpleHTTPRequestHandler):
         def __init__(self, *args, **kwargs):
             super().__init__(*args, directory=DIRECTORY, **kwargs)
        
         def do_GET(self):
             # Check if the requested file exists in the directory
             requested_path = self.directory + self.path
             if not os.path.exists(requested_path) or os.path.isdir(requested_path):
                self.path = "/index.html"
             return super().do_GET()
        
        
        # Start the server
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
         print(f"Serving at port {PORT}")
         httpd.serve_forever()


Run
  

    python run.py # for server, port 8000
    python main.py # for ui
**Documentation**:    
  

    just contact me

   
**Contributing**:    
    
   
  
     just contact me
  
    
**License**:    
    
 - Gooba is distributed under the **MIT** License. It is open-source and  
   free to use, including for commercial purposes, but remember that it  
   is not safe for production environments at this time.
