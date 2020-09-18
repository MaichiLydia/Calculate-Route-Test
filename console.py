import logging
import sys
from api.utils.filemanager import FileManager
from api.utils.dijkstra import Dijkstra
from api.track.schema import TrackSchema
track_schema = TrackSchema()


def get_valid_input(origin, destination, cost=None):
    track_input = {
        "origin": origin.upper(),
        "destination": destination.upper()
    }
    if cost:
        track_input['cost'] = cost
    has_errors = track_schema.validate(track_input)
    if has_errors:
        for key in has_errors.keys():
            logging.error(f"\n{key}: {str(has_errors[key])}")
        return False
    return track_input


def save_track(file_manager):
    exit_save_track = False
    did_save = False
    while not exit_save_track:
        origin = input(f"Digite a origem no formato IATA (3 letras):\n")
        destination = input(f"Digite o destino no formato IATA (3letras):\n")
        cost = input("Digite o custo desse trajeto:\n")
        track_input = get_valid_input(origin, destination, cost)
        if track_input:
            is_saved = file_manager.insert_new_line(track_input)
            if is_saved is True:
                did_save = True
                logging.info("Trajeto salvo com sucesso")
                exit_save_track = True
            else:
                should_continue = input("Não foi possível salvar, tente novamente, aperte S para tentar novamente")
                if should_continue.upper() != "S":
                    exit_save_track = True
    return did_save


def get_best_path(file_manager):
    exit_get_path = False
    succeded = False
    while not exit_get_path:
        origin = input(f"Digite a origem no formato IATA (3 letras):\n")
        destination = input(f"Digite o destino no formato IATA (3 letras):\n")
        track_input = get_valid_input(origin, destination)
        if track_input:
            result = Dijkstra(file_manager.valid_rows, track_input['origin'], track_input['destination']).get_best_path()
            if result:
                print(f"Melhor rota: {result['path']}: R${result['cost']}\n")
                succeded = True
                exit_get_path = True
            else:
                should_continue = input(
                    "Não foi possível encontrar esse caminho, "
                    "tente novamente, aperte S para tentar novamente,"
                    "para voltar ao menu inicial digite qualquer outra tecla")
                if should_continue.upper() != "S":
                    exit_get_path = True
    return succeded


def handle_choice(selected, file_manager):
    result = False
    if selected == 1:
        result = get_best_path(file_manager)
    if selected == 2:
        result = save_track(file_manager)
    return result

def main(argvs):
    system_inputs = argvs
    if len(system_inputs) < 2:
        logging.error(f"""
    Please enter a file and a optional environment setting('dev', 'test', 'prod')
    Example: python app.py file.csv dev
                or
             python app.py file.csv
            """)
    else:
        filename = system_inputs[1]
        file = FileManager(filename)
        choice = None
        print("Bem vindo ao sistema de trajetos, selecione uma opção:")
        while choice != 0:

            choice = int(input("""
1 - Escolher melhor rota 
2 - Cadastrar novo trajeto de viagem
0 - Sair

Qual ação deseja tomar ?"""))
            if choice != 0:
                result = handle_choice(choice, file)
                should_continue = None
                while not should_continue:
                    input_text = "Ação concluida com sucesso."\
                        if result else \
                        "Infelizmente não foi possível executar essa ação."
                    should_continue = input(f"{input_text} Para executar outra ação digite S,"
                    "para sair digite qualquer outra tecla")
                    if should_continue.upper() != "S":
                        choice = 0
        return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
