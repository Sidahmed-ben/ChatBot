from torch.utils.data import Dataset
# Initialiser notre data
class ChatDataset(Dataset):
    def __init__(self,X_entrain,Y_entrain):
        self.n_samples = len(X_entrain)
        self.X_data = X_entrain
        self.Y_data = Y_entrain
        
    def __getitem__(self,index):
        return self.X_data[index], self.Y_data[index]
    
    def __len__(self):
        return self.n_samples