import torch


def main():
    print(torch.__version__)
    # setting device on GPU if available, else CPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Using device:', device)
    print()

    torch.set_float32_matmul_precision('high')

    # Additional Info when using cuda
    if device.type == 'cuda':
        print(torch.cuda.get_device_name(0))
        print('Memory Usage:')
        print('Allocated:', round(torch.cuda.memory_allocated(0) / 1024**3, 1), 'GB')
        print('Cached:   ', round(torch.cuda.memory_reserved(0) / 1024**3, 1), 'GB')

    # test torch installation
    x = torch.rand(5, 3)
    print(x)

    if True:
        try:
            import torch._dynamo as dynamo
            import torchvision.models as models

            torch._dynamo.config.verbose = True
            torch.backends.cudnn.benchmark = True

            model = models.resnet18().cuda()
            model = torch.compile(model, mode="max-autotune", fullgraph=False)
            # model = torch.compile(model)
            print("Model compiled set")
        except Exception as err:
            print(f"Model compile not supported: {err}")

    if False:
        import torch
        import torchvision.models as models

        model = models.resnet18().cuda()
        optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
        # compiled_model = torch.compile(model)

        import torch._dynamo as dynamo

        torch._dynamo.config.verbose = True
        torch.backends.cudnn.benchmark = True

        compiled_model = torch.compile(model)

        x = torch.randn(16, 3, 224, 224).cuda()
        optimizer.zero_grad()
        out = compiled_model(x)
        out.sum().backward()
        optimizer.step()


if __name__ == "__main__":
    # main()
    pass
