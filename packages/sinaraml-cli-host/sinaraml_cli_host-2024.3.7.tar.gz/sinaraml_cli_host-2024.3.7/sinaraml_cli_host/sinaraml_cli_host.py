from .sinara_server import SinaraServer
from .sinara_model import SinaraModel

def init_cli(root_parser):
    SinaraServer.add_command_handlers(root_parser)
    SinaraModel.add_command_handlers(root_parser)

def get_subjects():
    return [
        SinaraServer.subject,
        SinaraModel.subject
    ]

def main():
    print('This is SinaraML host CLI plugin for the sinaraml_cli package')
    return -1

if __name__ == "__main__":
    main()
