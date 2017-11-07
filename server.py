from flask import Flask, request, send_from_directory,Response,make_response,abort,jsonify
import base64
import json
import time
from images.images import  PIXEL
import copy
from flask_cors import CORS,cross_origin
app = Flask(__name__, static_url_path='')

@app.route('/js/<path:path>')
def send_js(path):
		
	return send_from_directory('js', path)

@app.route("/ts")
@cross_origin(supports_credentials=True)
def gif():
	
	response = make_response(PIXEL)
	response.headers['Content-Type'] = 'image/gif'
	if 'userID' in request.cookies:

		username=request.cookies.get("userID")
    # do something
	else:

		username = request.args.get('userID')
	
	if username!= None:
		
		import pymongo
		import time
		client = pymongo.MongoClient('mongodb://test:test@13.81.119.126:27018/testapi')
		db = client.testapi
		col = db.users_logs
		try:
			col.insert({'name':username,'url':request.referrer,'time':time.time()})
		except:
			pass	
		response.set_cookie('userID', username)
	return response


@app.route('/segment/<string:user>', methods = ['GET'])
@cross_origin()

def get_segment(user):
	print 'recieved'
	
	import pymongo
	import time
	print time.time()*1000
	print request.referrer
	client = pymongo.MongoClient('mongodb://test:test@13.81.119.126:27018/testapi')
	db = client.testapi
	col = db.testusermd5
	doc=col.find({'user':user},{'_id':0}).limit(1)
	try:
		res=doc.next()
	except:
		res={'user':user,'segment':'unkhown'}
	print res

	js = json.dumps(res)
	resp = Response(js, status=200, mimetype='application/json')
	print 'sent'
	print time.time()*1000	
	return resp

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=3000, debug=True,threaded=True)


