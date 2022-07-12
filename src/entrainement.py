import json
from main import separe_phrase, racine, bag_de_mot
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet
from dataSet import ChatDataset
import spacy
nlp = spacy.load('fr_core_news_md')

# Ouvrir le fichier json contenant nos données
with open('intents.json', 'r') as f:
    intents = json.load(f)

# Initialiser la liste de touts les mots
tout_mots = []
# Initialiser la liste des tags
tags = []
# Initialiser la liste des tuples (mots,tags)
xy = []

for intent in intents['intents']:
    # Récupérer le tag
    tag = intent['tag']
    # Ajouter le tag recupéré dans la liste des tags
    tags.append(tag)
    # Recupérer le pattern  
    for pattern in intent['patterns']:
        # Séparer la pattern récupéré en mots
        mots = separe_phrase(pattern)
        # Ajouter tout les mots dans la liste des mots 
        tout_mots.extend(mots)
        xy.append((mots,tag)) 

# Initialisé la liste des mots ignorés
mot_ignore = ['?','!','.',',']
# Transformer chaque mot de la liste des mots à ça racine 
tout_mots = [racine(nlp(w.lower())) for w in tout_mots if w not in mot_ignore]
# Trier la liste de touts les mots pour supprimer les répétitions 
tout_mots = sorted(set(tout_mots))
tags = sorted(set(tags))

# initialiser la liste des input pour notre réseau de neuronnes
X_entrain = []
# initialiser la liste des output pour notre réseau de neuronnes
Y_entrain = []

for (pattern,tag) in xy :
    # Transformer chaque pattern en bag de mots
    bag = bag_de_mot(pattern,tout_mots)
    # Ajouter le bag dans la liste des input
    X_entrain.append(bag)
    # Extraire l'indice qui correspond au pattern courant 
    label = tags.index(tag)    
    # Ajouter l'indice du tag courrant dans la liste des outputs
    Y_entrain.append(label)
    
X_entrain = np.array(X_entrain)
Y_entrain = np.array(Y_entrain)


# Parameters
taille_batch = 8
taille_couche = 8
taille_sortie = len(tags)
taille_entre = len(X_entrain[0])
learning_rate = 0.0015
num_epochs = 1000

# dataset => chaque bag de mot est associé à son label
dataset = ChatDataset(X_entrain,Y_entrain)
# train_loader => contient la data paratagé en sous group de 8 samples pour faciliter l'entrainement
train_loader = DataLoader(dataset=dataset, batch_size=taille_batch, shuffle=True,num_workers =2)
# device => le type l'appareil sur laquelle en tourne (cpu/cuda)
device = torch.device('cpu')
# Création de notre model de réseau de neuronnes.
model = NeuralNet(taille_entre,taille_couche,taille_sortie)
criteration = nn.CrossEntropyLoss()
# Initialiser l'optimizer
optimizer = torch.optim.Adam(model.parameters(),lr=learning_rate)
# Itérer chaque epoch
for epoch in range(num_epochs):
    # Itération de chaque batch de notre data
    for (words,labels) in train_loader:
        # Passer les patterns comme entrée pour notre réseau
        words = words.to(device)
        # Passer les sorties attendues pour chaque entrée
        labels = labels.to(device)
        # Récupérer les sorties
        outputs = model(words)
        # Calculer le score
        score = criteration(outputs, labels)
        # Bckprobagation
        optimizer.zero_grad()
        score.backward()
        optimizer.step()
    if(epoch+1) % 100 == 0 :
        print("score => ", score.item())
print(" score final d'entrainement  => ", score.item())


# Stocker notre réseau de neuronne entrainé avec ses paramétres
data = {
    "model_state": model.state_dict(),
    "taille_entre": taille_entre,
    "taille_sortie": taille_sortie,
    "taille_couche": taille_couche,
    "tout_mots": tout_mots,
    "tags": tags
}

# Sauvegarder le réseau entrainé dans le fichier entraiement
FILE = "entrainement.pth"
torch.save(data,FILE)
print("Entrainement complet, fichier sauvegardé ")