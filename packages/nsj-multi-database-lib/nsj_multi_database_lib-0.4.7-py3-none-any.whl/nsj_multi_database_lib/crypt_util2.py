import argparse
import re

from cryptography.fernet import Fernet


class CryptUtil:
    def __init__(self, crypt_key: str) -> None:
        if crypt_key is not None:
            self.crypt_key = crypt_key.encode()
            self.fernet = Fernet(self.crypt_key)

    def decrypt(self, value: str):
        value = value.encode()
        value = self.fernet.decrypt(value).decode()

        return value

    def encrypt(self, value: str):
        value = value.encode()
        value = self.fernet.encrypt(value).decode()

        return value

    def decrypt_key_value_file(self, file_path: str, rewrite: bool = False):
        """
        Lê um arquivo do tipo chave valor, porém descriptgrafando os valores.

        Retorna um dicionário com os valores correspondentes, descriptografados.

        Se receber rewrite=True, reecreve o arquivo, descriptografando todo seus values.
        """
        return self._handle_file(file_path, False, rewrite)

    def encrypt_key_value_file(self, file_path: str, rewrite: bool = False):
        """
        Lê um arquivo do tipo chave valor, porém criptgrafando os valores.

        Retorna um dicionário com os valores correspondentes, criptografados.

        Se receber rewrite=True, reecreve o arquivo, criptografando todo seus values.
        """
        return self._handle_file(file_path, True, rewrite)

    def _handle_file(self, file_path: str, encrypt: bool, rewrite: bool = False):
        """
        Lê o arquivo chave_valor, passado pelo parâmetro file_path, criptografa ou descriptografa
        (de acordo com o parâmetro encrypt) e retorna o resultado.

        Se o parâmetro rewrite=True, reescreve o arquivo (em ordem alfabética das chaves), com
        o resultado do processo.
        """
        matcher_var = re.compile("^([^#=]+)=(.+)$")
        result = {}
        with open(file_path) as f:
            while True:
                line = f.readline()
                if not line:
                    break

                # Testando a expressão regular
                match = matcher_var.match(line)
                if match is None:
                    continue

                key = match.group(1).strip()
                value = match.group(2).strip()

                # Criptografando a variável
                if encrypt:
                    value = self.encrypt(value)
                else:
                    value = self.decrypt(value)

                # Guardando a variável no dicionário
                result[key] = value

        if rewrite:
            lista_keys = list(result)
            lista_keys.sort()

            with open(file_path, mode="w") as f:
                for key in lista_keys:
                    f.write(f"{key}={result[key]}\n")

        return result

    def generate_key(
        self,
    ):
        return Fernet.generate_key().decode()


if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser(
        description="""Utilitário para criptografia e descritografia de strings."""
    )

    # Adding arguments
    parser.add_argument(
        "-v",
        "--value",
        help="Valor a ser criptografado ou decriptografado.",
        required=False,
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Arquivo a ser criptografado ou decriptografado.",
        required=False,
    )
    parser.add_argument("-k", "--key", help="Chave de criptografia.")
    parser.add_argument(
        "-e",
        "--encrypt",
        help="Indica que o script irá criptografar o valor recebido.",
        action="store_true",
    )
    parser.add_argument(
        "-d",
        "--decrypt",
        help="Indica que o script irá descriptografar o valor recebido.",
        action="store_true",
    )
    parser.add_argument(
        "-g",
        "--generate",
        help="Gera uma nova chave de criptografia.",
        action="store_true",
    )

    # Fazendo o parser dos argumentos
    args, _ = parser.parse_known_args()

    # Setando a variável CRYPT_KEY, se passada uma chave por linha de comando
    crypt_util = CryptUtil(args.key)

    # Criptografando
    if args.encrypt:
        if args.value is None and args.file is None:
            raise Exception("Faltando argumento 'value', ou o argumento 'file'.")

        if args.value is not None:
            result = crypt_util.encrypt(args.value)
            print(result)
        elif args.file is not None:
            result = crypt_util.encrypt_key_value_file(args.file, True)
            print("Ok!")

    # Descriptografando
    if args.decrypt:
        if args.value is None and args.file is None:
            raise Exception("Faltando argumento 'value', ou o argumento 'file'.")

        if args.value is not None:
            result = crypt_util.decrypt(args.value)
            print(result)
        elif args.file is not None:
            result = crypt_util.decrypt_key_value_file(args.file, True)
            print("Ok!")

    # Gerando chave de criptografia
    if args.generate:
        result = crypt_util.generate_key()
        print(result)
