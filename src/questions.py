from PyInquirer import prompt


def get_sub_folder(options):
    if options.folder:
        return options.folder
    question = {
        'type': 'input',
        'name': 'folder',
        'default': './',
        'message': 'Sub folder containing all the components',
    }
    return prompt(question)['folder']


def get_remote_url(options):
    if options.remote:
        return options.remote
    question = {
        'type': 'input',
        'name': 'remote',
        'message': 'Git remote url for saving these components',
    }
    return prompt(question)['remote']
    