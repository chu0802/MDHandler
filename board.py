import argparse
from mdh.util import config_loading, ModelHandler, TensorboardTool

def argument_parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, default='sample_config/config.yaml')
    parser.add_argument('-h', '--host', type=str, default='clais1.csie.org')

    return parser.parse_args()

if __name__ == '__main__':
    # Get configuration
    args = argument_parsing()
    config = config_loading(args.config) 

    # load mdh
    mdh = ModelHandler(
        args.config['model_path']
        args.config['hash_table_path'], 
        title='Tensorboard Binding System',
    )

    # load tbtool
    tbtool = TensorboardTool(args.host)
    # binding
    while True:
        try:
            cfg = mdh.select_config()
            if cfg:
                log_dir = mdh.get_log(cfg)
                tbtool.run(str(log_dir), cfg=cfg)
            else:
                tbtool.list()
        except KeyboardInterrupt:
            print('Shutting Down')
            break
