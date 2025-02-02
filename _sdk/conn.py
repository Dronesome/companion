import asyncio
import mavsdk

async def main():
	mav = mavsdk.System()
	await mav.connect(system_address='serial:///dev/ttyAMA0')
	async for state in mav.core.connection_state():
		print(state)
		if state.is_connected:
			print("connected!")
			break
	v = await mav.info.get_identification()
	print(v)

asyncio.run(main())
