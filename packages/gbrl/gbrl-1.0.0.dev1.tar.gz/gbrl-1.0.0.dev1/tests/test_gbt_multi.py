import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

ROOT_PATH = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_PATH))

from sklearn import datasets

from gbrl import GradientBoostingTrees, cuda_available, ActorCriticGBRL
from gbrl.gbt import rmse 

N_EPOCHS = 100


def iteration_fit(X, y, model):
    X = X.astype(np.single)
    pg_preds, value_preds = model.predict(X)
    pg_loss, pg_loss_grad = rmse(pg_preds, y[:, :-1])
    vf_loss, value_loss_grad = rmse(value_preds, y[:, -1])
    if len(pg_loss_grad) == 1:
        pg_loss_grad = pg_loss_grad[:, np.newaxis]
    if len(value_loss_grad) == 1:
        value_loss_grad = value_loss_grad[:, np.newaxis]
    # if self.output_dim == 1 and len(loss_grad.shape) == 1:
    #     loss_grad = loss_grad[:, np.newaxis]
    pg_loss_grad = pg_loss_grad.astype(np.single)
    value_loss_grad = value_loss_grad.astype(np.single)

    model.fit(X, pg_loss_grad, value_loss_grad)
    print(f'boosting_iteration: {model.get_iteration()}: {model.get_num_trees()} pg_trees rmse: {pg_loss:.16f} vf_trees rmse: {vf_loss:.16f}')

