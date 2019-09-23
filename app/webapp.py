from flask import Flask, request, url_for, redirect, render_template, flash, session
import pandas as pd
import os
from python.gffGenerator import createGFF
from python.fastaFormatter import formatter
from python.batchRename import rename
from python.countCombiner import merge
app = Flask(__name__)
app.secret_key = "HARC"

# route for uploading fasta file
@app.route('/start', methods = ['GET', 'POST'])  
def upload():  
	if request.method == 'POST':  
		fastafile = request.files['fastafile']  
		fastafile.save(os.path.join("./HARCresults", fastafile.filename))
		session['fastaname'] = fastafile.filename
		return redirect("/gff")
	else:
		return render_template('start.html')


# route for converting fasta file
# asks for gff file name and step count
@app.route("/gff", methods=['GET', 'POST'])
def gff():
	path = './HARCresults/'
	verbose = False
	fastafile = session.get('fastaname', "None")
	if request.method == 'POST':
		if not os.path.exists(path):
			os.mkdir(path)
		formatter(path + fastafile, '>', path)
		gff = request.form['gff']
		step = request.form['step']
		createGFF(step, '>', path+fastafile, path+gff, verbose)
		return redirect('/results')
	else:
		return render_template('gff.html')

# route for renaming a directory/group of files
@app.route('/rename', methods=['GET', 'POST'])
def rename2():
	path = './HARCresults/'
	if request.method == 'POST':
		renamefiles = request.form['renamefiles']
		if renamefiles == True:
			renamepath = path + 'rename'
			if not os.path.exists(renamepath):
		 		os.mkdir(renamepath)
			files = request.form['files']
			rename = request.form['rename']
			os.system('cp -r ' + files + " " + path)
			rename(renamepath, rename)
			return redirect('/results')
		else:
			return render_template('rename.html')

#route for uploading files to combine the counts
@app.route('/combinesubmit', methods = ['GET', 'POST'])  
def comsub():  
	if request.method == 'POST':  
		# fastafile = request.files['fastafile']  
		# fastafile.save(os.path.join("./HARCresults", fastafile.filename))
		# session['fastaname'] = fastafile.filename
		return redirect("/combine")
	else:
		return render_template('combinesubmit.html')

#route for combing file counts
#asks for count type, name for merged file, and ext of files to be merged
@app.route("/combine", methods=['GET', 'POST'])
def combine():
	path = './HARCresults/'
	if request.method == 'POST':
		# combinecounts = request.form['combinecounts']
		# if combinecounts == True:
		# 	s = request.form['s']
		# 	u = request.form['u']
		# 	r = request.form['r']
		# 	if s == True:
		# 		col = "Stranded"
		# 	elif u == True:
		# 		col == "Unstranded"
		# 	elif r == True:
		# 		col = "Reverse"
		# 	else:
		# 		flash("ERROR: PICK ONLY ONE MERGE TYPE")
		# 	mergefiles = request.form['mergefiles']
		# 	mergename = request.form['mergename']
		# 	ext = request.form['ext']
		# 	merge(path+mergename, col, ext, mergefiles)
		return redirect('/results')
	else:
		return render_template('combine.html')	


# route for results page
# from here the user can do anotehr conversion, or chose to do another taskx
@app.route("/results")
def results():
	return render_template('results.html')

# route for project credits
@app.route("/credits")
def credits():
	return render_template('credits.html')

# route for project overview
@app.route("/overview")
def overview():
	return render_template('overview.html')

