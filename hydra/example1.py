import hydra

@hydra.main(config_path="conf", config_name="config.yaml")
def main(cfg):
    config = cfg

    image_path = cfg.data.train.image_path
    label_path = cfg.data.train.label_path
    print(f'image_path: {image_path}')
    print(f'label_path: {label_path}')

    dropout = cfg.model.hyperparam.dropout
    batch_size = cfg.model.hyperparam.batch_size
    epochs = cfg.model.hyperparam.epochs
    print(f'batch_size: {batch_size}')
    print(f'dropout: {dropout}')
    print(f'epochs: {epochs}')

if __name__ == "__main__":
    main()
