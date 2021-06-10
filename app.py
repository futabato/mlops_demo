import hydra

@hydra.main(config_path="./config.yaml")
def app(cfg):
    print(cfg.pretty())

if __name__ == "__main__":
    app()
