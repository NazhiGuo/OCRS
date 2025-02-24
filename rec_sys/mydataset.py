from torch.utils.data import Dataset
import pandas as pd


class MyDataset(Dataset):
    def __init__(self, rating):
        super(Dataset, self).__init__()
        self.user = rating['stu_id']
        self.weather = rating['course_index']
        self.rating = rating['rating']

    def __len__(self):
        return len(self.rating)

    def __getitem__(self, item):
        return self.user[item], self.weather[item], self.rating[item]
