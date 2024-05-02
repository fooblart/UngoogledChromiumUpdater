#!/usr/bin/env python3
class main:
	def clear(self, amount):
		for i in range(amount):
			print('\x1b[1A\x1b[2K', end='')

	def getCurrentVersion(self):
		try:
			r = requests.get('https://ungoogled-software.github.io/ungoogled-chromium-binaries/releases/appimage/64bit/', timeout = self.args.timeout)
			return 'ungoogled-chromium_' + r.text.split('<li>')[1].split('</li>')[0].split('">')[1].rstrip('</a>') + '.AppImage'
		except:
			return

	def genDesktopFile(self, version):
		cwd = os.getcwd()

		if not os.path.exists('chromium.png'):
			r = requests.get('https://duckduckgo.com/i/4e19f28e4e51f612.png', timeout = self.args.timeout)
			open('chromium.png', 'wb').write(r.content)

		open('ungoogledChromium.desktop', 'w').write(f'''[Desktop Entry]
Type=Application
Name=Ungoogled Chromium
Categories=Network;WebBrowser
Exec=sh -c '"{cwd}/{version}"'
Icon={cwd}/chromium.png
StartupWMClass=Ungoogled Chromium
''')
		os.chmod('ungoogledChromium.desktop', 0o755)
		print(f'{self.green}[+] Created ungoogledChromium.desktop file, drag to task bar to quickly start ungoogled chromium{self.end}')

#https://github.com/ungoogled-software/ungoogled-chromium-portablelinux/releases/download/123.0.6312.122-1/ungoogled-chromium_123.0.6312.122-1.AppImage

	def downloadChromium(self, version):
		# try:
		print(f'{self.green}[+] Downloading: {version}, May take a few minutes{self.end}')
		r = requests.get('https://github.com/ungoogled-software/ungoogled-chromium-portablelinux/releases/download/' + version.rstrip('.AppImage').lstrip('ungoogled-chromium_') + '/' + version, timeout = None)
		open(version, 'wb').write(r.content)
		os.chmod(version, 0o555)
		print(f'{self.green}[+] Installed {version}{self.end}')
		self.genDesktopFile(version)

		# except:
			# return


	def __init__(self):
		parser = argparse.ArgumentParser(description = '[!] Ungoogled chromium update utility')
		parser.add_argument('-d', '--desktop', action='store_true', dest='genDesktopFile', help='Generate desktop file')
		parser.add_argument('-u', '--upgrade', action='store_true', dest='doUpdate', help='Update chromium version')
		parser.add_argument('-t', '--timeout', action='store', dest='timeout', help='Timeout for requests', const = 5, default = 5, nargs = '?', type = int)
		self.args = parser.parse_args()
		self.end = '\x1b[0m'
		self.red = '\x1b[38;2;255;0;0m'
		self.green = '\x1b[38;2;0;255;0m'
		self.pink = '\x1b[38;2;255;0;255m'

		def sortFunc(e):
			return int(''.join(e.split('_')[1].split('-')[0].split('.')))

		appImages = list(set(i for i in os.listdir() if i.lower().endswith('.appimage')))
		for i in appImages:
			if 'ungoogled-chromium_' not in i:
				appImages.remove(i)
				continue

		if len(appImages) > 1:
			appImages.sort(key=sortFunc, reverse=True)
			chrome = appImages.pop(0)
			for i in appImages:
				print(f'{self.red}[!] Removing old version: {i}{self.end}')
				os.remove(i)
		elif len(appImages) == 0:
			print(f'{self.red}[!] Chromium is not installed!{self.end}')
		else:
			chrome = appImages[0]
		print(f'{self.pink}[*] Getting current version from server...{self.end}')
		currentVersion = self.getCurrentVersion()
		print(f'{self.pink}[*] Current version: {currentVersion}{self.end}')
		if currentVersion is not None:
			if 'chrome' in locals():
				print(f'{self.pink}[*] Current installed version: {chrome}{self.end}')
				if chrome == currentVersion:
					print(f'{self.green}[+] Already up-to date!{self.end}')
				else:
					self.downloadChromium(currentVersion)
					os.remove(chrome)
			else:
				self.downloadChromium(currentVersion)
		else:
			print(f'{self.red}[!] Could not get current version, check internet connection and try again!{self.end}')
			return

if __name__ == '__main__':
	import requests, os, argparse, stat
	main()

#must be able to upgrade(-u) chromium,
#gen desktop file(-d)
#delete the older versions
