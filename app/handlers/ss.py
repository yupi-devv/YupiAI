from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from app.ai.aigentext import generate, gen_from_image
from app.ai.aisearch import aisearch_internet
from app.ai.aigenimage import generate_image
from app.ai.aiaudio import transcribe_audio
from app.ai.aispeech import ai_speech
from app.ai.aimain import getfunc
from app.ai.scrape import sum_from_link, sum_from_inp
from app.utils.text import answer_manipulate
from app.utils.allowed_users import ALLOWED_IDS
from app.utils.pdf_to_text import extract_text_from_pdf
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
from aiogram.types import FSInputFile
import os
from loguru import logger
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.utils.history import append_to_json_file

rt = Router() 



class GenAns(StatesGroup):
    generate = State()


@rt.message(Command('clear_history'))
async def cleary(msg: Message, state: FSMContext):
    try:
        await state.clear()
        await msg.delete()
        os.remove(f"users_histories/{msg.from_user.id}.json")
        await msg.answer('✅ История сообщений очищена!')
    except Exception as ex:
        logger.error(f'Ошибка с очисткой:\n{ex}')

@rt.message(GenAns.generate)
async def mmm(msg: Message, state: FSMContext):
    try:
        dat = await state.get_data()
        msg_id = dat["genmessage_id"]
        await msg.delete()
        await msg.bot.edit_message_text(text='Подождите, идет генерация❗️❗️❗️', chat_id=msg.chat.id, message_id=msg_id)
    except:
        None


