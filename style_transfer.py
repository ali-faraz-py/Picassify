import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.models as models
import torch.nn.functional as F

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
 
 
class VGG19Features(nn.Module):
 
    def __init__(self):
        super(VGG19Features, self).__init__()
 
        vgg = models.vgg19(pretrained=True).features
 
        self.slice1 = nn.Sequential(*[vgg[i] for i in range(2)])
        self.slice2 = nn.Sequential(*[vgg[i] for i in range(2, 7)])
        self.slice3 = nn.Sequential(*[vgg[i] for i in range(7, 12)])
        self.slice4 = nn.Sequential(*[vgg[i] for i in range(12, 21)])
        self.slice5 = nn.Sequential(*[vgg[i] for i in range(21, 30)])
 
        for param in self.parameters():
            param.requires_grad = False
 
    def forward(self, x):
        h1 = self.slice1(x)
        h2 = self.slice2(h1)
        h3 = self.slice3(h2)
        h4 = self.slice4(h3)
        h5 = self.slice5(h4)
        return h1, h2, h3, h4, h5
 

def gram_matrix(features):
    batch, channels, height, width = features.size()
    features = features.view(channels, height * width)
    gram = torch.mm(features, features.t())
    return gram / (channels * height * width)
 
 
def content_loss(generated_features, content_features):
    return torch.mean((generated_features - content_features) ** 2)
 
 
def style_loss(generated_features, style_features):
    generated_gram = gram_matrix(generated_features)
    style_gram     = gram_matrix(style_features)
    return torch.mean((generated_gram - style_gram) ** 2)
 
 
def compute_total_loss(generated, content_image, style_image,
                       vgg, content_weight, style_weight):
 
    gen_features     = vgg(generated)
    content_features = vgg(content_image)
    style_features   = vgg(style_image)
 
    c_loss = content_loss(gen_features[3], content_features[3])
 
    s_loss = 0
    for gen_f, style_f in zip(gen_features, style_features):
        s_loss += style_loss(gen_f, style_f)
 
    total = content_weight * c_loss + style_weight * s_loss
 
    return total, c_loss, s_loss
 
 
def run_style_transfer(content_image, style_image,
                       steps=300,
                       content_weight=1,
                       style_weight=1000000,
                       progress_callback=None):
 
    vgg = VGG19Features().to(device)
 
    content_image = content_image.to(device)
    style_image   = style_image.to(device)
 
    generated = content_image.clone().requires_grad_(True).to(device)
 
    optimizer = optim.Adam([generated], lr=0.01)
 
    for step in range(1, steps + 1):
        optimizer.zero_grad()
 
        total, c_loss, s_loss = compute_total_loss(
            generated, content_image, style_image,
            vgg, content_weight, style_weight
        )
 
        total.backward()
        optimizer.step()
 
        with torch.no_grad():
            generated.clamp_(-2, 2)
 
        if progress_callback:
            progress_callback(step, steps, total.item(), c_loss.item(), s_loss.item())
 
    return generated
