import boto3
import json
import base64
import logging
from fk_queue import SETTINGS


class SQSMessageSender:
    def __init__(self, queue_url):
        session_params = {
            'region_name': SETTINGS.AWS_REGION_NAME
        }
        if SETTINGS.DEBUG_QUEUE:
            session_params['profile_name'] = SETTINGS.AWS_PROFILE_NAME

        self.queue_url = queue_url
        self.sqs = boto3.Session(**session_params).client('sqs')
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def send_message(self, message: str, path: str, method: str) -> bool:
        """
        Envía un mensaje a la cola SQS.

        :param message: El cuerpo del mensaje que se enviará.
        :param path: La ruta lambda a consumir.
        :param method: El método a utilizar en el consumo.
        :return: El ID del mensaje enviado.
        """
        try:
            # Serializa el objeto JSON a una cadena
            json_string = json.dumps(message)

            # Codifica la cadena en Base64
            base64_encoded = base64.b64encode(json_string.encode()).decode()
            python_obj = {"data": base64_encoded, "path": path, "method": method}

            # Convierte el objeto a una cadena JSON
            message_body = json.dumps(python_obj)

            if SETTINGS.DD_ENV in ["localhost"]:
                self.logger.info(f"Sending message in DD_ENV {SETTINGS.DD_ENV}:")
                self.logger.info(f"Queue_url: {self.queue_url}")
                self.logger.info(f"Message: {message_body}")
                return True

            self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=message_body
            )
            self.logger.info(f"Executed queue send_message with path: {path}")
            return True
        except Exception as e:
            self.logger.error(f"Error al enviar el mensaje: {str(e)}")
            return False
