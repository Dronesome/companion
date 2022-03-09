import asyncio
import mavsdk
import logging

class Mav():
	def __init__(self):
		logging.info("creating system...")
		self.__mav = mavsdk.System()
		logging.info("created system")
		self.battery = 1.0 # 0.0 - 1.0
		self.pos = [0.0, 0.0] # lat, lon
	
	async def __get_battery(self):
		async for val in self.__mav.telemetry.battery:
			logging.info(f"received battery: {val}")
			self.battery = val.remaining_percent
			logging.info(f"set battery to {self.battery}")

	async def __get_pos(self):
		async for val in self.__mav.telemetry.pos:
			logging.info(f"received pos {val}")
			self.pos = [val.latitude_deg, val.longitude_deg]
			logging.info(f"set pos to {self.pos}")

	async def keep_connected(self):
		logging.info("connecting...")
		await self.__mav.connect(system_address='serial:///dev/ttyAMA0')
		logging.info("connected")
		await self.__mav.param.set_param_int('COM_RC_IN_MODE', 2)
		await asyncio.gather(self.__get_battery, self.__get_pos)
		logging.info("disconnecting")

async def main():
	logging.getLogger().setLevel(logging.DEBUG)
	mav = Mav()
	await mav.keep_connected()

asyncio.run(main())
