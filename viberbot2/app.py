from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.location_message import Location
from viberbot.api.messages import TextMessage, LocationMessage, KeyboardMessage, RichMediaMessage
from viberbot.api.viber_requests import ViberConversationStartedRequest, ViberMessageRequest
import config, dbworker, requests

app = Flask(__name__)
viber = Api(BotConfiguration(
    auth_token=config.token,
    name='Test Bot5793',
    avatar='https://armlur.am/wp-content/uploads/2014/09/smile1.jpg'
))

# Обработка сообщений
def HandleText(req):
    msg = req.message.text
    userId = req.sender.id

    # Нажата клавиша "Заказать такси"
    if msg == 'order_taxi':
        dbworker.set_state(userId, config.States.S_START_BOOKING.value)
        return TextMessage(text='Просто отправьте своё местоположение или напишите адрес\n(Например: ул. Новокшонова, 6)', keyboard=config.cancel_kb)
    
    # Нажата клавиша "Да"
    elif msg == 'yes_answer':
        dbworker.set_state(userId, config.States.S_DONE.value)
        return TextMessage(text='Ваш заказ обрабатывается. Мы уведомим Вас.', keyboard=config.main_kb)

    # Нажата клавиша "Назад"
    elif msg == 'cancel_answer' or msg == 'no_answer':
        dbworker.set_state(userId, config.States.S_DONE.value)
        return KeyboardMessage(keyboard=config.main_kb)

    # Нажата клавиша "Назад"
    elif msg == 'back_answer':
        dbworker.set_state(userId, config.States.S_START_BOOKING.value)
        return TextMessage(text='Просто отправьте своё местоположение или напишите адрес\n(Например: ул. Новокшонова, 6)', keyboard=config.cancel_kb)

    # Нажата клавиша "Пропустить"
    elif msg == 'pass_answer':
        dbworker.set_state(userId, config.States.S_DONE.value)
        return TextMessage(text='Вызвать такси по этому адресу?\n' + config.temp_addr, keyboard=config.yes_no_kb)

    ####
    elif dbworker.get_current_state(userId) == config.States.S_START_BOOKING.value:
        dbworker.set_state(userId, config.States.S_ADDITION.value)
        config.temp_addr = msg
        return TextMessage(text='Напишите дополнительную информацию (например, номер подъезда) или нажмите на кнопку "Пропустить"', keyboard=config.back_pass_kb)        

    # Прислан адрес
    elif dbworker.get_current_state(userId) == config.States.S_CONFIRM_ORDER.value:
        #location = message
        dbworker.set_state(userId, config.States.S_CONFIRM_ORDER.value)
        return TextMessage(text='Вызвать такси по этому адресу?\n' + config.temp_addr + '\n\nДополнительная информация:\n' + msg, keyboard=config.yes_no_kb)

    # Прислана доп. информация
    elif dbworker.get_current_state(userId) == config.States.S_ADDITION.value:
        dbworker.set_state(userId, config.States.S_CONFIRM_ORDER.value)
        return

    # Нажата клавиша "Контакты"
    elif msg == 'contacts':
        return TextMessage(text='Пример обработки кнопки', keyboard=config.main_kb)

    # Нажата клавиша "Написать отзыв"
    elif msg == 'feedback':
        return TextMessage(text='Пример обработки кнопки', keyboard=config.main_kb)

    return TextMessage(text='Некорректный запрос', keyboard=config.main_kb)

# Обработка геолокации
def HandleLocation(req):
    location = req.message.location
    lat = location.latitude
    lng = location.longitude

    YANDEX_API_URI = f'https://geocode-maps.yandex.ru/1.x/?format=json&geocode=%D0%A1{lat},{lng}%D0%92'	
    api_request = requests.get(YANDEX_API_URI).json()
    address = api_request['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['formatted']

    # Если адрес не корректный
    if 'Зима' not in address:
        return TextMessage(text='Мы работаем только в пределах города)', keyboard=config.main_kb)

    # Иначе вернуть сообщение с подтверждением
    dbworker.set_state(req.sender.id, config.States.S_ADDITION.value)
    config.temp_addr = address
    return TextMessage(text='Напишите дополнительную информацию (например, номер подъезда) или нажмите на кнопку "Пропустить"', keyboard=config.back_pass_kb)        

    #return TextMessage(text='Ваш адрес: ' + address + '. \nВызвать такси?', keyboard=config.yes_no_kb)


@app.route('/incoming', methods=['POST'])
def incoming():
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        #handle text
        if type(viber_request.message) is TextMessage:
            viber.send_messages(viber_request.sender.id, [HandleText(viber_request)])

        #handle location        
        elif type(viber_request.message) is LocationMessage:
            viber.send_messages(viber_request.sender.id, [HandleLocation(viber_request)])        
    
    elif isinstance(viber_request, ViberConversationStartedRequest):
        viber.send_messages(viber_request.user.id, [TextMessage(text='Здравствуйте, ' + viber_request.user.name + '!\nЧтобы заказать такси, воспользуйтесь клавиатурой ниже', keyboard=config.main_kb)])

    return Response(status=200)

if __name__=='__main__':
    app.run()


# 