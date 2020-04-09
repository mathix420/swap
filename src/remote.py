from PyInquirer import prompt


def get_remote_url(options):
    if options.remote:
        return options.remote
    question = {
        'type': 'input',
        'name': 'remote',
        'message': 'Git remote url for saving these components',
    }
    return prompt(question)['remote']
    