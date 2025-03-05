import asyncio
import json
import logging

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AsyncSocketClient:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
    
    async def connect(self):
        try:
            reader, writer = await asyncio.open_connection(self.host, self.port)
            return reader, writer
        except Exception as e:
            logging.error(f'Помилка підключення: {e}')
            return None, None
    
    async def send_command(self, command):
        reader, writer = await self.connect()
        if not reader or not writer:
            return None
        
        try:
            # Надсилання команди
            writer.write(json.dumps(command).encode())
            await writer.drain()
            
            # Очікування відповіді
            response = await reader.read(1024)
            return json.loads(response.decode())
        
        except Exception as e:
            logging.error(f'Помилка при роботі з сервером: {e}')
            return None
        
        finally:
            writer.close()
            await writer.wait_closed()

async def test_client():
    client = AsyncSocketClient()
    
    # Тест команди отримання часу
    time_response = await client.send_command({
        'type': 'time'
    })
    logging.info(f'Відповідь на запит часу: {time_response}')
    
    # Тест математичної операції
    calc_response = await client.send_command({
        'type': 'calc',
        'operation': 'add',
        'a': 10,
        'b': 20
    })
    logging.info(f'Результат обчислення: {calc_response}')
    
    # Тест широкомовної розсилки
    broadcast_response = await client.send_command({
        'type': 'broadcast',
        'message': 'Привіт, всі!'
    })
    logging.info(f'Статус розсилки: {broadcast_response}')

async def main():
    await test_client()

if __name__ == '__main__':
    asyncio.run(main())