import asyncio
import mavsdk
import logging

async def status_text(mav):
	async for status in mav.telemetry.status_text():
		logging.info(f"-- Status: {status}")

async def main():
	logging.getLogger().setLevel(logging.DEBUG)

	# connect mav
	mav = mavsdk.System()
	await mav.connect(system_address='serial:///dev/ttyAMA0')
	logging.info("awaiting connection... (remember to sudo!)")
	async for state in mav.core.connection_state():
		logging.info(state)
		if state.is_connected:
			break
	
	# use mavlink instead of rc http://docs.px4.io/master/en/advanced_config/parameter_reference.html
	await mav.param.set_param_int('COM_RC_IN_MODE', 2)
	logging.info('changed param')

	# status text
	asyncio.create_task(status_text(mav))

	# wait for gps
	logging.info("waiting for global position estimate...")
	async for health in mav.telemetry.health():
		logging.info(health)
		if health.is_global_position_ok:
			logging.info("is_global_position_ok")
			break
	
	# calibrate
	logging.info("-- Starting gyroscope calibration")
	async for progress_data in mav.calibration.calibrate_gyro():
		logging.info(progress_data)
	logging.info("-- Gyroscope calibration finished")

	logging.info("-- Starting board level horizon calibration")
	async for progress_data in mav.calibration.calibrate_level_horizon():
		logging.info(progress_data)
	logging.info("-- Board level calibration finished")

	# takeoff and land
	logging.info("arming")
	await mav.action.arm()
	logging.info("taking off")
	await mav.action.takeoff()
	await asyncio.sleep(5)
	logging.info("landing")
	await mav.action.land()
	logging.info('landed')

	# get logs
	logfiles = await mav.log_files.get_entries()
	logging.info(logfiles)

asyncio.run(main())
