from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
 env = os.environ.get('APP_ENV' ,'Development')
 return render_template('index.html' ,environment=env)

@app.route('/health')
def health():
  return {"status": "healthy", "app" :"Flask Devops Project"}, 200

if __name__ =='__main__':
     app.run(host='0.0.0.0' ,port=5000, debug=True)
 
