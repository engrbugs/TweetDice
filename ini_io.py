import configparser

def save_history_to_config(history, file_path):
    history_config = configparser.ConfigParser()
    if not history_config.has_section('History'):
        history_config.add_section('History')
    history_config.set('History', 'numbers', ','.join(map(str, history)))
    with open(file_path, 'w') as configfile:
        history_config.write(configfile)


def retrieve_history_from_config(file_path):
    history_config = configparser.ConfigParser()
    history_config.read(file_path)
    history_numbers = []
    if 'History' in history_config:
        history_numbers = history_config['History'].get('numbers', '').split(',')
    return list(map(int, history_numbers))


def read_secret_config():
    secret_config = configparser.ConfigParser()
    secret_config.read('secret.ini')
    my_user_id = secret_config.get('Secret', 'user_id')
    my_twitter_data_path = secret_config.get('Secret', 'twitter_data_path')
    history_file = secret_config.get('Secret', 'history_file')
    return my_user_id, my_twitter_data_path, history_file