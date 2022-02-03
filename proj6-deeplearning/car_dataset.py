import json
from os.path import join
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

class CarDataset(Dataset):
    def __init__(self, json_file, root_dir, split="train", transform=None):
        """
        Parameters:
            json_file:  json file with annotations
            root_dir:  directory of images
            transform:  transformation to apply to images (optional)
                        If provided, it must take a PIL image and
                        return a tensor object.
        """
        super().__init__()
        
        with open(json_file, 'r') as f:
            self.labels = json.load(f)
        self.root_dir = root_dir
        self.split = split
        self.transform = transform or transforms.Compose([
            transforms.CenterCrop(224),
            transforms.transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],std=[0.229, 0.224, 0.225])
        ])

    def __getitem__(self, index):
        image_name = f"{index+1:05}.jpg" # Images are 1-indexed in our dataset whereas idx is zero indexed here
        path = join(self.root_dir, image_name)
        image = Image.open(path).convert("RGB")
        image = self.transform(image)
        label = self.labels[image_name] - 1 # Labels are 1-indexed, but here we need it zero indexed
        
        return (image, label)

    def __len__(self):
        return len(self.labels)
    
    def is_train_split(self):
        return self.split == "train"
