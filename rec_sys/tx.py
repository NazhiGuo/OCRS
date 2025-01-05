import torch
import torch.nn as nn
import pandas as pd
from torch.utils.data import DataLoader
import argparse
from rec_sys.model import GCN
from rec_sys.mydataset import MyDataset
def predict(id):


    # 设备是否支持cuda
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

    # 读取用户特征、天气特征、评分
    user_feature = pd.read_csv('rec_sys/data/stu.txt', encoding='utf-8', sep='\t')
    item_feature = pd.read_csv('rec_sys/data/course.txt', encoding='utf-8', sep='\t')
    rating = pd.read_csv('rec_sys/data/mooc_all_rating.txt', encoding='utf-8', sep='\t')
    train = pd.read_csv('rec_sys/data/train_rating.txt', encoding='utf-8', sep='\t')
    test = pd.read_csv('rec_sys/data/mooc_test_rating.txt', encoding='utf-8', sep='\t')
    # 构建数据集
    dataset = MyDataset(rating)
    train = MyDataset(train)
    test = MyDataset(test)
    trainLen = int(0.8 * len(dataset))
    # train, test = random_split(dataset, [trainLen, len(dataset) - trainLen])
    train_loader = DataLoader(train, batch_size=1024, shuffle=True, pin_memory=True)
    test_loader = DataLoader(test, batch_size=len(test))

    # 记录训练的超参数
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    # device = torch.device("cpu")
    model = GCN(user_feature, item_feature, rating)
    model.load_state_dict(torch.load('rec_sys/model/bestModeParms-04-12-16-47.pth'))
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    model.eval()
    user_id = id
    user_tensor = torch.tensor([int(user_id)] * model.num_item).to(device)  # 用户ID转换为张量
    item_tensor = torch.arange(model.num_item).to(device)  # 创建一个张量

    predictions = model(user_tensor, item_tensor)
    top_k_items = torch.topk(predictions, k=36)[1]
    prc=[]
    print("推荐项目:")
    for item in top_k_items:
        item = item.item()
        prc.append(item_feature.loc[item]['course_index']+1)
    return prc