class TestGBTMulti(unittest.TestCase):

    @classmethod 
    def setUpClass(cls):
        print('Loading data...')
        # Imagine this loads your actual data
        X ,y = datasets.load_diabetes(return_X_y=True, as_frame=False, scaled=False)
        out_dim = 1 if len(y.shape) == 1  else  y.shape[1]
        if out_dim == 1:
            y = y[:, np.newaxis]
        y_fake = y.copy()
        n_cols = 10
        for _ in range(n_cols - 1):
            y = np.concatenate([y, y_fake], axis= 1)
        out_dim = y.shape[1]
        cls.data = (X, y)
        cls.out_dim = out_dim
        cls.n_epochs = 100
        cls.test_dir = tempfile.mkdtemp()
    
    @classmethod 
    def tearDownClass(cls):
        # Remove the directory after the test
        shutil.rmtree(cls.test_dir)


    def test_cosine_cpu(self):
        print("Running Multi test_cosine_cpu")
        X, y = self.data
        tree_struct = {'max_depth': 4, 
                'n_bins': 256,'min_data_in_leaf': 0,
                'par_th': 2,
                'grow_policy': 'greedy'}
        optimizer = { 'algo': 'SGD',
                    'lr': 1.0,
                }
        gbrl_params = dict({"control_variates": False, "split_score_func": "Cosine"})
        model = GradientBoostingTrees(
                            output_dim=self.out_dim,
                            tree_struct=tree_struct,
                            optimizer=optimizer,
                            gbrl_params=gbrl_params,
                            verbose=0,
                            device='cpu')
        epoch = 0
        while epoch < self.n_epochs:
            _ = model.fit(X, y)
            epoch += 1
        y_pred = model.predict(X)
        loss = np.sqrt(np.mean((y_pred.squeeze() - y.squeeze())**2))
        self.assertTrue(loss < 2.0, f'Expected loss = {loss} < 2.0')
        model.save_model(os.path.join(self.test_dir, 'test_cosine_cpu'))

    def test_cosine_adam_cpu(self):
        print("Running Multi test_cosine_adam_cpu")
        X, y = self.data
        tree_struct = {'max_depth': 4, 
                'n_bins': 256,'min_data_in_leaf': 0,
                'par_th': 2,
                'grow_policy': 'greedy'}
        optimizer = { 'algo': 'Adam',
                    'lr': 1.0,
                }
        gbrl_params = dict({"control_variates": False, "split_score_func": "Cosine"})
        model = GradientBoostingTrees(
                            output_dim=self.out_dim,
                            tree_struct=tree_struct,
                            optimizer=optimizer,
                            gbrl_params=gbrl_params,
                            verbose=0,
                            device='cpu')
        epoch = 0
        while epoch < self.n_epochs:
            _ = model.fit(X, y)
            epoch += 1
        y_pred = model.predict(X)
        loss = np.sqrt(np.mean((y_pred.squeeze() - y.squeeze())**2))
        value = 50.0
        self.assertTrue(loss < value, f'Expected loss = {loss} < {value}')
        model.save_model(os.path.join(self.test_dir, 'test_cosine_adam_cpu'))

    @unittest.skipIf(not cuda_available(), "cuda not available skipping over gpu tests")
    def test_cosine_gpu(self):
        print("Running Multi test_cosine_gpu")
        X, y = self.data
        tree_struct = {'max_depth': 4, 
                       'n_bins': 256,'min_data_in_leaf': 0,
                       'par_th': 2,
                       'grow_policy': 'greedy'}
        optimizer = { 'algo': 'SGD',
                    'lr': 1.0,
                }
        gbrl_params = dict({"control_variates": False, "split_score_func": "Cosine"})
        model = GradientBoostingTrees(
                            output_dim=self.out_dim,
                            tree_struct=tree_struct,
                            optimizer=optimizer,
                            gbrl_params=gbrl_params,
                            verbose=0,
                            device='cuda')
        epoch = 0
        while epoch < self.n_epochs:
            _ = model.fit(X, y)
            epoch += 1
        y_pred = model.predict(X)
        loss = np.sqrt(np.mean((y_pred.squeeze() - y.squeeze())**2))
        self.assertTrue(loss < 2.0, f'Expected loss = {loss} < 2.0')
        model.save_model(os.path.join(self.test_dir, 'test_cosine_gpu'))

    def test_cosine_oblivious_cpu(self):
        print("Running Multi test_cosine_oblivious_cpu")
        X, y = self.data
        tree_struct = {'max_depth': 4, 
                'n_bins': 256,'min_data_in_leaf': 0,
                'par_th': 2,
                'grow_policy': 'oblivious'}
        optimizer = { 'algo': 'SGD',
                    'lr': 1.0,
                }
        gbrl_params = dict({"control_variates": False, "split_score_func": "Cosine"})
        model = GradientBoostingTrees(
                            output_dim=self.out_dim,
                            tree_struct=tree_struct,
                            optimizer=optimizer,
                            gbrl_params=gbrl_params,
                            verbose=0,
                            device='cpu')
        epoch = 0
        while epoch < self.n_epochs:
            _ = model.fit(X, y)
            epoch += 1
        y_pred = model.predict(X)
        loss = np.sqrt(np.mean((y_pred.squeeze() - y.squeeze())**2))
        self.assertTrue(loss < 12, f'Expected loss = {loss} < 12')
        model.save_model(os.path.join(self.test_dir, 'test_cosine_oblivious_cpu'))
    
    @unittest.skipIf(not cuda_available(), "cuda not available skipping over gpu tests")
    def test_cosine_oblivious_gpu(self):
        print("Running Multi test_cosine_oblivious_gpu")
        X, y = self.data
        tree_struct = {'max_depth': 4, 
                'n_bins': 256,'min_data_in_leaf': 0,
                'par_th': 2,
                'grow_policy': 'oblivious'}
        optimizer = { 'algo': 'SGD',
                    'lr': 1.0,
                }
        gbrl_params = dict({"control_variates": False, "split_score_func": "Cosine"})
        model = GradientBoostingTrees(
                            output_dim=self.out_dim,
                            tree_struct=tree_struct,
                            optimizer=optimizer,
                            gbrl_params=gbrl_params,
                            verbose=0,
                            device='cuda')
        epoch = 0
        while epoch < self.n_epochs:
            _ = model.fit(X, y)
            epoch += 1
        y_pred = model.predict(X)
        loss = np.sqrt(np.mean((y_pred.squeeze() - y.squeeze())**2))
        self.assertTrue(loss < 12, f'Expected loss = {loss} < 12')
        model.save_model(os.path.join(self.test_dir, 'test_cosine_oblivious_gpu'))

    def test_l2_cpu(self):
        print("Running Multi test_l2_cpu")
        X, y = self.data
        tree_struct = {'max_depth': 4, 
                'n_bins': 256,'min_data_in_leaf': 0,
                'par_th': 2,
                'grow_policy': 'greedy'}
        optimizer = { 'algo': 'SGD',
                    'lr': 1.0,
                }
        gbrl_params = dict({"control_variates": False, "split_score_func": "L2"})
        model = GradientBoostingTrees(
                            output_dim=self.out_dim,
                            tree_struct=tree_struct,
                            optimizer=optimizer,
                            gbrl_params=gbrl_params,
                            verbose=0,
                            device='cpu')
        epoch = 0
        while epoch < self.n_epochs:
            _ = model.fit(X, y)
            epoch += 1
        y_pred = model.predict(X)
        loss = np.sqrt(np.mean((y_pred.squeeze() - y.squeeze())**2))
        self.assertTrue(loss < 0.5, f'Expected loss = {loss} < 0.5')
        model.save_model(os.path.join(self.test_dir, 'test_l2_cpu'))

    @unittest.skipIf(not cuda_available(), "cuda not available skipping over gpu tests")
    def test_l2_gpu(self):
        print("Running Multi test_l2_gpu")
        X, y = self.data
        tree_struct = {'max_depth': 4, 
                'n_bins': 256,'min_data_in_leaf': 0,
                'par_th': 2,
                'grow_policy': 'greedy'}
        optimizer = { 'algo': 'SGD',
                    'lr': 1.0,
                }
        gbrl_params = dict({"control_variates": False, "split_score_func": "L2"})
        model = GradientBoostingTrees(
                            output_dim=self.out_dim,
                            tree_struct=tree_struct,
                            optimizer=optimizer,
                            gbrl_params=gbrl_params,
                            verbose=0,
                            device='cuda')
        epoch = 0
        while epoch < self.n_epochs:
            _ = model.fit(X, y)
            epoch += 1
        y_pred = model.predict(X)
        loss = np.sqrt(np.mean((y_pred.squeeze() - y.squeeze())**2))
        self.assertTrue(loss < 0.5, f'Expected loss = {loss} < 0.5')
        model.save_model(os.path.join(self.test_dir, 'test_l2_gpu'))

    def test_l2_oblivious_cpu(self):
        print("Running Multi test_l2_oblivious_cpu")
        X, y = self.data
        tree_struct = {'max_depth': 4, 
                'n_bins': 256,'min_data_in_leaf': 0,
                'par_th': 2,
                'grow_policy': 'oblivious'}
        optimizer = { 'algo': 'SGD',
                    'lr': 1.0,
                }
        gbrl_params = dict({"control_variates": False, "split_score_func": "L2"})
        model = GradientBoostingTrees(
                            output_dim=self.out_dim,
                            tree_struct=tree_struct,
                            optimizer=optimizer,
                            gbrl_params=gbrl_params,
                            verbose=0,
                            device='cpu')
        epoch = 0
        while epoch < self.n_epochs:
            _ = model.fit(X, y)
            epoch += 1
        y_pred = model.predict(X)
        loss = np.sqrt(np.mean((y_pred.squeeze() - y.squeeze())**2))
        self.assertTrue(loss < 10.0, f'Expected loss = {loss} < 10.0')
        model.save_model(os.path.join(self.test_dir, 'test_l2_oblivious_cpu'))

    def test_1shared_cpu(self):
        print("Running shared_cpu")
        X, y = self.data
        tree_struct = {'max_depth': 4, 
                        'n_bins': 256,'min_data_in_leaf': 0,
                        'par_th': 2,
                        'grow_policy': 'greedy'
                        }
        pg_optimizer = {
            'pg_algo': 'SGD',
            'pg_lr': 1.0,
        }
        value_optimizer = {
                    'vf_algo': 'SGD',
                    'vf_lr': 0.1,
                }
        gbrl_params = dict({"control_variates": False, "split_score_func": "cosine"})
        model = ActorCriticGBRL(
                            output_dim=self.out_dim,
                            tree_struct=tree_struct,
                            pg_optimizer=pg_optimizer,
                            shared_tree_struct=True,
                            value_optimizer=value_optimizer,
                            gbrl_params=gbrl_params,
                            verbose=0,
                            device='cpu')
        model.init_model()
        epoch = 0
        while epoch < self.n_epochs:
            iteration_fit(X, y, model)
            
            epoch += 1

        pg_y, vf_y = model.predict(X)
        pg_loss, _ = rmse(pg_y, y[:, :-1])
        vf_loss, _ = rmse(vf_y, y[:, -1])
        pg_value = 10.0
        vf_value = 30
        self.assertTrue(pg_loss < pg_value, f'Expected loss = {pg_loss} < {pg_value}')
        self.assertTrue(vf_loss < vf_value, f'Expected loss = {vf_loss} < {vf_value}')
        model.save_model(os.path.join(self.test_dir, 'test_shared_cpu'))

    def test_1separate_cpu(self):
        print("Running separate_cpu")
        X, y = self.data
        tree_struct = {'max_depth': 4, 
                        'n_bins': 256,'min_data_in_leaf': 0,
                        'par_th': 2,
                        'grow_policy': 'greedy'
                        }
        pg_optimizer = {
            'pg_algo': 'SGD',
            'pg_lr': 1.0,
        }
        value_optimizer = {
                    'vf_algo': 'SGD',
                    'vf_lr': 0.1,
                }
        gbrl_params = dict({"control_variates": False, "split_score_func": "cosine"})
        model = ActorCriticGBRL(
                            output_dim=self.out_dim,
                            tree_struct=tree_struct,
                            pg_optimizer=pg_optimizer,
                            shared_tree_struct=False,
                            value_optimizer=value_optimizer,
                            gbrl_params=gbrl_params,
                            verbose=0,
                            device='cpu')
        model.init_model()
        epoch = 0
        while epoch < self.n_epochs:
            iteration_fit(X, y, model)
            
            epoch += 1

        pg_y, vf_y = model.predict(X)
        pg_loss, _ = rmse(pg_y, y[:, :-1])
        vf_loss, _ = rmse(vf_y, y[:, -1])
        pg_value = 2.0
        vf_value = 30
        self.assertTrue(pg_loss < pg_value, f'Expected loss = {pg_loss} < {pg_value}')
        self.assertTrue(vf_loss < vf_value, f'Expected loss = {vf_loss} < {vf_value}')
        model.save_model(os.path.join(self.test_dir, 'test_separate_cpu'))

    @unittest.skipIf(not cuda_available(), "cuda not available skipping over gpu tests")
    def test_1separate_gpu(self):
        print("Running separate_gpu")
        X, y = self.data
        tree_struct = {'max_depth': 4, 
                        'n_bins': 256,'min_data_in_leaf': 0,
                        'par_th': 2,
                        'grow_policy': 'greedy'
                        }
        pg_optimizer = {
            'pg_algo': 'SGD',
            'pg_lr': 1.0,
        }
        value_optimizer = {
                    'vf_algo': 'SGD',
                    'vf_lr': 0.1,
                }
        gbrl_params = dict({"control_variates": False, "split_score_func": "cosine"})
        model = ActorCriticGBRL(
                            output_dim=self.out_dim,
                            tree_struct=tree_struct,
                            pg_optimizer=pg_optimizer,
                            shared_tree_struct=False,
                            value_optimizer=value_optimizer,
                            gbrl_params=gbrl_params,
                            verbose=0,
                            device='gpu')
        model.init_model()
        epoch = 0
        while epoch < self.n_epochs:
            iteration_fit(X, y, model)
            
            epoch += 1

        pg_y, vf_y = model.predict(X)
        pg_loss, _ = rmse(pg_y, y[:, :-1])
        vf_loss, _ = rmse(vf_y, y[:, -1])
        pg_value = 2.0
        vf_value = 30
        self.assertTrue(pg_loss < pg_value, f'Expected loss = {pg_loss} < {pg_value}')
        self.assertTrue(vf_loss < vf_value, f'Expected loss = {vf_loss} < {vf_value}')
        model.save_model(os.path.join(self.test_dir, 'test_separate_gpu'))

    @unittest.skipIf(not cuda_available(), "cuda not available skipping over gpu tests")
    def test_1shared_gpu(self):
        print("Running shared_gpu")
        X, y = self.data
        tree_struct = {'max_depth': 4, 
                        'n_bins': 256,'min_data_in_leaf': 0,
                        'par_th': 2,
                        'grow_policy': 'greedy'
                        }
        pg_optimizer = {
            'pg_algo': 'SGD',
            'pg_lr': 1.0,
        }
        value_optimizer = {
                    'vf_algo': 'SGD',
                    'vf_lr': 0.1,
                }
        gbrl_params = dict({"control_variates": False, "split_score_func": "cosine"})
        model = ActorCriticGBRL(
                            output_dim=self.out_dim,
                            tree_struct=tree_struct,
                            pg_optimizer=pg_optimizer,
                            shared_tree_struct=True,
                            value_optimizer=value_optimizer,
                            gbrl_params=gbrl_params,
                            verbose=0,
                            device='cuda')
        model.init_model()
        epoch = 0
        while epoch < self.n_epochs:
            iteration_fit(X, y, model)
            
            epoch += 1

        pg_y, vf_y = model.predict(X)
        pg_loss, _ = rmse(pg_y, y[:, :-1])
        vf_loss, _ = rmse(vf_y, y[:, -1])
        pg_value = 10.0
        vf_value = 30
        self.assertTrue(pg_loss < pg_value, f'Expected loss = {pg_loss} < {pg_value}')
        self.assertTrue(vf_loss < vf_value, f'Expected loss = {vf_loss} < {vf_value}')
        model.save_model(os.path.join(self.test_dir, 'test_shared_gpu'))

    @unittest.skipIf(not cuda_available(), "cuda not available skipping over gpu tests")
    def test_l2_oblivious_gpu(self):
        print("Running Multi test_l2_oblivious_gpu")
        X, y = self.data
        tree_struct = {'max_depth': 4, 
                'n_bins': 256,'min_data_in_leaf': 0,
                'par_th': 2,
                'grow_policy': 'oblivious'}
        optimizer = { 'algo': 'SGD',
                    'lr': 1.0,
                }
        gbrl_params = dict({"control_variates": False, "split_score_func": "L2"})
        model = GradientBoostingTrees(
                            output_dim=self.out_dim,
                            tree_struct=tree_struct,
                            optimizer=optimizer,
                            gbrl_params=gbrl_params,
                            verbose=0,
                            device='cuda')
        epoch = 0
        while epoch < self.n_epochs:
            _ = model.fit(X, y)
            epoch += 1
        y_pred = model.predict(X)
        loss = np.sqrt(np.mean((y_pred.squeeze() - y.squeeze())**2))
        self.assertTrue(loss < 10.0, f'Expected loss = {loss} < 10.0')
        model.save_model(os.path.join(self.test_dir, 'test_l2_oblivious_gpu'))

    def test_loading(self):
        X, y = self.data

        model = GradientBoostingTrees.load_model(os.path.join(self.test_dir, 'test_cosine_cpu'))
        y_pred = model.predict(X)
        loss = np.sqrt(np.mean((y_pred.squeeze() - y.squeeze())**2))
        self.assertTrue(loss < 2.0, f'Expected loss = {loss} < 2.0')
        
        
        model = GradientBoostingTrees.load_model(os.path.join(self.test_dir, 'test_l2_cpu'))
        y_pred = model.predict(X)
        loss = np.sqrt(np.mean((y_pred.squeeze() - y.squeeze())**2))
        self.assertTrue(loss < 0.5, f'Expected loss = {loss} < 0.5')

        model = ActorCriticGBRL.load_model(os.path.join(self.test_dir, 'test_shared_cpu'))
        pg_y, vf_y = model.predict(X)
        pg_loss, _ = rmse(pg_y, y[:, :-1])
        vf_loss, _ = rmse(vf_y, y[:, -1])
        pg_value = 10.0
        vf_value = 30
        self.assertTrue(pg_loss < pg_value, f'Expected loss = {pg_loss} < {pg_value}')
        self.assertTrue(vf_loss < vf_value, f'Expected loss = {vf_loss} < {vf_value}')

        model = ActorCriticGBRL.load_model(os.path.join(self.test_dir, 'test_separate_cpu'))
        pg_y, vf_y = model.predict(X)
        pg_loss, _ = rmse(pg_y, y[:, :-1])
        vf_loss, _ = rmse(vf_y, y[:, -1])
        pg_value = 2.0
        vf_value = 30
        self.assertTrue(pg_loss < pg_value, f'Expected loss = {pg_loss} < {pg_value}')
        self.assertTrue(vf_loss < vf_value, f'Expected loss = {vf_loss} < {vf_value}')
        
        if (cuda_available()):
            model = GradientBoostingTrees.load_model(os.path.join(self.test_dir, 'test_cosine_gpu'))
            y_pred = model.predict(X)
            loss = np.sqrt(np.mean((y_pred.squeeze() - y.squeeze())**2))
            self.assertTrue(loss < 2.0, f'Expected loss = {loss} < 2.0')
            
            model = GradientBoostingTrees.load_model(os.path.join(self.test_dir, 'test_cosine_oblivious_gpu'))
            y_pred = model.predict(X)
            loss = np.sqrt(np.mean((y_pred.squeeze() - y.squeeze())**2))
            self.assertTrue(loss < 12.0, f'Expected loss = {loss} < 12.0')
            
            model = GradientBoostingTrees.load_model(os.path.join(self.test_dir, 'test_l2_gpu'))
            y_pred = model.predict(X)
            loss = np.sqrt(np.mean((y_pred.squeeze() - y.squeeze())**2))
            self.assertTrue(loss < 0.5, f'Expected loss = {loss} < 0.5')

            model = GradientBoostingTrees.load_model(os.path.join(self.test_dir, 'test_l2_oblivious_gpu'))
            y_pred = model.predict(X)
            loss = np.sqrt(np.mean((y_pred.squeeze() - y.squeeze())**2))
            self.assertTrue(loss < 10.0, f'Expected loss = {loss} < 10.0')

            model = ActorCriticGBRL.load_model(os.path.join(self.test_dir, 'test_shared_gpu'))
            pg_y, vf_y = model.predict(X)
            pg_loss, _ = rmse(pg_y, y[:, :-1])
            vf_loss, _ = rmse(vf_y, y[:, -1])
            pg_value = 10.0
            vf_value = 30
            self.assertTrue(pg_loss < pg_value, f'Expected loss = {pg_loss} < {pg_value}')
            self.assertTrue(vf_loss < vf_value, f'Expected loss = {vf_loss} < {vf_value}')

            model = ActorCriticGBRL.load_model(os.path.join(self.test_dir, 'test_separate_gpu'))
            pg_y, vf_y = model.predict(X)
            pg_loss, _ = rmse(pg_y, y[:, :-1])
            vf_loss, _ = rmse(vf_y, y[:, -1])
            pg_value = 2.0
            vf_value = 30
            self.assertTrue(pg_loss < pg_value, f'Expected loss = {pg_loss} < {pg_value}')
            self.assertTrue(vf_loss < vf_value, f'Expected loss = {vf_loss} < {vf_value}')

        model = GradientBoostingTrees.load_model(os.path.join(self.test_dir, 'test_cosine_adam_cpu'))
        y_pred = model.predict(X)
        loss = np.sqrt(np.mean((y_pred.squeeze() - y.squeeze())**2))
        value = 50.0
        self.assertTrue(loss < value, f'Expected loss = {loss} < {value}')


if __name__ == '__main__':
    unittest.main()