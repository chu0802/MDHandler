from mdh.util import config_loading, ModelHandler

import argparse

def argument_parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, default='sample_config/sample_config.yaml')
    parser.add_argument('-m', '--model', type=str, default='sample_config/model1.yaml')

    return parser.parse_args()

if __name__ == '__main__':
    args = argument_parsing()
    cfg = config_loading(args.config)

    # Load mdh, one should specify:
    # 1). model_path: the directory saving multiple models
    # 2). hash_table_path: a pickle file saving the mapping relationship (one doesn't have to acces this file in general)
    mdh = ModelHandler(cfg['model_path'], cfg['hash_table_path'])

    # ----- training ------ 
    # (one should also pass MDH to the training process, or save it as an attribute in a model object)

    # ----- saving a model -----
    # After training, while saving a model:

    # the argument should be a dictionary (i.e., a config), one could also build an object o, and directly save o.__dict__
    cfg = config_loading(args.model)
    mdh.update(cfg)

    # The default directory hirarchy in MDH:
    # -- model_path/ (saving multiple models in this path)
    #  |__ model_1/ (in a hashing form)
    #  |  |__ log/ (training log, for tensorboard)
    #  |  |__ 1000.pt (a model checkpoint)
    #  |  |__ 2000.pt (another model checkpoint)
    #  |__ model_2/ 
    #     |__ log/
    #     |__ 1000.pt
    #  .
    #  .
    #  .

    # ----- selecting a model -----

    # By using MDH, one could select the prefered model in runtime
    config = mdh.select_config()
    
    # after getting the model config, MDH support 3 operations
    # 1). mdh.get_ckpt_dir(config)
    #  |__ Get the directory saving checkpoint by a model config
    # 2). mdh.get_ckpt(config, epoch=None)
    #  |__ Get the checkpoint in a certain epoch (by default, load 'final.pt')
    # 3). mdh.get_log(config)
    #  |__ Get the log directory by a model config
    # e.g., 
    ckpt_dir = mdh.get_ckpt_dir(config)
    print(ckpt_dir)

