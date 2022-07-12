import random
import json
import torch 
from model import NeuralNet
from main import bag_de_mot, separe_phrase

# device => le type l'appareil sur laquelle en tourne (cpu/cuda)
device = torch.device('cpu')

with open('intents.json','r') as f:
    intents = json.load(f)
    
FILE = "entrainement.pth"
data = torch.load(FILE)

taille_entre = data["taille_entre"]
taille_couche = data["taille_couche"]
taille_sortie = data["taille_sortie"]
tout_mots = data["tout_mots"]
tags = data["tags"]
model_state = data["model_state"]

# Creation de notre réseau de neuronnes
model = NeuralNet(taille_entre,taille_couche,taille_sortie).to(device)
# Enregistrer les "poids" et les "bias" fournis par notre apprentissage 
model.load_state_dict(model_state)
# Evaluer le model
model.eval()
nomBoot = "Sam"    

def get_response(message):    
    # Découpper notre input en mot
    sentence = separe_phrase(message)
    # Créer le bag word correspondant à notre saisie
    X = bag_de_mot(sentence,tout_mots)
    # Transformer X en un tableau 2d contenant 1 ligne 
    X = X.reshape(1, X.shape[0])
    # Créer un tableau de type tensor 
    X = torch.from_numpy(X)
    # Récupérer le output de notre réseau aprés l'injection de notre saisie comme input
    output = model(X)
    # Appliquer la fonction softmax sur le output ce qui va nous pérmétre de retourner 
    # la probabilité de chaque élément de notre output 
    probs = torch.softmax(output,dim=1)
    # Récupérer l'indice du tag correspondant à la probabilté maximalles
    _,predicted = torch.max(probs, dim =1)
    # Récupérer le tag correspondant à la probabilité maximalle 
    tag = tags[predicted.item()]
    # Récupérer la probabilité max
    prob = probs[0][predicted.item()]
    # Vérifier Si la probabilité est suppérrieur à 0.75
    # print(tag)
    print(prob.item())
    if prob.item() > 0.8:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return random.choice(intent["responses"])
    else:
        return "Désolé je ne comprend pas ce que vous dites"

