import config as cf
from handlers.check_handler import CheckHandler
from handlers.message_handler import MessageHandler
from handlers.login_handler import LogInHandler
from handlers.logout_handler import LogOutHandler
from rq import get_current_job

def run_task(service_type, ret_url, arg_list):
    task_id = get_current_job().get_id()

    if service_type == cf.WHATSAPP_CHECK:
        phone_number = arg_list[0]

        check_handler = CheckHandler(task_id, ret_url, phone_number)
        check_handler.run()

    elif service_type == cf.WHATSAPP_MESSAGE:
        phone_number = arg_list[0]
        message = arg_list[1]

        message_handler = MessageHandler(task_id, ret_url, phone_number, message)
        message_handler.run()
    
    elif service_type == cf.WHATSAPP_LOGIN:
        log_in_handler = LogInHandler(task_id, ret_url)
        log_in_handler.run()
    
    elif service_type == cf.WHATSAPP_LOGOUT:
        log_out_handler = LogOutHandler(task_id, ret_url)
        log_out_handler.run()
