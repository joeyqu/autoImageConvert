import os
import sys
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from time import sleep
from pystray import MenuItem as item
import pystray
import json
import logging
# set the default vars
script_dir = os.path.expanduser("~\Downloads\\")
config_editor_path = "notepad.exe"
config = {}
supportedFormats = ()
observer = None

def load_config():
  # Check if config.json exists
  if not os.path.exists(resource_path('app-config.json')):
    # Read the default config file
    with open(resource_path('config.json'), "r") as f:
      defaultconfig = json.load(f)
      with open('app-config.json', "w") as f:
        json.dump(defaultconfig, f, indent=4)
        
  global config
  config = json.load(open(resource_path('app-config.json'),"r"))
  # Get the listen_dir from the config file
  listen_dir = config.get("listen_dir")
  # Get the config_editor from the config file
  config_editor = config.get("config_editor")
  # Get the script_dir from the config file if not null
  supported_formats = tuple(config.get("supported_formats"))
  
  if listen_dir:
    global script_dir
    script_dir = os.path.abspath(listen_dir)
      
  # Get the config_editor from the config file if not null
  if config_editor:
    global config_editor_path
    config_editor_path = config_editor
  
  if supported_formats:
    global supportedFormats
    supportedFormats = tuple(supported_formats)
      
  


def openConfig(config_editor):
    logger.info(f"executing {config_editor} {resource_path('app-config.json')}")
    os.system(f"notepad.exe {resource_path('app-config.json')}")

def reloadConfig():
    logger.info(f"executing reload")
    old_config = script_dir, config_editor_path, supportedFormats
    logger.info(f"old config: {old_config}")
    logger.info(f"stopping observer")
    observer.stop()
    logger.info(f"waiting for observer to stop..............")
    observer.join()
    logger.info(f"reloading config")
    load_config()
    logger.info(f"new config: {script_dir, config_editor_path, supported_formats}")
    logger.info(f"restarting observer")
    observer = Observer()
    observer.schedule(NewFileHandler(), script_dir, recursive=True)
    observer.start()
    
def runAtStartup():
    os.system('SchTasks /Create /SC ONLOGON /TN "AutoStart auto-image-convert" /TR \"\'C:\\Program Files (x86)\Auto Image Convert\\convert.exe\'\" /rl HIGHEST /F')

def openLog(config_editor):
    logger.info(f"executing {config_editor} {resource_path('output.log')}")
    os.system(f"notepad.exe {resource_path('output.log')}")
    
def closeApp():
    os._exit(0)


class NewFileHandler(FileSystemEventHandler):
  def on_moved(self, event):
    sleep(3)
    logger.info('file moved ' + event.src_path)
    if not event.is_directory and '.png' not in event.src_path:
      
      filepath = event.src_path[:-11]
      logger.info(filepath)
      filename = "\\".join(filepath.split('\\')[-1:])
    
      if filename.endswith(supportedFormats):
        # Open the image file
        image = Image.open(filepath)
        # Convert the image to PNG format
        if image.format != 'PNG':
          new_filename = os.path.splitext(filepath)[0] + '.png'
          image.save(new_filename, 'PNG')
        # Close the image file
        image.close()
        # Remove the original image file
        os.remove(filepath)
        
  def on_created(self, event):
    logger.info('file created ' + event.src_path)
    if not event.is_directory and '.png' not in event.src_path and '.crdownload' not in event.src_path:
      
      filepath = event.src_path[:-11]
      logger.info(filepath)
      filename = "\\".join(filepath.split('\\')[-1:])
    
      if filename.endswith(('.jpg', '.jpeg', '.gif', '.png', '.bmp', '.tiff','.webp')):
        # Open the image file
        image = Image.open(filepath)
        # Convert the image to PNG format
        if image.format != 'PNG':
          new_filename = os.path.splitext(filepath)[0] + '.png'
          image.save(new_filename, 'PNG')
        # Close the image file
        image.close()
        # Remove the original image file
        os.remove(filepath)
 
def resource_path(relative_path):
    if relative_path == 'icons':
        base_path = sys._MEIPASS
        return os.path.join(base_path, relative_path)
    else:
      return os.path.abspath(os.fspath(relative_path))
  
logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',filename='output.log')
state = False

def on_clicked(icon, item):
    global state
    state = not item.checked
    if state:
        runAtStartup()
    else:
        os.system(r'SchTasks /Delete /TN "AutoStart auto-image-convert" /F')
        

if __name__ == '__main__':
  logger = logging.getLogger(__name__)
  logger.info('Started')
  logger.info(f"{os.path.abspath(os.fspath('output.log'))} vs {resource_path('output.log')}")
  logger.info(f'running from {resource_path("")}')
  load_config()
  logger.info(f'using script_dir {script_dir}')
  try:
    
    icon_folder = resource_path('icons')
    image = Image.open(os.path.join(icon_folder, 'favicon.ico'))
    menu = (
      item('Configuration', openConfig),
      item('Log', openLog),
      item('Reload', reloadConfig),
      item('Quit', closeApp),
      item(
        'RunAtStartup',
        on_clicked,
        checked=lambda item: state))
    icon = pystray.Icon("auto-image-convert-icon", image, "Auto Image Convert", menu)

    # Create an observer and attach the event handler
      
    observer = Observer()
    observer.schedule(NewFileHandler(), script_dir, recursive=True)
    observer.start()
    logger.info('script loaded, listening for new files in ' + script_dir)
    # start the tray icon
    icon.run()
    # Keep the program running
    try:
      while True:
        pass
    except KeyboardInterrupt:
      # Stop the observer
      observer.stop()
      
    # Wait until the observer thread stops
    observer.join()
    with open(resource_path('app-config.json'), "w") as f:
      json.dump(config, f, indent=4)
  except Exception as e:
    # Log any errors
   logging.error('Error at %s', 'division', exc_info=e)
    
  

