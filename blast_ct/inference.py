import argparse
import json
import os
import pandas as pd
import torch

from blast_ct.nifti.savers import NiftiPatchSaver
from blast_ct.read_config import get_model, get_test_loader
from blast_ct.trainer.inference import ModelInference, ModelInferenceEnsemble


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def run_inference(job_dir, test_csv_path, config_file, saved_model_paths, write_prob_maps, do_localisation,
                  num_reg_runs, native_space):

    with open(config_file, 'r') as f:
        config = json.load(f)

    model = get_model(config)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    if device == 'cpu':
        print('Warning: running on CPU!')
    use_cuda = device == 'cuda'

    test_loader = get_test_loader(config, model, test_csv_path, use_cuda)
    extra_output_names = config['test']['extra_output_names'] if 'extra_output_names' in config['test'] else None

    saver = NiftiPatchSaver(job_dir, test_loader, write_prob_maps=write_prob_maps,
                            extra_output_names=extra_output_names, do_localisation=do_localisation,
                            num_reg_runs=num_reg_runs, native_space=native_space)
    saved_model_paths = saved_model_paths.split()
    n_models = len(saved_model_paths)
    task = config['data']['task']

    if n_models == 1:
        ModelInference(job_dir, device, model, saver, saved_model_paths[0], task)(test_loader)
    elif n_models > 1:
        ModelInferenceEnsemble(job_dir, device, model, saver, saved_model_paths, task)(test_loader)


def inference():
    # install_dir = os.path.dirname(os.path.realpath(__file__))
    # default_config = os.path.join(install_dir, 'data/config.json')
    # saved_model_paths = [os.path.join(install_dir, f'data/saved_models/model_{i:d}.pt') for i in range(1, 13)]
    # default_model_paths = ' '.join(saved_model_paths)
    #
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--job-dir',
    #                     required=True,
    #                     type=str,
    #                     help='Directory for checkpoints, exports, and '
    #                          'logs. Use an existing directory to load a '
    #                          'trained model, or a new directory to retrain')
    # parser.add_argument('--test-csv-path',
    #                     default=None,
    #                     type=str,
    #                     help='Path to test csv file with paths of images and masks.')
    # parser.add_argument('--config-file',
    #                     default=default_config,
    #                     type=str,
    #                     help='A json configuration file for the job (see example files)')
    # parser.add_argument('--device',
    #                     type=str,
    #                     default='cpu',
    #                     help='Device to use for computation')
    # parser.add_argument('--saved-model-paths',
    #                     default=default_model_paths,
    #                     type=str,
    #                     help='Path to saved model or list of paths separated by spaces.')
    # parser.add_argument('--write-prob-maps',
    #                     type=str2bool, nargs='?',
    #                     const=True,
    #                     default=False,
    #                     help='Whether to write probability maps images to disk')
    # parser.add_argument('--do-localisation',
    #                     type=str2bool, nargs='?',
    #                     const=True,
    #                     default=False,
    #                     help='Whether to run localisation or not')
    # parser.add_argument('--num-reg-runs',
    #                     default=1,
    #                     type=int,
    #                     help='How many times to run registration between native scan and CT template.')
    # parser.add_argument('--overwrite',
    #                     type=str2bool, nargs='?',
    #                     const=True,
    #                     default=False,
    #                     help='Whether to overwrite run if already exists')
    # parser.add_argument('--native-space',
    #                     type=str2bool, nargs='?',
    #                     const=True,
    #                     default=True,
    #                     help='Whether to calculate the volumes in native space or atlas space.')
    # parse_args, unknown = parser.parse_known_args()

    # run_inference(**parse_args.__dict__)

    config_file_path = '/code/BLAST_CT_V2_4AIDE/blast_ct/data/config.json'
    saved_model_paths = ' '.join([os.path.join(f'/code/BLAST_CT_V2_4AIDE/blast_ct/models/saved_models/model_{i:d}.torch_model') for i in range(1, 15)])
    input_image_path = '/tmp/image.nii.gz'
    # input_image_path = '/code/BLAST_CT_V2_4AIDE/image.nii.gz'
    job_dir = '/tmp/'
    test_csv_path = os.path.join(job_dir, 'test.csv')
    pd.DataFrame(data=[['image', input_image_path]], columns=['id', 'image']).to_csv(test_csv_path, index=False)
    do_localisation = True
    native_space = True
    num_reg_runs = 1
    write_probability_maps = False

    run_inference(job_dir, test_csv_path, config_file_path, saved_model_paths,
                  write_probability_maps, do_localisation, num_reg_runs, native_space)


if __name__ == "__main__":
    inference()
