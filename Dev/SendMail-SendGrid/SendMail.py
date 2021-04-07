import sendgrid
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
try:

    #TEMPLATE_ID = 'd-76a5f553c9974524a65d9e744822b897' --> key del template dinamico hecho con dynamic templates por la pagina del sendgrid
    API_KEY = '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' # --> api key de la subcripcion del sendgrid
    mail_user = 'jsoaje@piconsulting.com.ar' # usuario o lista de usuarios a enviar mail
    message = Mail(
        from_email= , # --> usuario que envia el mail
        to_emails= mail_user,
        subject='Sending with SendGrid is Fun', # subject 
        html_content='<strong>and easy to do anywhere, even with Python</strong>' # cuerpo del mail el cual esta en html
        )
    '''message.dynamic_template_data = {
        'p_parametro': 'parametro'
        }''' # si tenemos un template hecho con dynamics templates podemos pasarle parametros los cuales se van a mostrar utilizando {{{ p_parametro }}} 
    #message.template_id = TEMPLATE_ID -->para agregar el template en el mensaje
    sendgrid_client = SendGridAPIClient(api_key=API_KEY)
    response = sendgrid_client.send(message)
    print("Codigo: ", response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print("Error al intentar Enviar correo: ", e)