from definitions import EXPERIMENTS_DIR, path_join, make_directory, logging


class Experiment(object):
    def __init__(self, name, experiments_dir=EXPERIMENTS_DIR):
        self.name = name
        self.directory = path_join(experiments_dir, name)
        self.images_dir = path_join(self.directory, 'images')
        self.description_file = path_join(self.directory, 'description.json')

        make_directory(self.directory)
        make_directory(self.images_dir)

        self.log_path = path_join(self.directory, 'log.log')
        logging.basicConfig(filename=self.log_path, level=logging.INFO)

    def __enter__(self):
        logging.info('Experiment "{}" folder created'.format(self.name))
        logging.info(str(self))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __str__(self):
        experiment_settings = dict()
        experiment_settings['name'] = self.name
        experiment_settings['directory'] = self.directory
        experiment_settings['images_directory'] = self.images_dir
        experiment_settings['description_file'] = self.description_file
        experiment_settings['log_path'] = self.log_path

        return experiment_settings.__str__()


if __name__ == '__main__':
    with Experiment('Example') as experiment:
        logging.info('Experiment "{}" folder created'.format(experiment.name))
        logging.info(experiment)