@rt.message(F.text, F.text != '/start', F.text != '/clear_history', F.func(lambda msg: msg if msg.from_user.id in ALLOWED_IDS or '*' in ALLOWED_IDS or str(msg.from_user.id) in ALLOWED_IDS else None))
async def cmd_text(msg: Message, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.button(text='Прислать ответ голосовым', callback_data='answer_audio')
    try:
        func = await getfunc(msg.text)
        func = func.lstrip('[').rstrip(']')
        
        data = {'role': 'user', 'content': msg.text}
        await append_to_json_file(data, f'users_histories/{msg.from_user.id}.json')
        if '_scrape_url_' in func:
            await msg.reply('📝 Погоди, сокращаю....')
            await state.set_state(GenAns.generate)
            await state.set_data(data={'genmessage_id': msg.message_id+1})
            result = ''
            for i in range(3):
                try:
                    link = func.split(', ')[1]

                    result = await sum_from_link(link)
                    ddd = await answer_manipulate(result)
                    if type(ddd) == list:
                        for i in ddd:
                            if ddd[0] == i:
                                await msg.bot.edit_message_text(text=i, chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                            elif ddd[-1] == i:
                                await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                            else:
                                await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    else:
                        await msg.bot.edit_message_text(text=ddd, reply_markup=kb.as_markup(), chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    await state.clear()
                    if result == '':
                        continue
                    break
                except:
                    continue
            dt = {'role': 'assistant', 'content': result}
            await append_to_json_file(dt, f'users_histories/{msg.from_user.id}.json')

                    
        elif '_gen_text_' in func:
            await msg.reply('🥸 Погоди, генерирую ответ....')
            await state.set_state(GenAns.generate)
            await state.set_data(data={'genmessage_id': msg.message_id+1})
            result = ''
            for i in range(3):
                try:
                    result = await generate(msg.text, msg.from_user.id)
                    ddd = await answer_manipulate(result)
                    if type(ddd) == list:
                        for i in ddd:
                            if ddd[0] == i:
                                await msg.bot.edit_message_text(text=i, chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                            elif ddd[-1] == i:
                                await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                            else:
                                await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    else:
                        await msg.bot.edit_message_text(text=ddd, reply_markup=kb.as_markup(), chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    await state.clear()
                    if result == '':
                        continue
                    break
                except:
                    continue
            dt = {'role': 'assistant', 'content': result}
            await append_to_json_file(dt, f'users_histories/{msg.from_user.id}.json')


        elif '_scrape_input_' in func:
            await msg.reply('📝 Погоди, сокращаю....')
            await state.set_state(GenAns.generate)
            await state.set_data(data={'genmessage_id': msg.message_id+1})
            result = ''
            for i in range(3):
                try:
                    result = await sum_from_inp(msg.text)
                    ddd = await answer_manipulate(result)
                    if type(ddd) == list:
                        for i in ddd:
                            if ddd[0] == i:
                                await msg.bot.edit_message_text(text=i, chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                            elif ddd[-1] == i:
                                await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                            else:
                                await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    else:
                        await msg.bot.edit_message_text(text=ddd, reply_markup=kb.as_markup(), chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    await state.clear()
                    if result == '':
                        continue
                    break
                except:
                    continue
            dt = {'role': 'assistant', 'content': result}
            await append_to_json_file(dt, f'users_histories/{msg.from_user.id}.json')


        elif '_gen_image_' in func:
            await msg.reply('🎆 Погоди, генерирую картинку....')
            await state.set_state(GenAns.generate)
            await state.set_data(data={'genmessage_id': msg.message_id+1})
            result = ''
            for i in range(3):
                try:
                    result = await generate_image(msg.text)
                    photo = FSInputFile(result)
                    await msg.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id+1)
                    await msg.reply_photo(photo, reply_to_message_id=msg.message_id)
                    await state.clear()
                    dd = await gen_from_image('Что изображено на этой картинке?', result)
                    os.remove(result)
                    if result == '':
                        continue
                    break
                except:
                    continue
            dt = {'role': 'assistant', 'content': dd}
            await append_to_json_file(dt, f'users_histories/{msg.from_user.id}.json')


        
        elif '_search_in_inet_' in func:
            await msg.reply('🌐 Погоди, ищу в инете....')
            await state.set_state(GenAns.generate)
            await state.set_data(data={'genmessage_id': msg.message_id+1})
            result = ''
            for i in range(3):
                try:
                    result = await aisearch_internet(text=msg.text, usr_id=msg.from_user.id)
                    ddd = await answer_manipulate(result)
                    if type(ddd) == list:
                        for i in ddd:
                            if ddd[0] == i:
                                await msg.bot.edit_message_text(text=i, chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                            elif ddd[-1] == i:
                                await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                            else:
                                await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    else:
                        await msg.bot.edit_message_text(text=ddd, chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    await state.clear()
                    if result == '':
                        continue
                    break
                except:
                    continue
            
            dt = {'role': 'assistant', 'content': result}
            await append_to_json_file(dt, f'users_histories/{msg.from_user.id}.json')

    except Exception as ex:
        logger.error(f'Ошибка:\n{ex}')    

    
@rt.message(F.document, F.func(lambda msg: msg if msg.from_user.id in ALLOWED_IDS or '*' in ALLOWED_IDS or str(msg.from_user.id) in ALLOWED_IDS else None))
async def doc(msg: Message, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.button(text='Прислать ответ голосовым', callback_data='answer_audio')
    cm = msg.document
    docm = cm.file_name
    file_id = cm.file_id
    if docm[-3]+docm[-2]+docm[-1] == 'pdf':
        dd = str(datetime.now()).split(' ')
        dttime = dd[0] + '_' + dd[1]
        file = await msg.bot.get_file(file_id)
        file_path = file.file_path
        await msg.bot.download_file(file_path, f"users_docs/{dttime}.pdf")
        ww = await extract_text_from_pdf(f'users_docs/{dttime}.pdf')
        ww = ww + f'{msg.caption}'
        os.remove(f'users_docs/{dttime}.pdf')
        data = {'role': 'user', 'content': msg.caption}
        await append_to_json_file(data, f'users_histories/{msg.from_user.id}.json')
        try:
            func = await getfunc(ww)
            func = func.lstrip('[').rstrip(']')
            if '_scrape_url_' in func:
                await msg.reply('📝 Погоди, сокращаю....')
                await state.set_state(GenAns.generate)
                await state.set_data(data={'genmessage_id': msg.message_id+1})
                result = ''
                for i in range(3):
                    try:
                        link = func.split(', ')[1]
                        
                        result = await sum_from_link(link)
                        ddd = await answer_manipulate(result)
                        if type(ddd) == list:
                            for i in ddd:
                                if ddd[0] == i:
                                    await msg.bot.edit_message_text(text=i, chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                                elif ddd[-1] == i:
                                    await msg.answer(text=i, reply_markup=kb.as_markup(), disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                                else:
                                    await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                        else:
                            await msg.bot.edit_message_text(text=ddd, reply_markup=kb.as_markup(), chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                        await state.clear()
                        if result == '':
                            continue
                        break
                    except:
                        continue
                dt = {'role': 'assistant', 'content': result}
                await append_to_json_file(dt, f'users_histories/{msg.from_user.id}.json')

                        
            elif '_gen_text_' in func:
                await msg.reply('🥸 Погоди, генерирую ответ....')
                await state.set_state(GenAns.generate)
                await state.set_data(data={'genmessage_id': msg.message_id+1})
                result = ''
                for i in range(3):
                    try:
                        result = await generate(ww, msg.from_user.id)
                        ddd = await answer_manipulate(result)
                        if type(ddd) == list:
                            for i in ddd:
                                if ddd[0] == i:
                                    await msg.bot.edit_message_text(text=i, chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                                elif ddd[-1] == i:
                                    await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                                else:
                                    await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                        else:
                            await msg.bot.edit_message_text(text=ddd, reply_markup=kb.as_markup(), chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                        await state.clear()
                        if result == '':
                            continue
                        break
                    except:
                        continue
                dt = {'role': 'assistant', 'content': result}
                await append_to_json_file(dt, f'users_histories/{msg.from_user.id}.json')

            elif '_scrape_input_' in func:
                await msg.reply('📝 Погоди, сокращаю....')
                await state.set_state(GenAns.generate)
                await state.set_data(data={'genmessage_id': msg.message_id+1})
                for i in range(3):
                    try:
                        result = await sum_from_inp(ww)
                        ddd = await answer_manipulate(result)
                        if type(ddd) == list:
                            for i in ddd:
                                if ddd[0] == i:
                                    await msg.bot.edit_message_text(text=i, chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                                elif ddd[-1] == i:
                                    await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                                else:
                                    await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                        else:
                            await msg.bot.edit_message_text(text=ddd, reply_markup=kb.as_markup(), chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                        await state.clear()
                        if result == '':
                            continue
                        break
                    except:
                        continue
                dt = {'role': 'assistant', 'content': result}
                await append_to_json_file(dt, f'users_histories/{msg.from_user.id}.json')

            elif '_gen_image_' in func:
                await msg.reply('🎆 Погоди, генерирую картинку....')
                await state.set_state(GenAns.generate)
                await state.set_data(data={'genmessage_id': msg.message_id+1})
                for i in range(3):
                    try:
                        result = await generate_image(ww)
                        photo = FSInputFile(result)
                        await msg.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id+1)
                        await msg.reply_photo(photo, reply_to_message_id=msg.message_id)
                        await state.clear()
                        os.remove(result)
                        break
                    except:
                        continue
                dt = {'role': 'assistant', 'content': result}
                await append_to_json_file(dt, f'users_histories/{msg.from_user.id}.json')
            
            elif '_search_in_inet_' in func:
                await msg.reply('🌐 Погоди, ищу в инете....')
                await state.set_state(GenAns.generate)
                await state.set_data(data={'genmessage_id': msg.message_id+1})
                result = ''
                for i in range(3):
                    try:
                        print(ww)
                        result = await aisearch_internet(text=ww, usr_id=msg.from_user.id)
                        print(result)
                        ddd = await answer_manipulate(result)
                        if type(ddd) == list:
                            for i in ddd:
                                if ddd[0] == i:
                                    await msg.bot.edit_message_text(text=i, chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                                elif ddd[-1] == i:
                                    await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                                else:
                                    await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                        else:
                            await msg.bot.edit_message_text(text=ddd, chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                        await state.clear()
                        if result == '':
                            continue
                        break
                    except:
                        continue
                dt = {'role': 'assistant', 'content': result}
                await append_to_json_file(dt, f'users_histories/{msg.from_user.id}.json')
        except Exception as ex:
            logger.error(f'Ошибка:\n{ex}')
    else:
        await msg.answer('Я понимаю только PDF файлы, убедитесь, что расширение вашего документа .pdf')
            

@rt.message(F.photo, F.func(lambda msg: msg if msg.from_user.id in ALLOWED_IDS or '*' in ALLOWED_IDS or str(msg.from_user.id) in ALLOWED_IDS else None))
async def phot(msg: Message, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.button(text='Прислать ответ голосовым', callback_data='answer_audio')
    podpis = msg.caption
    photo = msg.photo
    dd = str(datetime.now()).split(' ')
    dttime = dd[0] + '_' + dd[1]
    await msg.bot.download(photo[-1], destination=f'users_images/{dttime}.png')
    await msg.reply('🧐 Погоди, рассматриваю фотку')
    await state.set_state(GenAns.generate)
    await state.set_data(data={'genmessage_id': msg.message_id+1})
    for i in range(3):
        try:
            ee = await gen_from_image(text='Что изображено на этой картинке?', image_path=f'users_images/{dttime}.png')
            dt = {'role': 'user', 'content': ee}
            await append_to_json_file(dt, f'users_histories/{msg.from_user.id}.json')
            ww = await gen_from_image(text=f'{ee}\n{podpis}', image_path=f'users_images/{dttime}.png')
            ddd = await answer_manipulate(ww)
            if type(ddd) == list:
                for i in ddd:
                    if ddd[0] == i:
                        await msg.bot.edit_message_text(text=i, chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    elif ddd[-1] == i:
                        await msg.answer(text=i, reply_markup=kb.as_markup(), disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    else:
                        await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
            else:
                await msg.bot.edit_message_text(text=ddd, reply_markup=kb.as_markup(), chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)

            await state.clear()
            os.remove(f'users_images/{dttime}.png')
            if ww is not None:
                dt = {'role': 'assistant', 'content': ww}
                await append_to_json_file(dt, f'users_histories/{msg.from_user.id}.json')
                break
        except:
            continue


@rt.message(F.voice, F.func(lambda msg: msg if msg.from_user.id in ALLOWED_IDS or '*' in ALLOWED_IDS or str(msg.from_user.id) in ALLOWED_IDS else None))
async def aud(msg: Message, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.button(text='Прислать ответ голосовым', callback_data='answer_audio')
    cm = msg.voice
    file_id = cm.file_id
    dd = str(datetime.now()).split(' ')
    dttime = dd[0] + '_' + dd[1]
    file = await msg.bot.get_file(file_id)
    file_path = file.file_path
    await msg.bot.download_file(file_path, f"users_audios/{dttime}.mp3")
    for i in range(3):
        try:
            ee = await transcribe_audio(f"users_audios/{dttime}.mp3")
            data = {'role': 'user', 'content': ee}
            await append_to_json_file(data, f'users_histories/{msg.from_user.id}.json')
            if ee is not None:
                os.remove("users_audios/{dttime}.mp3")
                break
        except:
            continue
    try:
        func = await getfunc(ee)
        func = func.lstrip('[').rstrip(']')
        
        data = {'role': 'user', 'content': ee}
        await append_to_json_file(data, f'users_histories/{msg.from_user.id}.json')
        
        if '_scrape_url_' in func:
            await msg.reply('📝 Погоди, сокращаю....')
            await state.set_state(GenAns.generate)
            await state.set_data(data={'genmessage_id': msg.message_id+1})
            result = ''
            for i in range(3):
                try:
                    link = func.split(', ')[1]
                    result = await sum_from_link(link)
                    ddd = await answer_manipulate(result)
                    if type(ddd) == list:
                        for i in ddd:
                            if ddd[0] == i:
                                await msg.bot.edit_message_text(text=i, chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                            elif ddd[-1] == i:
                                await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                            else:
                                await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    else:
                        await msg.bot.edit_message_text(text=ddd, reply_markup=kb.as_markup(), chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    await state.clear()
                    if result == '':
                        continue
                    break
                except:
                    continue
            dt = {'role': 'assistant', 'content': result}
            await append_to_json_file(dt, f'users_histories/{msg.from_user.id}.json')

                    
        elif '_gen_text_' in func:
            await msg.reply('🥸 Погоди, генерирую ответ....')
            await state.set_state(GenAns.generate)
            await state.set_data(data={'genmessage_id': msg.message_id+1})
            result = ''
            for i in range(3):
                try:
                    result = await generate(ee, msg.from_user.id)
                    ddd = await answer_manipulate(result)
                    if type(ddd) == list:
                        for i in ddd:
                            if ddd[0] == i:
                                await msg.bot.edit_message_text(text=i, chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                            elif ddd[-1] == i:
                                await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                            else:
                                await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    else:
                        await msg.bot.edit_message_text(text=ddd, reply_markup=kb.as_markup(), chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    await state.clear()
                    if result == '':
                        continue
                    break
                except:
                    continue
            dt = {'role': 'assistant', 'content': result}
            await append_to_json_file(dt, f'users_histories/{msg.from_user.id}.json')


        elif '_scrape_input_' in func:
            await msg.reply('📝 Погоди, сокращаю....')
            await state.set_state(GenAns.generate)
            await state.set_data(data={'genmessage_id': msg.message_id+1})
            result = ''
            for i in range(3):
                try:
                    result = await sum_from_inp(ee)
                    ddd = await answer_manipulate(result)
                    if type(ddd) == list:
                        for i in ddd:
                            if ddd[0] == i:
                                await msg.bot.edit_message_text(text=i, chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                            elif ddd[-1] == i:
                                await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                            else:
                                await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    else:
                        await msg.bot.edit_message_text(text=ddd, reply_markup=kb.as_markup(), chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    await state.clear()
                    if result == '':
                        continue
                    break
                except:
                    continue
            dt = {'role': 'assistant', 'content': result}
            await append_to_json_file(dt, f'users_histories/{msg.from_user.id}.json')


        elif '_gen_image_' in func:
            await msg.reply('🎆 Погоди, генерирую картинку....')
            await state.set_state(GenAns.generate)
            await state.set_data(data={'genmessage_id': msg.message_id+1})
            result = ''
            for i in range(3):
                try:
                    result = await generate_image(ee)
                    photo = FSInputFile(result)
                    await msg.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id+1)
                    await msg.reply_photo(photo, reply_to_message_id=msg.message_id)
                    await state.clear()
                    dd = await gen_from_image('Что изображено на этой картинке?', result)
                    os.remove(result)
                    if result == '':
                        continue
                    break
                except:
                    continue
            dt = {'role': 'assistant', 'content': dd}
            await append_to_json_file(dt, f'users_histories/{msg.from_user.id}.json')


        
        elif '_search_in_inet_' in func:
            await msg.reply('🌐 Погоди, ищу в инете....')
            await state.set_state(GenAns.generate)
            await state.set_data(data={'genmessage_id': msg.message_id+1})
            result = ''
            for i in range(3):
                try:
                    result = await aisearch_internet(text=ee, usr_id=msg.from_user.id)
                    ddd = await answer_manipulate(result)
                    if type(ddd) == list:
                        for i in ddd:
                            if ddd[0] == i:
                                await msg.bot.edit_message_text(text=i, chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                            elif ddd[-1] == i:
                                await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                            else:
                                await msg.answer(text=i, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    else:
                        await msg.bot.edit_message_text(text=ddd, chat_id=msg.chat.id, message_id=msg.message_id+1, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
                    await state.clear()
                    if result == '':
                        continue
                    break
                except:
                    continue
            
            dt = {'role': 'assistant', 'content': result}
            await append_to_json_file(dt, f'users_histories/{msg.from_user.id}.json')
        os.remove(f"users_audios/{dttime}.mp3")
    except Exception as ex:
        logger.error(f'Ошибка:\n{ex}') 


@rt.callback_query(F.data == "answer_audio")
async def answer_audio(clck: CallbackQuery, state: FSMContext):
    for i in range(3):
        try:
            await clck.message.delete_reply_markup()
            ee = await ai_speech(clck.message.text)
            aud = FSInputFile(ee)
            
            
            #await clck.message.bot.send_audio(chat_id=msg.chat.id, audio=ee, reply_to_message_id=msg.message_id)
            await clck.message.answer_voice(aud, reply_to_message_id=clck.message.message_id)
            os.remove(ee)
            if ee is not None:
                break
        except:
            continue
