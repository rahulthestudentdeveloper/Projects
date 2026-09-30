import torch
import torchxrayvision as xrv
from preprocess import preprocess_image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = xrv.models.DenseNet(weights="densenet121-res224-all")
model.to(device)
model.eval()

diseases = model.pathologies


def predict(image):
    """
    Predict chest X-ray diseases. Returns a list of
    {"Disease": ..., "Probability": ...} sorted descending.
    """
    img = preprocess_image(image)
    img = torch.from_numpy(img).float().unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(img)
        outputs = torch.sigmoid(outputs)

    outputs = outputs.squeeze().cpu().numpy()

    results = []
    for disease, score in zip(diseases, outputs):
        results.append({
            "Disease": disease,
            "Probability": round(float(score) * 100, 2)
        })

    results.sort(key=lambda x: x["Probability"], reverse=True)
    return results