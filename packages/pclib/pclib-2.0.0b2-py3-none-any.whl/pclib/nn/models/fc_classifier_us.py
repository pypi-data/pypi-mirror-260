import torch
import torch.nn as nn
import torch.nn.functional as F

from pclib.nn.layers import FC
from pclib.nn.models import FCClassifier

# Based on Whittington and Bogacz 2017, but with targets predicting inputs
class FCClassifierUs(FCClassifier):
    """
    | A Unsupervised version of FCClassifier.
    | Learns a feature extractor (self.layers) via unsupervised learning.
    | Also learns an mlp classifier (self.classifier) which takes the output of self.layers as input, via supervised learning.

    Args:
        | in_features (int): Number of input features
        | num_classes (int): Number of classes
        | hidden_sizes (list): List of hidden layer sizes
        | steps (int): Number of steps to run inference for
        | bias (bool): Whether to include bias in layers
        | symmetric (bool): Whether to use same weights for top-down prediction and bottom-up error prop.
        | actv_fn (torch.nn.functional): Activation function to use
        | d_actv_fn (torch.nn.functional): Derivative of activation function to use
        | gamma (float): step size for x updates
        | device (torch.device): Device to run on
        | dtype (torch.dtype): Data type to use

    Attributes:
        | layers (torch.nn.ModuleList): List of layers
        | in_features (int): Number of input features
        | num_classes (int): Number of classes
        | hidden_sizes (list): List of hidden layer sizes
        | steps (int): Number of steps to run inference for
        | bias (bool): Whether to include bias in layers
        | symmetric (bool): Whether to use same weights for top-down prediction and bottom-up error prop.
        | classifier (torch.nn.Sequential): Classifier to use
    """
    def __init__(self, in_features, num_classes, hidden_sizes = [], steps=20, bias=True, symmetric=True, actv_fn=F.tanh, d_actv_fn=None, gamma=0.1, device=torch.device('cpu'), dtype=None):
        super().__init__(in_features, num_classes, hidden_sizes, steps, bias, symmetric, actv_fn, d_actv_fn, gamma, device, dtype)

    def init_layers(self):
        """
        | Initialises self.layers based on input parameters.
        | Initialises self.classifier as a simple MLP, to classify the output of self.layers.
        """
        layers = []
        in_features = None
        self.sizes = [self.in_features] + self.hidden_sizes
        for out_features in self.sizes:
            layers.append(FC(in_features, out_features, device=self.device, **self.factory_kwargs))
            in_features = out_features
        self.layers = nn.ModuleList(layers)
        
        self.classifier = nn.Sequential(
            nn.Linear(self.sizes[-1], 200, bias=True, device=self.device, dtype=self.factory_kwargs['dtype']),
            nn.ReLU(),
            nn.Linear(200, self.num_classes, bias=False, device=self.device, dtype=self.factory_kwargs['dtype']),
        )

    def to(self, device):
        self.device = device
        for layer in self.layers:
            layer.to(device)
        for layer in self.classifier:
            layer.to(device)
        return self

    def get_output(self, state):
        """
        Takes the output of the last layer from the feature extractor and passes it through the classifier.
        Returns the output of the classifier.

        Args:
            | state (list): List of layer state dicts, each containing 'x' and 'e'

        Returns:
            | out (torch.Tensor): Output of the classifier
        """
        x = state[-1]['x']
        out = self.classifier(x.detach())
        return out

    def forward(self, obs=None, steps=None, back_on_step=False):
        """
        | Performs inference phase of the model. 
        | Uses self.classifier to get output.

        Args:
            | obs (Optional[torch.Tensor]): Input data
            | steps (Optional[int]): Number of steps to run inference for. Uses self.steps if not provided.

        Returns:
            | out (torch.Tensor): Output of the model
            | state (list): List of layer state dicts, each containing 'x' and 'e'
        """
        if steps is None:
            steps = self.steps

        state = self.init_state(obs)

        for i in range(steps):
            temp = self.calc_temp(i, steps)
            self.step(state, obs, temp=temp)
            if back_on_step:
                self.vfe(state).backward()
            
        out = self.get_output(state)
            
        return out, state


    def classify(self, obs, steps=None):
        """
        | Performs inference on the observation and passes the output through the classifier.
        | Returns the argmax of the classifier output.

        Args:
            | obs (torch.Tensor): Input data
            | steps (Optional[int]): Number of steps to run inference for. Uses self.steps if not provided.

        Returns:
            | out (torch.Tensor): Argmax(dim=1) output of the classifier
        """
        return self.forward(obs, steps)[0].argmax(dim=1)


    def reconstruct(self, obs, steps=None):
        """
        | Initialises the state of the model using the observation.
        | Runs inference without pinning the observation.
        | In theory should reconstruct the observation.

        Args:
            | obs (torch.Tensor): Input data
            | steps (Optional[int]): Number of steps to run inference for. Uses self.steps if not provided.

        Returns:
            | out (torch.Tensor): Reconstructed observation
            | state (list): List of layer state dicts, each containing 'x' and 'e'
        """
        if steps is None:
            steps = self.steps
        
        state = self.init_state(obs)

        for i in range(steps):
            temp = self.calc_temp(i, steps)
            self.step(state, temp=temp)
        
        out = state[0]['x']

        return out, state

    
    def generate(self, y, steps=None):
        """
        | Not implemented as one cannot generate an input without a target, and this model does not pin targets.
        """
        raise(NotImplementedError)