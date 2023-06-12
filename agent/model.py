from torch import load, save, tensor, unsqueeze, argmax
from torch import float as tor_float
from torch import long as tor_long
from torch import max as tor_max
from torch.nn import Module, Linear, MSELoss
from torch.optim import Adam
from torch.nn.functional import relu
from os import path
from os import makedirs as os_makedirs

class LinearQNet(Module):
    def __init__(self, input_size, hidden_size_1, hidden_size_2, output_size):
        super().__init__()
        self.linear1 = Linear(input_size, hidden_size_1)
        self.linear2 = Linear(hidden_size_1, hidden_size_2)
        self.linear3 = Linear(hidden_size_2, output_size)

    def forward(self, x):
        x = relu(self.linear1(x))
        x = relu(self.linear2(x))
        x = self.linear3(x)
        return x
    
    def load(self, file_name='model.pth'):
        model_folder_path = './model/best'
        file_name = path.join(model_folder_path, file_name)
        model_state = load(file_name)
        self.load_state_dict(model_state)
        self.train()

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not path.exists(model_folder_path):
            os_makedirs(model_folder_path)
        file_name = path.join(model_folder_path, file_name)
        save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = Adam(model.parameters(), lr=self.lr)
        self.criterion = MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = tensor(state, dtype=tor_float)
        next_state = tensor(next_state, dtype=tor_float)
        action = tensor(action, dtype=tor_long)
        reward = tensor(reward, dtype=tor_float)

        if len(state.shape) == 1:
            state = unsqueeze(state, 0)
            next_state = unsqueeze(next_state, 0)
            action = unsqueeze(action, 0)
            reward = unsqueeze(reward, 0)
            done = (done, )

        # 1: predicted Q values with current state
        pred = self.model(state)
        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * tor_max(self.model(next_state[idx]))
            target[idx][argmax(action[idx]).item()] = Q_new
    
        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()



