import hydra

@hydra.main(config_path="conf", config_name="config")
def app(cfg) -> None:
    config = cfg
    print(config)
    batch_size = cfg.model.hyperparam.batch_size
    print(batch_size)
    data = cfg.data.train.img
    print(data)
if __name__ == "__main__":
    app()
