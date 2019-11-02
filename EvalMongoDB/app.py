from flask import Flask, render_template,request,redirect,url_for
from bson import ObjectId
from pymongo import MongoClient
import os

app = Flask(__name__)
title = "Evaluation MongoDB"
heading = "CRUD utilisant les fonctions de MongoDB"

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mabdd #Le nom de la base de données
taches = db.tache #Le nom de la collection

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/")
@app.route("/list")
def lists ():
	#Affiche toutes les tâches
	taches_select = taches.find()

	# Variable utilisée pour la class css qui affiche l'onglet en cours
	a1="active"

	return render_template('index.html', a1=a1, taches=taches_select, title=title, heading=heading)

@app.route("/uncompleted")
def tasks ():
	#Affiche uniquement les tâches incomplètes
	taches_select = taches.find({"done":"no"})

	# Variable utilisée pour la class css qui affiche l'onglet en cours
	a2="active"
	return render_template('index.html', a2=a2, taches=taches_select, title=title, heading=heading)


@app.route("/completed")
def completed ():
	#Affiche uniquement les tâches complètes
	taches_select = taches.find({"done":"yes"})

	# Variable utilisée pour la class css qui affiche l'onglet en cours
	a3="active"
	return render_template('index.html', a3=a3, taches=taches_select, title=title, heading=heading)

@app.route("/done")
def done ():
	#Affiche l'icone complet ou incomplet
	id=request.values.get("_id")
	task=taches.find({"_id":ObjectId(id)})
	if(task[0]["done"]=="yes"):
		taches.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
	else:
		taches.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
	redir=redirect_url()

	return redirect(redir)

@app.route("/action", methods=['POST'])
def action ():
	#Ajouter une tâche
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	taches.insert({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
	return redirect("/list")

@app.route("/remove")
def remove ():
	#Supprimer une tâche
	key=request.values.get("_id")
	taches.remove({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=taches.find({"_id":ObjectId(id)})
	return render_template('update.html', tasks=task, heading=heading, title=title)

@app.route("/action3", methods=['POST'])
def action3 ():
	#Mettre à jour une tâche
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	id=request.values.get("_id")
	taches.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date, "pr":pr }})
	return redirect("/")

@app.route("/search", methods=['GET'])
def search():
	#Rechercher une tâche en fonction de critères

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		taches_select = taches.find({refer:ObjectId(key)})
	else:
		taches_select = taches.find({refer:key})
	return render_template('searchlist.html', taches=taches_select, title=title, heading=heading)

if __name__ == "__main__":

    app.run()
