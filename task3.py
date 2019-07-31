from flask import Flask, jsonify, render_template
import json
import task1
import task2
import matplotlib.pyplot as plt

app = Flask(__name__)

with open("100_info.json", 'r') as f:
	file = json.loads(f.read())


@app.route('/')
def index():
	return 'Hello'

@app.route('/show_profile/<int:id>', methods = ['GET'])
def show_post(id):
	if id>99:
		abort(404)
		# show the post with the given id, the id is an integer
	return jsonify({str(id): file[str(id)]})

@app.route('/fetch_profile')
def fetch():
	task1.main()
	return 'fetch success'

@app.route('/cluster')
def show():
	filename = 'plot.jpg'
	points,mark,clustering = task2.cluster()
	for i in range(len(points)):
		plt.plot(points[i,0],points[i,1],mark[clustering.labels_[i]])
	plt.savefig('static/images/'+filename,format = 'jpg')
	return render_template('plot.html', name = filename)

if __name__ == '__main__':
	app.run(debug=True,port = 5000)