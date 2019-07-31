from app import app
#app.run(host='0.0.0.0', debug=True, threaded=True) 
app.run(host='0.0.0.0', debug=True, processes=True) #start debug model and mulity thread
#app.run(host='0.0.0.0', debug=True, processes=3) #start debug model and mulity thread
#app.run(host='0.0.0.0', debug=False, threaded=True) #reduce process to one
#app.run(host='0.0.0.0', use_reloader = False, threaded=True) #cannot reduce process to one   
