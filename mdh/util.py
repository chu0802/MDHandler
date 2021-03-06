import yaml
import pickle as pk
import hashlib
from pathlib import Path
import os
from collections import defaultdict
from tensorboard import program

def config_loading(cfg_path):
    return yaml.load(open(cfg_path, 'r'), Loader=yaml.FullLoader) if cfg_path is not None else None

class TensorboardTool:
    def __init__(self, host):
        self.processes = {}
        self.host = host

    def run(self, logdir, cfg):
        # Start tensorboard server
        tb = program.TensorBoard()
        tb.configure(argv=[None, '--logdir', logdir, '--host', self.host])
        url = tb.launch()
        self.processes[str(cfg)] = url

    def list(self, cont='c'):
        print('All starting up processes: ')
        for k, v in self.processes.items():
            print('%s: %s' % (k, v))

        print('press %s to continue...' % (cont))
        while True:
            opt = input()
            if opt == cont:
                break

class ModelHandler:
    def __init__(self, model_dir, hash_table_name, title=None):
        self.model_dir = Path(model_dir)
        self.hash_table_path = self.model_dir / hash_table_name
        self.title = title
        self.hash_table = defaultdict(dict)
        self.models = []
        self._load()
        
    def _load(self):
        # make the model directory
        self.model_dir.mkdir(parents=True, exist_ok=True)

        # Load the hash table (mapping hashstr to model config)
        if Path(self.hash_table_path).exists():
            with open(self.hash_table_path, 'rb') as f:
                self.hash_table = pk.load(f)
            self.models = list(sorted(
                self.hash_table.values(),
                key=lambda item: os.path.getctime(item['ckpt_dir'])
            ))

    def _list(self, slogan=None):
        self._load()

        os.system('clear')
        if self.title:
            print('\n', '-'*10, self.title, '-'*10, '\n')
        print('Options:')

        for i, val in enumerate(self.models):
            print('\t(%d): %s' % (i, str(val['config'])))

        print('\t(r): Refresh the options')
        print('\t(n): None (When binding tensorboard, list all processes)')
        print(slogan if slogan else 'Select an option', end=': ')

    def _hashing(self, cfg):
        return hashlib.md5(str(cfg).encode('utf-8')).hexdigest()

    def _select(self, slogan=None):
        self._list(slogan=slogan)
        while True:
            opt = input()
            if opt == 'r':
                self._list(slogan=slogan)
            elif opt == 'n':
                return None
            elif opt.isdigit() and (0 <= int(opt) < len(self.models)):
                return self.models[int(opt)]
            else:
                print('\tInvalid.')

    def select_config(self):
        model = self._select('Select a model')
        return model['config'] if model else None

    def get_ckpt_dir (self, cfg):
        return self.hash_table[self._hashing(cfg)]['ckpt_dir']

    def get_ckpt(self, cfg, epoch=None, name=None):
        ckpt_dir = self.get_ckpt_dir(cfg)
        ckpt_file = ('' if name is None else name) + (str(epoch) if epoch else 'final') + '.pt'
        return ckpt_dir / ckpt_file

    def get_log(self, cfg):
        return self.get_ckpt_dir(cfg) / 'log'

    def update(self, cfg):
        hashstr = self._hashing(cfg)

        self.hash_table[hashstr]['config'] = cfg
        self.hash_table[hashstr]['ckpt_dir'] = self.model_dir / hashstr

        # make the log directory
        (self.model_dir / hashstr / 'log').mkdir(parents=True, exist_ok=True)

        with open(self.hash_table_path, 'wb') as f:
            pk.dump(self.hash_table, f)

        self._load()
