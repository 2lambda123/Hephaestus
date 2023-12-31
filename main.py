import pyjson5 as json
from self_supervised.mocov2 import builder
from self_supervised.mae import mae_model
from utilities.utils import prepare_configuration
from training import train_contrastive, train_supervised
import argparse
import pprint
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--supervised', action='store', type=bool, default=True)
    parser.add_argument('--ssl_encoder_path', action='store', type=str, default=None)
    parser.add_argument('--ssl_config_path', action='store', type=str, default=None)
    parser.add_argument('--supervised_img_size', action='store', type=int, default=224)


    args = parser.parse_args()
    if args.supervised:
        config_path = "configs/supervised_configs.json"
        configs = json.load(open(config_path,'r'))
        if args.ssl_encoder_path is not None and args.ssl_config_path is not None:
            configs['ssl_encoder'] = args.ssl_encoder_path
            configs['ssl_config_path'] = args.ssl_config_path
            configs['image_size'] = args.supervised_img_size
        print('Initializing supervised training with configs: ')
        pprint.pprint(configs)
        train_supervised.train(configs)
    else:
        # Parse configurations
        config_path = "configs/configs.json"
        config = prepare_configuration(config_path)
        json.dump(config, open(config["checkpoint_path"] + "/config.json", "w"))

        if config["method"] == "mocov2":
            model = builder.MoCo(
                config,
                config["moco_dim"],
                config["moco_k"],
                config["moco_m"],
                config["moco_t"],
                config["mlp"],
            )
        elif config['method'] == "mae":
            raise NotImplementedError(f'{config["method"]} is not supported.')

        else:
            raise NotImplementedError(f'{config["method"]} is not supported.')

        train_contrastive.exec_model(model, config)
