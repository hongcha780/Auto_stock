import asyncio
import requests
import datetime
from config import telegram_token
from chat_command import ChatCommand
from get_setting import get_setting
from market_hour import MarketHour

# stop 한다고 프로그램이 꺼지는건 아니고 컴퓨터에서 직접 정지해야함
# 텔레그램에서는 해당명령어를 실행한 결과가 답장으로 나타나게 되어있음
#  ㄴ 종목 매수 등 어떤 과정이 진행중이거나 서버의 응답이 오래 걸리면 답이 늦어지는 경우도 있음
#  ㄴ 이때 답이 늦는다고 명령어를 여럿 보내면, 병목이 뚫렸을 때 프로그램이 밀린 명령어들을 한꺼번에 실행해버리게 됨

class MainApp:
	def __init__(self):
		self.chat_command = ChatCommand()
		self.last_update_id = 0
		self.telegram_url = f"https://api.telegram.org/bot{telegram_token}/getUpdates"
		self.keep_running = True
		self.today_started = False  # 오늘 start가 실행되었는지 추적
		self.today_stopped = False  # 오늘 stop이 실행되었는지 추적
		self.last_check_date = None  # 마지막으로 확인한 날짜
		
	def get_chat_updates(self):
		"""텔레그램 채팅 업데이트를 가져옵니다."""
		try:
			params = {
				'offset': self.last_update_id + 1,
				'timeout': 10
			}
			response = requests.get(self.telegram_url, params=params)
			data = response.json()
			
			if data.get('ok'):
				updates = data.get('result', [])
				for update in updates:
					self.last_update_id = update['update_id']
					
					if 'message' in update and 'text' in update['message']:
						text = update['message']['text']
						print(f"받은 메시지: {text}")
						return text
			return None
		except Exception as e:
			print(f"채팅 업데이트 가져오기 실패: {e}")
			return None
	
	
	async def check_market_timing(self):
		"""장 시작/종료 시간을 확인하고 자동 실행합니다."""
		auto_start = get_setting('auto_start', False)
		today = datetime.datetime.now().date()
		
		# 새로운 날이 되면 플래그 리셋
		if self.last_check_date != today:
			self.today_started = False
			self.today_stopped = False
			self.last_check_date = today
		
		if MarketHour.is_market_start_time() and auto_start and not self.today_started:
			print(f"장 시작 시간({MarketHour.MARKET_START_HOUR:02d}:{MarketHour.MARKET_START_MINUTE:02d})입니다. 자동으로 start 명령을 실행합니다.")
			await self.chat_command.start()
			self.today_started = True  # 오늘 start 실행 완료 표시
		elif MarketHour.is_market_end_time() and not self.today_stopped:
			print(f"장 종료 시간({MarketHour.MARKET_END_HOUR:02d}:{MarketHour.MARKET_END_MINUTE:02d})입니다. 자동으로 stop 명령을 실행합니다.")
			await self.chat_command.stop(False)  # auto_start를 false로 설정하지 않음
			print("자동으로 계좌평가 보고서를 발송합니다.")
			await self.chat_command.report()  # 장 종료 시 report도 자동 발송
			self.today_stopped = True  # 오늘 stop 실행 완료 표시
	
	async def run(self):
		"""메인 실행 루프"""
		print("채팅 모니터링을 시작합니다...")
		
		try:
			while self.keep_running:
				# 채팅 메시지 확인
				message = self.get_chat_updates()
				if message:
					await self.chat_command.process_command(message)
				
				# 장 시작/종료 시간 확인
				await self.check_market_timing()
				
				# 1초 대기
				await asyncio.sleep(1)
				
		except KeyboardInterrupt:
			print("\n프로그램을 종료합니다...")
			self.keep_running = False
			await self.chat_command.stop(False)

async def main():
	app = MainApp()
	await app.run()

if __name__ == '__main__':
	asyncio.run(main())
