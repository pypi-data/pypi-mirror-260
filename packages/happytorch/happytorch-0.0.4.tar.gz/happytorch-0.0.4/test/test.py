

import happytorch as ht

args = ht.get_args('/home/nemo/Mourn/a2pip/test/configs/4117b_stln_shanhai.yaml')

print(args.memory_size, type(args.memory_size)) 

class newRunner(ht.novaTrainer):
    def __init__(self, args):
        super().__init__(args)

    def test(self):
        print('test')

    def build_train_batch(self):
        return None
    
    def build_test_batch(self):
        return None
    
    def build_model(self):
        return None


runner = newRunner(args)

runner.test()
