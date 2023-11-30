#charger et utiliser un modèle entraîné pour classer des symboles

import torch
from torchvision import transforms
from PIL import Image
import os
import torch.nn.functional as nnf
import math
from pathlib import Path

os.environ['CUDA_VISIBLE_DEVICES'] ='0'

classes = ['!', '(', ')', '+', '|', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', 'A_', 'B_', 'C_', 'Delta', 'E_', 'F_', 'G_', 'H_', 'I_', 'L_', 'M_', 'N_', 'P_', 'R_', 'S_', 'T_', 'V_', 'X_', 'Y_', '[', ']', 'a', 'alpha', 'b', 'beta', 'c', 'cos', 'd', 'div', 'div_op', 'dot', 'e', 'exists', 'f', 'forall', 'g', 'gamma', 'geq', 'gt', 'h', 'i', 'in', 'infty', 'int', 'j', 'k', 'l', 'lambda', 'ldots', 'leq', 'lim', 'log', 'lt', 'm', 'mu', 'n', 'neq', 'o', 'p', 'phi', 'pi', 'pipe', 'pm', 'prime', 'q', 'r', 'rightarrow', 's', 'sigma', 'sin', 'sqrt', 'sum', 't', 'tan', 'theta', 'times', 'u', 'v', 'w', 'x', 'y', 'z', '{', '}']

# Construction du chemin
base_dir = Path(__file__).resolve().parent.parent.parent
MODEL_FOLDER = base_dir / "models"

#MODEL_FOLDER  = os.path.dirname(os.path.realpath(__file__)) + "/../../models/"

filters = 128
kernel_size = 3
layers = 3
dropout = True
fcLayerSize = 512
minbatchsize = 128
nb_classes = 101


class SymbolClassifier:

	def __init__(self) -> None:		
		self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
		self.net = SymbolClassifier_Model(fcLayerSize  , filters , kernel_size , layers , nb_classes , minbatchsize , dropout=dropout)
		self.net.load_state_dict(torch.load(os.path.join(MODEL_FOLDER , "best_model.nn"))) #load the model
		#print(self.net)

	def class_to_str( self , class_index):
		return classes[class_index]

	def classify_symbol_img( self , images ):
		top_p = []
		top_class = []
		for i in range( math.ceil( ( len(images) / minbatchsize) ) ):
			sub_images = images[i * minbatchsize : ( i + 1) * minbatchsize ]

			transform = transforms.Compose(
				[transforms.Grayscale(), #CROHME png are RGB, but already 32x32
				transforms.ToTensor(),
				transforms.Normalize((0.5,), (0.5,))])

			num_images = len(sub_images)
			tensorImages = []
			for i in range(num_images):
				tensorImages.append(transform(sub_images[i]).unsqueeze(0))
			
			reminder = minbatchsize - num_images
			tensorImages.extend([tensorImages[0]]*reminder)

			results =  self.compute(torch.cat(tensorImages))

			top_p.extend(results[0].cpu().detach().numpy()[:num_images])
			top_class.extend(results[1].cpu().detach().numpy()[:num_images])

		return (top_p , top_class)

	def classifiy_symbol( self , images_path ):
		images = []
		for image_path in images_path:
			images.append(Image.open(image_path))

		return self.classify_symbol_img(images)

	def compute(self , images):
		self.net.eval()
		with torch.no_grad():
			output = self.net(images)
			prob = nnf.softmax(output, dim=1)
			top_p, top_class = prob.topk(1, dim = 1)
			classIndex = top_class.cpu().detach().numpy()
			return (top_p ,top_class)


#----------- SYMBOL CLASSIFICATION MODEL -------------#

import torch.nn as nn
import torch.nn.functional as F

class SymbolClassifier_Model(nn.Module):
	def __init__(self , fcLayerSize , n_filters , kernel_size , layers , nb_classes , minibatchsize ,dropout = False ):
		super(SymbolClassifier_Model, self).__init__()
		self.pool = nn.MaxPool2d(2, 2)

		setattr(self,"conv0",nn.Conv2d(1 , n_filters , kernel_size))
		for i in range(layers-1):
			setattr(self,"conv"+str(i + 1),nn.Conv2d(n_filters , n_filters , kernel_size))
        
		self.layers = layers

		self.dropout = nn.Dropout(0.5 * dropout)

		self.fc1 = nn.Linear(fcLayerSize, 256)
		self.fc2 = nn.Linear(256, 200)
		self.fc3 = nn.Linear(200, nb_classes)
		
		self.nb_classes =nb_classes 
		self.minibatchsize = minibatchsize

	def forward(self, x):
		for i in range(self.layers):
			x = self.pool(F.relu(getattr(self,"conv"+str(i))(x)) )

		x = x.view(self.minibatchsize,-1)
		x = F.relu(self.fc1(x))
		x = self.dropout(x)
		x = F.relu(self.fc2(x))

		return x